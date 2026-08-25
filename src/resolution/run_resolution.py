from pathlib import Path

import pandas as pd

from resolution_engine import ResolutionEngine


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)

RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "resolution"
)

OUTPUT_PATH = (
    OUTPUT_DIRECTORY
    / "resolution_results.csv"
)


# =================================================
# LOAD DATA
# =================================================

def load_reconciliation_results():

    return pd.read_csv(
        RECONCILIATION_PATH
    )


# =================================================
# MAIN
# =================================================

def main():

    print("\n" + "=" * 60)
    print("RUNNING EXCEPTION RESOLUTION ENGINE")
    print("=" * 60)

    results = (
        load_reconciliation_results()
    )

    resolution_engine = (
        ResolutionEngine()
    )

    resolution_results = []

    for _, row in results.iterrows():

        resolution = (
            resolution_engine.resolve(
                row["exception_type"]
            )
        )

        resolution_results.append({

            "payment_id": row["payment_id"],

            "status": row["status"],

            "exception_type": (
                row["exception_type"]
            ),

            "risk_level": (
                resolution["risk_level"]
            ),

            "recommended_action": (
                resolution[
                    "recommended_action"
                ]
            ),

            "auto_resolvable": (
                resolution[
                    "auto_resolvable"
                ]
            )
        })


    # =================================================
    # CREATE DATAFRAME
    # =================================================

    resolution_dataframe = (
        pd.DataFrame(
            resolution_results
        )
    )


    # =================================================
    # CREATE OUTPUT DIRECTORY
    # =================================================

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )


    # =================================================
    # SAVE RESULTS
    # =================================================

    resolution_dataframe.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print(
        f"\nProcessed "
        f"{len(resolution_dataframe)} transactions"
    )

    print(
        "\n✓ Resolution results saved:"
    )

    print(
        OUTPUT_PATH
    )


    # =================================================
    # RISK SUMMARY
    # =================================================

    print("\n" + "=" * 60)
    print("RISK SUMMARY")
    print("=" * 60)

    print(
        resolution_dataframe[
            "risk_level"
        ].value_counts()
    )


    # =================================================
    # SAMPLE HIGH RISK EXCEPTIONS
    # =================================================

    high_risk = (
        resolution_dataframe[
            resolution_dataframe[
                "risk_level"
            ] == "HIGH"
        ]
    )

    print("\nHigh Risk Exceptions:")

    if high_risk.empty:

        print(
            "No high risk exceptions found."
        )

    else:

        print(
            high_risk[
                [
                    "payment_id",
                    "exception_type",
                    "recommended_action"
                ]
            ]
            .head(10)
            .to_string(
                index=False
            )
        )


if __name__ == "__main__":

    main()