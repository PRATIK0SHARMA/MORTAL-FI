from pathlib import Path

import pandas as pd


# =================================================
# PROJECT PATHS
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


AI_AGENT_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_agent"
    / "agent_decisions.csv"
)


EXECUTION_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "execution"
    / "execution_audit.csv"
)


VERIFICATION_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "execution"
    / "verification_audit.csv"
)


# =================================================
# AGENT PERFORMANCE ANALYZER
# =================================================

class AgentPerformanceAnalyzer:

    # =============================================
    # INITIALIZE
    # =============================================

    def __init__(self):

        self.agent_decisions = None

        self.execution_audit = None

        self.verification_audit = None


    # =============================================
    # LOAD DATA
    # =============================================

    def load_data(self):

        print(
            "\nLoading agent performance data..."
        )


        self.agent_decisions = pd.read_csv(
            AI_AGENT_PATH
        )


        if EXECUTION_AUDIT_PATH.exists():

            self.execution_audit = pd.read_csv(
                EXECUTION_AUDIT_PATH
            )

        else:

            self.execution_audit = pd.DataFrame()


        if VERIFICATION_AUDIT_PATH.exists():

            self.verification_audit = pd.read_csv(
                VERIFICATION_AUDIT_PATH
            )

        else:

            self.verification_audit = pd.DataFrame()


        print(
            f"Agent decisions loaded: "
            f"{len(self.agent_decisions)}"
        )


        print(
            f"Execution audit records loaded: "
            f"{len(self.execution_audit)}"
        )


        print(
            f"Verification audit records loaded: "
            f"{len(self.verification_audit)}"
        )


    # =============================================
    # TOTAL EXCEPTIONS
    # =============================================

    def total_exceptions(self):

        return len(
            self.agent_decisions
        )


    # =============================================
    # AUTO RESOLUTION COUNT
    # =============================================

    def auto_resolutions(self):

        return int(
            (
                self.agent_decisions[
                    "agent_decision"
                ]
                == "AUTO_RESOLVE"
            ).sum()
        )


    # =============================================
    # ESCALATION COUNT
    # =============================================

    def escalations(self):

        return int(
            (
                self.agent_decisions[
                    "agent_decision"
                ]
                == "ESCALATE"
            ).sum()
        )


    # =============================================
    # MANUAL REVIEW COUNT
    # =============================================

    def manual_reviews(self):

        return int(
            (
                self.agent_decisions[
                    "human_review_required"
                ]
                == True
            ).sum()
        )


    # =============================================
    # AUTO RESOLUTION RATE
    # =============================================

    def auto_resolution_rate(self):

        total = self.total_exceptions()

        if total == 0:

            return 0.0


        return round(
            (
                self.auto_resolutions()
                / total
            )
            * 100,
            2
        )


    # =============================================
    # ESCALATION RATE
    # =============================================

    def escalation_rate(self):

        total = self.total_exceptions()

        if total == 0:

            return 0.0


        return round(
            (
                self.escalations()
                / total
            )
            * 100,
            2
        )


    # =============================================
    # AVERAGE CONFIDENCE
    # =============================================

    def average_confidence(self):

        confidence = pd.to_numeric(
            self.agent_decisions[
                "confidence"
            ],
            errors="coerce"
        )


        if confidence.empty:

            return 0.0


        return round(
            confidence.mean() * 100,
            2
        )


    # =============================================
    # HIGH RISK COUNT
    # =============================================

    def high_risk_count(self):

        return int(
            (
                self.agent_decisions[
                    "financial_risk"
                ]
                == "HIGH"
            ).sum()
        )


    # =============================================
    # LOW RISK COUNT
    # =============================================

    def low_risk_count(self):

        return int(
            (
                self.agent_decisions[
                    "financial_risk"
                ]
                == "LOW"
            ).sum()
        )


    # =============================================
    # EXECUTION SUCCESS
    # =============================================

    def execution_success_count(self):

        if self.execution_audit.empty:

            return 0


        return int(
            (
                self.execution_audit[
                    "execution_status"
                ]
                == "EXECUTED"
            ).sum()
        )


    # =============================================
    # VERIFICATION SUCCESS
    # =============================================

    def verification_success_count(self):

        if self.verification_audit.empty:

            return 0


        return int(
            (
                self.verification_audit[
                    "verification_status"
                ]
                == "VERIFIED"
            ).sum()
        )


    # =============================================
    # VERIFICATION RATE
    # =============================================

    def verification_rate(self):

        auto_resolved = (
            self.auto_resolutions()
        )


        if auto_resolved == 0:

            return 0.0


        verified = (
            self.verification_success_count()
        )


        # -----------------------------------------
        # Cap at auto-resolution count
        # -----------------------------------------
        #
        # Prevent repeated audit records from
        # artificially increasing the rate.
        #
        # -----------------------------------------

        verified = min(
            verified,
            auto_resolved
        )


        return round(
            (
                verified
                / auto_resolved
            )
            * 100,
            2
        )


    # =============================================
    # BUILD PERFORMANCE SUMMARY
    # =============================================

    def build_summary(self):

        return {

            "total_exceptions":
                self.total_exceptions(),

            "auto_resolutions":
                self.auto_resolutions(),

            "escalations":
                self.escalations(),

            "manual_reviews":
                self.manual_reviews(),

            "auto_resolution_rate":
                self.auto_resolution_rate(),

            "escalation_rate":
                self.escalation_rate(),

            "average_confidence":
                self.average_confidence(),

            "high_risk_exceptions":
                self.high_risk_count(),

            "low_risk_exceptions":
                self.low_risk_count(),

            "successful_executions":
                self.execution_success_count(),

            "verified_resolutions":
                self.verification_success_count(),

            "verification_rate":
                self.verification_rate()
        }


# =================================================
# TEST
# =================================================

def main():

    print("\n" + "=" * 60)

    print(
        "AI AGENT PERFORMANCE ANALYSIS"
    )

    print("=" * 60)


    analyzer = (
        AgentPerformanceAnalyzer()
    )


    analyzer.load_data()


    summary = (
        analyzer.build_summary()
    )


    print("\nPerformance Metrics:")
    print("-" * 60)


    print(
        f"Total Exceptions: "
        f"{summary['total_exceptions']}"
    )


    print(
        f"Auto Resolutions: "
        f"{summary['auto_resolutions']}"
    )


    print(
        f"Escalations: "
        f"{summary['escalations']}"
    )


    print(
        f"Manual Reviews: "
        f"{summary['manual_reviews']}"
    )


    print(
        f"Auto Resolution Rate: "
        f"{summary['auto_resolution_rate']}%"
    )


    print(
        f"Escalation Rate: "
        f"{summary['escalation_rate']}%"
    )


    print(
        f"Average AI Confidence: "
        f"{summary['average_confidence']}%"
    )


    print(
        f"High Risk Exceptions: "
        f"{summary['high_risk_exceptions']}"
    )


    print(
        f"Low Risk Exceptions: "
        f"{summary['low_risk_exceptions']}"
    )


    print(
        f"Successful Executions: "
        f"{summary['successful_executions']}"
    )


    print(
        f"Verified Resolutions: "
        f"{summary['verified_resolutions']}"
    )


    print(
        f"Verification Rate: "
        f"{summary['verification_rate']}%"
    )


    print("\n" + "=" * 60)

    print(
        "AGENT PERFORMANCE ANALYSIS COMPLETE"
    )

    print("=" * 60)


# =================================================
# ENTRY POINT
# =================================================

if __name__ == "__main__":

    main()