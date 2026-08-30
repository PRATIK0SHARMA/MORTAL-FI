from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


# =================================================
# DATA PATHS
# =================================================

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


DASHBOARD_KPI_PATH = (
    PROJECT_ROOT
    / "data"
    / "dashboard"
    / "dashboard_kpis.csv"
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)


# =================================================
# DAY 5 SYSTEM VALIDATOR
# =================================================

class Day5SystemValidator:


    def __init__(self):

        self.system_metrics = None

        self.audit = None

        self.dashboard_kpis = None

        self.ai_resolution = None


    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        print(
            "\nLoading Day 5 validation data..."
        )


        self.system_metrics = (
            pd.read_csv(
                SYSTEM_METRICS_PATH
            )
        )


        self.audit = (
            pd.read_csv(
                END_TO_END_AUDIT_PATH
            )
        )


        self.dashboard_kpis = (
            pd.read_csv(
                DASHBOARD_KPI_PATH
            )
        )


        self.ai_resolution = (
            pd.read_csv(
                AI_RESOLUTION_PATH
            )
        )


        print(
            f"System metrics records: "
            f"{len(self.system_metrics)}"
        )


        print(
            f"End-to-end audit records: "
            f"{len(self.audit)}"
        )


        print(
            f"Dashboard KPI records: "
            f"{len(self.dashboard_kpis)}"
        )


        print(
            f"AI resolution records: "
            f"{len(self.ai_resolution)}"
        )


    # =================================================
    # METRICS VALIDATION
    # =================================================

    def validate_metrics(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "METRICS VALIDATION"
        )

        print(
            "=" * 60
        )


        required_columns = [

            "total_transactions",

            "matched_transactions",

            "exceptions_detected",

            "total_ai_decisions",

            "auto_resolutions",

            "escalations",

            "ai_validity_rate",

            "guardrail_violations"

        ]


        missing_columns = [

            column

            for column in required_columns

            if column not in (
                self.system_metrics.columns
            )

        ]


        is_valid = (

            len(
                self.system_metrics
            )
            > 0

            and

            len(
                missing_columns
            )
            == 0

        )


        if missing_columns:

            print(
                "Missing Columns:"
            )

            for column in missing_columns:

                print(
                    f"- {column}"
                )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        return is_valid


    # =================================================
    # END-TO-END AUDIT VALIDATION
    # =================================================

    def validate_audit(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "END-TO-END AUDIT VALIDATION"
        )

        print(
            "=" * 60
        )


        metrics_row = (
            self.system_metrics.iloc[0]
        )


        total_transactions = (
            int(
                metrics_row[
                    "total_transactions"
                ]
            )
        )


        audit_count = (
            len(
                self.audit
            )
        )


        is_valid = (

            audit_count
            ==
            total_transactions

        )


        print(
            f"Expected Records: "
            f"{total_transactions}"
        )


        print(
            f"Audit Records: "
            f"{audit_count}"
        )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        return is_valid


    # =================================================
    # AI RESOLUTION VALIDATION
    # =================================================

    def validate_ai_resolution(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "AI RESOLUTION VALIDATION"
        )

        print(
            "=" * 60
        )


        metrics_row = (
            self.system_metrics.iloc[0]
        )


        total_ai_decisions = (
            int(
                metrics_row[
                    "total_ai_decisions"
                ]
            )
        )


        metrics_auto_resolutions = (
            int(
                metrics_row[
                    "auto_resolutions"
                ]
            )
        )


        metrics_escalations = (
            int(
                metrics_row[
                    "escalations"
                ]
            )
        )


        ai_resolution_count = (
            len(
                self.ai_resolution
            )
        )


        auto_resolutions = (
            len(

                self.ai_resolution[

                    self.ai_resolution[
                        "agent_decision"
                    ]
                    ==
                    "AUTO_RESOLVE"

                ]

            )
        )


        escalations = (
            len(

                self.ai_resolution[

                    self.ai_resolution[
                        "agent_decision"
                    ]
                    ==
                    "ESCALATE"

                ]

            )
        )


        count_valid = (

            ai_resolution_count
            ==
            total_ai_decisions

        )


        auto_resolution_valid = (

            auto_resolutions
            ==
            metrics_auto_resolutions

        )


        escalation_valid = (

            escalations
            ==
            metrics_escalations

        )


        is_valid = (

            count_valid

            and

            auto_resolution_valid

            and

            escalation_valid

        )


        print(
            f"AI Resolution Records: "
            f"{ai_resolution_count}"
        )


        print(
            f"Expected AI Decisions: "
            f"{total_ai_decisions}"
        )


        print(
            f"Auto Resolutions: "
            f"{auto_resolutions}"
        )


        print(
            f"Escalations: "
            f"{escalations}"
        )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        return is_valid


    # =================================================
    # DASHBOARD KPI VALIDATION
    # =================================================

    def validate_dashboard_kpis(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "DASHBOARD KPI VALIDATION"
        )

        print(
            "=" * 60
        )


        metrics_row = (
            self.system_metrics.iloc[0]
        )


        dashboard_row = (
            self.dashboard_kpis.iloc[0]
        )


        # ---------------------------------------------
        # SYSTEM METRICS
        # ---------------------------------------------

        total_transactions = (
            int(
                metrics_row[
                    "total_transactions"
                ]
            )
        )


        matched_transactions = (
            int(
                metrics_row[
                    "matched_transactions"
                ]
            )
        )


        exceptions_detected = (
            int(
                metrics_row[
                    "exceptions_detected"
                ]
            )
        )


        auto_resolutions = (
            int(
                metrics_row[
                    "auto_resolutions"
                ]
            )
        )


        escalations = (
            int(
                metrics_row[
                    "escalations"
                ]
            )
        )


        # ---------------------------------------------
        # DASHBOARD KPIs
        # ---------------------------------------------

        dashboard_total = (
            int(
                dashboard_row[
                    "total_transactions"
                ]
            )
        )


        dashboard_matched = (
            int(
                dashboard_row[
                    "matched_transactions"
                ]
            )
        )


        dashboard_exceptions = (
            int(
                dashboard_row[
                    "exceptions_detected"
                ]
            )
        )


        dashboard_auto = (
            int(
                dashboard_row[
                    "auto_resolutions"
                ]
            )
        )


        dashboard_escalations = (
            int(
                dashboard_row[
                    "escalations"
                ]
            )
        )


        dashboard_end_to_end = (
            int(
                dashboard_row[
                    "end_to_end_records"
                ]
            )
        )


        pipeline_fully_processed = (
            dashboard_row[
                "pipeline_fully_processed"
            ]
        )


        # ---------------------------------------------
        # INDIVIDUAL VALIDATIONS
        # ---------------------------------------------

        total_valid = (

            dashboard_total
            ==
            total_transactions

        )


        matched_valid = (

            dashboard_matched
            ==
            matched_transactions

        )


        exceptions_valid = (

            dashboard_exceptions
            ==
            exceptions_detected

        )


        auto_valid = (

            dashboard_auto
            ==
            auto_resolutions

        )


        escalation_valid = (

            dashboard_escalations
            ==
            escalations

        )


        end_to_end_valid = (

            dashboard_end_to_end
            ==
            total_transactions

        )


        pipeline_valid = (

            str(
                pipeline_fully_processed
            ).lower()
            ==
            "true"

        )


        is_valid = (

            total_valid

            and

            matched_valid

            and

            exceptions_valid

            and

            auto_valid

            and

            escalation_valid

            and

            end_to_end_valid

            and

            pipeline_valid

        )


        print(
            f"Total Transactions: "
            f"{dashboard_total}"
        )


        print(
            f"Matched Transactions: "
            f"{dashboard_matched}"
        )


        print(
            f"Exceptions Detected: "
            f"{dashboard_exceptions}"
        )


        print(
            f"Auto Resolutions: "
            f"{dashboard_auto}"
        )


        print(
            f"Escalations: "
            f"{dashboard_escalations}"
        )


        print(
            f"End-to-End Records: "
            f"{dashboard_end_to_end}"
        )


        print(
            f"Pipeline Fully Processed: "
            f"{pipeline_fully_processed}"
        )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        return is_valid


    # =================================================
    # FINAL PROCESSING STATUS VALIDATION
    # =================================================

    def validate_processing_status(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "FINAL PROCESSING STATUS VALIDATION"
        )

        print(
            "=" * 60
        )


        status_counts = (

            self.audit[
                "final_processing_status"
            ]
            .value_counts()

        )


        matched = (

            status_counts.get(
                "MATCHED_NO_AI_ACTION",
                0
            )

        )


        manual_review = (

            status_counts.get(
                "MANUAL_REVIEW_REQUIRED",
                0
            )

        )


        resolved = (

            status_counts.get(
                "RESOLVED",
                0
            )

        )


        total_processed = (

            matched
            +
            manual_review
            +
            resolved

        )


        metrics_row = (
            self.system_metrics.iloc[0]
        )


        total_transactions = (
            int(
                metrics_row[
                    "total_transactions"
                ]
            )
        )


        is_valid = (

            total_processed
            ==
            total_transactions

        )


        print(
            f"Matched: "
            f"{matched}"
        )


        print(
            f"Manual Review Required: "
            f"{manual_review}"
        )


        print(
            f"Resolved: "
            f"{resolved}"
        )


        print(
            f"Total Processed: "
            f"{total_processed}"
        )


        print(
            f"Expected Total: "
            f"{total_transactions}"
        )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        return is_valid


    # =================================================
    # RUN ALL VALIDATIONS
    # =================================================

    def run_validation(self):

        self.load_data()


        results = {

            "metrics": (
                self.validate_metrics()
            ),

            "audit": (
                self.validate_audit()
            ),

            "ai_resolution": (
                self.validate_ai_resolution()
            ),

            "dashboard": (
                self.validate_dashboard_kpis()
            ),

            "processing_status": (
                self.validate_processing_status()
            )

        }


        all_valid = (

            all(
                results.values()
            )

        )


        print(
            "\n" + "=" * 60
        )

        print(
            "FINAL DAY 5 SYSTEM VALIDATION"
        )

        print(
            "=" * 60
        )


        if all_valid:

            print(
                "\n✓ DAY 5 SYSTEM VERIFIED"
            )

            print(
                "Metrics, AI decisions, "
                "audit records, and dashboard "
                "KPIs are consistent."
            )

        else:

            print(
                "\n✗ DAY 5 SYSTEM VALIDATION FAILED"
            )

            print(
                "Cross-system inconsistencies "
                "were detected."
            )


        print(
            "\nValidation Results:"
        )


        for name, result in results.items():

            print(
                f"{name}: "
                f"{'PASS' if result else 'FAIL'}"
            )


        print(
            "=" * 60
        )


        return all_valid


# =================================================
# MAIN
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "DAY 5 METRICS AND AUDIT SYSTEM VALIDATION"
    )

    print(
        "=" * 60
    )


    validator = (
        Day5SystemValidator()
    )


    validator.run_validation()


if __name__ == "__main__":

    main()