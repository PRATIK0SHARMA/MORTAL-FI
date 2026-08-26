from pathlib import Path
from datetime import datetime

import pandas as pd


# =================================================
# PATH CONFIGURATION
# =================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RECONCILIATION_RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)

RESOLUTION_RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "resolution"
    / "resolution_results.csv"
)

REPORTS_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "reports"
)


# =================================================
# EXCEPTION REPORT BUILDER
# =================================================

def build_exception_report():

    print("\n" + "=" * 60)
    print("BUILDING HONEST EXCEPTION REPORT")
    print("=" * 60)


    # ---------------------------------------------
    # LOAD RECONCILIATION RESULTS
    # ---------------------------------------------

    print("\nLoading reconciliation results...")

    reconciliation = pd.read_csv(
        RECONCILIATION_RESULTS_PATH
    )

    print(
        f"Loaded {len(reconciliation)} "
        f"reconciliation records"
    )


    # ---------------------------------------------
    # LOAD RESOLUTION RESULTS
    # ---------------------------------------------

    print("\nLoading resolution results...")

    resolution = pd.read_csv(
        RESOLUTION_RESULTS_PATH
    )

    print(
        f"Loaded {len(resolution)} "
        f"resolution records"
    )


    # ---------------------------------------------
    # FILTER EXCEPTIONS
    # ---------------------------------------------

    exceptions = reconciliation[
        reconciliation["status"]
        == "EXCEPTION"
    ].copy()


    print(
        f"\nTotal Exceptions Found: "
        f"{len(exceptions)}"
    )


    # ---------------------------------------------
    # MERGE RESOLUTION INFORMATION
    # ---------------------------------------------

    resolution_columns = [

        "payment_id",

        "risk_level",

        "recommended_action"

    ]


    exceptions = exceptions.merge(

        resolution[
            resolution_columns
        ],

        on="payment_id",

        how="left"

    )


    # ---------------------------------------------
    # EXCEPTION TYPE SUMMARY
    # ---------------------------------------------

    exception_summary = (

        exceptions[
            "exception_type"
        ]

        .value_counts()

        .reset_index()

    )


    exception_summary.columns = [

        "exception_type",

        "count"

    ]


    # ---------------------------------------------
    # AUTO VS MANUAL RESOLUTION
    # ---------------------------------------------

    auto_resolvable_types = [

        "REFERENCE_MISMATCH"

    ]


    exceptions[
        "resolution_status"
    ] = exceptions[
        "exception_type"
    ].apply(

        lambda exception_type:

        (
            "AUTO_RECOVERED"

            if exception_type
            in auto_resolvable_types

            else "MANUAL_REVIEW_REQUIRED"
        )

    )


    # ---------------------------------------------
    # RESOLUTION SUMMARY
    # ---------------------------------------------

    resolution_summary = (

        exceptions[
            "resolution_status"
        ]

        .value_counts()

        .reset_index()

    )


    resolution_summary.columns = [

        "resolution_status",

        "count"

    ]


    # ---------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------

    REPORTS_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True

    )


    # ---------------------------------------------
    # SAVE EXCEPTION LIST
    # ---------------------------------------------

    exception_list_path = (

        REPORTS_DIRECTORY
        / "unresolved_exceptions.csv"

    )


    unresolved_exceptions = exceptions[

        exceptions[
            "resolution_status"
        ]

        == "MANUAL_REVIEW_REQUIRED"

    ].copy()


    unresolved_exceptions.to_csv(

        exception_list_path,

        index=False

    )


    # ---------------------------------------------
    # SAVE SUMMARY
    # ---------------------------------------------

    exception_summary_path = (

        REPORTS_DIRECTORY
        / "exception_summary.csv"

    )


    exception_summary.to_csv(

        exception_summary_path,

        index=False

    )


    # ---------------------------------------------
    # PRINT REPORT
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("EXCEPTION TYPE SUMMARY")
    print("=" * 60)

    print(
        exception_summary.to_string(
            index=False
        )
    )


    print("\n" + "=" * 60)
    print("RESOLUTION STATUS")
    print("=" * 60)

    print(
        resolution_summary.to_string(
            index=False
        )
    )


    print("\n" + "=" * 60)
    print("HONEST EXCEPTION LIST")
    print("=" * 60)

    print(
        f"Automatically Recovered: "
        f"{len(exceptions) - len(unresolved_exceptions)}"
    )

    print(
        f"Manual Review Required: "
        f"{len(unresolved_exceptions)}"
    )


    print("\n✓ Exception summary saved:")

    print(
        exception_summary_path
    )


    print("\n✓ Unresolved exceptions saved:")

    print(
        exception_list_path
    )


    return {

        "exceptions": exceptions,

        "exception_summary": exception_summary,

        "unresolved_exceptions": unresolved_exceptions

    }


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":

    build_exception_report()