from pathlib import Path
import sys

import pandas as pd
import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

STREAMLIT_URL = "http://localhost:8501"


PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


AGENT_DECISIONS_PATH = (
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


# ============================================================
# EXPECTED BASELINE
# ============================================================

EXPECTED_TOTAL_TRANSACTIONS = 103

EXPECTED_MATCHED = 80

EXPECTED_EXCEPTIONS = 23

EXPECTED_AUTO_RESOLUTIONS = 4

EXPECTED_ESCALATIONS = 19


EXPECTED_EXCEPTION_DISTRIBUTION = {

    "AMOUNT_MISMATCH": 5,

    "MISSING_SETTLEMENT": 5,

    "MISSING_ORDER": 3,

    "DUPLICATE_PAYMENT": 6,

    "REFERENCE_MISMATCH": 4

}


# ============================================================
# TEST STATE
# ============================================================

TEST_RESULTS = []


# ============================================================
# HELPERS
# ============================================================

def section(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)


def record_test(
    name,
    condition,
    details=""
):

    status = (
        "PASS"
        if condition
        else "FAIL"
    )


    TEST_RESULTS.append({

        "test":
            name,

        "status":
            status,

        "details":
            details

    })


    symbol = (
        "✓"
        if condition
        else "✗"
    )


    print(
        f"{symbol} {name}: {status}"
    )


    if details:

        print(
            f"  {details}"
        )


def api_get(endpoint):

    response = requests.get(

        f"{API_BASE_URL}{endpoint}",

        timeout=10

    )


    response.raise_for_status()


    return response.json()


def bool_series(series):

    normalized = (
        series
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return normalized.map({

        "true": True,
        "1": True,
        "1.0": True,
        "yes": True,
        "y": True,

        "false": False,
        "0": False,
        "0.0": False,
        "no": False,
        "n": False

    })

# ============================================================
# 1. SERVICE HEALTH
# ============================================================

def test_service_health():

    section(
        "1. SERVICE HEALTH"
    )


    # --------------------------------------------------------
    # FASTAPI
    # --------------------------------------------------------

    try:

        response = requests.get(

            API_BASE_URL,

            timeout=10

        )


        api_ok = (
            response.status_code
            == 200
        )


        record_test(

            "FastAPI reachable",

            api_ok,

            (
                f"HTTP {response.status_code}"
            )

        )


        if api_ok:

            payload = response.json()


            record_test(

                "FastAPI project identity",

                (
                    payload.get("project")
                    == "MORTAL-FI"
                ),

                str(payload)

            )


    except Exception as error:

        record_test(

            "FastAPI reachable",

            False,

            str(error)

        )


    # --------------------------------------------------------
    # STREAMLIT
    # --------------------------------------------------------

    try:

        response = requests.get(

            STREAMLIT_URL,

            timeout=10

        )


        record_test(

            "Streamlit reachable",

            (
                response.status_code
                == 200
            ),

            (
                f"HTTP {response.status_code}"
            )

        )


    except Exception as error:

        record_test(

            "Streamlit reachable",

            False,

            str(error)

        )


# ============================================================
# 2. API ENDPOINT VALIDATION
# ============================================================

def test_api_endpoints():

    section(
        "2. API ENDPOINT VALIDATION"
    )


    endpoints = [

        "/metrics",

        "/dashboard/kpis",

        "/exceptions",

        "/audit",

        "/analytics/exceptions",

        "/analytics/processing-status",

        "/ai/resolutions",

        "/ai/agent-decisions",

        "/analytics/ai",

        "/execution/audit",

        "/execution/verification",

        "/analytics/agent-performance"

    ]


    for endpoint in endpoints:

        try:

            response = requests.get(

                f"{API_BASE_URL}{endpoint}",

                timeout=10

            )


            record_test(

                f"GET {endpoint}",

                (
                    response.status_code
                    == 200
                ),

                (
                    f"HTTP "
                    f"{response.status_code}"
                )

            )


        except Exception as error:

            record_test(

                f"GET {endpoint}",

                False,

                str(error)

            )


# ============================================================
# 3. RECONCILIATION CONSISTENCY
# ============================================================

def test_reconciliation():

    section(
        "3. RECONCILIATION CONSISTENCY"
    )


    metrics = api_get(
        "/metrics"
    )


    total = int(
        metrics.get(
            "total_transactions",
            0
        )
    )


    matched = int(
        metrics.get(
            "matched_transactions",
            0
        )
    )


    exceptions = int(
        metrics.get(
            "exceptions_detected",
            0
        )
    )


    record_test(

        "Total transaction count",

        (
            total
            == EXPECTED_TOTAL_TRANSACTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_TOTAL_TRANSACTIONS}, "
            f"got {total}"
        )

    )


    record_test(

        "Matched transaction count",

        (
            matched
            == EXPECTED_MATCHED
        ),

        (
            f"Expected "
            f"{EXPECTED_MATCHED}, "
            f"got {matched}"
        )

    )


    record_test(

        "Exception count",

        (
            exceptions
            == EXPECTED_EXCEPTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_EXCEPTIONS}, "
            f"got {exceptions}"
        )

    )


    record_test(

        "Matched + Exceptions = Total",

        (
            matched
            +
            exceptions
            ==
            total
        ),

        (
            f"{matched} + "
            f"{exceptions} = "
            f"{matched + exceptions}"
        )

    )


    expected_match_rate = round(

        (
            matched
            /
            total
        )
        *
        100,

        2

    )


    actual_match_rate = round(

        float(
            metrics.get(
                "match_rate",
                0
            )
        ),

        2

    )


    record_test(

        "Match rate consistency",

        (
            actual_match_rate
            ==
            expected_match_rate
        ),

        (
            f"Expected "
            f"{expected_match_rate}%, "
            f"got "
            f"{actual_match_rate}%"
        )

    )


