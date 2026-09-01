from datetime import datetime
from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


EXECUTION_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "execution"
)


EXECUTION_AUDIT_PATH = (
    EXECUTION_DIRECTORY
    / "execution_audit.csv"
)


# =================================================
# RESOLUTION EXECUTOR
# =================================================

class ResolutionExecutor:

    # =============================================
    # EXECUTE RESOLUTION
    # =============================================

    def execute(
        self,
        decision,
        context
    ):

        action = decision.get(
            "action_taken"
        )


        # -----------------------------------------
        # IDEMPOTENCY CHECK
        # -----------------------------------------

        if self.already_executed(
            context
        ):

            execution_result = {

                "execution_status":
                    "ALREADY_EXECUTED",

                "execution_message":
                    (
                        "Resolution has already been "
                        "successfully executed"
                    ),

                "execution_action":
                    action,

                "validation_status":
                    "ALREADY_EXECUTED",

                "execution_timestamp":
                    datetime.now().isoformat()

            }


            self.save_execution_audit(
                execution_result,
                decision,
                context
            )


            return execution_result


        # -----------------------------------------
        # LINK RECOVERED SETTLEMENT
        # -----------------------------------------

        if action == "LINK_RECOVERED_SETTLEMENT":

            execution_result = (
                self.link_recovered_settlement(
                    decision,
                    context
                )
            )


        # -----------------------------------------
        # NO AUTO EXECUTION
        # -----------------------------------------

        else:

            execution_result = {

                "execution_status":
                    "NOT_EXECUTED",

                "execution_message":
                    "No automatic execution performed",

                "execution_action":
                    action,

                "validation_status":
                    "NOT_APPLICABLE",

                "execution_timestamp":
                    datetime.now().isoformat()

            }


        # -----------------------------------------
        # SAVE EXECUTION AUDIT
        # -----------------------------------------

        self.save_execution_audit(
            execution_result,
            decision,
            context
        )


        return execution_result


    # =============================================
    # IDEMPOTENCY CHECK
    # =============================================

    def already_executed(
        self,
        context
    ):

        payment_id = context.get(
            "payment_id"
        )


        settlement = context.get(
            "settlement",
            {}
        )


        settlement_id = settlement.get(
            "settlement_id"
        )


        # -----------------------------------------
        # NO AUDIT FILE
        # -----------------------------------------

        if not EXECUTION_AUDIT_PATH.exists():

            return False


        # -----------------------------------------
        # LOAD EXECUTION AUDIT
        # -----------------------------------------

        try:

            audit_df = pd.read_csv(
                EXECUTION_AUDIT_PATH
            )

        except Exception:

            return False


        if audit_df.empty:

            return False


        # -----------------------------------------
        # PAYMENT + SETTLEMENT MATCH
        # -----------------------------------------

        matching_records = audit_df[

            (
                audit_df[
                    "payment_id"
                ].astype(str)
                ==
                str(payment_id)
            )

            &

            (
                audit_df[
                    "settlement_id"
                ].astype(str)
                ==
                str(settlement_id)
            )

            &

            (
                audit_df[
                    "execution_status"
                ].astype(str)
                ==
                "EXECUTED"
            )

        ]


        return not matching_records.empty


    # =============================================
    # LINK RECOVERED SETTLEMENT
    # =============================================

    def link_recovered_settlement(
        self,
        decision,
        context
    ):

        payment = context.get(
            "payment",
            {}
        )


        settlement = context.get(
            "settlement",
            {}
        )


        payment_id = context.get(
            "payment_id"
        )


        settlement_id = settlement.get(
            "settlement_id"
        )


        payment_amount = payment.get(
            "amount"
        )


        settlement_amount = settlement.get(
            "gross_amount"
        )


        # -----------------------------------------
        # EXECUTION TIMESTAMP
        # -----------------------------------------

        execution_timestamp = (
            datetime.now().isoformat()
        )


        # =========================================
        # SETTLEMENT VALIDATION
        # =========================================

        if settlement_id is None:

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    "Recovered settlement ID is missing",

                "execution_action":
                    "LINK_RECOVERED_SETTLEMENT",

                "validation_status":
                    "FAILED",

                "execution_timestamp":
                    execution_timestamp

            }


        # =========================================
        # AMOUNT EXISTENCE VALIDATION
        # =========================================

        if (

            payment_amount is None

            or

            settlement_amount is None

        ):

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    "Payment or settlement amount is missing",

                "execution_action":
                    "LINK_RECOVERED_SETTLEMENT",

                "validation_status":
                    "FAILED",

                "execution_timestamp":
                    execution_timestamp

            }


        # =========================================
        # AMOUNT MATCH VALIDATION
        # =========================================

        if payment_amount != settlement_amount:

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    (
                        "Settlement amount does not "
                        "match payment amount"
                    ),

                "execution_action":
                    "LINK_RECOVERED_SETTLEMENT",

                "validation_status":
                    "FAILED",

                "execution_timestamp":
                    execution_timestamp

            }


        # =========================================
        # EXECUTION SUCCESS
        # =========================================

        return {

            "execution_status":
                "EXECUTED",

            "execution_message":
                (
                    "Recovered settlement successfully "
                    "linked to payment"
                ),

            "execution_action":
                "LINK_RECOVERED_SETTLEMENT",

            "validation_status":
                "PASSED",

            "payment_id":
                payment_id,

            "settlement_id":
                settlement_id,

            "payment_amount":
                payment_amount,

            "settlement_amount":
                settlement_amount,

            "execution_timestamp":
                execution_timestamp

        }


    # =============================================
    # SAVE EXECUTION AUDIT
    # =============================================

    def save_execution_audit(
        self,
        execution_result,
        decision,
        context
    ):

        EXECUTION_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )


        payment = context.get(
            "payment",
            {}
        )


        settlement = context.get(
            "settlement",
            {}
        )


        audit_record = {

            "payment_id":
                context.get(
                    "payment_id"
                ),

            "settlement_id":
                settlement.get(
                    "settlement_id"
                ),

            "exception_type":
                context.get(
                    "exception_type"
                ),

            "agent_decision":
                decision.get(
                    "agent_decision"
                ),

            "action_taken":
                decision.get(
                    "action_taken"
                ),

            "execution_status":
                execution_result.get(
                    "execution_status"
                ),

            "execution_message":
                execution_result.get(
                    "execution_message"
                ),

            "validation_status":
                execution_result.get(
                    "validation_status"
                ),

            "payment_amount":
                payment.get(
                    "amount"
                ),

            "settlement_amount":
                settlement.get(
                    "gross_amount"
                ),

            "execution_timestamp":
                execution_result.get(
                    "execution_timestamp"
                )

        }


        new_record = pd.DataFrame(
            [audit_record]
        )


        # -----------------------------------------
        # APPEND TO EXISTING AUDIT
        # -----------------------------------------

        if EXECUTION_AUDIT_PATH.exists():

            existing = pd.read_csv(
                EXECUTION_AUDIT_PATH
            )


            dataframe = pd.concat(
                [
                    existing,
                    new_record
                ],
                ignore_index=True
            )


        else:

            dataframe = new_record


        dataframe.to_csv(
            EXECUTION_AUDIT_PATH,
            index=False
        )