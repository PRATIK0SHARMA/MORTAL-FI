import pandas as pd
import random
from pathlib import Path
from faker import Faker


# -------------------------------------------------
# Reproducibility
# -------------------------------------------------
random.seed(42)

fake = Faker("en_IN")
Faker.seed(42)


# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# Configuration
# -------------------------------------------------
NUM_TRANSACTIONS = 100


# -------------------------------------------------
# Generate Base Data
# -------------------------------------------------
def generate_base_data():

    orders = []
    payments = []
    settlements = []

    for i in range(1, NUM_TRANSACTIONS + 1):

        order_id = f"ORD{i:04d}"
        payment_id = f"PAY{i:04d}"

        customer_id = f"CUST{i:04d}"

        amount = random.choice(
            [499, 799, 999, 1499, 1999, 2499, 2999, 4999]
        )

        order_date = fake.date_time_between(
            start_date="-30d",
            end_date="-2d"
        )

        payment_date = order_date

        settlement_date = fake.date_time_between(
            start_date=payment_date,
            end_date="now"
        )

        payment_method = random.choice(
            ["UPI", "Credit Card", "Debit Card", "Net Banking"]
        )

        fee = round(amount * 0.02, 2)
        tax = round(fee * 0.18, 2)

        net_amount = round(amount - fee - tax, 2)

        # -----------------------------
        # Order
        # -----------------------------
        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_amount": amount,
                "order_date": order_date,
                "order_status": "completed"
            }
        )

        # -----------------------------
        # Payment
        # -----------------------------
        payments.append(
            {
                "payment_id": payment_id,
                "order_id": order_id,
                "amount": amount,
                "payment_status": "captured",
                "payment_date": payment_date,
                "payment_method": payment_method,
                "gateway_reference": f"GW-{random.randint(100000, 999999)}"
            }
        )

        # -----------------------------
        # Settlement
        # -----------------------------
        settlements.append(
            {
                "settlement_id": f"SET{i:04d}",
                "payment_reference": payment_id,
                "gross_amount": amount,
                "fee": fee,
                "tax": tax,
                "net_amount": net_amount,
                "settlement_date": settlement_date,
                "settlement_status": "processed"
            }
        )

    return orders, payments, settlements


# -------------------------------------------------
# Inject Exceptions
# -------------------------------------------------
def inject_exceptions(orders, payments, settlements):

    # ---------------------------------------------
    # 1. Amount mismatches
    # ---------------------------------------------
    for i in range(70, 75):

        settlements[i]["gross_amount"] = (
            settlements[i]["gross_amount"] - 100
        )

        settlements[i]["net_amount"] = round(
            settlements[i]["gross_amount"]
            - settlements[i]["fee"]
            - settlements[i]["tax"],
            2
        )

    # ---------------------------------------------
    # 2. Missing settlements
    # ---------------------------------------------
    settlements = [
        settlement
        for index, settlement in enumerate(settlements)
        if index not in range(75, 80)
    ]

    # ---------------------------------------------
    # 3. Missing order references
    # ---------------------------------------------
    for i in range(80, 83):

        payments[i]["order_id"] = f"ORD_MISSING_{i}"

    # ---------------------------------------------
    # 4. Duplicate payments
    # ---------------------------------------------
    for i in range(83, 86):

        duplicate = payments[i].copy()

        duplicate["payment_id"] = f"DUP_PAY{i:04d}"

        payments.append(duplicate)

    # ---------------------------------------------
    # 5. Reference ID mismatch
    # ---------------------------------------------
    for i in range(86, 90):

        settlements[i]["payment_reference"] = (
            settlements[i]["payment_reference"]
            .replace("PAY", "PAY_REF_")
        )

    return orders, payments, settlements


# -------------------------------------------------
# Save Data
# -------------------------------------------------
def save_data(orders, payments, settlements):

    orders_df = pd.DataFrame(orders)
    payments_df = pd.DataFrame(payments)
    settlements_df = pd.DataFrame(settlements)

    orders_path = RAW_DATA_DIR / "orders.csv"
    payments_path = RAW_DATA_DIR / "payments.csv"
    settlements_path = RAW_DATA_DIR / "settlements.csv"

    orders_df.to_csv(
        orders_path,
        index=False
    )

    payments_df.to_csv(
        payments_path,
        index=False
    )

    settlements_df.to_csv(
        settlements_path,
        index=False
    )

    print("\nData generation complete!\n")

    print(f"Orders generated: {len(orders_df)}")
    print(f"Payments generated: {len(payments_df)}")
    print(f"Settlements generated: {len(settlements_df)}")

    print("\nFiles saved in:")
    print(RAW_DATA_DIR)


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    print("Generating synthetic financial data...")

    orders, payments, settlements = generate_base_data()

    orders, payments, settlements = inject_exceptions(
        orders,
        payments,
        settlements
    )

    save_data(
        orders,
        payments,
        settlements
    )


if __name__ == "__main__":
    main()