# ============================================================
# 4. EXCEPTION DISTRIBUTION
# ============================================================

def test_exception_distribution():

    section(
        "4. EXCEPTION DISTRIBUTION"
    )


    data = api_get(
        "/analytics/exceptions"
    )


    records = data.get(

        "exception_distribution",

        []

    )


    distribution = {

        str(
            row.get(
                "exception_type"
            )
        ):
        int(
            row.get(
                "count",
                0
            )
        )

        for row in records

    }


    for exception_type, expected_count in (
        EXPECTED_EXCEPTION_DISTRIBUTION.items()
    ):

        actual_count = distribution.get(

            exception_type,

            0

        )


        record_test(

            exception_type,

            (
                actual_count
                ==
                expected_count
            ),

            (
                f"Expected "
                f"{expected_count}, "
                f"got "
                f"{actual_count}"
            )

        )


    record_test(

        "Exception distribution total",

        (
            sum(
                distribution.values()
            )
            ==
            EXPECTED_EXCEPTIONS
        ),

        (
            f"Total = "
            f"{sum(distribution.values())}"
        )

    )


# ============================================================
# 5. AI DECISION VALIDATION
# ============================================================

def test_ai_decisions():

    section(
        "5. AI AGENT DECISION VALIDATION"
    )


    decisions = pd.DataFrame(

        api_get(
            "/ai/agent-decisions"
        )

    )


    record_test(

        "AI decision count",

        (
            len(decisions)
            ==
            EXPECTED_EXCEPTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_EXCEPTIONS}, "
            f"got "
            f"{len(decisions)}"
        )

    )


    if decisions.empty:

        return


    auto_count = (

        decisions[
            "agent_decision"
        ]
        .astype(str)
        .eq(
            "AUTO_RESOLVE"
        )
        .sum()

    )


    escalate_count = (

        decisions[
            "agent_decision"
        ]
        .astype(str)
        .eq(
            "ESCALATE"
        )
        .sum()

    )


    record_test(

        "AUTO_RESOLVE count",

        (
            auto_count
            ==
            EXPECTED_AUTO_RESOLUTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_AUTO_RESOLUTIONS}, "
            f"got "
            f"{auto_count}"
        )

    )


    record_test(

        "ESCALATE count",

        (
            escalate_count
            ==
            EXPECTED_ESCALATIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_ESCALATIONS}, "
            f"got "
            f"{escalate_count}"
        )

    )


    record_test(

        "All AI decisions accounted for",

        (
            auto_count
            +
            escalate_count
            ==
            EXPECTED_EXCEPTIONS
        ),

        (
            f"{auto_count} + "
            f"{escalate_count}"
        )

    )


