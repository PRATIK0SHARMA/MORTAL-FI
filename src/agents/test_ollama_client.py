from src.agents.ollama_client import (
    OllamaClient
)


def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "TESTING LOCAL OLLAMA LLM"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # CREATE CLIENT
    # ---------------------------------------------

    client = (

        OllamaClient()

    )


    # ---------------------------------------------
    # TEST PROMPT
    # ---------------------------------------------

    prompt = """

You are an AI financial reconciliation assistant.

Explain why a payment amount mismatch
should require manual review.

Keep your answer concise and focused
on financial reconciliation.

"""


    # ---------------------------------------------
    # GENERATE RESPONSE
    # ---------------------------------------------

    response = (

        client.generate(
            prompt
        )

    )


    # ---------------------------------------------
    # DISPLAY RESPONSE
    # ---------------------------------------------

    print(
        "\nAI RESPONSE:\n"
    )


    print(
        response
    )


if __name__ == "__main__":

    main()