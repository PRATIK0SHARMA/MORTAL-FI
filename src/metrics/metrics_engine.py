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

RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)


AI_EVALUATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_evaluation"
    / "ai_agent_evaluation.csv"
)


AI_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_audit"
    / "ai_agent_audit_trail.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "metrics"
)


# =================================================
# CENTRALIZED METRICS ENGINE
# =================================================

class MetricsEngine:

    def __init__(self):

        self.reconciliation = None

        self.ai_resolution = None

        self.ai_evaluation = None

        self.ai_audit = None


    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        print(
            "\nLoading centralized metrics data..."
        )


        self.reconciliation = (
            pd.read_csv(
                RECONCILIATION_PATH
            )
        )


        self.ai_resolution = (
            pd.read_csv(
                AI_RESOLUTION_PATH
            )
        )


        self.ai_evaluation = (
            pd.read_csv(
                AI_EVALUATION_PATH
            )
        )


        self.ai_audit = (
            pd.read_csv(
                AI_AUDIT_PATH
            )
        )


        print(
            f"Reconciliation records: "
            f"{len(self.reconciliation)}"
        )


        print(
            f"AI resolution records: "
            f"{len(self.ai_resolution)}"
        )


        print(
            f"AI evaluation records: "
            f"{len(self.ai_evaluation)}"
        )


        print(
            f"AI audit records: "
            f"{len(self.ai_audit)}"
        )


    # =================================================
    # RECONCILIATION METRICS
    # =================================================

    def calculate_reconciliation_metrics(
        self
    ):

        total_transactions = len(
            self.reconciliation
        )


        matched_transactions = len(

            self.reconciliation[

                self.reconciliation[
                    "status"
                ]
                == "MATCHED"

            ]

        )


        exceptions = len(

            self.reconciliation[

                self.reconciliation[
                    "status"
                ]
                == "EXCEPTION"

            ]

        )


        match_rate = (

            matched_transactions
            /
            total_transactions
            *
            100

            if total_transactions > 0

            else 0

        )


        exception_rate = (

            exceptions
            /
            total_transactions
            *
            100

            if total_transactions > 0

            else 0

        )


        return {

            "total_transactions":
                total_transactions,

            "matched_transactions":
                matched_transactions,

            "exceptions_detected":
                exceptions,

            "match_rate":
                round(
                    match_rate,
                    2
                ),

            "exception_rate":
                round(
                    exception_rate,
                    2
                )
        }


    # =================================================
    # EXCEPTION METRICS
    # =================================================

    def calculate_exception_metrics(
        self
    ):

        exception_records = (

            self.reconciliation[

                self.reconciliation[
                    "status"
                ]
                == "EXCEPTION"

            ]

        )


        exception_counts = (

            exception_records[
                "exception_type"
            ]
            .value_counts()
            .to_dict()

        )


        metrics = {

            "amount_mismatch":
                exception_counts.get(
                    "AMOUNT_MISMATCH",
                    0
                ),

            "missing_settlement":
                exception_counts.get(
                    "MISSING_SETTLEMENT",
                    0
                ),

            "missing_order":
                exception_counts.get(
                    "MISSING_ORDER",
                    0
                ),

            "duplicate_payment":
                exception_counts.get(
                    "DUPLICATE_PAYMENT",
                    0
                ),

            "reference_mismatch":
                exception_counts.get(
                    "REFERENCE_MISMATCH",
                    0
                )
        }


        return metrics


    # =================================================
    # AI RESOLUTION METRICS
    # =================================================

    def calculate_ai_metrics(
        self
    ):

        total_ai_decisions = len(
            self.ai_resolution
        )


        auto_resolutions = len(

            self.ai_resolution[

                self.ai_resolution[
                    "agent_decision"
                ]
                == "AUTO_RESOLVE"

            ]

        )


        escalations = len(

            self.ai_resolution[

                self.ai_resolution[
                    "agent_decision"
                ]
                == "ESCALATE"

            ]

        )


        valid_ai_responses = len(

            self.ai_resolution[

                self.ai_resolution[
                    "ai_response_valid"
                ]
                == True

            ]

        )


        guardrail_violations = (

            self.ai_resolution[
                "guardrail_violations"
            ]
            .fillna("")
            .astype(str)
            .str.strip()
            .apply(

                lambda value:

                value not in (
                    "",
                    "[]",
                    "None",
                    "nan"
                )

            )
            .sum()

        )


        ai_validity_rate = (

            valid_ai_responses
            /
            total_ai_decisions
            *
            100

            if total_ai_decisions > 0

            else 0

        )


        return {

            "total_ai_decisions":
                total_ai_decisions,

            "auto_resolutions":
                auto_resolutions,

            "escalations":
                escalations,

            "valid_ai_responses":
                valid_ai_responses,

            "ai_validity_rate":
                round(
                    ai_validity_rate,
                    2
                ),

            "guardrail_violations":
                int(
                    guardrail_violations
                )
        }


    # =================================================
    # AI EVALUATION METRICS
    # =================================================

    def calculate_evaluation_metrics(
        self
    ):

        total_records = len(
            self.ai_evaluation
        )


        decision_agreement = len(

            self.ai_evaluation[

                self.ai_evaluation[
                    "decision_agreement"
                ]
                == True

            ]

        )


        risk_agreement = len(

            self.ai_evaluation[

                self.ai_evaluation[
                    "risk_agreement"
                ]
                == True

            ]

        )


        decision_agreement_rate = (

            decision_agreement
            /
            total_records
            *
            100

            if total_records > 0

            else 0

        )


        risk_agreement_rate = (

            risk_agreement
            /
            total_records
            *
            100

            if total_records > 0

            else 0

        )


        return {

            "baseline_decision_agreement":
                decision_agreement,

            "baseline_decision_agreement_rate":
                round(
                    decision_agreement_rate,
                    2
                ),

            "risk_agreement":
                risk_agreement,

            "risk_agreement_rate":
                round(
                    risk_agreement_rate,
                    2
                )
        }


    # =================================================
    # BUILD CENTRALIZED METRICS
    # =================================================

    def build_metrics(
        self
    ):

        reconciliation_metrics = (

            self.calculate_reconciliation_metrics()

        )


        exception_metrics = (

            self.calculate_exception_metrics()

        )


        ai_metrics = (

            self.calculate_ai_metrics()

        )


        evaluation_metrics = (

            self.calculate_evaluation_metrics()

        )


        metrics = {

            **reconciliation_metrics,

            **exception_metrics,

            **ai_metrics,

            **evaluation_metrics
        }


        return metrics


    # =================================================
    # SAVE METRICS
    # =================================================

    def save_metrics(
        self,
        metrics
    ):

        OUTPUT_DIRECTORY.mkdir(

            parents=True,

            exist_ok=True

        )


        output_path = (

            OUTPUT_DIRECTORY
            / "system_metrics.csv"

        )


        metrics_dataframe = (

            pd.DataFrame(
                [metrics]
            )

        )


        metrics_dataframe.to_csv(

            output_path,

            index=False

        )


        print(
            "\n✓ Centralized metrics saved:"
        )

        print(
            output_path
        )


        return output_path


    # =================================================
    # DISPLAY METRICS
    # =================================================

    def display_metrics(
        self,
        metrics
    ):

        print(
            "\n" + "=" * 60
        )

        print(
            "CENTRALIZED SYSTEM METRICS"
        )

        print(
            "=" * 60
        )


        for key, value in metrics.items():

            label = (

                key
                .replace(
                    "_",
                    " "
                )
                .title()

            )


            print(

                f"{label}: "
                f"{value}"

            )