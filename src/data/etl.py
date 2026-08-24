from pathlib import Path
import pandas as pd


# =================================================
# PATHS
# =================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =================================================
# SCHEMAS
# =================================================

SCHEMAS = {

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
# VALID VALUES
# =================================================

VALID_ORDER_STATUSES = {
    "completed",
    "cancelled",
    "pending"
}

VALID_PAYMENT_STATUSES = {
    "captured",
    "failed",
    "refunded"
}

VALID_PAYMENT_METHODS = {
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking"
}

VALID_SETTLEMENT_STATUSES = {
    "processed",
    "pending",
    "failed"
}

# =================================================
# LOAD DATA
# =================================================

def load_dataset(dataset_name):

    file_path = (
        RAW_DATA_DIR
        / f"{dataset_name}.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    print(f"Loading {dataset_name}.csv...")

    dataframe = pd.read_csv(
        file_path
    )

    return dataframe


# =================================================
# SCHEMA VALIDATION
# =================================================

def validate_schema(
    dataframe,
    dataset_name
):

    expected_columns = set(
        SCHEMAS[dataset_name]
    )

    actual_columns = set(
        dataframe.columns
    )

    missing_columns = (
        expected_columns
        - actual_columns
    )

    unexpected_columns = (
        actual_columns
        - expected_columns
    )

    if missing_columns:

        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{missing_columns}"
        )

    if unexpected_columns:

        print(
            f"Warning: {dataset_name} contains "
            f"unexpected columns: "
            f"{unexpected_columns}"
        )

    print(
        f"✓ Schema validation passed: "
        f"{dataset_name}"
    )


# =================================================
# REMOVE FULLY DUPLICATE ROWS
# =================================================

def remove_duplicates(
    dataframe,
    dataset_name
):

    original_count = len(
        dataframe
    )

    dataframe = dataframe.drop_duplicates()

    removed_count = (
        original_count
        - len(dataframe)
    )

    print(
        f"{dataset_name}: "
        f"{removed_count} full duplicate rows removed"
    )

    return dataframe


# =================================================
# NORMALIZE STRING COLUMNS
# =================================================

def normalize_strings(
    dataframe
):

    string_columns = dataframe.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in string_columns:

        dataframe[column] = (
            dataframe[column]
            .astype(str)
            .str.strip()
        )

    return dataframe


# =================================================
# CONVERT DATES
# =================================================

def convert_dates(
    dataframe,
    date_columns
):

    for column in date_columns:

        dataframe[column] = pd.to_datetime(
            dataframe[column],
            errors="coerce"
        )

    return dataframe


# =================================================
# CONVERT NUMERIC COLUMNS
# =================================================

def convert_numeric(
    dataframe,
    numeric_columns
):

    for column in numeric_columns:

        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    return dataframe


# =================================================
# CLEAN ORDERS
# =================================================

def clean_orders(dataframe):

    dataframe = normalize_strings(
        dataframe
    )

    dataframe = convert_dates(
        dataframe,
        ["order_date"]
    )

    dataframe = convert_numeric(
        dataframe,
        ["order_amount"]
    )

    return dataframe


# =================================================
# CLEAN PAYMENTS
# =================================================

def clean_payments(dataframe):

    dataframe = normalize_strings(
        dataframe
    )

    dataframe = convert_dates(
        dataframe,
        ["payment_date"]
    )

    dataframe = convert_numeric(
        dataframe,
        ["amount"]
    )

    return dataframe


# =================================================
# CLEAN SETTLEMENTS
# =================================================

def clean_settlements(dataframe):

    dataframe = normalize_strings(
        dataframe
    )

    dataframe = convert_dates(
        dataframe,
        ["settlement_date"]
    )

    dataframe = convert_numeric(
        dataframe,
        [
            "gross_amount",
            "fee",
            "tax",
            "net_amount"
        ]
    )

    return dataframe


# =================================================
# DATA QUALITY VALIDATION
# =================================================

def validate_data_quality(
    dataframe,
    dataset_name
):

    missing_values = (
        dataframe.isnull().sum().sum()
    )

    print(
        f"{dataset_name}: "
        f"{missing_values} missing values"
    )

    if missing_values > 0:

        print(
            f"Warning: {dataset_name} contains "
            f"missing or invalid values"
        )

# =================================================
# FINANCIAL VALIDATION
# =================================================

def validate_financial_rules(
    dataframe,
    dataset_name
):

    print(
        f"\nRunning financial validation "
        f"for {dataset_name}..."
    )

    invalid_records = 0


    # ---------------------------------------------
    # ORDERS
    # ---------------------------------------------
    if dataset_name == "orders":

        invalid_amounts = dataframe[
            dataframe["order_amount"] <= 0
        ]

        invalid_statuses = dataframe[
            ~dataframe["order_status"].isin(
                VALID_ORDER_STATUSES
            )
        ]

        invalid_dates = dataframe[
            dataframe["order_date"].isna()
        ]

        invalid_records = (
            len(invalid_amounts)
            + len(invalid_statuses)
            + len(invalid_dates)
        )


    # ---------------------------------------------
    # PAYMENTS
    # ---------------------------------------------
    elif dataset_name == "payments":

        invalid_amounts = dataframe[
            dataframe["amount"] <= 0
        ]

        invalid_statuses = dataframe[
            ~dataframe["payment_status"].isin(
                VALID_PAYMENT_STATUSES
            )
        ]

        invalid_methods = dataframe[
            ~dataframe["payment_method"].isin(
                VALID_PAYMENT_METHODS
            )
        ]

        invalid_dates = dataframe[
            dataframe["payment_date"].isna()
        ]

        invalid_records = (
            len(invalid_amounts)
            + len(invalid_statuses)
            + len(invalid_methods)
            + len(invalid_dates)
        )


    # ---------------------------------------------
    # SETTLEMENTS
    # ---------------------------------------------
    elif dataset_name == "settlements":

        invalid_gross_amount = dataframe[
            dataframe["gross_amount"] <= 0
        ]

        invalid_fee = dataframe[
            dataframe["fee"] < 0
        ]

        invalid_tax = dataframe[
            dataframe["tax"] < 0
        ]

        invalid_net_amount = dataframe[
            dataframe["net_amount"] <= 0
        ]

        expected_net_amount = (
            dataframe["gross_amount"]
            - dataframe["fee"]
            - dataframe["tax"]
        ).round(2)

        invalid_calculation = dataframe[
            dataframe["net_amount"].round(2)
            != expected_net_amount
        ]

        invalid_records = (
            len(invalid_gross_amount)
            + len(invalid_fee)
            + len(invalid_tax)
            + len(invalid_net_amount)
            + len(invalid_calculation)
        )


    print(
        f"{dataset_name}: "
        f"{invalid_records} financial validation issues"
    )

    return invalid_records


# =================================================
# SAVE PROCESSED DATA
# =================================================

def save_processed_data(
    dataframe,
    dataset_name
):

    output_path = (
        PROCESSED_DATA_DIR
        / f"{dataset_name}_processed.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {output_path}"
    )


# =================================================
# ETL PIPELINE
# =================================================

def process_dataset(
    dataset_name,
    cleaning_function
):

    print("\n" + "=" * 60)
    print(
        f"PROCESSING {dataset_name.upper()}"
    )
    print("=" * 60)

    dataframe = load_dataset(
        dataset_name
    )

    validate_schema(
        dataframe,
        dataset_name
    )

    dataframe = remove_duplicates(
        dataframe,
        dataset_name
    )

    dataframe = cleaning_function(
        dataframe
    )

    validate_data_quality(
        dataframe,
        dataset_name
    )

    validate_financial_rules(
        dataframe,
        dataset_name
    )
    
    save_processed_data(
    dataframe,
    dataset_name
    )

    print(
        f"✓ {dataset_name} processed successfully"
    )


# =================================================
# MAIN
# =================================================

def main():

    process_dataset(
        "orders",
        clean_orders
    )

    process_dataset(
        "payments",
        clean_payments
    )

    process_dataset(
        "settlements",
        clean_settlements
    )


if __name__ == "__main__":
    main()