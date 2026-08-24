from datetime import datetime
from pathlib import Path
import json


# =================================================
# PATHS
# =================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "data" / "reports"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =================================================
# SAVE REPORT
# =================================================

def save_report(report):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_path = (
        REPORT_DIR
        / f"etl_report_{timestamp}.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print("\nETL Audit Report Generated")

    print(
        f"Saved to:\n{output_path}"
    )