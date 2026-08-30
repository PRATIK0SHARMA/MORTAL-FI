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


    return (
        metrics,
        kpis,
        exceptions,
        audit
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
        audit
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

    exception_counts = (

        exceptions_df[
            "exception_type"
        ]
        .value_counts()
        .reset_index()

    )


    exception_counts.columns = [

        "Exception Type",

        "Count"

    ]


    exception_chart = (

        px.bar(

            exception_counts,

            x="Exception Type",

            y="Count",

            title="Exception Type Distribution"

        )

    )


    chart_col1.plotly_chart(

        exception_chart,

        use_container_width=True

    )


# ---------------------------------------------
# FINAL PROCESSING STATUS
# ---------------------------------------------

if not audit_df.empty:

    processing_counts = (

        audit_df[
            "final_processing_status"
        ]
        .value_counts()
        .reset_index()

    )


    processing_counts.columns = [

        "Processing Status",

        "Count"

    ]


    processing_chart = (

        px.pie(

            processing_counts,

            names="Processing Status",

            values="Count",

            title="Final Processing Status"

        )

    )


    chart_col2.plotly_chart(

        processing_chart,

        use_container_width=True

    )


st.divider()


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
# FOOTER
# =================================================

st.divider()


st.caption(
    "MORTAL-FI | "
    "AI-Powered Financial Reconciliation System"
)