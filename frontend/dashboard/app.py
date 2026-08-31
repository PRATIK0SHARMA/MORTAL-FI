import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="MORTAL-FI Dashboard",
    page_icon="💳",
    layout="wide"
)


# =================================================
# API CONFIGURATION
# =================================================

API_BASE_URL = (
    "http://127.0.0.1:8000"
)

EXCEPTION_ANALYTICS_URL = (
    "http://127.0.0.1:8000/"
    "analytics/exceptions"
)


PROCESSING_STATUS_URL = (
    "http://127.0.0.1:8000/"
    "analytics/processing-status"
)


# =================================================
# DATA LOADING FUNCTIONS
# =================================================

@st.cache_data(
    ttl=30
)
def load_data():

    metrics = requests.get(
        f"{API_BASE_URL}/metrics"
    ).json()


    kpis = requests.get(
        f"{API_BASE_URL}/dashboard/kpis"
    ).json()


    exceptions = requests.get(
        f"{API_BASE_URL}/exceptions"
    ).json()


    audit = requests.get(
        f"{API_BASE_URL}/audit"
    ).json()


    exception_analytics = requests.get(
        EXCEPTION_ANALYTICS_URL
    ).json()


    processing_status = requests.get(
        PROCESSING_STATUS_URL
    ).json()

    ai_resolutions = requests.get(
        f"{API_BASE_URL}/ai/resolutions"
    ).json()


    return (
        metrics,
        kpis,
        exceptions,
        audit,
        exception_analytics,
        processing_status,
        ai_resolutions
    )
# =================================================
# DASHBOARD HEADER
# =================================================

st.title(
    "MORTAL-FI"
)


st.caption(
    "AI-Powered Financial Reconciliation "
    "and Exception Resolution System"
)


st.divider()


# =================================================
# LOAD DATA
# =================================================

try:

    (
        metrics,
        kpis,
        exceptions,
        audit,
        exception_analytics,
        processing_status,
        ai_resolutions
    ) = load_data()


except Exception:

    st.error(
        "Unable to connect to the MORTAL-FI API."
    )


    st.info(
        "Make sure the FastAPI server is running:"
    )


    st.code(
        "uvicorn src.api.app:app --reload"
    )


    st.stop()


# =================================================
# PIPELINE STATUS
# =================================================

if kpis.get(
    "pipeline_fully_processed"
):

    st.success(
        "Pipeline Status: FULLY PROCESSED"
    )


else:

    st.warning(
        "Pipeline Status: PROCESSING INCOMPLETE"
    )


# =================================================
# SYSTEM OVERVIEW
# =================================================

st.header(
    "System Overview"
)


col1, col2, col3, col4, col5 = st.columns(
    5
)


col1.metric(
    "Total Transactions",
    metrics.get(
        "total_transactions",
        0
    )
)


col2.metric(
    "Matched Transactions",
    metrics.get(
        "matched_transactions",
        0
    )
)


col3.metric(
    "Exceptions",
    metrics.get(
        "exceptions_detected",
        0
    )
)


col4.metric(
    "Match Rate",
    f"{metrics.get('match_rate', 0)}%"
)


col5.metric(
    "Auto Resolutions",
    metrics.get(
        "auto_resolutions",
        0
    )
)


st.divider()


# =================================================
# AI RESOLUTION OVERVIEW
# =================================================

st.header(
    "AI Resolution Overview"
)


ai_col1, ai_col2, ai_col3, ai_col4 = st.columns(
    4
)


ai_col1.metric(
    "AI Decisions",
    metrics.get(
        "total_ai_decisions",
        0
    )
)


ai_col2.metric(
    "Auto Resolutions",
    metrics.get(
        "auto_resolutions",
        0
    )
)


ai_col3.metric(
    "Escalations",
    metrics.get(
        "escalations",
        0
    )
)


ai_col4.metric(
    "AI Validity",
    f"{metrics.get('ai_validity_rate', 0)}%"
)


st.divider()


# =================================================
# EXCEPTION DATAFRAME
# =================================================

exceptions_df = pd.DataFrame(
    exceptions
)


audit_df = pd.DataFrame(
    audit
)

ai_resolutions_df = pd.DataFrame(
    ai_resolutions
)


# =================================================
# EXCEPTION ANALYTICS
# =================================================

st.header(
    "Exception Analytics"
)


chart_col1, chart_col2 = st.columns(
    2
)


# ---------------------------------------------
# EXCEPTION TYPE DISTRIBUTION
# ---------------------------------------------

if not exceptions_df.empty:

    exception_counts = pd.DataFrame(
        exception_analytics[
            "exception_distribution"
        ]
    )


    exception_chart = px.bar(

        exception_counts,

        x="exception_type",

        y="count",

        title="Exception Type Distribution"

    )


    chart_col1.plotly_chart(

        exception_chart,

        use_container_width=True

    )

# ---------------------------------------------
# FINAL PROCESSING STATUS
# ---------------------------------------------

if not audit_df.empty:

    processing_counts = pd.DataFrame(
        processing_status[
            "processing_distribution"
        ]
    )


    processing_chart = px.pie(

        processing_counts,

        names="final_processing_status",

        values="count",

        title="Final Processing Status"

    )


    chart_col2.plotly_chart(

        processing_chart,

        use_container_width=True

    )
# =================================================
# AI DECISION DISTRIBUTION
# =================================================

st.header(
    "AI Decision Distribution"
)


ai_decision_data = pd.DataFrame(

    {

        "Decision": [

            "Auto Resolve",

            "Escalate"

        ],

        "Count": [

            metrics.get(
                "auto_resolutions",
                0
            ),

            metrics.get(
                "escalations",
                0
            )

        ]

    }

)


