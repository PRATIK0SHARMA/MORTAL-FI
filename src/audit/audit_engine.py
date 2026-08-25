from datetime import datetime

import pandas as pd


# =================================================
# AUDIT ENGINE
# =================================================

class AuditEngine:

    def __init__(
        self,
        reconciliation_results,
        resolution_results
    ):

        self.reconciliation_results = (
            reconciliation_results.copy()
        )

        self.resolution_results = (
            resolution_results.copy()
        )


    # =================================================
    # BUILD AUDIT TRAIL
    # =================================================

    def build_audit_trail(self):

        print("\n" + "=" * 60)
        print("BUILDING AUDIT TRAIL")
        print("=" * 60)

        # ---------------------------------------------
        # MERGE RECONCILIATION + RESOLUTION RESULTS
        # ---------------------------------------------

        audit_dataframe = pd.merge(

            self.reconciliation_results,

            self.resolution_results[
                [
                    "payment_id",
                    "risk_level",
                    "recommended_action",
                    "auto_resolvable"
                ]
            ],

            on="payment_id",

            how="left"
        )


        # ---------------------------------------------
        # GENERATE AUDIT TIMESTAMP
        # ---------------------------------------------

        audit_timestamp = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        audit_dataframe[
            "audit_timestamp"
        ] = audit_timestamp


        # ---------------------------------------------
        # GENERATE DECISION EXPLANATION
        # ---------------------------------------------

        audit_dataframe[
            "decision_explanation"
        ] = (
            audit_dataframe.apply(
                self._generate_explanation,
                axis=1
            )
        )


        # ---------------------------------------------
        # REORDER COLUMNS
        # ---------------------------------------------

        column_order = [

            "audit_timestamp",

            "payment_id",

            "order_id",

            "payment_amount",

            "status",

            "exception_type",

            "settlement_id",

            "settlement_amount",

            "match_method",

            "risk_level",

            "auto_resolvable",

            "recommended_action",

            "decision_explanation"
        ]

        audit_dataframe = (
            audit_dataframe[
                column_order
            ]
        )


        print(
            f"\nAudit records created: "
            f"{len(audit_dataframe)}"
        )

        return audit_dataframe


    # =================================================
    # GENERATE EXPLANATION
    # =================================================

    def _generate_explanation(
        self,
        row
    ):

        status = row["status"]

        exception_type = (
            row["exception_type"]
        )


        # ---------------------------------------------
        # MATCHED
        # ---------------------------------------------

        if status == "MATCHED":

            return (
                f"Payment {row['payment_id']} "
                f"matched settlement "
                f"{row['settlement_id']} "
                f"using {row['match_method']}. "
                f"Payment amount "
                f"{row['payment_amount']} matches "
                f"settlement amount "
                f"{row['settlement_amount']}."
            )


        # ---------------------------------------------
        # REFERENCE MISMATCH
        # ---------------------------------------------

        if (
            exception_type
            == "REFERENCE_MISMATCH"
        ):

            return (
                f"No exact settlement reference was found "
                f"for payment {row['payment_id']}. "
                f"A likely settlement "
                f"{row['settlement_id']} was recovered "
                f"using reference recovery logic."
            )


        # ---------------------------------------------
        # AMOUNT MISMATCH
        # ---------------------------------------------

        if (
            exception_type
            == "AMOUNT_MISMATCH"
        ):

            return (
                f"Payment {row['payment_id']} "
                f"has amount "
                f"{row['payment_amount']}, while "
                f"settlement {row['settlement_id']} "
                f"has gross amount "
                f"{row['settlement_amount']}."
            )


        # ---------------------------------------------
        # MISSING SETTLEMENT
        # ---------------------------------------------

        if (
            exception_type
            == "MISSING_SETTLEMENT"
        ):

            return (
                f"No settlement record was found "
                f"for payment {row['payment_id']} "
                f"after exact matching and reference "
                f"recovery checks."
            )


        # ---------------------------------------------
        # DUPLICATE PAYMENT
        # ---------------------------------------------

        if (
            exception_type
            == "DUPLICATE_PAYMENT"
        ):

            return (
                f"Payment {row['payment_id']} "
                f"was identified as a possible duplicate "
                f"business payment based on duplicate "
                f"detection rules."
            )


        # ---------------------------------------------
        # MISSING ORDER
        # ---------------------------------------------

        if (
            exception_type
            == "MISSING_ORDER"
        ):

            return (
                f"Payment {row['payment_id']} "
                f"references order {row['order_id']}, "
                f"but the order was not found in the "
                f"order source data."
            )


        # ---------------------------------------------
        # FALLBACK
        # ---------------------------------------------

        return (
            f"Transaction {row['payment_id']} "
            f"requires manual investigation."
        )