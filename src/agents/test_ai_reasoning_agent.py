from src.agents.context_builder import (
    ExceptionContextBuilder
)

from src.agents.financial_reasoner import (
    FinancialReasoner
)

from src.agents.ai_reasoning_agent import (
    AIReasoningAgent
)


# =================================================
# DISPLAY AI REASONING RESULT
# =================================================

def display_result(
    result
):

    print(
        "\n" + "-" * 60
    )


    print(
        f"Payment ID: "
        f"{result['payment_id']}"
    )


    print(
        f"Exception Type: "
        f"{result['exception_type']}"
    )


    print(
        f"Deterministic Analysis: "
        f"{result['deterministic_analysis']}"
    )


    print(
        f"Financial Risk: "
        f"{result['financial_risk']}"
    )


    print(
        f"Confidence: "
        f"{result['confidence']}"
    )


    print(
        f"Auto Resolvable: "
        f"{result['auto_resolvable']}"
    )


    print(
        f"AI Response Valid: "
        f"{result['ai_response_valid']}"
    )


    print(
        "\nGuardrail Violations:"
    )


    violations = (
        result.get(
            "guardrail_violations",
            []
        )
    )


    if violations:

        for violation in violations:

            print(
                f"- {violation}"
            )

    else:

        print(
            "None"
        )


    print(
        "\nAI FINANCIAL REASONING:"
    )


    print(
        result[
            "ai_reasoning"
        ]
    )


# =================================================
# TEST SINGLE EXCEPTION
# =================================================

def test_exception(
    payment_id,
    context_builder,
    financial_reasoner,
    ai_agent
):

    # ---------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------

    context = (
        context_builder.build_context(
            payment_id
        )
    )


    if context is None:

        print(
            f"\nContext not found "
            f"for {payment_id}"
        )

        return


    # ---------------------------------------------
    # DETERMINISTIC REASONING
    # ---------------------------------------------

    reasoning = (
        financial_reasoner.analyze_exception(
            context
        )
    )


    # ---------------------------------------------
    # AI REASONING
    # ---------------------------------------------

    result = (
        ai_agent.analyze_exception(
            context,
            reasoning
        )
    )


    # ---------------------------------------------
    # DISPLAY
    # ---------------------------------------------

    display_result(
        result
    )


# =================================================
# MAIN
# =================================================

def main():

    # ---------------------------------------------
    # INITIALIZE COMPONENTS
    # ---------------------------------------------

    context_builder = (
        ExceptionContextBuilder()
    )


    financial_reasoner = (
        FinancialReasoner()
    )


    ai_agent = (
        AIReasoningAgent()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    context_builder.load_data()


    # ---------------------------------------------
    # GET ALL EXCEPTION CONTEXTS
    # ---------------------------------------------

    contexts = (

        context_builder
        .build_exception_contexts()

    )


    # ---------------------------------------------
    # FIND TEST CASES
    # ---------------------------------------------

    high_risk_payment_id = None

    auto_resolvable_payment_id = None


    for context in contexts:

        reasoning = (
            financial_reasoner.analyze_exception(
                context
            )
        )


        # -----------------------------------------
        # FIND HIGH RISK CASE
        # -----------------------------------------

        if (

            high_risk_payment_id is None

            and

            reasoning.get(
                "financial_risk"
            ) == "HIGH"

        ):

            high_risk_payment_id = (

                context[
                    "payment_id"
                ]

            )


        # -----------------------------------------
        # FIND AUTO RESOLVABLE CASE
        # -----------------------------------------

        if (

            auto_resolvable_payment_id is None

            and

            reasoning.get(
                "auto_resolvable"
            ) is True

        ):

            auto_resolvable_payment_id = (

                context[
                    "payment_id"
                ]

            )


    # ---------------------------------------------
    # DISPLAY TEST HEADER
    # ---------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "TESTING AI FINANCIAL REASONING AGENT"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # TEST HIGH RISK EXCEPTION
    # ---------------------------------------------

    if high_risk_payment_id:

        print(
            "\nTEST CASE 1: "
            "HIGH RISK EXCEPTION"
        )

        test_exception(

            high_risk_payment_id,

            context_builder,

            financial_reasoner,

            ai_agent

        )

    else:

        print(
            "\nNo HIGH risk exception found."
        )


    # ---------------------------------------------
    # TEST AUTO RESOLVABLE EXCEPTION
    # ---------------------------------------------

    if auto_resolvable_payment_id:

        print(
            "\nTEST CASE 2: "
            "AUTO RESOLVABLE EXCEPTION"
        )

        test_exception(

            auto_resolvable_payment_id,

            context_builder,

            financial_reasoner,

            ai_agent

        )

    else:

        print(
            "\nNo auto-resolvable exception found."
        )


if __name__ == "__main__":

    main()