ai_chart = (

    px.bar(

        ai_decision_data,

        x="Decision",

        y="Count",

        title="AI Agent Decisions"

    )

)


st.plotly_chart(

    ai_chart,

    use_container_width=True

)


st.divider()


# =================================================
# RECENT EXCEPTIONS
# =================================================

st.header(
    "Detected Exceptions"
)


if not exceptions_df.empty:

    display_columns = [

        "payment_id",

        "order_id",

        "payment_amount",

        "exception_type",

        "settlement_id",

        "settlement_amount",

        "match_method"

    ]


    available_columns = [

        column

        for column in display_columns

        if column in exceptions_df.columns

    ]


    st.dataframe(

        exceptions_df[
            available_columns
        ],

        use_container_width=True,

        hide_index=True

    )


else:

    st.info(
        "No exceptions detected."
    )


# =================================================
# AI RESOLUTION ANALYSIS
# =================================================

st.divider()

st.header(
    "AI Resolution Analysis"
)

st.caption(
    "Explainable AI analysis for detected financial exceptions."
)


if not ai_resolutions_df.empty:

    # ---------------------------------------------
    # SELECT PAYMENT
    # ---------------------------------------------

    payment_ids = (
        ai_resolutions_df[
            "payment_id"
        ]
        .astype(str)
        .tolist()
    )


    selected_payment = st.selectbox(
        "Select Exception / Payment",
        payment_ids
    )


    # ---------------------------------------------
    # SELECTED AI RECORD
    # ---------------------------------------------

    selected_record = (
        ai_resolutions_df[
            ai_resolutions_df[
                "payment_id"
            ].astype(str)
            == selected_payment
        ]
        .iloc[0]
    )


    # ---------------------------------------------
    # DECISION SUMMARY
    # ---------------------------------------------

    st.subheader(
        "AI Decision Summary"
    )


    decision_col1, decision_col2, decision_col3, decision_col4 = (
        st.columns(4)
    )


    decision_col1.metric(
        "Payment ID",
        selected_record.get(
            "payment_id",
            "N/A"
        )
    )


    decision_col2.metric(
        "Exception Type",
        selected_record.get(
            "exception_type",
            "N/A"
        )
    )


    decision_col3.metric(
        "Financial Risk",
        selected_record.get(
            "financial_risk",
            "N/A"
        )
    )


    confidence = selected_record.get(
        "confidence",
        0
    )


    if pd.notna(confidence):

        try:

            confidence_display = (
                f"{float(confidence) * 100:.1f}%"
            )

        except:

            confidence_display = str(
                confidence
            )

    else:

        confidence_display = "N/A"


    decision_col4.metric(
        "AI Confidence",
        confidence_display
    )


    # ---------------------------------------------
    # DECISION / STATUS
    # ---------------------------------------------

    status_col1, status_col2, status_col3, status_col4 = (
        st.columns(4)
    )


    status_col1.write(
        "**Agent Decision**"
    )

    status_col1.info(
        str(
            selected_record.get(
                "agent_decision",
                "N/A"
            )
        )
    )


    status_col2.write(
        "**Resolution Status**"
    )

    status_col2.info(
        str(
            selected_record.get(
                "resolution_status",
                "N/A"
            )
        )
    )


    status_col3.write(
        "**Auto Resolvable**"
    )

    status_col3.info(
        str(
            selected_record.get(
                "auto_resolvable",
                "N/A"
            )
        )
    )


    status_col4.write(
        "**Human Review Required**"
    )

    status_col4.info(
        str(
            selected_record.get(
                "human_review_required",
                "N/A"
            )
        )
    )


    st.divider()


    # ---------------------------------------------
    # AI REASONING
    # ---------------------------------------------

    st.subheader(
        "AI Reasoning"
    )


    reasoning = selected_record.get(
        "ai_reasoning",
        "No reasoning available."
    )


    st.write(
        reasoning
    )


    # ---------------------------------------------
    # DETERMINISTIC EVIDENCE
    # ---------------------------------------------

    st.subheader(
        "Deterministic Evidence"
    )


    evidence = selected_record.get(
        "deterministic_evidence",
        "No deterministic evidence available."
    )


    st.info(
        evidence
    )


    # ---------------------------------------------
    # RESOLUTION ACTION
    # ---------------------------------------------

    st.subheader(
        "Resolution Action"
    )


    action_col1, action_col2 = (
        st.columns(2)
    )


    action_col1.write(
        "**Action Taken**"
    )


    action_col1.info(
        str(
            selected_record.get(
                "action_taken",
                "N/A"
            )
        )
    )


    action_col2.write(
        "**AI Response Status**"
    )


    action_col2.info(
        str(
            selected_record.get(
                "reasoning_status",
                "N/A"
            )
        )
    )


    # ---------------------------------------------
    # VALIDATION / GUARDRAILS
    # ---------------------------------------------

    st.subheader(
        "AI Safety & Validation"
    )


    validation_col1, validation_col2 = (
        st.columns(2)
    )


    validation_col1.write(
        "**AI Response Valid**"
    )


    validation_col1.info(
        str(
            selected_record.get(
                "ai_response_valid",
                "N/A"
            )
        )
    )


    validation_col2.write(
        "**Guardrail Violations**"
    )


    violations = selected_record.get(
        "guardrail_violations",
        0
    )


    validation_col2.info(
        str(violations)
    )


else:

    st.info(
        "No AI resolution records available."
    )


# =================================================
# FOOTER
# =================================================

st.divider()


st.caption(
    "MORTAL-FI | "
    "AI-Powered Financial Reconciliation System"
)