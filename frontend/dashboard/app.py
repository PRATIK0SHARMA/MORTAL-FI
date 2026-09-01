import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MORTAL-FI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONSTANTS
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        background-color: rgba(128,128,128,0.05);
    }

    .status-box {
        padding: 0.8rem 1rem;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 1rem;
    }

    .timeline-step {
        padding: 0.8rem;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }

    .small-text {
        font-size: 0.85rem;
        opacity: 0.75;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API HELPER
# ============================================================

def api_get(endpoint):

    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=30)
def load_data():

    metrics = api_get("/metrics")

    kpis = api_get("/dashboard/kpis")

    exceptions = api_get("/exceptions")

    audit = api_get("/audit")

    exception_analytics = api_get(
        "/analytics/exceptions"
    )

    processing_status = api_get(
        "/analytics/processing-status"
    )

    ai_resolutions = api_get(
        "/ai/resolutions"
    )

    ai_agent_decisions = api_get(
        "/ai/agent-decisions"
    )

    ai_analytics = api_get(
        "/analytics/ai"
    )

    execution_audit = api_get(
        "/execution/audit"
    )

    verification_audit = api_get(
        "/execution/verification"
    )

    agent_performance = api_get(
        "/analytics/agent-performance"
    )

    return (
        metrics,
        kpis,
        exceptions,
        audit,
        exception_analytics,
        processing_status,
        ai_resolutions,
        ai_agent_decisions,
        ai_analytics,
        execution_audit,
        verification_audit,
        agent_performance
    )


# ============================================================
# LOAD API DATA
# ============================================================

try:

    (
        metrics,
        kpis,
        exceptions,
        audit,
        exception_analytics,
        processing_status,
        ai_resolutions,
        ai_agent_decisions,
        ai_analytics,
        execution_audit,
        verification_audit,
        agent_performance
    ) = load_data()

except Exception as error:

    st.error(
        "Unable to connect to the MORTAL-FI API."
    )

    st.info(
        "Make sure FastAPI is running:"
    )

    st.code(
        "uvicorn src.api.app:app --reload"
    )

    st.caption(
        f"Connection error: {error}"
    )

    st.stop()


# ============================================================
# DATAFRAMES
# ============================================================

exceptions_df = pd.DataFrame(
    exceptions
)

audit_df = pd.DataFrame(
    audit
)

ai_resolutions_df = pd.DataFrame(
    ai_resolutions
)

ai_agent_df = pd.DataFrame(
    ai_agent_decisions
)

execution_df = pd.DataFrame(
    execution_audit.get(
        "records",
        []
    )
)

verification_df = pd.DataFrame(
    verification_audit.get(
        "records",
        []
    )
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💳 MORTAL-FI")

    st.caption(
        "Financial Reconciliation Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "🚨 Exceptions",
            "🔍 Investigation",
            "⚙️ Execution",
            "📋 Audit & Explainability",
            "🎬 Demo Mode"
        ]
    )

    st.divider()

    st.caption(
        "SYSTEM"
    )

    if kpis.get(
        "pipeline_fully_processed"
    ):

        st.success(
            "🟢 Pipeline Operational"
        )

    else:

        st.warning(
            "🟡 Pipeline Incomplete"
        )

    st.caption(
        "API: Connected"
    )

    st.caption(
        "Auto-refresh: 30 seconds"
    )

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# GLOBAL HEADER
# ============================================================

st.title(
    "💳 MORTAL-FI"
)

st.caption(
    "AI-Powered Financial Reconciliation "
    "and Exception Resolution System"
)

st.divider()


