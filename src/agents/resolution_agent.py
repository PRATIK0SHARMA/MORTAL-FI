from src.agents.context_builder import (
    ExceptionContextBuilder
)

from src.agents.financial_reasoner import (
    FinancialReasoner
)

from src.agents.ai_reasoning_agent import (
    AIReasoningAgent
)

from src.agents.resolution_executor import (
    ResolutionExecutor
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


        self.ai_reasoning_agent = (
            AIReasoningAgent()
        )

        self.resolution_executor = (
            ResolutionExecutor()
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
        reasoning,
        ai_result
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


            # -----------------------------------------
            # DETERMINISTIC REASONING
            # -----------------------------------------

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


            # -----------------------------------------
            # AI REASONING
            # -----------------------------------------

            "ai_reasoning":

                ai_result.get(
                    "ai_reasoning"
                ),


            "ai_response_valid":

                ai_result.get(
                    "ai_response_valid"
                ),


            "guardrail_violations":

                ai_result.get(
                    "guardrail_violations"
                ),


            # -----------------------------------------
            # FINAL AGENT DECISION
            # -----------------------------------------

            "agent_decision":

                None,


            "resolution_status":

                None,


            "action_taken":

                None,


            "human_review_required":

                None,

            "execution_status":

                None,

            "execution_message":

                None,

            "execution_result":

                None,    

            "execution_action": 

                None,

            "execution_timestamp":

                None,    


            # -----------------------------------------
            # EVIDENCE
            # -----------------------------------------

            "deterministic_evidence":

                reasoning.get(
                    "evidence",
                    []
                )

        }


        # =================================================
        # SAFETY GUARDRAIL
        # =================================================
        #
        # The LLM MUST NOT override deterministic
        # financial safety decisions.
        #
        # =================================================


        # ---------------------------------------------
        # SAFE AUTO RESOLUTION
        # ---------------------------------------------

        if reasoning.get(
            "auto_resolvable"
        ):


            # -----------------------------------------
            # AI RESPONSE INVALID
            # -----------------------------------------

            if not ai_result.get(
                "ai_response_valid"
            ):


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
                    "AI_RESPONSE_INVALID"
                )


                decision[
                    "human_review_required"
                ] = True


                return decision


            # -----------------------------------------
            # SAFE AUTO RESOLUTION
            # -----------------------------------------

            decision[
                "agent_decision"
            ] = (
                "AUTO_RESOLVE"
            )

            decision[
                "action_taken"
            ] = (
                "LINK_RECOVERED_SETTLEMENT"
            )

            decision[
                "human_review_required"
            ] = False


            # ---------------------------------------------
            # EXECUTE APPROVED ACTION
            # ---------------------------------------------

            execution_result = (

                self.resolution_executor
                .execute(
                    decision,
                    context
                )

            )


            decision[
                "execution_status"
            ] = (

                execution_result.get(
                    "execution_status"
                )

            )


            decision[
                "execution_message"
            ] = (

                execution_result.get(
                    "execution_message"
                )

            )

            decision[
                "execution_action"
            ] = (

                execution_result.get(
                    "execution_action"
                )

            )


            decision[
                "execution_timestamp"
            ] = (

                execution_result.get(
                    "execution_timestamp"
                )

            )


            decision[
                "execution_result"
            ] = execution_result


            # ---------------------------------------------
            # VERIFY EXECUTION
            # ---------------------------------------------
            execution_status=execution_result.get(
                "execution_status"
            )
            if execution_status in(
                "EXECUTED",
                "ALREADY_EXECUTED"
            ):

                decision[
                    "agent_decision"
                ] = "AUTO_RESOLVE"


                decision[
                    "resolution_status"
                ] = "RESOLVED"


                decision[
                    "human_review_required"
                ] = False


            else:

                decision[
                    "agent_decision"
                ] = "REVIEW_REQUIRED"


                decision[
                    "resolution_status"
                ] = "MANUAL_REVIEW_REQUIRED"


                decision[
                    "human_review_required"
                ] = True

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

            self.context_builder
            .build_context(
                payment_id
            )

        )


        if context is None:

            return None


        # ---------------------------------------------
        # RUN DETERMINISTIC FINANCIAL REASONING
        # ---------------------------------------------

        reasoning = (

            self.financial_reasoner
            .analyze_exception(
                context
            )

        )


        # ---------------------------------------------
        # RUN AI FINANCIAL REASONING
        # ---------------------------------------------

        ai_result = (

            self.ai_reasoning_agent
            .analyze_exception(
                context,
                reasoning
            )

        )


        # ---------------------------------------------
        # BUILD FINAL AGENT DECISION
        # ---------------------------------------------

        decision = (

            self.build_agent_decision(

                context,

                reasoning,

                ai_result

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