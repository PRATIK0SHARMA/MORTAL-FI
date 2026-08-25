from pathlib import Path

from loader import load_all_data
from engine import ReconciliationEngine


# =================================================
# PROJECT PATH SETUP
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
)

OUTPUT_PATH = (
    OUTPUT_DIRECTORY
    / "reconciliation_results.csv"
)


def main():

    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    data = load_all_data()

    # ---------------------------------------------
    # CREATE ENGINE
    # ---------------------------------------------

    engine = ReconciliationEngine(
        orders=data["orders"],
        payments=data["payments"],
        settlements=data["settlements"]
    )

    # ---------------------------------------------
    # RUN RECONCILIATION
    # ---------------------------------------------

    results = engine.run()

    # ---------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------
    # SAVE RESULTS
    # ---------------------------------------------

    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        "\n✓ Reconciliation results saved:"
    )

    print(
        OUTPUT_PATH
    )

    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("RECONCILIATION SUMMARY")
    print("=" * 60)

    print(
        results["status"]
        .value_counts()
    )

    print("\nException Types:")

    print(
        results["exception_type"]
        .value_counts(
            dropna=False
        )
    )

    # ---------------------------------------------
    # SAMPLE RESULTS
    # ---------------------------------------------

    print("\nSample Results:")

    print(
        results.head(10)
    )


if __name__ == "__main__":
    main()