# ============================================================
# 6B — EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.header(
        "Executive Overview"
    )

    st.caption(
        "High-level operational view of the "
        "financial reconciliation pipeline."
    )

    # --------------------------------------------------------
    # PIPELINE STATUS
    # --------------------------------------------------------

    if kpis.get(
        "pipeline_fully_processed"
    ):

        st.success(
            "🟢 Pipeline Status: FULLY PROCESSED"
        )

    else:

        st.warning(
            "🟡 Pipeline Status: PROCESSING INCOMPLETE"
        )

    # --------------------------------------------------------
    # CORE KPIs
    # --------------------------------------------------------

    st.subheader(
        "Reconciliation Performance"
    )

    col1, col2, col3, col4, col5 = (
        st.columns(5)
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

    # --------------------------------------------------------
    # AI KPIs
    # --------------------------------------------------------

    st.subheader(
        "AI Resolution Performance"
    )

    ai_col1, ai_col2, ai_col3, ai_col4 = (
        st.columns(4)
    )

    ai_col1.metric(
        "AI Decisions",
        agent_performance.get(
            "total_exceptions",
            0
        )
    )

    ai_col2.metric(
        "Auto Resolved",
        agent_performance.get(
            "auto_resolutions",
            0
        )
    )

    ai_col3.metric(
        "Escalated",
        agent_performance.get(
            "escalations",
            0
        )
    )

    ai_confidence = (
        agent_performance.get(
            "average_ai_confidence",
            0
        )
        * 100
    )

    ai_col4.metric(
        "Average AI Confidence",
        f"{ai_confidence:.2f}%"
    )

    st.divider()

    # --------------------------------------------------------
    # AGENT PERFORMANCE
    # --------------------------------------------------------

    st.subheader(
        "Agent Performance"
    )

    performance_col1, performance_col2, performance_col3, performance_col4, performance_col5 = (
        st.columns(5)
    )

    performance_col1.metric(
        "Auto Resolution Rate",
        f"{agent_performance.get('auto_resolution_rate', 0):.2f}%"
    )

    performance_col2.metric(
        "Escalation Rate",
        f"{agent_performance.get('escalation_rate', 0):.2f}%"
    )

    performance_col3.metric(
        "Successful Executions",
        agent_performance.get(
            "successful_executions",
            0
        )
    )

    performance_col4.metric(
        "Verified Resolutions",
        agent_performance.get(
            "verified_resolutions",
            0
        )
    )

    performance_col5.metric(
        "Verification Rate",
        f"{agent_performance.get('verification_rate', 0):.2f}%"
    )

    st.divider()

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    st.subheader(
        "Operational Analytics"
    )

    chart_col1, chart_col2 = (
        st.columns(2)
    )

    decision_distribution = pd.DataFrame(
        ai_analytics.get(
            "decision_distribution",
            []
        )
    )

    if not decision_distribution.empty:

        decision_chart = px.bar(
            decision_distribution,
            x="agent_decision",
            y="count",
            title="AI Decision Distribution",
            labels={
                "agent_decision": "Agent Decision",
                "count": "Exceptions"
            }
        )

        chart_col1.plotly_chart(
            decision_chart,
            use_container_width=True
        )

    risk_distribution = pd.DataFrame(
        ai_analytics.get(
            "risk_distribution",
            []
        )
    )

    if not risk_distribution.empty:

        risk_chart = px.pie(
            risk_distribution,
            names="financial_risk",
            values="count",
            title="Financial Risk Distribution"
        )

        chart_col2.plotly_chart(
            risk_chart,
            use_container_width=True
        )

    exception_distribution = pd.DataFrame(
        exception_analytics.get(
            "exception_distribution",
            []
        )
    )

    if not exception_distribution.empty:

        exception_chart = px.bar(
            exception_distribution,
            x="exception_type",
            y="count",
            title="Exception Type Distribution",
            labels={
                "exception_type": "Exception Type",
                "count": "Count"
            }
        )

        st.plotly_chart(
            exception_chart,
            use_container_width=True
        )


# ============================================================
# 6C — EXCEPTIONS
# ============================================================

elif page == "🚨 Exceptions":

    st.header(
        "Exception Management"
    )

    st.caption(
        "Review and filter reconciliation exceptions."
    )

    if exceptions_df.empty:

        st.success(
            "No exceptions detected."
        )

    else:

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        filter_col1, filter_col2, filter_col3 = (
            st.columns(3)
        )

        exception_types = sorted(
            exceptions_df[
                "exception_type"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_exception_type = (
            filter_col1.selectbox(
                "Exception Type",
                ["ALL"] + exception_types
            )
        )

        search_payment = (
            filter_col2.text_input(
                "Search Payment ID"
            )
        )

        search_order = (
            filter_col3.text_input(
                "Search Order ID"
            )
        )

        filtered_df = (
            exceptions_df.copy()
        )

        if (
            selected_exception_type
            != "ALL"
        ):

            filtered_df = filtered_df[
                filtered_df[
                    "exception_type"
                ]
                .astype(str)
                == selected_exception_type
            ]

        if search_payment:

            filtered_df = filtered_df[
                filtered_df[
                    "payment_id"
                ]
                .astype(str)
                .str.contains(
                    search_payment,
                    case=False,
                    na=False
                )
            ]

        if search_order:

            filtered_df = filtered_df[
                filtered_df[
                    "order_id"
                ]
                .astype(str)
                .str.contains(
                    search_order,
                    case=False,
                    na=False
                )
            ]

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.caption(
            f"Showing {len(filtered_df)} exception(s)"
        )

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
            if column in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[
                available_columns
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 6C — INVESTIGATION UI
# ============================================================

elif page == "🔍 Investigation":

    st.header(
        "AI Exception Investigation"
    )

    st.caption(
        "Investigate an individual financial exception "
        "using deterministic evidence and AI analysis."
    )

    if ai_resolutions_df.empty:

        st.info(
            "No AI resolution records available."
        )

    else:

        payment_ids = (
            ai_resolutions_df[
                "payment_id"
            ]
            .astype(str)
            .unique()
            .tolist()
        )

        selected_payment = st.selectbox(
            "Select Payment / Exception",
            payment_ids
        )

        selected_ai_record = (
            ai_resolutions_df[
                ai_resolutions_df[
                    "payment_id"
                ]
                .astype(str)
                == selected_payment
            ]
            .iloc[0]
        )

        # ----------------------------------------------------
        # DECISION SUMMARY
        # ----------------------------------------------------

        st.subheader(
            "AI Decision Summary"
        )

        decision_col1, decision_col2, decision_col3, decision_col4 = (
            st.columns(4)
        )

        decision_col1.metric(
            "Payment ID",
            selected_ai_record.get(
                "payment_id",
                "N/A"
            )
        )

        decision_col2.metric(
            "Exception Type",
            selected_ai_record.get(
                "exception_type",
                "N/A"
            )
        )

        decision_col3.metric(
            "Financial Risk",
            selected_ai_record.get(
                "financial_risk",
                "N/A"
            )
        )

        confidence = selected_ai_record.get(
            "confidence",
            0
        )

        try:

            confidence_display = (
                f"{float(confidence) * 100:.1f}%"
            )

        except:

            confidence_display = str(
                confidence
            )

        decision_col4.metric(
            "AI Confidence",
            confidence_display
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        st.subheader(
            "Resolution Status"
        )

        status_col1, status_col2, status_col3, status_col4 = (
            st.columns(4)
        )

        status_col1.write(
            "**Agent Decision**"
        )

        status_col1.info(
            str(
                selected_ai_record.get(
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
                selected_ai_record.get(
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
                selected_ai_record.get(
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
                selected_ai_record.get(
                    "human_review_required",
                    "N/A"
                )
            )
        )

        # ----------------------------------------------------
        # FINANCIAL EVIDENCE
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "Financial Evidence"
        )

        selected_exception = (
            exceptions_df[
                exceptions_df[
                    "payment_id"
                ]
                .astype(str)
                == selected_payment
            ]
            if "payment_id" in exceptions_df.columns
            else pd.DataFrame()
        )

        if not selected_exception.empty:

            selected_exception_record = (
                selected_exception.iloc[0]
            )

            payment_amount = (
                selected_exception_record.get(
                    "payment_amount"
                )
            )

            settlement_amount = (
                selected_exception_record.get(
                    "settlement_amount"
                )
            )

            evidence_col1, evidence_col2, evidence_col3, evidence_col4 = (
                st.columns(4)
            )

            evidence_col1.metric(
                "Payment Amount",
                (
                    f"₹{float(payment_amount):,.2f}"
                    if pd.notna(payment_amount)
                    else "N/A"
                )
            )

            evidence_col2.metric(
                "Settlement Amount",
                (
                    f"₹{float(settlement_amount):,.2f}"
                    if pd.notna(settlement_amount)
                    else "N/A"
                )
            )

            if (
                pd.notna(payment_amount)
                and pd.notna(settlement_amount)
            ):

                difference = (
                    float(payment_amount)
                    -
                    float(settlement_amount)
                )

                if float(payment_amount) != 0:

                    difference_percentage = (
                        abs(difference)
                        /
                        abs(float(payment_amount))
                        *
                        100
                    )

                else:

                    difference_percentage = 0

                evidence_col3.metric(
                    "Amount Difference",
                    f"₹{difference:,.2f}"
                )

                evidence_col4.metric(
                    "Difference %",
                    f"{difference_percentage:.2f}%"
                )

            else:

                evidence_col3.metric(
                    "Amount Difference",
                    "N/A"
                )

                evidence_col4.metric(
                    "Difference %",
                    "N/A"
                )

        else:

            st.info(
                "Financial evidence unavailable."
            )

        # ----------------------------------------------------
        # AI REASONING
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "AI Reasoning"
        )

        st.write(
            selected_ai_record.get(
                "ai_reasoning",
                "No reasoning available."
            )
        )

        # ----------------------------------------------------
        # DETERMINISTIC EVIDENCE
        # ----------------------------------------------------

        st.subheader(
            "Deterministic Evidence"
        )

        st.info(
            selected_ai_record.get(
                "deterministic_evidence",
                "No deterministic evidence available."
            )
        )

        # ----------------------------------------------------
        # RESOLUTION ACTION
        # ----------------------------------------------------

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
                selected_ai_record.get(
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
                selected_ai_record.get(
                    "reasoning_status",
                    "N/A"
                )
            )
        )

        # ----------------------------------------------------
        # SAFETY
        # ----------------------------------------------------

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
                selected_ai_record.get(
                    "ai_response_valid",
                    "N/A"
                )
            )
        )

        validation_col2.write(
            "**Guardrail Violations**"
        )

        validation_col2.info(
            str(
                selected_ai_record.get(
                    "guardrail_violations",
                    0
                )
            )
        )


# ============================================================
# 6D — EXECUTION MONITORING
# ============================================================

elif page == "⚙️ Execution":

    st.header(
        "Resolution Execution"
    )

    st.caption(
        "Monitor AI resolution execution and "
        "post-execution verification."
    )

    # --------------------------------------------------------
    # EXECUTION COUNTS
    # --------------------------------------------------------

    executed_count = 0
    already_executed_count = 0
    failed_execution_count = 0

    if not execution_df.empty:

        if "execution_status" in execution_df.columns:

            executed_count = len(
                execution_df[
                    execution_df[
                        "execution_status"
                    ]
                    == "EXECUTED"
                ]
            )

            already_executed_count = len(
                execution_df[
                    execution_df[
                        "execution_status"
                    ]
                    == "ALREADY_EXECUTED"
                ]
            )

            failed_execution_count = len(
                execution_df[
                    execution_df[
                        "execution_status"
                    ]
                    == "FAILED"
                ]
            )

    execution_col1, execution_col2, execution_col3 = (
        st.columns(3)
    )

    execution_col1.metric(
        "Executed",
        executed_count
    )

    execution_col2.metric(
        "Already Executed",
        already_executed_count
    )

    execution_col3.metric(
        "Failed",
        failed_execution_count
    )

    # --------------------------------------------------------
    # EXECUTION TABLE
    # --------------------------------------------------------

    if not execution_df.empty:

        st.subheader(
            "Execution Audit"
        )

        st.dataframe(
            execution_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No execution records available."
        )

    st.divider()

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    st.subheader(
        "Post-Execution Verification"
    )

    verified_count = 0
    verification_failed_count = 0

    if not verification_df.empty:

        if "verification_status" in verification_df.columns:

            verified_count = len(
                verification_df[
                    verification_df[
                        "verification_status"
                    ]
                    == "VERIFIED"
                ]
            )

            verification_failed_count = len(
                verification_df[
                    verification_df[
                        "verification_status"
                    ]
                    != "VERIFIED"
                ]
            )

    verification_col1, verification_col2 = (
        st.columns(2)
    )

    verification_col1.metric(
        "Verified",
        verified_count
    )

    verification_col2.metric(
        "Verification Failures",
        verification_failed_count
    )

    if not verification_df.empty:

        st.dataframe(
            verification_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No verification records available."
        )

    # --------------------------------------------------------
    # EXECUTION TIMELINE
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Resolution Lifecycle"
    )

    timeline_col1, timeline_col2, timeline_col3, timeline_col4, timeline_col5 = (
        st.columns(5)
    )

    timeline_col1.info(
        "1\n\nException Detected"
    )

    timeline_col2.info(
        "2\n\nAI Investigated"
    )

    timeline_col3.info(
        "3\n\nDecision Generated"
    )

    timeline_col4.info(
        "4\n\nResolution Executed"
    )

    timeline_col5.info(
        "5\n\nVerification Completed"
    )


# ============================================================
# 6E — AUDIT & EXPLAINABILITY
# ============================================================

elif page == "📋 Audit & Explainability":

    st.header(
        "Audit & Explainability"
    )

    st.caption(
        "Complete evidence trail for AI-assisted "
        "financial reconciliation."
    )

    # --------------------------------------------------------
    # AUDIT OVERVIEW
    # --------------------------------------------------------

    audit_col1, audit_col2, audit_col3, audit_col4 = (
        st.columns(4)
    )

    audit_col1.metric(
        "AI Records",
        len(ai_resolutions_df)
    )

    audit_col2.metric(
        "Execution Records",
        len(execution_df)
    )

    audit_col3.metric(
        "Verification Records",
        len(verification_df)
    )

    audit_col4.metric(
        "Audit Records",
        len(audit_df)
    )

    st.divider()

    # --------------------------------------------------------
    # AUDIT TABLE
    # --------------------------------------------------------

    if not audit_df.empty:

        st.subheader(
            "Reconciliation Audit"
        )

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No reconciliation audit records available."
        )

    st.divider()

    # --------------------------------------------------------
    # EXPLAINABILITY SELECTOR
    # --------------------------------------------------------

    if not ai_resolutions_df.empty:

        payment_ids = (
            ai_resolutions_df[
                "payment_id"
            ]
            .astype(str)
            .unique()
            .tolist()
        )

        selected_payment = st.selectbox(
            "Select Payment for Explainability",
            payment_ids
        )

        selected_record = (
            ai_resolutions_df[
                ai_resolutions_df[
                    "payment_id"
                ]
                .astype(str)
                == selected_payment
            ]
            .iloc[0]
        )

        st.subheader(
            "Decision Evidence Chain"
        )

        evidence_items = [
            (
                "Exception Type",
                selected_record.get(
                    "exception_type",
                    "N/A"
                )
            ),
            (
                "Financial Risk",
                selected_record.get(
                    "financial_risk",
                    "N/A"
                )
            ),
            (
                "AI Confidence",
                selected_record.get(
                    "confidence",
                    "N/A"
                )
            ),
            (
                "Agent Decision",
                selected_record.get(
                    "agent_decision",
                    "N/A"
                )
            ),
            (
                "Deterministic Evidence",
                selected_record.get(
                    "deterministic_evidence",
                    "N/A"
                )
            ),
            (
                "AI Reasoning",
                selected_record.get(
                    "ai_reasoning",
                    "N/A"
                )
            ),
            (
                "Action Taken",
                selected_record.get(
                    "action_taken",
                    "N/A"
                )
            ),
            (
                "AI Response Valid",
                selected_record.get(
                    "ai_response_valid",
                    "N/A"
                )
            ),
            (
                "Guardrail Violations",
                selected_record.get(
                    "guardrail_violations",
                    0
                )
            )
        ]

        for label, value in evidence_items:

            with st.expander(
                label
            ):

                st.write(
                    value
                )


# ============================================================
# 6G — DEMO MODE
# ============================================================

elif page == "🎬 Demo Mode":

    st.header(
        "🎬 MORTAL-FI Demo Mode"
    )

    st.caption(
        "Presentation-oriented walkthrough of a "
        "financial exception from detection to verification."
    )

    if ai_resolutions_df.empty:

        st.warning(
            "No AI resolution records available for demo."
        )

    else:

        payment_ids = (
            ai_resolutions_df[
                "payment_id"
            ]
            .astype(str)
            .unique()
            .tolist()
        )

        demo_payment = st.selectbox(
            "Select Demo Transaction",
            payment_ids
        )

        demo_ai = (
            ai_resolutions_df[
                ai_resolutions_df[
                    "payment_id"
                ]
                .astype(str)
                == demo_payment
            ]
            .iloc[0]
        )

        demo_exception = pd.DataFrame()

        if "payment_id" in exceptions_df.columns:

            demo_exception = (
                exceptions_df[
                    exceptions_df[
                        "payment_id"
                    ]
                    .astype(str)
                    == demo_payment
                ]
            )

        # ----------------------------------------------------
        # DEMO HEADER
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "Transaction Investigation"
        )

        demo_col1, demo_col2, demo_col3, demo_col4 = (
            st.columns(4)
        )

        demo_col1.metric(
            "Payment ID",
            demo_payment
        )

        demo_col2.metric(
            "Exception",
            demo_ai.get(
                "exception_type",
                "N/A"
            )
        )

        demo_col3.metric(
            "Risk",
            demo_ai.get(
                "financial_risk",
                "N/A"
            )
        )

        demo_confidence = demo_ai.get(
            "confidence",
            0
        )

        try:

            demo_confidence = (
                float(demo_confidence) * 100
            )

        except:

            demo_confidence = 0

        demo_col4.metric(
            "AI Confidence",
            f"{demo_confidence:.1f}%"
        )

        # ----------------------------------------------------
        # DEMO PIPELINE
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "AI Resolution Lifecycle"
        )

        step_col1, step_col2, step_col3, step_col4, step_col5 = (
            st.columns(5)
        )

        step_col1.success(
            "✓\n\nException Detected"
        )

        step_col2.success(
            "✓\n\nEvidence Analyzed"
        )

        step_col3.success(
            "✓\n\nAI Decision"
        )

        # Determine execution state

        demo_execution = pd.DataFrame()

        if not execution_df.empty:

            if "payment_id" in execution_df.columns:

                demo_execution = (
                    execution_df[
                        execution_df[
                            "payment_id"
                        ]
                        .astype(str)
                        == demo_payment
                    ]
                )

        demo_verification = pd.DataFrame()

        if not verification_df.empty:

            if "payment_id" in verification_df.columns:

                demo_verification = (
                    verification_df[
                        verification_df[
                            "payment_id"
                        ]
                        .astype(str)
                        == demo_payment
                    ]
                )

        if not demo_execution.empty:

            step_col4.success(
                "✓\n\nResolution Executed"
            )

        else:

            step_col4.warning(
                "○\n\nExecution Pending"
            )

        if not demo_verification.empty:

            latest_verification = (
                demo_verification.iloc[-1]
            )

            if (
                latest_verification.get(
                    "verification_status"
                )
                == "VERIFIED"
            ):

                step_col5.success(
                    "✓\n\nVerified"
                )

            else:

                step_col5.warning(
                    "!\n\nVerification Pending"
                )

        else:

            step_col5.warning(
                "○\n\nVerification Pending"
            )

        # ----------------------------------------------------
        # DEMO AI REASONING
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "AI Investigation"
        )

        st.write(
            demo_ai.get(
                "ai_reasoning",
                "No AI reasoning available."
            )
        )

        st.subheader(
            "Deterministic Evidence"
        )

        st.info(
            demo_ai.get(
                "deterministic_evidence",
                "No deterministic evidence available."
            )
        )

        # ----------------------------------------------------
        # DEMO DECISION
        # ----------------------------------------------------

        st.subheader(
            "AI Decision"
        )

        decision_demo_col1, decision_demo_col2, decision_demo_col3 = (
            st.columns(3)
        )

        decision_demo_col1.metric(
            "Agent Decision",
            demo_ai.get(
                "agent_decision",
                "N/A"
            )
        )

        decision_demo_col2.metric(
            "Resolution Status",
            demo_ai.get(
                "resolution_status",
                "N/A"
            )
        )

        decision_demo_col3.metric(
            "Human Review",
            demo_ai.get(
                "human_review_required",
                "N/A"
            )
        )

        # ----------------------------------------------------
        # DEMO ACTION
        # ----------------------------------------------------

        st.subheader(
            "Resolution Action"
        )

        st.info(
            demo_ai.get(
                "action_taken",
                "No action recorded."
            )
        )

        # ----------------------------------------------------
        # DEMO VERIFICATION
        # ----------------------------------------------------

        if not demo_verification.empty:

            st.subheader(
                "Verification"
            )

            latest_verification = (
                demo_verification.iloc[-1]
            )

            verification_status = (
                latest_verification.get(
                    "verification_status",
                    "N/A"
                )
            )

            if verification_status == "VERIFIED":

                st.success(
                    "✓ Resolution successfully verified."
                )

            else:

                st.warning(
                    f"Verification status: "
                    f"{verification_status}"
                )

            st.write(
                latest_verification.get(
                    "verification_message",
                    "No verification message."
                )
            )

        # ----------------------------------------------------
        # DEMO FOOTER
        # ----------------------------------------------------

        st.divider()

        st.success(
            "MORTAL-FI demonstrates an explainable "
            "AI-assisted reconciliation workflow with "
            "execution validation and post-execution verification."
        )


