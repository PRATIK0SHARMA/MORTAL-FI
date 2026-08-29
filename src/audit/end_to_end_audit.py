from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


# =================================================
# DATA PATHS
# =================================================

RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)


AI_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_audit"
    / "ai_agent_audit_trail.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "audit"
)


# =================================================
# END-TO-END AUDIT BUILDER
# =================================================

class EndToEndAuditBuilder:


    def __init__(self):

        self.reconciliation = None

        self.ai_resolution = None

        self.ai_audit = None


    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        print(
            "\nLoading end-to-end audit data..."
        )


        self.reconciliation = (
            pd.read_csv(
                RECONCILIATION_PATH
            )
        )


        self.ai_resolution = (
            pd.read_csv(
                AI_RESOLUTION_PATH
            )
        )


        self.ai_audit = (
            pd.read_csv(
                AI_AUDIT_PATH
            )
        )


        print(
            f"Reconciliation records: "
            f"{len(self.reconciliation)}"
        )


        print(
            f"AI resolution records: "
            f"{len(self.ai_resolution)}"
        )


        print(
            f"AI audit records: "
            f"{len(self.ai_audit)}"
        )


    # =================================================
    # BUILD END-TO-END AUDIT
    # =================================================

    def build_audit(self):

        audit_dataframe = (

            self.reconciliation.copy()

        )


        # ---------------------------------------------
        # MERGE AI RESOLUTION RESULTS
        # ---------------------------------------------

        ai_columns = [

            "payment_id",

            "agent_decision",

            "resolution_status",

            "action_taken",

            "financial_risk",

            "confidence",

            "auto_resolvable",

            "ai_response_valid",

            "human_review_required"

        ]


        available_ai_columns = [

            column

            for column in ai_columns

            if column
            in self.ai_resolution.columns

        ]


        audit_dataframe = (

            audit_dataframe.merge(

                self.ai_resolution[
                    available_ai_columns
                ],

                on="payment_id",

                how="left"

            )

        )


        # ---------------------------------------------
        # MERGE AI AUDIT INFORMATION
        # ---------------------------------------------

        audit_columns = [

            "payment_id",

            "guardrail_violations"

        ]


        available_audit_columns = [

            column

            for column in audit_columns

            if column
            in self.ai_audit.columns

        ]


        audit_dataframe = (

            audit_dataframe.merge(

                self.ai_audit[
                    available_audit_columns
                ],

                on="payment_id",

                how="left"

            )

        )


        # ---------------------------------------------
        # FINAL AUDIT STATUS
        # ---------------------------------------------

        audit_dataframe[
            "final_processing_status"
        ] = (

            audit_dataframe[
                "resolution_status"
            ]
            .fillna(
                "MATCHED_NO_AI_ACTION"
            )

        )


        return audit_dataframe


    # =================================================
    # SAVE AUDIT
    # =================================================

    def save_audit(
        self,
        audit_dataframe
    ):

        OUTPUT_DIRECTORY.mkdir(

            parents=True,

            exist_ok=True

        )


        output_path = (

            OUTPUT_DIRECTORY
            / "end_to_end_audit_trail.csv"

        )


        audit_dataframe.to_csv(

            output_path,

            index=False

        )


        print(
            "\n✓ End-to-end audit trail saved:"
        )

        print(
            output_path
        )


        return output_path


    # =================================================
    # DISPLAY SUMMARY
    # =================================================

    def display_summary(
        self,
        audit_dataframe
    ):

        print(
            "\n" + "=" * 60
        )

        print(
            "END-TO-END AUDIT SUMMARY"
        )

        print(
            "=" * 60
        )


        print(
            f"Total Records: "
            f"{len(audit_dataframe)}"
        )


        print(
            "\nFinal Processing Status:"
        )


        print(

            audit_dataframe[
                "final_processing_status"
            ]
            .value_counts()

        )


# =================================================
# MAIN
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "BUILDING END-TO-END AUDIT TRAIL"
    )

    print(
        "=" * 60
    )


    builder = (
        EndToEndAuditBuilder()
    )


    builder.load_data()


    audit_dataframe = (
        builder.build_audit()
    )


    builder.display_summary(
        audit_dataframe
    )


    builder.save_audit(
        audit_dataframe
    )


if __name__ == "__main__":

    main()