from pathlib import Path
import pandas as pd


# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# -------------------------------------------------
# Load Data
# -------------------------------------------------
def load_data():

    orders = pd.read_csv(
        RAW_DATA_DIR / "orders.csv"
    )

    payments = pd.read_csv(
        RAW_DATA_DIR / "payments.csv"
    )

    settlements = pd.read_csv(
        RAW_DATA_DIR / "settlements.csv"
    )

    return orders, payments, settlements


# -------------------------------------------------
# Validate Amount Mismatches
# -------------------------------------------------
def validate_amount_mismatches(payments, settlements):

    merged = payments.merge(
        settlements,
        left_on="payment_id",
        right_on="payment_reference",
        how="inner"
    )

    mismatches = merged[
        merged["amount"] != merged["gross_amount"]
    ]

    print("\nAMOUNT MISMATCHES")
    print("-" * 50)
    print(f"Found: {len(mismatches)}")

    if not mismatches.empty:
        print(
            mismatches[
                [
                    "payment_id",
                    "amount",
                    "gross_amount"
                ]
            ]
        )


# -------------------------------------------------
# Validate Missing Settlements
# -------------------------------------------------
def validate_missing_settlements(payments, settlements):

    missing = payments[
        ~payments["payment_id"].isin(
            settlements["payment_reference"]
        )
    ]

    print("\nMISSING SETTLEMENTS")
    print("-" * 50)
    print(f"Found: {len(missing)}")

    if not missing.empty:
        print(
            missing[
                [
                    "payment_id",
                    "order_id",
                    "amount"
                ]
            ]
        )


# -------------------------------------------------
# Validate Missing Orders
# -------------------------------------------------
def validate_missing_orders(orders, payments):

    missing = payments[
        ~payments["order_id"].isin(
            orders["order_id"]
        )
    ]

    print("\nPAYMENTS WITH MISSING ORDERS")
    print("-" * 50)
    print(f"Found: {len(missing)}")

    if not missing.empty:
        print(
            missing[
                [
                    "payment_id",
                    "order_id",
                    "amount"
                ]
            ]
        )


# -------------------------------------------------
# Validate Duplicate Business Payments
# -------------------------------------------------
def validate_duplicate_payments(payments):

    duplicates = payments[
        payments.duplicated(
            subset=[
                "order_id",
                "amount"
            ],
            keep=False
        )
    ]

    print("\nDUPLICATE BUSINESS PAYMENTS")
    print("-" * 50)
    print(f"Found: {len(duplicates)}")

    if not duplicates.empty:
        print(
            duplicates[
                [
                    "payment_id",
                    "order_id",
                    "amount"
                ]
            ].sort_values(
                by="order_id"
            )
        )


# -------------------------------------------------
# Validate Reference Mismatches
# -------------------------------------------------
def validate_reference_mismatches(
    payments,
    settlements
):

    mismatches = settlements[
        ~settlements["payment_reference"].isin(
            payments["payment_id"]
        )
    ]

    print("\nREFERENCE ID MISMATCHES")
    print("-" * 50)
    print(f"Found: {len(mismatches)}")

    if not mismatches.empty:
        print(
            mismatches[
                [
                    "settlement_id",
                    "payment_reference",
                    "gross_amount"
                ]
            ]
        )


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    orders, payments, settlements = load_data()

    print("\n" + "=" * 60)
    print("SYNTHETIC DATA EXCEPTION VALIDATION")
    print("=" * 60)

    validate_amount_mismatches(
        payments,
        settlements
    )

    validate_missing_settlements(
        payments,
        settlements
    )

    validate_missing_orders(
        orders,
        payments
    )

    validate_duplicate_payments(
        payments
    )

    validate_reference_mismatches(
        payments,
        settlements
    )


if __name__ == "__main__":
    main()