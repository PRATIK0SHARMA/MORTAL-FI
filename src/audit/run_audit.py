from pathlib import Path

import pandas as pd

from audit_engine import AuditEngine


# =================================================
# PROJECT PATHS
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

RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "resolution"
    / "resolution_results.csv"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "audit"
)

OUTPUT_PATH = (
    OUTPUT_DIRECTORY
    / "audit_trail.csv"
)


# =================================================
# LOAD DATA
# =================================================

def load_audit_data():

    print("\nLoading reconciliation results...")

    reconciliation_results = (
        pd.read_csv(
            RECONCILIATION_PATH
        )
    )

    print(
        f"Loaded {len(reconciliation_results)} "
        f"reconciliation records"
    )


    print("\nLoading resolution results...")

    resolution_results = (
        pd.read_csv(
            RESOLUTION_PATH
        )
    )

    print(
        f"Loaded {len(resolution_results)} "
        f"resolution records"
    )


    return (
        reconciliation_results,
        resolution_results
    )


# =================================================
# MAIN
# =================================================

def main():

    reconciliation_results, resolution_results = (
        load_audit_data()
    )


    # ---------------------------------------------
    # CREATE AUDIT ENGINE
    # ---------------------------------------------

    audit_engine = AuditEngine(

        reconciliation_results=
        reconciliation_results,

        resolution_results=
        resolution_results
    )


    # ---------------------------------------------
    # BUILD AUDIT TRAIL
    # ---------------------------------------------

    audit_trail = (
        audit_engine.build_audit_trail()
    )


    # ---------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )


    # ---------------------------------------------
    # SAVE AUDIT TRAIL
    # ---------------------------------------------

    audit_trail.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print(
        "\n✓ Audit trail saved:"
    )

    print(
        OUTPUT_PATH
    )


    # ---------------------------------------------
    # AUDIT SUMMARY
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)

    print(
        audit_trail[
            "status"
        ]
        .value_counts()
    )


    # ---------------------------------------------
    # SAMPLE EXCEPTION AUDIT RECORDS
    # ---------------------------------------------

    exceptions = (
        audit_trail[
            audit_trail[
                "status"
            ] != "MATCHED"
        ]
    )


    print(
        "\nSample Exception Audit Records:"
    )

    print(
        exceptions[
            [
                "payment_id",
                "exception_type",
                "risk_level",
                "recommended_action"
            ]
        ]
        .head(10)
        .to_string(
            index=False
        )
    )


if __name__ == "__main__":

    main()