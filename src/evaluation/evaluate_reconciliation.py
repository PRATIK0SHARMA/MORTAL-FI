import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# =================================================
# PROJECT PATH SETUP
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

GROUND_TRUTH_PATH = (
    PROJECT_ROOT
    / "data"
    / "ground_truth"
    / "transaction_labels.csv"
)


# =================================================
# LOAD DATA
# =================================================

def load_data():

    reconciliation_results = pd.read_csv(
        RECONCILIATION_PATH
    )

    ground_truth = pd.read_csv(
        GROUND_TRUTH_PATH
    )

    return (
        reconciliation_results,
        ground_truth
    )


# =================================================
# MAP ENGINE RESULTS
# =================================================

def map_engine_status(
    exception_type,
    status
):

    if status == "MATCHED":

        return "MATCHED"

    if exception_type == "DUPLICATE_PAYMENT":

        return "DUPLICATE"

    if exception_type == "REFERENCE_MISMATCH":

        return "FUZZY_MATCH"

    return "EXCEPTION"


# =================================================
# PREPARE EVALUATION DATA
# =================================================

def prepare_evaluation_data():

    (
        reconciliation_results,
        ground_truth
    ) = load_data()

    reconciliation_results[
        "predicted_status"
    ] = reconciliation_results.apply(
        lambda row: map_engine_status(
            exception_type=row[
                "exception_type"
            ],
            status=row[
                "status"
            ]
        ),
        axis=1
    )

    evaluation_data = (
        ground_truth.merge(
            reconciliation_results[
                [
                    "payment_id",
                    "predicted_status"
                ]
            ],
            on="payment_id",
            how="left"
        )
    )

    return evaluation_data


# =================================================
# CALCULATE METRICS
# =================================================

def calculate_metrics(
    evaluation_data
):

    y_true = (
        evaluation_data[
            "expected_status"
        ]
    )

    y_pred = (
        evaluation_data[
            "predicted_status"
        ]
    )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    report = classification_report(
        y_true,
        y_pred,
        digits=4
    )

    matrix = confusion_matrix(
        y_true,
        y_pred
    )

    return (
        accuracy,
        report,
        matrix
    )


# =================================================
# SHOW MISCLASSIFICATIONS
# =================================================

def show_misclassifications(
    evaluation_data
):

    mistakes = (
        evaluation_data[
            evaluation_data[
                "expected_status"
            ]
            !=
            evaluation_data[
                "predicted_status"
            ]
        ]
    )

    print("\n" + "=" * 60)
    print("MISCLASSIFIED RECORDS")
    print("=" * 60)

    if mistakes.empty:

        print(
            "No misclassifications found."
        )

        return

    print(
        mistakes[
            [
                "payment_id",
                "expected_status",
                "predicted_status",
                "exception_type"
            ]
        ]
        .to_string(
            index=False
        )
    )


# =================================================
# MAIN
# =================================================

def main():

    print("\n" + "=" * 60)
    print("RECONCILIATION ENGINE EVALUATION")
    print("=" * 60)

    evaluation_data = (
        prepare_evaluation_data()
    )

    accuracy, report, matrix = (
        calculate_metrics(
            evaluation_data
        )
    )

    print(
        f"\nOverall Accuracy: "
        f"{accuracy:.2%}"
    )

    print("\nClassification Report:")
    print(report)

    print("\nConfusion Matrix:")
    print(matrix)

    show_misclassifications(
        evaluation_data
    )


if __name__ == "__main__":

    main()