# ============================================================
# 6. RISK / RESOLUTION SAFETY
# ============================================================

def test_risk_logic():

    section(
        "6. FINANCIAL RISK & SAFETY LOGIC"
    )


    decisions = pd.DataFrame(

        api_get(
            "/ai/agent-decisions"
        )

    )


    if decisions.empty:

        record_test(

            "Risk validation",

            False,

            "No AI decisions"

        )

        return


    auto_df = decisions[
        decisions[
            "agent_decision"
        ]
        ==
        "AUTO_RESOLVE"
    ]


    escalated_df = decisions[
        decisions[
            "agent_decision"
        ]
        ==
        "ESCALATE"
    ]


    auto_low_risk = (

        auto_df[
            "financial_risk"
        ]
        .astype(str)
        .eq(
            "LOW"
        )
        .all()

    )


    escalation_high_risk = (

        escalated_df[
            "financial_risk"
        ]
        .astype(str)
        .eq(
            "HIGH"
        )
        .all()

    )


    record_test(

        "Auto resolutions are LOW risk",

        auto_low_risk

    )


    record_test(

        "Escalations are HIGH risk",

        escalation_high_risk

    )


    auto_types = set(

        auto_df[
            "exception_type"
        ]
        .astype(str)
        .tolist()

    )


    record_test(

        "Only safe REFERENCE_MISMATCH auto-resolved",

        (
            auto_types
            ==
            {
                "REFERENCE_MISMATCH"
            }
        ),

        (
            f"Auto-resolved types: "
            f"{sorted(auto_types)}"
        )

    )


# ============================================================
# 7. HUMAN REVIEW LOGIC
# ============================================================

def test_human_review():

    section(
        "7. HUMAN REVIEW CONTROL"
    )


    decisions = pd.DataFrame(

        api_get(
            "/ai/agent-decisions"
        )

    )


    review_flags = bool_series(

        decisions[
            "human_review_required"
        ]

    )


    escalated_mask = (

        decisions[
            "agent_decision"
        ]
        ==
        "ESCALATE"

    )


    auto_mask = (

        decisions[
            "agent_decision"
        ]
        ==
        "AUTO_RESOLVE"

    )


    record_test(

        "Escalated cases require human review",

        bool(
            review_flags[
                escalated_mask
            ]
            .fillna(False)
            .all()
        )

    )


    record_test(

        "Auto-resolved cases avoid human review",

        bool(
            (
                ~review_flags[
                    auto_mask
                ]
                .fillna(True)
            )
            .all()
        )

    )


# ============================================================
# 8. AI RESPONSE / GUARDRAILS
# ============================================================

