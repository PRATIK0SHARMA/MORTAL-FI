from src.agents.context_builder import (
    ExceptionContextBuilder
)

from src.agents.financial_reasoner import (
    FinancialReasoner
)


# =================================================
# AI EXCEPTION RESOLUTION AGENT
# =================================================

class ResolutionAgent:

    def __init__(self):

        self.context_builder = (
            ExceptionContextBuilder()
        )

        self.financial_reasoner = (
            FinancialReasoner()
        )


    # =================================================
    # LOAD AGENT DATA
    # =================================================

    def load_data(self):

        self.context_builder.load_data()


    # =================================================
    # BUILD AGENT DECISION
    # =================================================

    def build_agent_decision(
        self,
        context,
        reasoning
    ):

        payment_id = (
            context["payment_id"]
        )


        exception_type = (
            context["exception_type"]
        )


        # ---------------------------------------------
        # DEFAULT DECISION
        # ---------------------------------------------

        decision = {

            "payment_id":
                payment_id,

            "exception_type":
                exception_type,

            "reasoning_status":
                reasoning.get(
                    "analysis_status"
                ),

            "financial_risk":
                reasoning.get(
                    "financial_risk"
                ),

            "confidence":
                reasoning.get(
                    "confidence"
                ),

            "auto_resolvable":
                reasoning.get(
                    "auto_resolvable"
                ),

            "agent_decision":
                None,

            "resolution_status":
                None,

            "action_taken":
                None,

            "human_review_required":
                None,

            "reasoning":
                reasoning.get(
                    "evidence",
                    []
                )
        }


        # ---------------------------------------------
        # SAFE AUTO RESOLUTION
        # ---------------------------------------------

        if reasoning.get("auto_resolvable"):

            decision[
                "agent_decision"
            ] = (
                "AUTO_RESOLVE"
            )


            decision[
                "resolution_status"
            ] = (
                "RESOLVED"
            )


            decision[
                "action_taken"
            ] = (
                "LINK_RECOVERED_SETTLEMENT"
            )


            decision[
                "human_review_required"
            ] = False


            return decision


        # ---------------------------------------------
        # HIGH RISK ESCALATION
        # ---------------------------------------------

        if reasoning.get(
            "financial_risk"
        ) == "HIGH":

            decision[
                "agent_decision"
            ] = (
                "ESCALATE"
            )


            decision[
                "resolution_status"
            ] = (
                "MANUAL_REVIEW_REQUIRED"
            )


            decision[
                "action_taken"
            ] = (
                "ESCALATE_TO_FINANCIAL_REVIEW"
            )


            decision[
                "human_review_required"
            ] = True


            return decision


        # ---------------------------------------------
        # MEDIUM / UNKNOWN RISK
        # ---------------------------------------------

        decision[
            "agent_decision"
        ] = (
            "REVIEW_REQUIRED"
        )


        decision[
            "resolution_status"
        ] = (
            "MANUAL_REVIEW_REQUIRED"
        )


        decision[
            "action_taken"
        ] = (
            "REQUIRE_HUMAN_VALIDATION"
        )


        decision[
            "human_review_required"
        ] = True


        return decision


    # =================================================
    # RESOLVE SINGLE EXCEPTION
    # =================================================

    def resolve_exception(
        self,
        payment_id
    ):

        # ---------------------------------------------
        # BUILD CONTEXT
        # ---------------------------------------------

        context = (
            self.context_builder.build_context(
                payment_id
            )
        )


        if context is None:

            return None


        # ---------------------------------------------
        # RUN FINANCIAL REASONING
        # ---------------------------------------------

        reasoning = (
            self.financial_reasoner.analyze_exception(
                context
            )
        )


        # ---------------------------------------------
        # BUILD AGENT DECISION
        # ---------------------------------------------

        decision = (
            self.build_agent_decision(
                context,
                reasoning
            )
        )


        return decision


    # =================================================
    # RESOLVE ALL EXCEPTIONS
    # =================================================

    def resolve_all_exceptions(self):

        # ---------------------------------------------
        # LOAD DATA
        # ---------------------------------------------

        self.load_data()


        # ---------------------------------------------
        # GET EXCEPTION CONTEXTS
        # ---------------------------------------------

        contexts = (

            self.context_builder
            .build_exception_contexts()

        )


        decisions = []


        # ---------------------------------------------
        # PROCESS EACH EXCEPTION
        # ---------------------------------------------

        for context in contexts:

            payment_id = (
                context[
                    "payment_id"
                ]
            )


            decision = (
                self.resolve_exception(
                    payment_id
                )
            )


            if decision is not None:

                decisions.append(
                    decision
                )


        return decisions