import pandas as pd

from duplicate_detector import DuplicateDetector
from reference_matcher import ReferenceMatcher


# =================================================
# RECONCILIATION ENGINE
# =================================================

class ReconciliationEngine:

    def __init__(
        self,
        orders,
        payments,
        settlements
    ):

        self.orders = orders.copy()

        self.payments = payments.copy()

        self.settlements = settlements.copy()

        self.results = []

        self.duplicate_detector = (
            DuplicateDetector(
                payments=self.payments
            )
        )

        self.reference_matcher = (
            ReferenceMatcher()
        )


    # =================================================
    # RUN RECONCILIATION
    # =================================================

    def run(self):

        print("\n" + "=" * 60)
        print("RUNNING RECONCILIATION ENGINE")
        print("=" * 60)

        for _, payment in self.payments.iterrows():

            result = self.reconcile_payment(
                payment
            )

            self.results.append(
                result
            )

        results_dataframe = pd.DataFrame(
            self.results
        )

        print(
            f"\nReconciliation completed: "
            f"{len(results_dataframe)} payments processed"
        )

        return results_dataframe


    # =================================================
    # RECONCILE SINGLE PAYMENT
    # =================================================

    def reconcile_payment(
        self,
        payment
    ):

        payment_id = payment["payment_id"]

        order_id = payment["order_id"]

        payment_amount = payment["amount"]


        # ---------------------------------------------
        # DEFAULT RESULT
        # ---------------------------------------------

        result = {

            "payment_id": payment_id,

            "order_id": order_id,

            "payment_amount": payment_amount,

            "status": "UNPROCESSED",

            "exception_type": None,

            "settlement_id": None,

            "settlement_amount": None,

            "match_method": None
        }


        # ---------------------------------------------
        # STEP 1:
        # CHECK ORDER EXISTS
        # ---------------------------------------------

        order_exists = (
            order_id
            in self.orders["order_id"].values
        )

        if not order_exists:

            result["status"] = "EXCEPTION"

            result["exception_type"] = (
                "MISSING_ORDER"
            )

            result["match_method"] = (
                "ORDER_VALIDATION"
            )

            return result


        # ---------------------------------------------
        # STEP 2:
        # CHECK DUPLICATE PAYMENT
        # ---------------------------------------------

        is_duplicate = (
            self.duplicate_detector.is_duplicate(
                payment
            )
        )

        if is_duplicate:

            result["status"] = "EXCEPTION"

            result["exception_type"] = (
                "DUPLICATE_PAYMENT"
            )

            result["match_method"] = (
                "DUPLICATE_DETECTION"
            )

            return result


        # ---------------------------------------------
        # STEP 3:
        # EXACT SETTLEMENT MATCH
        # ---------------------------------------------

        settlement_match = (
            self.settlements[
                self.settlements[
                    "payment_reference"
                ]
                == payment_id
            ]
        )


        # ---------------------------------------------
        # NO EXACT MATCH
        # TRY REFERENCE RECOVERY
        # ---------------------------------------------

        if settlement_match.empty:

            recovered_settlement = (
                self.reference_matcher.find_match(
                    payment=payment,
                    settlements=self.settlements
                )
            )


            # -----------------------------------------
            # RECOVERED REFERENCE MATCH
            # -----------------------------------------

            if recovered_settlement is not None:

                result["status"] = (
                    "EXCEPTION"
                )

                result["exception_type"] = (
                    "REFERENCE_MISMATCH"
                )

                result["settlement_id"] = (
                    recovered_settlement[
                        "settlement_id"
                    ]
                )

                result["settlement_amount"] = (
                    recovered_settlement[
                        "gross_amount"
                    ]
                )

                result["match_method"] = (
                    "REFERENCE_RECOVERY"
                )

                return result


            # -----------------------------------------
            # NO RECOVERABLE MATCH
            # -----------------------------------------

            result["status"] = (
                "UNMATCHED"
            )

            result["exception_type"] = (
                "NO_SETTLEMENT_MATCH"
            )

            result["match_method"] = (
                "REFERENCE_RECOVERY_FAILED"
            )

            return result


        # ---------------------------------------------
        # SETTLEMENT FOUND
        # ---------------------------------------------

        settlement = (
            settlement_match.iloc[0]
        )

        settlement_amount = (
            settlement["gross_amount"]
        )


        result["settlement_id"] = (
            settlement["settlement_id"]
        )

        result["settlement_amount"] = (
            settlement_amount
        )


        # ---------------------------------------------
        # STEP 4:
        # AMOUNT VALIDATION
        # ---------------------------------------------

        if payment_amount != settlement_amount:

            result["status"] = (
                "EXCEPTION"
            )

            result["exception_type"] = (
                "AMOUNT_MISMATCH"
            )

            result["match_method"] = (
                "EXACT_REFERENCE"
            )

            return result


        # ---------------------------------------------
        # PERFECT MATCH
        # ---------------------------------------------

        result["status"] = "MATCHED"

        result["exception_type"] = None

        result["match_method"] = (
            "EXACT_REFERENCE"
        )

        return result