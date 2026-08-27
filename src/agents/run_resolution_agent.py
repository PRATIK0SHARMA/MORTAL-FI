import json

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
    / "ai_agent"

)


# =================================================
# RUN AI RESOLUTION AGENT
# =================================================

def main():

    print("\n" + "=" * 60)
    print("STARTING AI EXCEPTION RESOLUTION AGENT")
    print("=" * 60)


    # ---------------------------------------------
    # CREATE AGENT
    # ---------------------------------------------

    agent = (
        ResolutionAgent()
    )


    # ---------------------------------------------
    # PROCESS EXCEPTIONS
    # ---------------------------------------------

    decisions = (
        agent.resolve_all_exceptions()
    )


    # ---------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------

    OUTPUT_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True

    )


    # ---------------------------------------------
    # SAVE JSON
    # ---------------------------------------------

    json_path = (

        OUTPUT_DIRECTORY
        / "agent_decisions.json"

    )


    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(

            decisions,

            file,

            indent=4,

            default=str

        )


    # ---------------------------------------------
    # SAVE CSV
    # ---------------------------------------------

    dataframe = (

        pd.DataFrame(
            decisions
        )

    )


    csv_path = (

        OUTPUT_DIRECTORY
        / "agent_decisions.csv"

    )


    dataframe.to_csv(

        csv_path,

        index=False

    )


    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("AI AGENT RESOLUTION SUMMARY")
    print("=" * 60)


    print(

        f"\nExceptions Processed: "
        f"{len(decisions)}"

    )


    if not dataframe.empty:

        print("\nAgent Decisions:")

        print(

            dataframe[
                "agent_decision"
            ].value_counts()

        )


        print("\nResolution Status:")

        print(

            dataframe[
                "resolution_status"
            ].value_counts()

        )


        print("\nFinancial Risk:")

        print(

            dataframe[
                "financial_risk"
            ].value_counts()

        )


        print("\nAverage Confidence:")

        print(

            f"{dataframe['confidence'].mean():.2%}"

        )


    print("\n✓ Agent decisions saved:")

    print(
        csv_path
    )

    print(
        json_path
    )


if __name__ == "__main__":

    main()