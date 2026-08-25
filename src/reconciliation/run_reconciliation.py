from loader import load_all_data
from engine import ReconciliationEngine


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