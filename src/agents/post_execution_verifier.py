from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


PAYMENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "payments_processed.csv"
)


SETTLEMENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "settlements_processed.csv"
)


EXECUTION_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "execution"
    / "execution_audit.csv"
)


VERIFICATION_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "execution"
    / "verification_audit.csv"
)


# =================================================
# POST EXECUTION VERIFIER
# =================================================

class PostExecutionVerifier:

    # =============================================
    # INITIALIZE
    # =============================================

    def __init__(self):

        self.payments = None

        self.settlements = None

        self.execution_audit = None


    # =============================================
    # LOAD DATA
    # =============================================

    def load_data(self):

        print(
            "\nLoading post-execution "
            "verification data..."
        )


        self.payments = pd.read_csv(
            PAYMENTS_PATH
        )


        self.settlements = pd.read_csv(
            SETTLEMENTS_PATH
        )


        self.execution_audit = pd.read_csv(
            EXECUTION_AUDIT_PATH
        )


        print(
            f"Payments loaded: "
            f"{len(self.payments)}"
        )


        print(
            f"Settlements loaded: "
            f"{len(self.settlements)}"
        )


        print(
            f"Execution audit records loaded: "
            f"{len(self.execution_audit)}"
        )


    # =============================================
    # VERIFY EXECUTION
    # =============================================

    def verify_execution(
        self,
        execution_record
    ):

        payment_id = execution_record.get(
            "payment_id"
        )


        settlement_id = execution_record.get(
            "settlement_id"
        )


        execution_status = execution_record.get(
            "execution_status"
        )


        # =========================================
        # BASIC EXECUTION VALIDATION
        # =========================================

        if execution_status not in (
            "EXECUTED",
            "ALREADY_EXECUTED"
        ):

            return {

                "verification_status":
                    "NOT_VERIFIED",

                "verification_message":
                    (
                        "Execution was not "
                        "successfully completed"
                    ),

                "payment_id":
                    payment_id,

                "settlement_id":
                    settlement_id

            }


        # =========================================
        # PAYMENT EXISTENCE
        # =========================================

        payment_record = self.payments[
            self.payments[
                "payment_id"
            ]
            == payment_id
        ]


        if payment_record.empty:

            return {

                "verification_status":
                    "VERIFICATION_FAILED",

                "verification_message":
                    "Payment record does not exist",

                "payment_id":
                    payment_id,

                "settlement_id":
                    settlement_id

            }


        payment = (
            payment_record
            .iloc[0]
            .to_dict()
        )


        # =========================================
        # SETTLEMENT EXISTENCE
        # =========================================

        settlement_record = self.settlements[
            self.settlements[
                "settlement_id"
            ]
            == settlement_id
        ]


        if settlement_record.empty:

            return {

                "verification_status":
                    "VERIFICATION_FAILED",

                "verification_message":
                    "Settlement record does not exist",

                "payment_id":
                    payment_id,

                "settlement_id":
                    settlement_id

            }


        settlement = (
            settlement_record
            .iloc[0]
            .to_dict()
        )


        # =========================================
        # AMOUNT VALIDATION
        # =========================================

        payment_amount = payment.get(
            "amount"
        )


        settlement_amount = settlement.get(
            "gross_amount"
        )


        if (

            payment_amount is None

            or

            settlement_amount is None

        ):

            return {

                "verification_status":
                    "VERIFICATION_FAILED",

                "verification_message":
                    (
                        "Payment or settlement "
                        "amount is missing"
                    ),

                "payment_id":
                    payment_id,

                "settlement_id":
                    settlement_id

            }


        if payment_amount != settlement_amount:

            return {

                "verification_status":
                    "VERIFICATION_FAILED",

                "verification_message":
                    (
                        "Payment amount does not "
                        "match settlement amount"
                    ),

                "payment_id":
                    payment_id,

                "settlement_id":
                    settlement_id,

                "payment_amount":
                    payment_amount,

                "settlement_amount":
                    settlement_amount

            }


        # =========================================
        # VERIFICATION SUCCESS
        # =========================================

        return {

            "verification_status":
                "VERIFIED",

            "verification_message":
                (
                    "Payment and recovered "
                    "settlement successfully "
                    "verified"
                ),

            "payment_id":
                payment_id,

            "settlement_id":
                settlement_id,

            "payment_amount":
                payment_amount,

            "settlement_amount":
                settlement_amount

        }


    # =============================================
    # VERIFY ALL EXECUTIONS
    # =============================================

    def verify_all_executions(self):

        successful_executions = (

            self.execution_audit[

                self.execution_audit[
                    "execution_status"
                ].isin(
                    [
                        "EXECUTED",
                        "ALREADY_EXECUTED"
                    ]
                )

            ]

        )


        verification_results = []


        for _, record in (
            successful_executions.iterrows()
        ):

            result = self.verify_execution(
                record.to_dict()
            )


            verification_results.append(
                result
            )


        return verification_results


    # =============================================
    # SAVE VERIFICATION AUDIT
    # =============================================

    def save_verification_audit(
        self,
        verification_results
    ):

        VERIFICATION_AUDIT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        dataframe = pd.DataFrame(
            verification_results
        )


        dataframe.to_csv(
            VERIFICATION_AUDIT_PATH,
            index=False
        )


        return VERIFICATION_AUDIT_PATH


# =================================================
# TEST
# =================================================

def main():

    print("\n" + "=" * 60)

    print(
        "POST-EXECUTION VERIFICATION"
    )

    print("=" * 60)


    verifier = (
        PostExecutionVerifier()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    verifier.load_data()


    # ---------------------------------------------
    # VERIFY EXECUTIONS
    # ---------------------------------------------

    results = (
        verifier.verify_all_executions()
    )


    # ---------------------------------------------
    # SAVE AUDIT
    # ---------------------------------------------

    output_path = (
        verifier.save_verification_audit(
            results
        )
    )


    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    dataframe = pd.DataFrame(
        results
    )


    print(
        "\nVerification Records:"
        f" {len(dataframe)}"
    )


    if not dataframe.empty:

        print(
            "\nVerification Status:"
        )


        print(
            dataframe[
                "verification_status"
            ].value_counts()
        )


        print(
            "\nVerification Results:\n"
        )


        print(
            dataframe.to_string(
                index=False
            )
        )


    print(
        "\n✓ Verification audit saved:"
    )


    print(
        output_path
    )


if __name__ == "__main__":

    main()