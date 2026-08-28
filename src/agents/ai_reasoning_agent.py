from src.agents.ollama_client import OllamaClient


# =================================================
# AI REASONING AGENT
# =================================================

class AIReasoningAgent:


    def __init__(self):

        self.llm_client = (
            OllamaClient()
        )


    # =================================================
    # BUILD FINANCIAL PROMPT
    # =================================================

    def build_prompt(
        self,
        context,
        reasoning
    ):

        payment_id = (
            context.get(
                "payment_id"
            )
        )


        exception_type = (
            context.get(
                "exception_type"
            )
        )


        payment = (
            context.get(
                "payment"
            )
        )


        order = (
            context.get(
                "order"
            )
        )


        settlement = (
            context.get(
                "settlement"
            )
        )


        analysis_status = (
            reasoning.get(
                "analysis_status"
            )
        )


        financial_risk = (
            reasoning.get(
                "financial_risk"
            )
        )


        confidence = (
            reasoning.get(
                "confidence"
            )
        )


        auto_resolvable = (
            reasoning.get(
                "auto_resolvable"
            )
        )


        evidence = (
            reasoning.get(
                "evidence",
                []
            )
        )


        evidence_text = "\n".join(

            f"- {item}"

            for item in evidence

        )


        prompt = f"""
You are an AI financial reconciliation analysis assistant.

Your task is to EXPLAIN the deterministic financial
decision provided below.

IMPORTANT RULES:

1. The deterministic financial analysis is authoritative.
2. You MUST NOT override the financial risk classification.
3. You MUST NOT override the auto_resolvable value.
4. You MUST NOT recommend AUTO RESOLUTION when
   Auto Resolvable is False.
5. If Financial Risk is HIGH, HUMAN_REVIEW must be YES.
6. Your RECOMMENDED_ACTION must be consistent with
   the deterministic analysis.
7. You must use ONLY the provided transaction data.
8. You must NOT invent information.

AUTHORITATIVE DETERMINISTIC DECISION:

Analysis Status:
{analysis_status}

Financial Risk:
{financial_risk}

Confidence:
{confidence}

Auto Resolvable:
{auto_resolvable}

TRANSACTION DATA:

Payment ID:
{payment_id}

Exception Type:
{exception_type}

Payment:
{payment}

Order:
{order}

Settlement:
{settlement}

EVIDENCE:

{evidence_text}

You are NOT allowed to change the following rules:

If Auto Resolvable = False:
- HUMAN_REVIEW must be YES.
- Do not recommend automatic resolution.

If Financial Risk = HIGH:
- HUMAN_REVIEW must be YES.
- Recommend financial investigation or manual review.

If Auto Resolvable = True:
- HUMAN_REVIEW may be NO.
- Recommend safe automated resolution only if supported
  by the evidence.

Return EXACTLY this format:

EXCEPTION_ANALYSIS:
<brief explanation>

RISK_ANALYSIS:
<brief financial risk explanation>

RECOMMENDED_ACTION:
<recommended action>

HUMAN_REVIEW:
YES or NO

Do not return any additional sections.
"""

        return prompt


# =================================================
# VALIDATE AI DECISION
# =================================================

    def validate_ai_response(
        self,
        ai_response,
        reasoning
    ):

        violations = []


        auto_resolvable = (
            reasoning.get(
                "auto_resolvable"
            )
        )


        financial_risk = (
            reasoning.get(
                "financial_risk"
            )
        )


        response_upper = (
            ai_response.upper()
        )


        # ---------------------------------------------
        # CHECK HUMAN REVIEW REQUIREMENT
        # ---------------------------------------------

        if auto_resolvable is False:

            if "HUMAN_REVIEW:\nNO" in response_upper:

                violations.append(
                    "LLM incorrectly rejected required human review"
                )


        if financial_risk == "HIGH":

            if "HUMAN_REVIEW:\nNO" in response_upper:

                violations.append(
                    "LLM recommended no human review for HIGH risk transaction"
                )


        # ---------------------------------------------
        # CHECK UNSAFE AUTO RESOLUTION
        # ---------------------------------------------

        unsafe_keywords = [

            "AUTOMATICALLY RESOLVED",

            "AUTO RESOLUTION",

            "AUTOMATIC RESOLUTION",

            "AUTOMATICALLY ADJUST"

        ]


        if auto_resolvable is False:

            for keyword in unsafe_keywords:

                if keyword in response_upper:

                    violations.append(

                        f"Unsafe automatic action detected: {keyword}"

                    )


        # ---------------------------------------------
        # VALIDATION RESULT
        # ---------------------------------------------

        is_valid = (

            len(
                violations
            ) == 0

        )


        return {

            "is_valid":
                is_valid,

            "violations":
                violations
        }


    # =================================================
    # ANALYZE EXCEPTION WITH AI
    # =================================================

    def analyze_exception(
        self,
        context,
        reasoning
    ):

        prompt = (
            self.build_prompt(
                context,
                reasoning
            )
        )


        ai_response = (
            self.llm_client.generate(
                prompt
            )
        )

        validation = (
            self.validate_ai_response(
                ai_response,
                reasoning
            )
        )

        result = {

            "payment_id":

                context.get(
                    "payment_id"
                ),


            "exception_type":

                context.get(
                    "exception_type"
                ),


            "deterministic_analysis":

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


            "ai_reasoning":

                ai_response,


            "ai_response_valid":

                validation.get(
                    "is_valid"
                ),


            "guardrail_violations":

                validation.get(
                    "violations"
                )
        }
        


        return result