from pathlib import Path

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


AI_EVALUATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_evaluation"
    / "ai_agent_evaluation.csv"
)


AI_AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_audit"
    / "ai_agent_audit_trail.csv"
)


# =================================================
# LOAD DATASETS
# =================================================

def load_datasets():

    print(
        "\nLoading AI resolution datasets..."
    )


    ai_resolution = pd.read_csv(
        AI_RESOLUTION_PATH
    )


    ai_evaluation = pd.read_csv(
        AI_EVALUATION_PATH
    )


    ai_audit = pd.read_csv(
        AI_AUDIT_PATH
    )


    print(
        f"AI Resolution Records: "
        f"{len(ai_resolution)}"
    )


    print(
        f"AI Evaluation Records: "
        f"{len(ai_evaluation)}"
    )


    print(
        f"AI Audit Records: "
        f"{len(ai_audit)}"
    )


    return {

        "AI RESOLUTION":
            ai_resolution,

        "AI EVALUATION":
            ai_evaluation,

        "AI AUDIT":
            ai_audit

    }


# =================================================
# VALIDATE RECORD COUNTS
# =================================================

def validate_record_counts(
    datasets
):

    print(
        "\n" + "=" * 60
    )

    print(
        "RECORD COUNT VALIDATION"
    )

    print(
        "=" * 60
    )


    counts = {

        name: len(dataframe)

        for name, dataframe
        in datasets.items()

    }


    for name, count in counts.items():

        print(
            f"{name}: "
            f"{count} records"
        )


    expected_count = (
        counts["AI RESOLUTION"]
    )


    valid = all(

        count == expected_count

        for count
        in counts.values()

    )


    return valid


# =================================================
# VALIDATE PAYMENT IDS
# =================================================

def validate_payment_ids(
    datasets
):

    print(
        "\n" + "=" * 60
    )

    print(
        "PAYMENT ID VALIDATION"
    )

    print(
        "=" * 60
    )


    resolution_ids = set(

        datasets[
            "AI RESOLUTION"
        ][
            "payment_id"
        ]

    )


    all_valid = True


    for name in [

        "AI EVALUATION",

        "AI AUDIT"

    ]:


        stage_ids = set(

            datasets[
                name
            ][
                "payment_id"
            ]

        )


        missing_ids = (

            resolution_ids
            -
            stage_ids

        )


        extra_ids = (

            stage_ids
            -
            resolution_ids

        )


        is_valid = (

            len(missing_ids) == 0

            and

            len(extra_ids) == 0

        )


        print(
            f"\n{name}"
        )


        print(
            f"Missing IDs: "
            f"{len(missing_ids)}"
        )


        print(
            f"Extra IDs: "
            f"{len(extra_ids)}"
        )


        print(
            f"Status: "
            f"{'PASS' if is_valid else 'FAIL'}"
        )


        if not is_valid:

            all_valid = False


    return all_valid


# =================================================
# VALIDATE AI RESPONSES
# =================================================

def validate_ai_responses(
    ai_resolution
):

    print(
        "\n" + "=" * 60
    )

    print(
        "AI RESPONSE VALIDATION"
    )

    print(
        "=" * 60
    )


    valid_count = (

        ai_resolution[
            "ai_response_valid"
        ].sum()

    )


    total_count = len(
        ai_resolution
    )


    invalid_count = (

        total_count
        -
        valid_count

    )


    print(
        f"Valid AI Responses: "
        f"{valid_count}"
    )


    print(
        f"Invalid AI Responses: "
        f"{invalid_count}"
    )


    return (

        invalid_count == 0

    )


# =================================================
# VALIDATE GUARDRAILS
# =================================================

def validate_guardrails(
    ai_resolution
):

    print(
        "\n" + "=" * 60
    )

    print(
        "GUARDRAIL VALIDATION"
    )

    print(
        "=" * 60
    )


    violations = (

        ai_resolution[
            "guardrail_violations"
        ]
        .notna()
        .sum()

    )


    print(
        f"Guardrail Violations: "
        f"{violations}"
    )


    return (

        violations == 0

    )


# =================================================
# VALIDATE DECISION AGREEMENT
# =================================================

def validate_decision_agreement(
    ai_evaluation
):

    print(
        "\n" + "=" * 60
    )

    print(
        "AI DECISION AGREEMENT VALIDATION"
    )

    print(
        "=" * 60
    )


    disagreement_count = len(

        ai_evaluation[

            ai_evaluation[
                "decision_agreement"
            ]
            == False

        ]

    )


    total_count = len(
        ai_evaluation
    )


    agreement_count = (

        total_count
        -
        disagreement_count

    )


    print(
        f"Agreement: "
        f"{agreement_count}/{total_count}"
    )


    print(
        f"Disagreements: "
        f"{disagreement_count}"
    )


    return (

        disagreement_count == 0

    )


# =================================================
# MAIN VALIDATION
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "FINAL AI RESOLUTION SYSTEM VALIDATION"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    datasets = (
        load_datasets()
    )


    # ---------------------------------------------
    # VALIDATIONS
    # ---------------------------------------------

    record_count_valid = (
        validate_record_counts(
            datasets
        )
    )


    payment_ids_valid = (
        validate_payment_ids(
            datasets
        )
    )


    ai_responses_valid = (
        validate_ai_responses(

            datasets[
                "AI RESOLUTION"
            ]

        )
    )


    guardrails_valid = (
        validate_guardrails(

            datasets[
                "AI RESOLUTION"
            ]

        )
    )


    agreement_valid = (
        validate_decision_agreement(

            datasets[
                "AI EVALUATION"
            ]

        )
    )


    # ---------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------

    system_valid = (

        record_count_valid

        and

        payment_ids_valid

        and

        ai_responses_valid

        and

        guardrails_valid

        and

        agreement_valid

    )


    print(
        "\n" + "=" * 60
    )


    if system_valid:

        print(
            "✓ AI RESOLUTION SYSTEM VERIFIED"
        )


        print(
            "All AI decisions are valid, "
            "auditable, and consistent "
            "with the evaluation baseline."
        )

    else:

        print(
            "✗ AI RESOLUTION SYSTEM VALIDATION FAILED"
        )


    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()