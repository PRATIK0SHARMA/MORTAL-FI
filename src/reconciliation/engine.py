import pandas as pd


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
        # ---------------------------------------------

        if settlement_match.empty:

            result["status"] = (
                "UNMATCHED"
            )

            result["exception_type"] = (
                "NO_EXACT_SETTLEMENT_MATCH"
            )

            result["match_method"] = (
                "EXACT_REFERENCE"
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
        # STEP 3:
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