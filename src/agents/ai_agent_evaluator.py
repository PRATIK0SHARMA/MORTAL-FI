from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)


BASELINE_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "resolution"
    / "resolution_results.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "ai_evaluation"
)


# =================================================
# AI AGENT EVALUATOR
# =================================================

class AIAgentEvaluator:


    def __init__(self):

        self.ai_results = None

        self.baseline_results = None


    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        print(
            "\nLoading AI agent evaluation data..."
        )


        self.ai_results = pd.read_csv(
            AI_RESOLUTION_PATH
        )


        self.baseline_results = pd.read_csv(
            BASELINE_RESOLUTION_PATH
        )


        print(
            f"AI resolution records loaded: "
            f"{len(self.ai_results)}"
        )


        print(
            f"Baseline resolution records loaded: "
            f"{len(self.baseline_results)}"
        )


    # =================================================
    # EVALUATE AI DECISIONS
    # =================================================

    def evaluate(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "EVALUATING AI RESOLUTION AGENT"
        )

        print(
            "=" * 60
        )


        # ---------------------------------------------
        # KEEP EXCEPTIONS ONLY
        # ---------------------------------------------

        baseline_exceptions = (

            self.baseline_results[

                self.baseline_results[
                    "status"
                ]
                == "EXCEPTION"

            ]

        )


        # ---------------------------------------------
        # MERGE AI + BASELINE RESULTS
        # ---------------------------------------------

        evaluation = (

            self.ai_results.merge(

                baseline_exceptions[

                    [

                        "payment_id",

                        "exception_type",

                        "risk_level",

                        "recommended_action",

                        "auto_resolvable"

                    ]

                ],

                on=[

                    "payment_id",

                    "exception_type"

                ],

                how="left",

                suffixes=(

                    "_ai",

                    "_baseline"

                )

            )

        )


        # ---------------------------------------------
        # NORMALIZE BASELINE DECISION
        # ---------------------------------------------

        evaluation[

            "baseline_decision"

        ] = (

            evaluation[
                "auto_resolvable_baseline"
            ].apply(

                lambda value:

                "AUTO_RESOLVE"

                if value

                else

                "ESCALATE"

            )

        )


        # ---------------------------------------------
        # DECISION AGREEMENT
        # ---------------------------------------------

        evaluation[

            "decision_agreement"

        ] = (

            evaluation[
                "agent_decision"
            ]

            ==

            evaluation[
                "baseline_decision"
            ]

        )


        # ---------------------------------------------
        # RISK AGREEMENT
        # ---------------------------------------------

        evaluation[

            "risk_agreement"

        ] = (

            evaluation[
                "financial_risk"
            ]

            ==

            evaluation[
                "risk_level"
            ]

        )


        # ---------------------------------------------
        # SUMMARY METRICS
        # ---------------------------------------------

        total_records = len(
            evaluation
        )


        decision_agreement_count = (

            evaluation[
                "decision_agreement"
            ].sum()

        )


        risk_agreement_count = (

            evaluation[
                "risk_agreement"
            ].sum()

        )


        ai_valid_count = (

            evaluation[
                "ai_response_valid"
            ].sum()

        )


        guardrail_violation_count = (

            evaluation[
                "guardrail_violations"
            ]
            .notna()
            .sum()

        )


        decision_agreement_rate = (

            decision_agreement_count
            /
            total_records
            *
            100

            if total_records > 0

            else 0

        )


        risk_agreement_rate = (

            risk_agreement_count
            /
            total_records
            *
            100

            if total_records > 0

            else 0

        )


        ai_valid_rate = (

            ai_valid_count
            /
            total_records
            *
            100

            if total_records > 0

            else 0

        )


        auto_resolve_count = len(

            evaluation[

                evaluation[
                    "agent_decision"
                ]
                == "AUTO_RESOLVE"

            ]

        )


        escalate_count = len(

            evaluation[

                evaluation[
                    "agent_decision"
                ]
                == "ESCALATE"

            ]

        )


        summary = {

            "total_exceptions":

                total_records,


            "ai_decision_agreement":

                int(
                    decision_agreement_count
                ),


            "ai_decision_agreement_rate":

                round(
                    decision_agreement_rate,
                    2
                ),


            "risk_agreement":

                int(
                    risk_agreement_count
                ),


            "risk_agreement_rate":

                round(
                    risk_agreement_rate,
                    2
                ),


            "ai_valid_responses":

                int(
                    ai_valid_count
                ),


            "ai_valid_response_rate":

                round(
                    ai_valid_rate,
                    2
                ),


            "auto_resolutions":

                auto_resolve_count,


            "escalations":

                escalate_count,


            "guardrail_violations":

                guardrail_violation_count

        }


        return (

            evaluation,

            summary

        )


    # =================================================
    # SAVE RESULTS
    # =================================================

    def save_results(

        self,

        evaluation,

        summary

    ):


        OUTPUT_DIRECTORY.mkdir(

            parents=True,

            exist_ok=True

        )


        evaluation_path = (

            OUTPUT_DIRECTORY
            / "ai_agent_evaluation.csv"

        )


        summary_path = (

            OUTPUT_DIRECTORY
            / "ai_agent_evaluation_summary.csv"

        )


        evaluation.to_csv(

            evaluation_path,

            index=False

        )


        pd.DataFrame(

            [summary]

        ).to_csv(

            summary_path,

            index=False

        )


        print(
            "\n✓ AI evaluation saved:"
        )

        print(
            evaluation_path
        )


        print(
            "\n✓ AI evaluation summary saved:"
        )

        print(
            summary_path
        )


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
            "AI AGENT EVALUATION SUMMARY"
        )

        print(
            "=" * 60
        )


        for key, value in summary.items():

            print(

                f"{key.replace('_', ' ').title()}: "
                f"{value}"

            )


# =================================================
# MAIN
# =================================================

def main():


    evaluator = (
        AIAgentEvaluator()
    )


    evaluator.load_data()


    evaluation, summary = (
        evaluator.evaluate()
    )


    evaluator.display_summary(
        summary
    )


    evaluator.save_results(

        evaluation,

        summary

    )


if __name__ == "__main__":

    main()