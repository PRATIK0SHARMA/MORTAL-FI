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
# LOAD DATA
# =================================================

def load_processed_dataset(dataset_name):

    file_path = (
        PROCESSED_DATA_DIR
        / f"{dataset_name}_processed.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}"
        )

    return pd.read_csv(
        file_path
    )


# =================================================
# INSPECT DATASET
# =================================================

def inspect_dataset(dataset_name):

    dataframe = load_processed_dataset(
        dataset_name
    )

    print("\n" + "=" * 60)
    print(
        f"{dataset_name.upper()} PROCESSED DATA"
    )
    print("=" * 60)

    print("\nShape:")
    print(dataframe.shape)

    print("\nData Types:")
    print(dataframe.dtypes)

    print("\nMissing Values:")
    print(dataframe.isnull().sum())

    print("\nFirst 3 Records:")
    print(dataframe.head(3))


# =================================================
# MAIN
# =================================================

def main():

    inspect_dataset("orders")

    inspect_dataset("payments")

    inspect_dataset("settlements")


if __name__ == "__main__":
    main()