# ============================================================
# GLOBAL FOOTER
# ============================================================

st.divider()

st.caption(
    "MORTAL-FI | "
    "AI-Powered Financial Reconciliation System"
)
































# import streamlit as st
# import pandas as pd
# import requests
# import plotly.express as px


# # =================================================
# # PAGE CONFIGURATION
# # =================================================

# st.set_page_config(
#     page_title="MORTAL-FI | AI Reconciliation",
#     page_icon="💳",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# # =================================================
# # API CONFIGURATION
# # =================================================

# API_BASE_URL = "http://127.0.0.1:8000"


# # =================================================
# # API HELPER
# # =================================================

# def api_get(endpoint):

#     response = requests.get(
#         f"{API_BASE_URL}{endpoint}",
#         timeout=10
#     )

#     response.raise_for_status()

#     return response.json()


# # =================================================
# # DATA LOADING
# # =================================================

# @st.cache_data(ttl=30)
# def load_data():

#     metrics = api_get("/metrics")
#     kpis = api_get("/dashboard/kpis")
#     exceptions = api_get("/exceptions")
#     audit = api_get("/audit")

#     exception_analytics = api_get(
#         "/analytics/exceptions"
#     )

#     processing_status = api_get(
#         "/analytics/processing-status"
#     )

#     ai_resolutions = api_get(
#         "/ai/resolutions"
#     )

