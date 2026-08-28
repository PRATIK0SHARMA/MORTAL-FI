from pathlib import Path
import pandas as pd

from src.agents.resolution_agent import (
    ResolutionAgent
)


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
)


OUTPUT_PATH = (
    OUTPUT_DIRECTORY
    / "ai_resolution_results.csv"
)


# =================================================
# RUN AI RESOLUTION AGENT
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "RUNNING AI EXCEPTION RESOLUTION AGENT"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # INITIALIZE AGENT
    # ---------------------------------------------

    agent = (
        ResolutionAgent()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    print(
        "\nInitializing AI resolution agent..."
    )

    agent.load_data()


    # ---------------------------------------------
    # GET ALL EXCEPTIONS
    # ---------------------------------------------

    exception_contexts = (

        agent.context_builder
        .build_exception_contexts()

    )


    total_exceptions = len(
        exception_contexts
    )


    print(
        f"\nTotal Exceptions Found: "
        f"{total_exceptions}"
    )


    # ---------------------------------------------
    # PROCESS EXCEPTIONS
    # ---------------------------------------------

    decisions = []


    print(
        "\nProcessing exceptions...\n"
    )


    for index, context in enumerate(

        exception_contexts,

        start=1

    ):


        payment_id = (

            context[
                "payment_id"
            ]

        )


        exception_type = (

            context[
                "exception_type"
            ]

        )


        print(
            f"[{index}/{total_exceptions}] "
            f"Processing "
            f"{payment_id} "
            f"({exception_type})..."
        )


        # -----------------------------------------
        # RESOLVE EXCEPTION
        # -----------------------------------------

        decision = (

            agent.resolve_exception(
                payment_id
            )

        )


        if decision is not None:

            decisions.append(
                decision
            )


            print(

                f"    Decision: "
                f"{decision['agent_decision']}"

            )


            print(

                f"    Risk: "
                f"{decision['financial_risk']}"

            )


            print(

                f"    AI Valid: "
                f"{decision['ai_response_valid']}"

            )


        else:

            print(
                "    Failed to generate decision"
            )


    # ---------------------------------------------
    # CHECK RESULTS
    # ---------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "AI RESOLUTION PROCESSING COMPLETE"
    )

    print(
        "=" * 60
    )


    print(
        f"\nTotal Exceptions: "
        f"{total_exceptions}"
    )


    print(
        f"AI Decisions Generated: "
        f"{len(decisions)}"
    )


    if not decisions:

        print(
            "\nNo AI decisions generated."
        )

        return


    # ---------------------------------------------
    # CONVERT TO DATAFRAME
    # ---------------------------------------------

    results = (

        pd.DataFrame(
            decisions
        )

    )


    # ---------------------------------------------
    # FORMAT COMPLEX COLUMNS
    # ---------------------------------------------

    for column in [

        "guardrail_violations",

        "deterministic_evidence"

    ]:

        if column in results.columns:

            results[column] = (

                results[column]
                .apply(
                    lambda value:
                    " | ".join(
                        value
                    )

                    if isinstance(
                        value,
                        list
                    )

                    else value
                )

            )


    # ---------------------------------------------
    # SAVE RESULTS
    # ---------------------------------------------

    OUTPUT_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True

    )


    results.to_csv(

        OUTPUT_PATH,

        index=False

    )


    print(
        "\n✓ AI resolution results saved:"
    )

    print(
        OUTPUT_PATH
    )


    # ---------------------------------------------
    # DECISION SUMMARY
    # ---------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "AGENT DECISION SUMMARY"
    )

    print(
        "=" * 60
    )


    print(
        results[
            "agent_decision"
        ]
        .value_counts()
    )


    # ---------------------------------------------
    # RESOLUTION STATUS SUMMARY
    # ---------------------------------------------

    print(
        "\nRESOLUTION STATUS SUMMARY"
    )

    print(
        results[
            "resolution_status"
        ]
        .value_counts()
    )


    # ---------------------------------------------
    # RISK SUMMARY
    # ---------------------------------------------

    print(
        "\nFINANCIAL RISK SUMMARY"
    )

    print(
        results[
            "financial_risk"
        ]
        .value_counts()
    )


    # ---------------------------------------------
    # AI VALIDATION SUMMARY
    # ---------------------------------------------

    print(
        "\nAI RESPONSE VALIDATION"
    )


    print(
        results[
            "ai_response_valid"
        ]
        .value_counts()
    )


    # ---------------------------------------------
    # GUARDRAIL VIOLATIONS
    # ---------------------------------------------

    if "guardrail_violations" in results.columns:


        violations = (

            results[

                results[
                    "guardrail_violations"
                ]
                .notna()

                &

                (
                    results[
                        "guardrail_violations"
                    ]
                    != ""
                )

            ]

        )


        print(
            f"\nRecords with Guardrail Violations: "
            f"{len(violations)}"
        )


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":

    main()