def test_ai_guardrails():

    section(
        "8. AI RESPONSE & GUARDRAILS"
    )

    decisions = pd.DataFrame(
        api_get(
            "/ai/agent-decisions"
        )
    )

    if decisions.empty:

        record_test(
            "AI guardrail validation",
            False,
            "No AI decisions available"
        )

        return

    # --------------------------------------------------------
    # AI RESPONSE VALIDITY
    # --------------------------------------------------------

    if "ai_response_valid" in decisions.columns:

        validity = bool_series(
            decisions[
                "ai_response_valid"
            ]
        )

        auto_mask = (
            decisions[
                "agent_decision"
            ]
            .astype(str)
            .eq(
                "AUTO_RESOLVE"
            )
        )

        # Critical safety invariant:
        # NOTHING may auto-resolve using an invalid AI response.

        auto_valid = (
            validity[
                auto_mask
            ]
            .fillna(False)
            .all()
        )

        record_test(
            "All AUTO_RESOLVE decisions have valid AI responses",
            bool(auto_valid)
        )

        # Invalid AI responses are allowed ONLY if the system
        # keeps them away from autonomous execution.

        invalid_mask = (
            validity
            .fillna(False)
            .eq(False)
        )

        invalid_count = int(
            invalid_mask.sum()
        )

        unsafe_invalid = decisions[
            invalid_mask
            &
            auto_mask
        ]

        record_test(
            "Invalid AI responses are never auto-resolved",
            unsafe_invalid.empty,
            (
                f"Invalid AI responses found: "
                f"{invalid_count}; "
                f"unsafe auto-resolutions: "
                f"{len(unsafe_invalid)}"
            )
        )

    else:

        record_test(
            "AI response validity field available",
            False,
            "ai_response_valid column missing"
        )

    # --------------------------------------------------------
    # GUARDRAIL VIOLATIONS
    # --------------------------------------------------------

    if "guardrail_violations" in decisions.columns:

        violations = (
            decisions[
                "guardrail_violations"
            ]
            .astype(str)
            .str.strip()
        )

        acceptable_empty = violations.isin(
            [
                "",
                "[]",
                "{}",
                "0",
                "0.0",
                "None",
                "none",
                "nan",
                "NaN"
            ]
        )

        # We do NOT necessarily require all cases to have zero
        # violations. What matters is that cases with violations
        # must never autonomously execute.

        violation_mask = ~acceptable_empty

        auto_mask = (
            decisions[
                "agent_decision"
            ]
            .astype(str)
            .eq(
                "AUTO_RESOLVE"
            )
        )

        unsafe_guardrail_cases = decisions[
            violation_mask
            &
            auto_mask
        ]

        record_test(
            "Guardrail violations never reach AUTO_RESOLVE",
            unsafe_guardrail_cases.empty,
            (
                f"Guardrail violation records: "
                f"{int(violation_mask.sum())}; "
                f"unsafe auto-resolutions: "
                f"{len(unsafe_guardrail_cases)}"
            )
        )

    else:

        record_test(
            "Guardrail violation field available",
            False,
            "guardrail_violations column missing"
        )
# ============================================================
# 9. EXECUTION VALIDATION
# ============================================================

def test_execution():

    section(
        "9. RESOLUTION EXECUTION"
    )


    execution_response = api_get(
        "/execution/audit"
    )


    execution = pd.DataFrame(

        execution_response.get(
            "records",
            []
        )

    )


    if execution.empty:

        record_test(

            "Execution records available",

            False

        )

        return


    executed = execution[
        execution[
            "execution_status"
        ]
        ==
        "EXECUTED"
    ]


    unique_executed = (

        executed[
            "payment_id"
        ]
        .astype(str)
        .nunique()

    )


    record_test(

        "Unique successful executions",

        (
            unique_executed
            ==
            EXPECTED_AUTO_RESOLUTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_AUTO_RESOLUTIONS}, "
            f"got "
            f"{unique_executed}"
        )

    )


    if (
        "validation_status"
        in executed.columns
    ):

        record_test(

            "Executed records passed validation",

            bool(
                executed[
                    "validation_status"
                ]
                .astype(str)
                .eq(
                    "PASSED"
                )
                .all()
            )

        )


    amounts_match = (

        pd.to_numeric(
            executed[
                "payment_amount"
            ],
            errors="coerce"
        )

        ==

        pd.to_numeric(
            executed[
                "settlement_amount"
            ],
            errors="coerce"
        )

    )


    record_test(

        "Executed payment/settlement amounts match",

        bool(
            amounts_match.all()
        )

    )