#     ai_agent_decisions = api_get(
#         "/ai/agent-decisions"
#     )

#     ai_analytics = api_get(
#         "/analytics/ai"
#     )

#     execution_audit = api_get(
#         "/execution/audit"
#     )

#     verification_audit = api_get(
#         "/execution/verification"
#     )

#     agent_performance = api_get(
#         "/analytics/agent-performance"
#     )

#     return (
#         metrics,
#         kpis,
#         exceptions,
#         audit,
#         exception_analytics,
#         processing_status,
#         ai_resolutions,
#         ai_agent_decisions,
#         ai_analytics,
#         execution_audit,
#         verification_audit,
#         agent_performance
#     )


# # =================================================
# # SIDEBAR
# # =================================================

# with st.sidebar:

#     st.title("💳 MORTAL-FI")

#     st.caption(
#         "AI-Powered Financial Reconciliation"
#     )

#     st.divider()

#     st.subheader("System")

#     st.write("🟢 FastAPI Backend")

#     st.write("🟢 Reconciliation Engine")

#     st.write("🟢 AI Resolution Agent")

#     st.write("🟢 Execution Guardrails")

#     st.write("🟢 Verification Engine")

#     st.divider()

#     if st.button(
#         "🔄 Refresh Dashboard",
#         use_container_width=True
#     ):

