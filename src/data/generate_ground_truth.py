import pandas as pd
from pathlib import Path


# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

GROUND_TRUTH_DIR = PROJECT_ROOT / "data" / "ground_truth"
GROUND_TRUTH_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# Load Data
# -------------------------------------------------
def load_data():

    payments = pd.read_csv(
        RAW_DATA_DIR / "payments.csv"
    )

    return payments


# -------------------------------------------------
# Generate Ground Truth
# -------------------------------------------------
def generate_ground_truth(payments):

    labels = []

    for _, payment in payments.iterrows():

        payment_id = payment["payment_id"]

        expected_status = "MATCHED"
        exception_type = "NONE"

        # -----------------------------------------
        # Amount Mismatch
        # -----------------------------------------
        if payment_id in [
            "PAY0071",
            "PAY0072",
            "PAY0073",
            "PAY0074",
            "PAY0075"
        ]:

            expected_status = "EXCEPTION"
            exception_type = "AMOUNT_MISMATCH"

        # -----------------------------------------
        # Missing Settlement
        # -----------------------------------------
        elif payment_id in [
            "PAY0076",
            "PAY0077",
            "PAY0078",
            "PAY0079",
            "PAY0080"
        ]:

            expected_status = "EXCEPTION"
            exception_type = "MISSING_SETTLEMENT"

        # -----------------------------------------
        # Missing Order
        # -----------------------------------------
        elif payment_id in [
            "PAY0081",
            "PAY0082",
            "PAY0083"
        ]:

            expected_status = "EXCEPTION"
            exception_type = "MISSING_ORDER"

        # -----------------------------------------
        # Duplicate Payments
        # -----------------------------------------
        elif payment_id in [
            "PAY0084",
            "PAY0085",
            "PAY0086",
            "DUP_PAY0083",
            "DUP_PAY0084",
            "DUP_PAY0085"
        ]:

            expected_status = "DUPLICATE"
            exception_type = "DUPLICATE_PAYMENT"

        # -----------------------------------------
        # Reference Mismatch
        # -----------------------------------------
        elif payment_id in [
            "PAY0092",
            "PAY0093",
            "PAY0094",
            "PAY0095"
        ]:

            expected_status = "FUZZY_MATCH"
            exception_type = "REFERENCE_MISMATCH"

        labels.append(
            {
                "payment_id": payment_id,
                "expected_status": expected_status,
                "exception_type": exception_type
            }
        )

    return pd.DataFrame(labels)


# -------------------------------------------------
# Save Ground Truth
# -------------------------------------------------
def save_ground_truth(labels):

    output_path = (
        GROUND_TRUTH_DIR
        / "transaction_labels.csv"
    )

    labels.to_csv(
        output_path,
        index=False
    )

    print("\nGround truth generated successfully!")
    print(f"Total labels: {len(labels)}")

    print("\nStatus Distribution:")
    print(
        labels["expected_status"]
        .value_counts()
    )

    print("\nException Distribution:")
    print(
        labels["exception_type"]
        .value_counts()
    )

    print(f"\nSaved to:\n{output_path}")


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    payments = load_data()

    labels = generate_ground_truth(
        payments
    )

    save_ground_truth(
        labels
    )


if __name__ == "__main__":
    main()