# ============================================================
# 10. IDEMPOTENCY VALIDATION
# ============================================================

def test_idempotency():

    section(
        "10. IDEMPOTENCY / DUPLICATE EXECUTION PROTECTION"
    )


    execution = pd.DataFrame(

        api_get(
            "/execution/audit"
        )
        .get(
            "records",
            []
        )

    )


    if execution.empty:

        record_test(

            "Idempotency evidence",

            False,

            "Execution audit empty"

        )

        return


    already = execution[
        execution[
            "execution_status"
        ]
        ==
        "ALREADY_EXECUTED"
    ]


    record_test(

        "ALREADY_EXECUTED events recorded",

        (
            len(already)
            > 0
        ),

        (
            f"Found "
            f"{len(already)} "
            f"idempotent retry event(s)"
        )

    )


    actual_execution_counts = (

        execution[
            execution[
                "execution_status"
            ]
            ==
            "EXECUTED"
        ]
        .groupby(
            "payment_id"
        )
        .size()

    )


    record_test(

        "No payment actually executed more than once",

        bool(
            (
                actual_execution_counts
                <=
                1
            )
            .all()
        ),

        (
            f"Max actual executions/payment: "
            f"{actual_execution_counts.max()}"
        )

    )


# ============================================================
# 11. VERIFICATION VALIDATION
# ============================================================

def test_verification():

    section(
        "11. POST-EXECUTION VERIFICATION"
    )


    verification = pd.DataFrame(

        api_get(
            "/execution/verification"
        )
        .get(
            "records",
            []
        )

    )


    if verification.empty:

        record_test(

            "Verification records available",

            False

        )

        return


    verified = verification[
        verification[
            "verification_status"
        ]
        ==
        "VERIFIED"
    ]


    unique_verified = (

        verified[
            "payment_id"
        ]
        .astype(str)
        .nunique()

    )


    record_test(

        "Unique verified resolutions",

        (
            unique_verified
            ==
            EXPECTED_AUTO_RESOLUTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_AUTO_RESOLUTIONS}, "
            f"got "
            f"{unique_verified}"
        )

    )


    amounts_match = (

        pd.to_numeric(
            verified[
                "payment_amount"
            ],
            errors="coerce"
        )

        ==

        pd.to_numeric(
            verified[
                "settlement_amount"
            ],
            errors="coerce"
        )

    )


    record_test(

        "Verified amounts remain consistent",

        bool(
            amounts_match.all()
        )

    )


# ============================================================
# 12. AGENT PERFORMANCE METRICS
# ============================================================

def test_agent_performance():

    section(
        "12. AGENT PERFORMANCE METRICS"
    )


    performance = api_get(
        "/analytics/agent-performance"
    )


    expected_values = {

        "total_exceptions":
            23,

        "auto_resolutions":
            4,

        "escalations":
            19,

        "manual_reviews":
            19,

        "successful_executions":
            4,

        "verified_resolutions":
            4

    }


    for key, expected in (
        expected_values.items()
    ):

        actual = performance.get(
            key
        )


        record_test(

            key,

            (
                actual
                ==
                expected
            ),

            (
                f"Expected "
                f"{expected}, "
                f"got "
                f"{actual}"
            )

        )


    verification_rate = float(

        performance.get(
            "verification_rate",
            0
        )

    )


    record_test(

        "Verification rate = 100%",

        (
            verification_rate
            ==
            100.0
        ),

        (
            f"Got "
            f"{verification_rate}%"
        )

    )


    auto_rate = round(

        float(
            performance.get(
                "auto_resolution_rate",
                0
            )
        ),

        2

    )


    record_test(

        "Auto-resolution rate = 17.39%",

        (
            auto_rate
            ==
            17.39
        ),

        (
            f"Got "
            f"{auto_rate}%"
        )

    )


# ============================================================
# 13. PIPELINE STATUS
# ============================================================