#         st.cache_data.clear()

#         st.rerun()

#     st.divider()

#     st.caption(
#         "MORTAL-FI v1.0"
#     )

#     st.caption(
#         "AI + Deterministic Controls"
#     )


# # =================================================
# # HEADER
# # =================================================

# st.title(
#     "💳 MORTAL-FI"
# )

# st.caption(
#     "AI-Powered Financial Reconciliation "
#     "and Exception Resolution System"
# )


# # =================================================
# # LOAD DATA
# # =================================================

# try:

#     (
#         metrics,
#         kpis,
#         exceptions,
#         audit,
#         exception_analytics,
#         processing_status,
#         ai_resolutions,
#         ai_agent_decisions,
#         ai_analytics,
#         execution_audit,
#         verification_audit,
#         agent_performance
#     ) = load_data()


# except Exception as error:

#     st.error(
#         "Unable to connect to the MORTAL-FI API."
#     )

#     st.info(
#         "Start FastAPI using:"
#     )

#     st.code(
#         "uvicorn src.api.app:app --reload"
#     )

#     st.caption(
#         f"Connection error: {error}"
#     )

#     st.stop()


# # =================================================
# # DATAFRAMES
# # =================================================

# exceptions_df = pd.DataFrame(
#     exceptions
# )

# audit_df = pd.DataFrame(
#     audit
# )

# ai_resolutions_df = pd.DataFrame(
#     ai_resolutions
# )

# ai_agent_df = pd.DataFrame(
#     ai_agent_decisions
# )

# execution_df = pd.DataFrame(
#     execution_audit.get(
#         "records",
#         []
#     )
# )

# verification_df = pd.DataFrame(
#     verification_audit.get(
#         "records",
#         []
#     )
# )


# # =================================================
# # PIPELINE STATUS
# # =================================================

# pipeline_processed = kpis.get(
#     "pipeline_fully_processed",
#     False
# )

# if pipeline_processed:

#     st.success(
#         "🟢 PIPELINE STATUS: FULLY PROCESSED"
#     )

# else:

#     st.warning(
#         "🟡 PIPELINE STATUS: PROCESSING INCOMPLETE"
#     )


# # =================================================
# # OVERVIEW TABS
# # =================================================

