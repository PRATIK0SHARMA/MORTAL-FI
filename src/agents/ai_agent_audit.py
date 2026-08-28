from pathlib import Path
from datetime import datetime

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)


OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "ai_audit"
)


# =================================================
# AI AGENT AUDIT BUILDER
# =================================================

class AIAgentAudit:


    def __init__(self):

        self.ai_results = None


    # =================================================
    # LOAD AI RESULTS
    # =================================================

    def load_data(self):

        print(
            "\nLoading AI resolution results..."
        )


        self.ai_results = pd.read_csv(
            AI_RESOLUTION_PATH
        )


        print(
            f"AI resolution records loaded: "
            f"{len(self.ai_results)}"
        )


    # =================================================
    # BUILD AUDIT TRAIL
    # =================================================

    def build_audit_trail(self):

        audit_records = []


        for _, record in self.ai_results.iterrows():

            audit_record = {

                # -------------------------------------
                # AUDIT METADATA
                # -------------------------------------

                "audit_timestamp":

                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),


                "agent_name":

                    "MORTAL-FI AI Resolution Agent",


                # -------------------------------------
                # TRANSACTION
                # -------------------------------------

                "payment_id":

                    record.get(
                        "payment_id"
                    ),


                "exception_type":

                    record.get(
                        "exception_type"
                    ),


                # -------------------------------------
                # DETERMINISTIC REASONING
                # -------------------------------------

                "reasoning_status":

                    record.get(
                        "reasoning_status"
                    ),


                "financial_risk":

                    record.get(
                        "financial_risk"
                    ),


                "confidence":

                    record.get(
                        "confidence"
                    ),


                "auto_resolvable":

                    record.get(
                        "auto_resolvable"
                    ),


                # -------------------------------------
                # AI VALIDATION
                # -------------------------------------

                "ai_response_valid":

                    record.get(
                        "ai_response_valid"
                    ),


                "guardrail_violations":

                    record.get(
                        "guardrail_violations"
                    ),


                # -------------------------------------
                # FINAL AGENT DECISION
                # -------------------------------------

                "agent_decision":

                    record.get(
                        "agent_decision"
                    ),


                "resolution_status":

                    record.get(
                        "resolution_status"
                    ),


                "action_taken":

                    record.get(
                        "action_taken"
                    ),


                "human_review_required":

                    record.get(
                        "human_review_required"
                    )

            }


            audit_records.append(
                audit_record
            )


        audit_dataframe = (
            pd.DataFrame(
                audit_records
            )
        )


        return audit_dataframe


    # =================================================
    # SAVE AUDIT TRAIL
    # =================================================

    def save_audit_trail(
        self,
        audit_dataframe
    ):


        OUTPUT_DIRECTORY.mkdir(

            parents=True,

            exist_ok=True

        )


        output_path = (

            OUTPUT_DIRECTORY
            / "ai_agent_audit_trail.csv"

        )


        audit_dataframe.to_csv(

            output_path,

            index=False

        )


        print(
            "\n✓ AI agent audit trail saved:"
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
            "AI AGENT AUDIT SUMMARY"
        )

        print(
            "=" * 60
        )


        print(
            f"Total AI Decisions: "
            f"{len(audit_dataframe)}"
        )


        print(
            f"Valid AI Responses: "
            f"{audit_dataframe['ai_response_valid'].sum()}"
        )


        print(
            f"Guardrail Violations: "
            f"{audit_dataframe['guardrail_violations'].notna().sum()}"
        )


        print(
            f"Auto Resolutions: "
            f"{len(audit_dataframe[audit_dataframe['agent_decision'] == 'AUTO_RESOLVE'])}"
        )


        print(
            f"Escalations: "
            f"{len(audit_dataframe[audit_dataframe['agent_decision'] == 'ESCALATE'])}"
        )


# =================================================
# MAIN
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "BUILDING AI AGENT AUDIT TRAIL"
    )

    print(
        "=" * 60
    )


    audit_builder = (
        AIAgentAudit()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    audit_builder.load_data()


    # ---------------------------------------------
    # BUILD AUDIT
    # ---------------------------------------------

    audit_dataframe = (

        audit_builder.build_audit_trail()

    )


    # ---------------------------------------------
    # DISPLAY SUMMARY
    # ---------------------------------------------

    audit_builder.display_summary(
        audit_dataframe
    )


    # ---------------------------------------------
    # SAVE AUDIT
    # ---------------------------------------------

    audit_builder.save_audit_trail(
        audit_dataframe
    )


if __name__ == "__main__":

    main()