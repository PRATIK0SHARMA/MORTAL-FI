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

RAW_PAYMENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "payments.csv"
)

PROCESSED_PAYMENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "payments_processed.csv"
)

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


# =================================================
# LOAD DATA
# =================================================

def load_datasets():

    datasets = {

        "RAW PAYMENTS":
            pd.read_csv(
                RAW_PAYMENTS_PATH
            ),

        "PROCESSED PAYMENTS":
            pd.read_csv(
                PROCESSED_PAYMENTS_PATH
            ),

        "RECONCILIATION":
            pd.read_csv(
                RECONCILIATION_PATH
            ),

        "RESOLUTION":
            pd.read_csv(
                RESOLUTION_PATH
            ),

        "AUDIT":
            pd.read_csv(
                AUDIT_PATH
            )
    }

    return datasets


# =================================================
# VALIDATE RECORD COUNTS
# =================================================

def validate_record_counts(
    datasets
):

    print("\n" + "=" * 60)
    print("RECORD COUNT VALIDATION")
    print("=" * 60)

    counts = {}

    for name, dataframe in datasets.items():

        count = len(
            dataframe
        )

        counts[name] = count

        print(
            f"{name}: "
            f"{count} records"
        )


    expected_count = (
        counts[
            "RAW PAYMENTS"
        ]
    )


    validation_results = {}

    for name, count in counts.items():

        validation_results[name] = (
            count == expected_count
        )


    return (
        counts,
        validation_results
    )


# =================================================
# VALIDATE PAYMENT IDS
# =================================================

def validate_payment_ids(
    datasets
):

    print("\n" + "=" * 60)
    print("PAYMENT ID VALIDATION")
    print("=" * 60)

    raw_payment_ids = set(

        datasets[
            "RAW PAYMENTS"
        ][
            "payment_id"
        ]

    )


    stages = {

        "PROCESSED PAYMENTS":
            datasets[
                "PROCESSED PAYMENTS"
            ][
                "payment_id"
            ],

        "RECONCILIATION":
            datasets[
                "RECONCILIATION"
            ][
                "payment_id"
            ],

        "RESOLUTION":
            datasets[
                "RESOLUTION"
            ][
                "payment_id"
            ],

        "AUDIT":
            datasets[
                "AUDIT"
            ][
                "payment_id"
            ]
    }


    validation_results = {}

    for stage, payment_ids in stages.items():

        stage_ids = set(
            payment_ids
        )

        missing_ids = (
            raw_payment_ids
            -
            stage_ids
        )

        extra_ids = (
            stage_ids
            -
            raw_payment_ids
        )

        is_valid = (

            len(
                missing_ids
            ) == 0

            and

            len(
                extra_ids
            ) == 0
        )

        validation_results[
            stage
        ] = is_valid


        print(
            f"\n{stage}"
        )

        print(
            f"Missing IDs: "
            f"{len(missing_ids)}"
        )

        print(
            f"Extra IDs: "
            f"{len(extra_ids)}"
        )

        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


    return validation_results


# =================================================
# MAIN
# =================================================

def main():

    print("\n" + "=" * 60)
    print("END-TO-END PIPELINE VALIDATION")
    print("=" * 60)


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    datasets = (
        load_datasets()
    )


    # ---------------------------------------------
    # RECORD COUNT VALIDATION
    # ---------------------------------------------

    counts, count_validation = (
        validate_record_counts(
            datasets
        )
    )


    # ---------------------------------------------
    # PAYMENT ID VALIDATION
    # ---------------------------------------------

    id_validation = (
        validate_payment_ids(
            datasets
        )
    )


    # ---------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------

    all_valid = (

        all(
            count_validation.values()
        )

        and

        all(
            id_validation.values()
        )
    )


    print("\n" + "=" * 60)

    if all_valid:

        print(
            "✓ PIPELINE INTEGRITY VERIFIED"
        )

        print(
            "All pipeline stages contain "
            "consistent payment records."
        )

    else:

        print(
            "✗ PIPELINE INTEGRITY FAILED"
        )

        print(
            "Record count or payment ID "
            "mismatches detected."
        )

    print("=" * 60)


if __name__ == "__main__":

    main()