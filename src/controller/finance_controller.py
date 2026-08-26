from pathlib import Path
from datetime import datetime

import pandas as pd


# =================================================
# PATH CONFIGURATION
# =================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "resolution"
    / "resolution_results.csv"
)


AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "audit"
    / "audit_trail.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "controller"
)


# =================================================
# FINANCE CONTROLLER
# =================================================

class FinanceController:


    def __init__(self):

        self.reconciliation = None

        self.resolution = None

        self.audit = None


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    def load_data(self):

        print("\nLoading reconciliation data...")

        self.reconciliation = pd.read_csv(
            RECONCILIATION_PATH
        )


        print(
            f"Loaded "
            f"{len(self.reconciliation)} "
            f"reconciliation records"
        )


        print("\nLoading resolution data...")

        self.resolution = pd.read_csv(
            RESOLUTION_PATH
        )


        print(
            f"Loaded "
            f"{len(self.resolution)} "
            f"resolution records"
        )


        print("\nLoading audit trail...")

        self.audit = pd.read_csv(
            AUDIT_PATH
        )


        print(
            f"Loaded "
            f"{len(self.audit)} "
            f"audit records"
        )


    # ---------------------------------------------
    # BUILD SUMMARY
    # ---------------------------------------------

    def build_summary(self):

        total_transactions = len(
            self.reconciliation
        )


        matched_transactions = len(

            self.reconciliation[

                self.reconciliation["status"]
                == "MATCHED"

            ]

        )


        total_exceptions = len(

            self.reconciliation[

                self.reconciliation["status"]
                == "EXCEPTION"

            ]

        )


        recovered_transactions = len(

            self.reconciliation[

                self.reconciliation[
                    "exception_type"
                ]
                == "REFERENCE_MISMATCH"

            ]

        )


        manual_review_required = (

            total_exceptions
            -
            recovered_transactions

        )


        high_risk_transactions = len(

            self.resolution[

                self.resolution[
                    "risk_level"
                ]
                == "HIGH"

            ]

        )


        low_risk_transactions = len(

            self.resolution[

                self.resolution[
                    "risk_level"
                ]
                == "LOW"

            ]

        )


        pipeline_integrity = (

            "VERIFIED"

            if (

                len(self.reconciliation)
                ==
                len(self.resolution)
                ==
                len(self.audit)

            )

            else "FAILED"

        )


        summary = {

            "report_generated_at":

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),


            "total_transactions":

                total_transactions,


            "successfully_matched":

                matched_transactions,


            "total_exceptions":

                total_exceptions,


            "auto_recovered":

                recovered_transactions,


            "manual_review_required":

                manual_review_required,


            "high_risk_transactions":

                high_risk_transactions,


            "low_risk_transactions":

                low_risk_transactions,


            "pipeline_integrity":

                pipeline_integrity

        }


        return summary


    # ---------------------------------------------
    # SAVE SUMMARY
    # ---------------------------------------------

    def save_summary(
        self,
        summary
    ):

        OUTPUT_DIRECTORY.mkdir(

            parents=True,

            exist_ok=True

        )


        output_path = (

            OUTPUT_DIRECTORY
            / "finance_controller_summary.csv"

        )


        summary_dataframe = (

            pd.DataFrame(

                [summary]

            )

        )


        summary_dataframe.to_csv(

            output_path,

            index=False

        )


        print("\n✓ Finance controller summary saved:")

        print(
            output_path
        )


        return output_path


    # ---------------------------------------------
    # DISPLAY SUMMARY
    # ---------------------------------------------

    def display_summary(
        self,
        summary
    ):

        print("\n" + "=" * 60)
        print("FINANCE CONTROLLER SUMMARY")
        print("=" * 60)


        print(

            f"\nTransactions Processed: "
            f"{summary['total_transactions']}"

        )


        print(

            f"Successfully Matched: "
            f"{summary['successfully_matched']}"

        )


        print(

            f"Exceptions Detected: "
            f"{summary['total_exceptions']}"

        )


        print(

            f"Automatically Recovered: "
            f"{summary['auto_recovered']}"

        )


        print(

            f"Manual Review Required: "
            f"{summary['manual_review_required']}"

        )


        print(

            f"High Risk Transactions: "
            f"{summary['high_risk_transactions']}"

        )


        print(

            f"Low Risk Transactions: "
            f"{summary['low_risk_transactions']}"

        )


        print(

            f"Pipeline Integrity: "
            f"{summary['pipeline_integrity']}"

        )



    # ---------------------------------------------
    # RUN CONTROLLER
    # ---------------------------------------------

    def run(self):

        # -----------------------------------------
        # LOAD DATA
        # -----------------------------------------

        self.load_data()


        # -----------------------------------------
        # BUILD SUMMARY
        # -----------------------------------------

        summary = self.build_summary()


        # -----------------------------------------
        # DISPLAY SUMMARY
        # -----------------------------------------

        self.display_summary(
            summary
        )


        # -----------------------------------------
        # SAVE SUMMARY
        # -----------------------------------------

        self.save_summary(
            summary
        )


        return summary




# =================================================
# MAIN
# =================================================

def main():

    print("\n" + "=" * 60)
    print("STARTING FINANCE CONTROLLER")
    print("=" * 60)


    controller = FinanceController()


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    controller.load_data()


    # ---------------------------------------------
    # BUILD SUMMARY
    # ---------------------------------------------

    summary = controller.build_summary()


    # ---------------------------------------------
    # DISPLAY SUMMARY
    # ---------------------------------------------

    controller.display_summary(
        summary
    )


    # ---------------------------------------------
    # SAVE SUMMARY
    # ---------------------------------------------

    controller.save_summary(
        summary
    )


if __name__ == "__main__":

    main()