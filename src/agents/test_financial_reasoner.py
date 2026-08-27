from src.agents.context_builder import (
    ExceptionContextBuilder
)

from src.agents.financial_reasoner import (
    FinancialReasoner
)


# =================================================
# TEST FINANCIAL REASONER
# =================================================

def main():

    # ---------------------------------------------
    # CREATE CONTEXT BUILDER
    # ---------------------------------------------

    context_builder = (
        ExceptionContextBuilder()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    context_builder.load_data()


    # ---------------------------------------------
    # BUILD EXCEPTION CONTEXTS
    # ---------------------------------------------

    contexts = (
        context_builder
        .build_exception_contexts()
    )


    # ---------------------------------------------
    # CREATE FINANCIAL REASONER
    # ---------------------------------------------

    reasoner = (
        FinancialReasoner()
    )


    # ---------------------------------------------
    # DISPLAY HEADER
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("TESTING FINANCIAL REASONING ENGINE")
    print("=" * 60)


    print(
        f"\nTotal Exception Contexts: "
        f"{len(contexts)}"
    )


    # ---------------------------------------------
    # ANALYZE EXCEPTIONS
    # ---------------------------------------------

    for context in contexts:

        analysis = (

            reasoner.analyze_exception(
                context
            )

        )


        print("\n" + "-" * 60)


        print(
            f"Payment ID: "
            f"{context['payment_id']}"
        )


        print(
            f"Exception Type: "
            f"{context['exception_type']}"
        )


        print(
            f"Analysis Status: "
            f"{analysis['analysis_status']}"
        )


        print(
            f"Financial Risk: "
            f"{analysis['financial_risk']}"
        )


        print(
            f"Auto Resolvable: "
            f"{analysis['auto_resolvable']}"
        )


        print(
            f"Confidence: "
            f"{analysis['confidence']}"
        )


        # -----------------------------------------
        # DISPLAY AMOUNT ANALYSIS IF AVAILABLE
        # -----------------------------------------

        if "amount_difference" in analysis:

            print(
                f"Amount Difference: "
                f"{analysis['amount_difference']}"
            )


        if "difference_percentage" in analysis:

            print(
                f"Difference Percentage: "
                f"{analysis['difference_percentage']}%"
            )


        # -----------------------------------------
        # DISPLAY EVIDENCE
        # -----------------------------------------

        print("\nEvidence:")


        for evidence in analysis["evidence"]:

            print(
                f"- {evidence}"
            )


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":

    main()