def test_pipeline_status():

    section(
        "13. PIPELINE STATUS"
    )


    kpis = api_get(
        "/dashboard/kpis"
    )


    record_test(

        "Pipeline fully processed",

        bool(
            kpis.get(
                "pipeline_fully_processed",
                False
            )
        )

    )


    record_test(

        "End-to-end record count",

        (
            int(
                kpis.get(
                    "end_to_end_records",
                    0
                )
            )
            ==
            EXPECTED_TOTAL_TRANSACTIONS
        ),

        (
            f"Expected "
            f"{EXPECTED_TOTAL_TRANSACTIONS}, "
            f"got "
            f"{kpis.get('end_to_end_records')}"
        )

    )


# ============================================================
# 14. PAYMENT-ID CONSISTENCY
# ============================================================

def test_payment_ids():

    section(
        "14. PAYMENT ID CONSISTENCY"
    )


    exceptions = pd.DataFrame(

        api_get(
            "/exceptions"
        )

    )


    decisions = pd.DataFrame(

        api_get(
            "/ai/agent-decisions"
        )

    )


    exception_ids = set(

        exceptions[
            "payment_id"
        ]
        .astype(str)

    )


    decision_ids = set(

        decisions[
            "payment_id"
        ]
        .astype(str)

    )


    missing_in_ai = (

        exception_ids
        -
        decision_ids

    )


    extra_in_ai = (

        decision_ids
        -
        exception_ids

    )


    record_test(

        "Every exception has AI decision",

        (
            len(
                missing_in_ai
            )
            ==
            0
        ),

        (
            f"Missing: "
            f"{sorted(missing_in_ai)}"
        )

    )


    record_test(

        "No unexpected AI decisions",

        (
            len(
                extra_in_ai
            )
            ==
            0
        ),

        (
            f"Extra: "
            f"{sorted(extra_in_ai)}"
        )

    )


# ============================================================
# FINAL SUMMARY
# ============================================================

def print_final_summary():

    section(
        "DAY 6H — FINAL SYSTEM TEST SUMMARY"
    )


    results_df = pd.DataFrame(
        TEST_RESULTS
    )


    passed = int(

        (
            results_df[
                "status"
            ]
            ==
            "PASS"
        )
        .sum()

    )


    failed = int(

        (
            results_df[
                "status"
            ]
            ==
            "FAIL"
        )
        .sum()

    )


    total = len(
        results_df
    )


    print(
        f"\nTotal Tests: {total}"
    )

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )


    if failed == 0:

        print(
            "\n"
            + "=" * 70
        )

        print(
            "✓ MORTAL-FI FINAL SYSTEM VALIDATION PASSED"
        )

        print(
            "All core reconciliation, AI, safety, "
            "execution, verification, API, and "
            "frontend health checks passed."
        )

        print(
            "=" * 70
        )


    else:

        print(
            "\nFAILED TESTS:"
        )


        failed_tests = results_df[
            results_df[
                "status"
            ]
            ==
            "FAIL"
        ]


        print(

            failed_tests[
                [
                    "test",
                    "details"
                ]
            ]
            .to_string(
                index=False
            )

        )


        print(
            "\n"
            + "=" * 70
        )

        print(
            "✗ FINAL VALIDATION FAILED"
        )

        print(
            "Fix the failed checks before the final demo."
        )

        print(
            "=" * 70
        )


    return failed


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        + "=" * 70
    )

    print(
        "MORTAL-FI — DAY 6H FINAL SYSTEM VALIDATION"
    )

    print(
        "=" * 70
    )


    test_service_health()

    test_api_endpoints()

    test_reconciliation()

    test_exception_distribution()

    test_ai_decisions()

    test_risk_logic()

    test_human_review()

    test_ai_guardrails()

    test_execution()

    test_idempotency()

    test_verification()

    test_agent_performance()

    test_pipeline_status()

    test_payment_ids()


    failed = (
        print_final_summary()
    )


    if failed > 0:

        sys.exit(1)


    sys.exit(0)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()