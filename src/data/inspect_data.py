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
# Inspect Dataset
# -------------------------------------------------
def inspect_dataset(name, dataframe):

    print("\n" + "=" * 50)
    print(f"{name.upper()} DATASET")
    print("=" * 50)

    print("\nShape:")
    print(dataframe.shape)

    print("\nColumns:")
    print(dataframe.columns.tolist())

    print("\nData Types:")
    print(dataframe.dtypes)

    print("\nMissing Values:")
    print(dataframe.isnull().sum())

    print("\nDuplicate Rows:")
    print(dataframe.duplicated().sum())

    print("\nFirst 5 Records:")
    print(dataframe.head())


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    orders, payments, settlements = load_data()

    inspect_dataset(
        "Orders",
        orders
    )

    inspect_dataset(
        "Payments",
        payments
    )

    inspect_dataset(
        "Settlements",
        settlements
    )


if __name__ == "__main__":
    main()