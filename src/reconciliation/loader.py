from pathlib import Path
import pandas as pd


# =================================================
# PATHS
# =================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = (
    PROJECT_ROOT / "data" / "processed"
)


# =================================================
# REQUIRED COLUMNS
# =================================================

REQUIRED_COLUMNS = {

    "orders": [
        "order_id",
        "customer_id",
        "order_amount",
        "order_date",
        "order_status"
    ],

    "payments": [
        "payment_id",
        "order_id",
        "amount",
        "payment_status",
        "payment_date",
        "payment_method",
        "gateway_reference"
    ],

    "settlements": [
        "settlement_id",
        "payment_reference",
        "gross_amount",
        "fee",
        "tax",
        "net_amount",
        "settlement_date",
        "settlement_status"
    ]
}


# =================================================
# LOAD DATASET
# =================================================

def load_dataset(
    dataset_name,
    date_columns
):

    file_path = (
        PROCESSED_DATA_DIR
        / f"{dataset_name}_processed.csv"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Processed dataset not found: "
            f"{file_path}"
        )

    dataframe = pd.read_csv(
        file_path
    )

    # Parse dates explicitly
    for column in date_columns:

        dataframe[column] = pd.to_datetime(
            dataframe[column],
            errors="coerce"
        )

    # Validate columns
    validate_columns(
        dataframe,
        dataset_name
    )

    print(
        f"Loaded {dataset_name}: "
        f"{len(dataframe)} records"
    )

    return dataframe


# =================================================
# VALIDATE COLUMNS
# =================================================

def validate_columns(
    dataframe,
    dataset_name
):

    required = set(
        REQUIRED_COLUMNS[dataset_name]
    )

    actual = set(
        dataframe.columns
    )

    missing_columns = (
        required - actual
    )

    if missing_columns:

        raise ValueError(
            f"{dataset_name} missing required "
            f"columns: {missing_columns}"
        )


# =================================================
# LOAD ALL DATA
# =================================================

def load_all_data():

    print("\n" + "=" * 60)
    print("LOADING RECONCILIATION DATA")
    print("=" * 60)

    orders = load_dataset(
        "orders",
        ["order_date"]
    )

    payments = load_dataset(
        "payments",
        ["payment_date"]
    )

    settlements = load_dataset(
        "settlements",
        ["settlement_date"]
    )

    print(
        "\n✓ All reconciliation data loaded successfully"
    )

    return {
        "orders": orders,
        "payments": payments,
        "settlements": settlements
    }


# =================================================
# MAIN - TEST
# =================================================

if __name__ == "__main__":

    data = load_all_data()

    print("\nDataset Shapes:")

    for name, dataframe in data.items():

        print(
            f"{name}: {dataframe.shape}"
        )

    print("\nDate Data Types:")

    print(
        "\nOrders:",
        data["orders"]["order_date"].dtype
    )

    print(
        "Payments:",
        data["payments"]["payment_date"].dtype
    )

    print(
        "Settlements:",
        data["settlements"]
        ["settlement_date"]
        .dtype
    )