# overview_tab, exceptions_tab, ai_tab, execution_tab = st.tabs(
#     [
#         "📊 Overview",
#         "⚠️ Exceptions",
#         "🤖 AI Investigation",
#         "⚙️ Execution & Verification"
#     ]
# )


# # =================================================
# # OVERVIEW TAB
# # =================================================

# with overview_tab:

#     st.header(
#         "System Overview"
#     )

#     col1, col2, col3, col4, col5 = st.columns(5)

#     col1.metric(
#         "Total Transactions",
#         metrics.get(
#             "total_transactions",
#             0
#         )
#     )

#     col2.metric(
#         "Matched Transactions",
#         metrics.get(
#             "matched_transactions",
#             0
#         )
#     )

#     col3.metric(
#         "Exceptions",
#         metrics.get(
#             "exceptions_detected",
#             0
#         )
#     )

#     col4.metric(
#         "Match Rate",
#         f"{metrics.get('match_rate', 0)}%"
#     )

#     col5.metric(
#         "Auto Resolutions",
#         metrics.get(
#             "auto_resolutions",
#             0
#         )
#     )

#     st.divider()

#     # =================================================
#     # AI OVERVIEW
#     # =================================================

#     st.header(
#         "AI Resolution Overview"
#     )

#     ai_col1, ai_col2, ai_col3, ai_col4 = st.columns(4)

#     ai_col1.metric(
#         "AI Decisions",
#         agent_performance.get(
#             "total_exceptions",
#             0
#         )
#     )

#     ai_col2.metric(
#         "Auto Resolved",
#         agent_performance.get(
#             "auto_resolutions",
#             0
#         )
#     )

#     ai_col3.metric(
#         "Escalated",
#         agent_performance.get(
#             "escalations",
#             0
#         )
#     )

#     average_confidence = (
#         agent_performance.get(
#             "average_ai_confidence",
#             0
#         )
#         * 100
#     )

#     ai_col4.metric(
#         "Average Confidence",
#         f"{average_confidence:.2f}%"
#     )

#     st.divider()

#     # =================================================
#     # AGENT PERFORMANCE
#     # =================================================

#     st.header(
#         "AI Agent Performance"
#     )

#     perf_col1, perf_col2, perf_col3, perf_col4, perf_col5 = (
#         st.columns(5)
#     )

#     perf_col1.metric(
#         "Auto Resolution Rate",
#         f"{agent_performance.get('auto_resolution_rate', 0):.2f}%"
#     )

#     perf_col2.metric(
#         "Escalation Rate",
#         f"{agent_performance.get('escalation_rate', 0):.2f}%"
#     )

#     perf_col3.metric(
#         "Successful Executions",
#         agent_performance.get(
#             "successful_executions",
#             0
#         )
#     )

#     perf_col4.metric(
#         "Verified Resolutions",
#         agent_performance.get(
#             "verified_resolutions",
#             0
#         )
#     )

#     perf_col5.metric(
#         "Verification Rate",
#         f"{agent_performance.get('verification_rate', 0):.2f}%"
#     )

#     st.divider()

#     # =================================================
#     # ANALYTICS
#     # =================================================

#     st.header(
#         "System Analytics"
#     )

#     chart_col1, chart_col2 = st.columns(2)

#     decision_distribution = pd.DataFrame(
#         ai_analytics.get(
#             "decision_distribution",
#             []
#         )
#     )

#     if not decision_distribution.empty:

#         decision_chart = px.bar(
#             decision_distribution,
#             x="agent_decision",
#             y="count",
#             title="AI Decision Distribution",
#             labels={
#                 "agent_decision": "Agent Decision",
#                 "count": "Exceptions"
#             }
#         )

#         chart_col1.plotly_chart(
#             decision_chart,
#             use_container_width=True
#         )

#     risk_distribution = pd.DataFrame(
#         ai_analytics.get(
#             "risk_distribution",
#             []
#         )
#     )

#     if not risk_distribution.empty:

#         risk_chart = px.pie(
#             risk_distribution,
#             names="financial_risk",
#             values="count",
#             title="Financial Risk Distribution"
#         )

#         chart_col2.plotly_chart(
#             risk_chart,
#             use_container_width=True
#         )

#     chart_col3, chart_col4 = st.columns(2)

#     exception_counts = pd.DataFrame(
#         exception_analytics.get(
#             "exception_distribution",
#             []
#         )
#     )

#     if not exception_counts.empty:

#         exception_chart = px.bar(
#             exception_counts,
#             x="exception_type",
#             y="count",
#             title="Exception Type Distribution",
#             labels={
#                 "exception_type": "Exception Type",
#                 "count": "Exceptions"
#             }
#         )

#         chart_col3.plotly_chart(
#             exception_chart,
#             use_container_width=True
#         )

#     processing_counts = pd.DataFrame(
#         processing_status.get(
#             "processing_distribution",
#             []
#         )
#     )

#     if not processing_counts.empty:

#         processing_chart = px.pie(
#             processing_counts,
#             names="final_processing_status",
#             values="count",
#             title="Final Processing Status"
#         )

#         chart_col4.plotly_chart(
#             processing_chart,
#             use_container_width=True
#         )

#     st.divider()

#     # =================================================
#     # FINAL HEALTH
#     # =================================================

#     st.header(
#         "System Health"
#     )

#     health_col1, health_col2, health_col3, health_col4 = (
#         st.columns(4)
#     )

#     health_col1.metric(
#         "Total Exceptions",
#         agent_performance.get(
#             "total_exceptions",
#             0
#         )
#     )

#     health_col2.metric(
#         "High Risk Exceptions",
#         agent_performance.get(
#             "high_risk_exceptions",
#             0
#         )
#     )

#     health_col3.metric(
#         "Successful Executions",
#         agent_performance.get(
#             "successful_executions",
#             0
#         )
#     )

#     health_col4.metric(
#         "Verification Rate",
#         f"{agent_performance.get('verification_rate', 0):.2f}%"
#     )


# # =================================================
# # EXCEPTIONS TAB
# # =================================================

# with exceptions_tab:

#     st.header(
#         "⚠️ Detected Exceptions"
#     )

#     st.caption(
#         "Exceptions identified by the deterministic reconciliation engine."
#     )

#     if not exceptions_df.empty:

