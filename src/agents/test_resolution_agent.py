from src.agents.resolution_agent import (
    ResolutionAgent
)


# =================================================
# TEST RESOLUTION AGENT
# =================================================

def display_decision(
    title,
    decision
):

    print(
        "\n" + "=" * 60
    )

    print(
        title
    )

    print(
        "=" * 60
    )


    if decision is None:

        print(
            "\nDecision could not be generated."
        )

        return


    print(
        f"\nPayment ID: "
        f"{decision['payment_id']}"
    )


    print(
        f"Exception Type: "
        f"{decision['exception_type']}"
    )


    print(
        f"Reasoning Status: "
        f"{decision['reasoning_status']}"
    )


    print(
        f"Financial Risk: "
        f"{decision['financial_risk']}"
    )


    print(
        f"Confidence: "
        f"{decision['confidence']}"
    )


    print(
        f"Auto Resolvable: "
        f"{decision['auto_resolvable']}"
    )


    print(
        f"\nAI Response Valid: "
        f"{decision['ai_response_valid']}"
    )


    print(
        f"Guardrail Violations: "
        f"{decision['guardrail_violations']}"
    )


    print(
        f"\nAgent Decision: "
        f"{decision['agent_decision']}"
    )


    print(
        f"Resolution Status: "
        f"{decision['resolution_status']}"
    )


    print(
        f"Action Taken: "
        f"{decision['action_taken']}"
    )


    print(
        f"Human Review Required: "
        f"{decision['human_review_required']}"
    )


    print(
        "\nAI FINANCIAL REASONING:"
    )

    print(
        decision[
            "ai_reasoning"
        ]
    )


# =================================================
# MAIN
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "TESTING INTEGRATED AI RESOLUTION AGENT"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # INITIALIZE AGENT
    # ---------------------------------------------

    agent = (
        ResolutionAgent()
    )


    # ---------------------------------------------
    # LOAD DATA ONCE
    # ---------------------------------------------

    agent.load_data()


    # =============================================
    # TEST CASE 1
    # HIGH RISK EXCEPTION
    # =============================================

    decision_1 = (

        agent.resolve_exception(
            "PAY0071"
        )

    )


    display_decision(

        "TEST CASE 1: HIGH RISK EXCEPTION",

        decision_1

    )


    # =============================================
    # TEST CASE 2
    # SAFE AUTO RESOLUTION
    # =============================================

    decision_2 = (

        agent.resolve_exception(
            "PAY0092"
        )

    )


    display_decision(

        "TEST CASE 2: SAFE AUTO RESOLUTION",

        decision_2

    )


if __name__ == "__main__":

    main()