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


ORDERS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "orders_processed.csv"
)


SETTLEMENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "settlements_processed.csv"
)


RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


BASELINE_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "resolution"
    / "resolution_results.csv"
)


# =================================================
# AI CONTEXT BUILDER
# =================================================

class ExceptionContextBuilder:


    def __init__(self):

        self.payments = None

        self.orders = None

        self.settlements = None

        self.reconciliation = None

        self.baseline_resolution = None


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    def load_data(self):

        print("\nLoading AI agent context data...")


        self.payments = pd.read_csv(
            PAYMENTS_PATH
        )


        self.orders = pd.read_csv(
            ORDERS_PATH
        )


        self.settlements = pd.read_csv(
            SETTLEMENTS_PATH
        )


        self.reconciliation = pd.read_csv(
            RECONCILIATION_PATH
        )


        self.baseline_resolution = pd.read_csv(
            BASELINE_RESOLUTION_PATH
        )


        print(
            f"Payments loaded: "
            f"{len(self.payments)}"
        )

        print(
            f"Orders loaded: "
            f"{len(self.orders)}"
        )

        print(
            f"Settlements loaded: "
            f"{len(self.settlements)}"
        )

        print(
            f"Reconciliation records loaded: "
            f"{len(self.reconciliation)}"
        )

        print(
            f"Baseline resolution records loaded: "
            f"{len(self.baseline_resolution)}"
        )


    # ---------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------

    def build_context(
        self,
        payment_id
    ):

        # -----------------------------------------
        # GET RECONCILIATION RECORD
        # -----------------------------------------

        reconciliation_record = (

            self.reconciliation[

                self.reconciliation[
                    "payment_id"
                ]
                == payment_id

            ]

        )


        if reconciliation_record.empty:

            return None


        reconciliation_record = (
            reconciliation_record.iloc[0]
        )


        # -----------------------------------------
        # GET PAYMENT
        # -----------------------------------------

        payment_record = (

            self.payments[

                self.payments[
                    "payment_id"
                ]
                == payment_id

            ]

        )


        if payment_record.empty:

            return None


        payment_record = (
            payment_record.iloc[0]
        )


        # -----------------------------------------
        # GET ORDER
        # -----------------------------------------

        order_record = (

            self.orders[

                self.orders[
                    "order_id"
                ]
                == payment_record[
                    "order_id"
                ]

            ]

        )


        order_data = None


        if not order_record.empty:

            order_data = (
                order_record.iloc[0].to_dict()
            )


        # -----------------------------------------
        # GET SETTLEMENT
        # -----------------------------------------

        settlement_data = None


        settlement_id = (
            reconciliation_record.get(
                "settlement_id"
            )
        )


        if pd.notna(settlement_id):

            settlement_record = (

                self.settlements[

                    self.settlements[
                        "settlement_id"
                    ]
                    == settlement_id

                ]

            )


            if not settlement_record.empty:

                settlement_data = (

                    settlement_record
                    .iloc[0]
                    .to_dict()

                )


        # -----------------------------------------
        # GET BASELINE RESOLUTION
        # -----------------------------------------

        baseline_record = (

            self.baseline_resolution[

                self.baseline_resolution[
                    "payment_id"
                ]
                == payment_id

            ]

        )


        baseline_data = None


        if not baseline_record.empty:

            baseline_data = (

                baseline_record
                .iloc[0]
                .to_dict()

            )


        # -----------------------------------------
        # BUILD STRUCTURED CONTEXT
        # -----------------------------------------

        context = {

            "payment_id":
                payment_id,


            "exception_type":

                reconciliation_record.get(
                    "exception_type"
                ),


            "reconciliation_status":

                reconciliation_record.get(
                    "status"
                ),


            "payment":

                payment_record.to_dict(),


            "order":

                order_data,


            "settlement":

                settlement_data,


            "reconciliation":

                reconciliation_record.to_dict(),


            "baseline_resolution":

                baseline_data
        }


        return context


    # ---------------------------------------------
    # BUILD ALL EXCEPTION CONTEXTS
    # ---------------------------------------------

    def build_exception_contexts(self):

        exception_records = (

            self.reconciliation[

                self.reconciliation[
                    "status"
                ]
                == "EXCEPTION"

            ]

        )


        contexts = []


        for _, record in exception_records.iterrows():

            payment_id = (
                record[
                    "payment_id"
                ]
            )


            context = (
                self.build_context(
                    payment_id
                )
            )


            if context is not None:

                contexts.append(
                    context
                )


        return contexts


# =================================================
# TEST
# =================================================

def main():

    builder = (
        ExceptionContextBuilder()
    )


    builder.load_data()


    contexts = (
        builder.build_exception_contexts()
    )


    print("\n" + "=" * 60)
    print("AI EXCEPTION CONTEXT BUILDER")
    print("=" * 60)


    print(
        f"\nException contexts built: "
        f"{len(contexts)}"
    )


    if contexts:

        print("\nSample Context:\n")

        print(
            contexts[0]
        )


if __name__ == "__main__":

    main()