#         display_columns = [
#             "payment_id",
#             "order_id",
#             "payment_amount",
#             "exception_type",
#             "settlement_id",
#             "settlement_amount",
#             "match_method"
#         ]

#         available_columns = [
#             column
#             for column in display_columns
#             if column in exceptions_df.columns
#         ]

#         # ---------------------------------------------
#         # FILTER
#         # ---------------------------------------------

#         if "exception_type" in exceptions_df.columns:

#             exception_types = [
#                 "ALL"
#             ] + sorted(
#                 exceptions_df[
#                     "exception_type"
#                 ]
#                 .dropna()
#                 .astype(str)
#                 .unique()
#                 .tolist()
#             )

#             selected_exception_type = st.selectbox(
#                 "Filter by Exception Type",
#                 exception_types
#             )

#             filtered_exceptions = exceptions_df.copy()

#             if selected_exception_type != "ALL":

#                 filtered_exceptions = filtered_exceptions[
#                     filtered_exceptions[
#                         "exception_type"
#                     ]
#                     .astype(str)
#                     == selected_exception_type
#                 ]

#         else:

#             filtered_exceptions = exceptions_df

#         st.metric(
#             "Exceptions Displayed",
#             len(filtered_exceptions)
#         )

#         st.dataframe(
#             filtered_exceptions[
#                 available_columns
#             ],
#             use_container_width=True,
#             hide_index=True
#         )

#     else:

#         st.success(
#             "No exceptions detected."
#         )


# # =================================================
# # AI INVESTIGATION TAB
# # =================================================

# with ai_tab:

#     st.header(
#         "🤖 AI Exception Investigation"
#     )

#     st.caption(
#         "Explainable AI decision-making backed by deterministic financial evidence."
#     )

#     if not ai_resolutions_df.empty:

#         payment_ids = (
#             ai_resolutions_df[
#                 "payment_id"
#             ]
#             .astype(str)
#             .unique()
#             .tolist()
#         )

#         selected_payment = st.selectbox(
#             "Select Exception / Payment",
#             payment_ids
#         )

#         selected_ai_records = ai_resolutions_df[
#             ai_resolutions_df[
#                 "payment_id"
#             ]
#             .astype(str)
#             == selected_payment
#         ]

#         if selected_ai_records.empty:

#             st.warning(
#                 "AI record not found."
#             )

#         else:

#             selected_ai_record = (
#                 selected_ai_records.iloc[-1]
#             )

#             # -----------------------------------------
#             # DECISION SUMMARY
#             # -----------------------------------------

#             st.subheader(
#                 "AI Decision Summary"
#             )

#             decision_col1, decision_col2, decision_col3, decision_col4 = (
#                 st.columns(4)
#             )

#             decision_col1.metric(
#                 "Payment ID",
#                 selected_ai_record.get(
#                     "payment_id",
#                     "N/A"
#                 )
#             )

#             decision_col2.metric(
#                 "Exception Type",
#                 selected_ai_record.get(
#                     "exception_type",
#                     "N/A"
#                 )
#             )

#             decision_col3.metric(
#                 "Financial Risk",
#                 selected_ai_record.get(
#                     "financial_risk",
#                     "N/A"
#                 )
#             )

#             confidence = selected_ai_record.get(
#                 "confidence",
#                 0
#             )

#             try:

#                 confidence_display = (
#                     f"{float(confidence) * 100:.1f}%"
#                 )

#             except:

#                 confidence_display = str(
#                     confidence
#                 )

#             decision_col4.metric(
#                 "AI Confidence",
#                 confidence_display
#             )

#             # -----------------------------------------
#             # STATUS
#             # -----------------------------------------

#             st.subheader(
#                 "Decision Status"
#             )

#             status_col1, status_col2, status_col3, status_col4 = (
#                 st.columns(4)
#             )

#             status_col1.write(
#                 "**Agent Decision**"
#             )

#             status_col1.info(
#                 str(
#                     selected_ai_record.get(
#                         "agent_decision",
#                         "N/A"
#                     )
#                 )
#             )

#             status_col2.write(
#                 "**Resolution Status**"
#             )

#             status_col2.info(
#                 str(
#                     selected_ai_record.get(
#                         "resolution_status",
#                         "N/A"
#                     )
#                 )
#             )

#             status_col3.write(
#                 "**Auto Resolvable**"
#             )

#             status_col3.info(
#                 str(
#                     selected_ai_record.get(
#                         "auto_resolvable",
#                         "N/A"
#                     )
#                 )
#             )

#             status_col4.write(
#                 "**Human Review Required**"
#             )

#             status_col4.info(
#                 str(
#                     selected_ai_record.get(
#                         "human_review_required",
#                         "N/A"
#                     )
#                 )
#             )

#             # -----------------------------------------
#             # FINANCIAL EVIDENCE
#             # -----------------------------------------

#             st.divider()

#             st.subheader(
#                 "Financial Evidence"
#             )

#             selected_exception = exceptions_df[
#                 exceptions_df[
#                     "payment_id"
#                 ]
#                 .astype(str)
#                 == selected_payment
#             ]

#             if not selected_exception.empty:

#                 exception_record = (
#                     selected_exception.iloc[0]
#                 )

#                 payment_amount = exception_record.get(
#                     "payment_amount"
#                 )

#                 settlement_amount = exception_record.get(
#                     "settlement_amount"
#                 )

#                 evidence_col1, evidence_col2, evidence_col3, evidence_col4 = (
#                     st.columns(4)
#                 )

#                 evidence_col1.metric(
#                     "Payment Amount",
#                     (
#                         f"₹{float(payment_amount):,.2f}"
#                         if pd.notna(payment_amount)
#                         else "N/A"
#                     )
#                 )

#                 evidence_col2.metric(
#                     "Settlement Amount",
#                     (
#                         f"₹{float(settlement_amount):,.2f}"
#                         if pd.notna(settlement_amount)
#                         else "N/A"
#                     )
#                 )

#                 if (
#                     pd.notna(payment_amount)
#                     and pd.notna(settlement_amount)
#                 ):

#                     difference = (
#                         float(payment_amount)
#                         -
#                         float(settlement_amount)
#                     )

#                     if float(payment_amount) != 0:

