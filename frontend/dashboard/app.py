import streamlit as st

from api_client import (

    get_system_metrics,

    get_dashboard_kpis,

    get_exceptions,

    get_ai_resolutions

)


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(

    page_title="MORTAL-FI",

    page_icon="💰",

    layout="wide"

)


# =================================================
# PAGE TITLE
# =================================================

st.title(

    "MORTAL-FI"

)


st.subheader(

    "AI-Powered Financial Reconciliation System"

)


st.divider()


# =================================================
# LOAD DATA
# =================================================

metrics = (
    get_system_metrics()
)


kpis = (
    get_dashboard_kpis()
)


# =================================================
# API ERROR CHECK
# =================================================

if "error" in metrics:

    st.error(

        "Unable to connect to FastAPI backend."
    )


    st.write(

        metrics["error"]
    )


    st.stop()


if "error" in kpis:

    st.error(

        "Unable to load dashboard KPIs."
    )


    st.write(

        kpis["error"]
    )


    st.stop()


# =================================================
# KPI SECTION
# =================================================

st.header(

    "System Overview"

)


col1, col2, col3, col4, col5 = (

    st.columns(5)

)


# ---------------------------------------------
# TOTAL TRANSACTIONS
# ---------------------------------------------

col1.metric(

    "Total Transactions",

    metrics[
        "total_transactions"
    ]

)


# ---------------------------------------------
# MATCH RATE
# ---------------------------------------------

col2.metric(

    "Match Rate",

    f"{metrics['match_rate']}%"

)


# ---------------------------------------------
# EXCEPTIONS
# ---------------------------------------------

col3.metric(

    "Exceptions Detected",

    metrics[
        "exceptions_detected"
    ]

)


# ---------------------------------------------
# AUTO RESOLUTIONS
# ---------------------------------------------

col4.metric(

    "AI Auto Resolutions",

    metrics[
        "auto_resolutions"
    ]

)


# ---------------------------------------------
# ESCALATIONS
# ---------------------------------------------

col5.metric(

    "Manual Escalations",

    metrics[
        "escalations"
    ]

)


st.divider()


# =================================================
# SYSTEM HEALTH
# =================================================

st.header(

    "System Health"

)


health_col1, health_col2, health_col3 = (

    st.columns(3)

)


health_col1.metric(

    "AI Validity Rate",

    f"{metrics['ai_validity_rate']}%"

)


health_col2.metric(

    "Baseline Agreement",

    f"{metrics['baseline_decision_agreement_rate']}%"

)


health_col3.metric(

    "Guardrail Violations",

    metrics[
        "guardrail_violations"
    ]

)


st.divider()


# =================================================
# PIPELINE STATUS
# =================================================

st.header(

    "Pipeline Status"

)


if kpis[

    "pipeline_fully_processed"

]:

    st.success(

        "✓ Financial reconciliation pipeline fully processed"

    )


else:

    st.warning(

        "Pipeline processing incomplete"

    )


# =================================================
# EXCEPTION SUMMARY
# =================================================

st.header(

    "Exception Summary"

)


exceptions = (

    get_exceptions()

)


if "error" not in exceptions:

    st.metric(

        "Total Exception Records",

        len(
            exceptions
        )

    )


else:

    st.error(

        "Unable to load exception records"

    )


# =================================================
# AI DECISION SUMMARY
# =================================================

st.header(

    "AI Resolution Summary"

)


ai_resolutions = (

    get_ai_resolutions()

)


if "error" not in ai_resolutions:

    auto_resolve_count = sum(

        1

        for record
        in ai_resolutions

        if record.get(
            "agent_decision"
        )

        == "AUTO_RESOLVE"

    )


    escalation_count = sum(

        1

        for record
        in ai_resolutions

        if record.get(
            "agent_decision"
        )

        == "ESCALATE"

    )


    ai_col1, ai_col2 = (

        st.columns(2)

    )


    ai_col1.metric(

        "Auto Resolved",

        auto_resolve_count

    )


    ai_col2.metric(

        "Escalated",

        escalation_count

    )


else:

    st.error(

        "Unable to load AI resolution records"

    )


# =================================================
# FOOTER
# =================================================

st.divider()


st.caption(

    "MORTAL-FI | AI-Powered Financial Reconciliation & Resolution System"

)