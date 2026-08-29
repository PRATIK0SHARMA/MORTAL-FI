from pathlib import Path
from datetime import datetime

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


SYSTEM_METRICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "metrics"
    / "system_metrics.csv"
)


END_TO_END_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "audit"
    / "end_to_end_audit_trail.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "dashboard"
)


# =================================================
# DASHBOARD METRICS BUILDER
# =================================================

class DashboardMetricsBuilder:


    def __init__(self):

        self.system_metrics = None

        self.audit_data = None


    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        print(
            "\nLoading dashboard metrics data..."
        )


        self.system_metrics = (
            pd.read_csv(
                SYSTEM_METRICS_PATH
            )
        )


        self.audit_data = (
            pd.read_csv(
                END_TO_END_AUDIT_PATH
            )
        )


        print(
            f"System metrics records: "
            f"{len(self.system_metrics)}"
        )


        print(
            f"Audit records: "
            f"{len(self.audit_data)}"
        )


    # =================================================
    # BUILD DASHBOARD KPI SUMMARY
    # =================================================

    def build_dashboard_summary(
        self
    ):

        metrics = (
            self.system_metrics.iloc[0]
        )


        total_transactions = int(

            metrics[
                "total_transactions"
            ]

        )


        matched_transactions = int(

            metrics[
                "matched_transactions"
            ]

        )


        exceptions_detected = int(

            metrics[
                "exceptions_detected"
            ]

        )


        auto_resolutions = int(

            metrics[
                "auto_resolutions"
            ]

        )


        escalations = int(

            metrics[
                "escalations"
            ]

        )


        match_rate = float(

            metrics[
                "match_rate"
            ]

        )


        ai_validity_rate = float(

            metrics[
                "ai_validity_rate"
            ]

        )


        decision_agreement_rate = float(

            metrics[
                "baseline_decision_agreement_rate"
            ]

        )


        guardrail_violations = int(

            metrics[
                "guardrail_violations"
            ]

        )


        resolved_rate = (

            auto_resolutions
            /
            exceptions_detected
            *
            100

            if exceptions_detected > 0

            else 0

        )


        manual_review_rate = (

            escalations
            /
            exceptions_detected
            *
            100

            if exceptions_detected > 0

            else 0

        )


        fully_processed = (

            len(
                self.audit_data
            )

            ==
            total_transactions

        )


        summary = {

            "generated_at":

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),


            "total_transactions":

                total_transactions,


            "matched_transactions":

                matched_transactions,


            "exceptions_detected":

                exceptions_detected,


            "match_rate":

                match_rate,


            "auto_resolutions":

                auto_resolutions,


            "escalations":

                escalations,


            "exception_auto_resolution_rate":

                round(
                    resolved_rate,
                    2
                ),


            "exception_manual_review_rate":

                round(
                    manual_review_rate,
                    2
                ),


            "ai_validity_rate":

                ai_validity_rate,


            "baseline_decision_agreement_rate":

                decision_agreement_rate,


            "guardrail_violations":

                guardrail_violations,


            "end_to_end_records":

                len(
                    self.audit_data
                ),


            "pipeline_fully_processed":

                fully_processed

        }


        return summary


    # =================================================
    # SAVE DASHBOARD SUMMARY
    # =================================================

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
            / "dashboard_kpis.csv"
        )


        dataframe = (

            pd.DataFrame(
                [summary]
            )

        )


        dataframe.to_csv(

            output_path,

            index=False

        )


        print(
            "\n✓ Dashboard KPI summary saved:"
        )

        print(
            output_path
        )


        return output_path


    # =================================================
    # DISPLAY SUMMARY
    # =================================================

    def display_summary(
        self,
        summary
    ):

        print(
            "\n" + "=" * 60
        )

        print(
            "DASHBOARD KPI SUMMARY"
        )

        print(
            "=" * 60
        )


        for key, value in summary.items():

            label = (

                key
                .replace(
                    "_",
                    " "
                )
                .title()

            )


            print(
                f"{label}: {value}"
            )


# =================================================
# MAIN
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "BUILDING DASHBOARD KPI SUMMARY"
    )

    print(
        "=" * 60
    )


    builder = (
        DashboardMetricsBuilder()
    )


    builder.load_data()


    summary = (
        builder.build_dashboard_summary()
    )


    builder.display_summary(
        summary
    )


    builder.save_summary(
        summary
    )


if __name__ == "__main__":

    main()