#                         difference_percentage = (
#                             abs(difference)
#                             /
#                             abs(float(payment_amount))
#                             *
#                             100
#                         )

#                     else:

#                         difference_percentage = 0

#                     evidence_col3.metric(
#                         "Amount Difference",
#                         f"₹{difference:,.2f}"
#                     )

#                     evidence_col4.metric(
#                         "Difference %",
#                         f"{difference_percentage:.2f}%"
#                     )

#                 else:

#                     evidence_col3.metric(
#                         "Amount Difference",
#                         "N/A"
#                     )

#                     evidence_col4.metric(
#                         "Difference %",
#                         "N/A"
#                     )

#             # -----------------------------------------
#             # AI REASONING
#             # -----------------------------------------

#             st.subheader(
#                 "AI Reasoning"
#             )

#             st.write(
#                 selected_ai_record.get(
#                     "ai_reasoning",
#                     "No reasoning available."
#                 )
#             )

#             # -----------------------------------------
#             # DETERMINISTIC EVIDENCE
#             # -----------------------------------------

#             st.subheader(
#                 "Deterministic Evidence"
#             )

#             st.info(
#                 selected_ai_record.get(
#                     "deterministic_evidence",
#                     "No deterministic evidence available."
#                 )
#             )

#             # -----------------------------------------
#             # RESOLUTION ACTION
#             # -----------------------------------------

#             st.subheader(
#                 "Resolution Action"
#             )

#             action_col1, action_col2 = st.columns(2)

#             action_col1.write(
#                 "**Action Taken**"
#             )

#             action_col1.info(
#                 str(
#                     selected_ai_record.get(
#                         "action_taken",
#                         "N/A"
#                     )
#                 )
#             )

#             action_col2.write(
#                 "**AI Response Status**"
#             )

#             action_col2.info(
#                 str(
#                     selected_ai_record.get(
#                         "reasoning_status",
#                         "N/A"
#                     )
#                 )
#             )

#             # -----------------------------------------
#             # SAFETY
#             # -----------------------------------------

#             st.subheader(
#                 "AI Safety & Validation"
#             )

#             validation_col1, validation_col2 = (
#                 st.columns(2)
#             )

#             validation_col1.write(
#                 "**AI Response Valid**"
#             )

#             validation_col1.info(
#                 str(
#                     selected_ai_record.get(
#                         "ai_response_valid",
#                         "N/A"
#                     )
#                 )
#             )

#             validation_col2.write(
#                 "**Guardrail Violations**"
#             )

#             validation_col2.info(
#                 str(
#                     selected_ai_record.get(
#                         "guardrail_violations",
#                         0
#                     )
#                 )
#             )

#     else:

#         st.info(
#             "No AI resolution records available."
#         )


# # =================================================
# # EXECUTION TAB
# # =================================================

# with execution_tab:

#     st.header(
#         "⚙️ Execution & Verification"
#     )

#     st.caption(
#         "Controlled resolution execution followed by independent post-execution verification."
#     )

#     # =================================================
#     # LATEST EXECUTION STATE
#     # =================================================

#     if not execution_df.empty:

#         latest_execution_df = execution_df.copy()

#         if "payment_id" in latest_execution_df.columns:

#             latest_execution_df = (
#                 latest_execution_df
#                 .drop_duplicates(
#                     subset=["payment_id"],
#                     keep="last"
#                 )
#             )

#         executed_count = 0
#         already_executed_count = 0
#         failed_execution_count = 0

#         if "execution_status" in latest_execution_df.columns:

#             executed_count = len(
#                 latest_execution_df[
#                     latest_execution_df[
#                         "execution_status"
#                     ]
#                     == "EXECUTED"
#                 ]
#             )

#             already_executed_count = len(
#                 latest_execution_df[
#                     latest_execution_df[
#                         "execution_status"
#                     ]
#                     == "ALREADY_EXECUTED"
#                 ]
#             )

#             failed_execution_count = len(
#                 latest_execution_df[
#                     latest_execution_df[
#                         "execution_status"
#                     ]
#                     == "FAILED"
#                 ]
#             )

#         exec_col1, exec_col2, exec_col3 = (
#             st.columns(3)
#         )

#         exec_col1.metric(
#             "Executed",
#             executed_count
#         )

#         exec_col2.metric(
#             "Already Executed",
#             already_executed_count
#         )

#         exec_col3.metric(
#             "Failed",
#             failed_execution_count
#         )

#         st.subheader(
#             "Latest Execution State"
#         )

#         st.dataframe(
#             latest_execution_df,
#             use_container_width=True,
#             hide_index=True
#         )

#     else:

#         st.info(
#             "No execution audit records available."
#         )

#     st.divider()

#     # =================================================
#     # LATEST VERIFICATION STATE
#     # =================================================

#     if not verification_df.empty:

#         latest_verification_df = verification_df.copy()

#         if "payment_id" in latest_verification_df.columns:

#             latest_verification_df = (
#                 latest_verification_df
#                 .drop_duplicates(
#                     subset=["payment_id"],
#                     keep="last"
#                 )
#             )

#         verified_count = 0
#         verification_failed_count = 0

#         if "verification_status" in latest_verification_df.columns:

#             verified_count = len(
#                 latest_verification_df[
#                     latest_verification_df[
#                         "verification_status"
#                     ]
#                     == "VERIFIED"
#                 ]
#             )

#             verification_failed_count = len(
#                 latest_verification_df[
#                     latest_verification_df[
#                         "verification_status"
#                     ]
#                     != "VERIFIED"
#                 ]
#             )

#         verify_col1, verify_col2 = (
#             st.columns(2)
#         )

#         verify_col1.metric(
#             "Verified",
#             verified_count
#         )

#         verify_col2.metric(
#             "Verification Failures",
#             verification_failed_count
#         )

#         st.subheader(
#             "Latest Verification State"
#         )

#         st.dataframe(
#             latest_verification_df,
#             use_container_width=True,
#             hide_index=True
#         )

#     else:

#         st.info(
#             "No verification audit records available."
#         )


# # =================================================
# # FOOTER
# # =================================================

# st.divider()

# st.caption(
#     "MORTAL-FI | "
#     "AI-Powered Financial Reconciliation System"
# )
