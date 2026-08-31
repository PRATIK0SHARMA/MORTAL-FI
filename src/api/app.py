from pathlib import Path
import math
import pandas as pd
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =================================================
# PROJECT PATH
# =================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)


# =================================================
# DATA PATHS
# =================================================

SYSTEM_METRICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "metrics"
    / "system_metrics.csv"
)


DASHBOARD_KPIS_PATH = (
    PROJECT_ROOT
    / "data"
    / "dashboard"
    / "dashboard_kpis.csv"
)


AUDIT_PATH = (
    PROJECT_ROOT
    / "data"
    / "audit"
    / "end_to_end_audit_trail.csv"
)


AI_RESOLUTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_resolution"
    / "ai_resolution_results.csv"
)

AI_AGENT_DECISIONS_PATH = (
    PROJECT_ROOT
    / "data"
    / "ai_agent"
    / "agent_decisions.csv"
)


RECONCILIATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "reconciliation"
    / "reconciliation_results.csv"
)


def clean_json_data(data):

    if isinstance(data, dict):

        return {

            key: clean_json_data(value)

            for key, value in data.items()

        }


    elif isinstance(data, list):

        return [

            clean_json_data(item)

            for item in data

        ]


    elif isinstance(
        data,
        (float, np.floating)
    ):

        if pd.isna(data):

            return None

        if math.isinf(data):

            return None

        return float(data)


    elif isinstance(
        data,
        (int, np.integer)
    ):

        return int(data)


    elif pd.isna(data):

        return None


    return data

# =================================================
# FASTAPI APPLICATION
# =================================================

app = FastAPI(

    title="MORTAL-FI API",

    description=(
        "API layer for the MORTAL-FI "
        "AI-powered financial reconciliation system"
    ),

    version="1.0.0"

)


# =================================================
# CORS CONFIGURATION
# =================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:8501"

    ],

    allow_credentials=True,

    allow_methods=[

        "*"

    ],

    allow_headers=[

        "*"

    ]

)


# =================================================
# HOME ENDPOINT
# =================================================

@app.get("/")

def home():

    return {

        "project": "MORTAL-FI",

        "status": "API_RUNNING",

        "message": (
            "AI-powered financial reconciliation "
            "system API"
        )

    }


# =================================================
# SYSTEM METRICS
# =================================================

@app.get("/metrics")

def get_system_metrics():

    metrics = pd.read_csv(
        SYSTEM_METRICS_PATH
    )


    return clean_json_data(

        metrics
        .iloc[0]
        .to_dict()

    )


# =================================================
# DASHBOARD KPIs
# =================================================

@app.get("/dashboard/kpis")

def get_dashboard_kpis():

    kpis = pd.read_csv(
        DASHBOARD_KPIS_PATH
    )


    return clean_json_data(

        kpis
        .iloc[0]
        .to_dict()

    )


# =================================================
# ALL RECONCILIATION RECORDS
# =================================================

@app.get("/reconciliation")

def get_reconciliation_records():

    reconciliation = pd.read_csv(
        RECONCILIATION_PATH
    )


    return clean_json_data(

        reconciliation
        .to_dict(
            orient="records"
        )

    )


# =================================================
# ALL AI RESOLUTION RECORDS
# =================================================

@app.get("/ai/resolutions")

def get_ai_resolutions():

    resolutions = pd.read_csv(
        AI_RESOLUTION_PATH
    )


    return clean_json_data(

        resolutions
        .to_dict(
            orient="records"
        )

    )

# =================================================
# AI AGENT DECISIONS
# =================================================

@app.get("/ai/agent-decisions")

def get_ai_agent_decisions():

    decisions = pd.read_csv(
        AI_AGENT_DECISIONS_PATH
    )


    return clean_json_data(

        decisions
        .to_dict(
            orient="records"
        )

    )

# =================================================
# SINGLE AI AGENT DECISION
# =================================================

@app.get("/ai/agent-decisions/{payment_id}")

def get_ai_agent_decision(
    payment_id: str
):

    decisions = pd.read_csv(
        AI_AGENT_DECISIONS_PATH
    )


    decision = decisions[
        decisions["payment_id"]
        == payment_id
    ]


    if decision.empty:

        return {

            "error":
                "AI decision not found"

        }


    return clean_json_data(

        decision
        .iloc[0]
        .to_dict()

    )

# =================================================
# AI AGENT ANALYTICS
# =================================================

@app.get("/analytics/ai")

def get_ai_agent_analytics():

    decisions = pd.read_csv(
        AI_AGENT_DECISIONS_PATH
    )


    total_decisions = len(
        decisions
    )


    auto_resolved = len(
        decisions[
            decisions["agent_decision"]
            == "AUTO_RESOLVE"
        ]
    )


    escalated = len(
        decisions[
            decisions["agent_decision"]
            == "ESCALATE"
        ]
    )


    manual_review = len(
        decisions[
            decisions["human_review_required"]
            == True
        ]
    )


    average_confidence = (

        decisions["confidence"]
        .mean()

    )


    decision_distribution = (

        decisions[
            "agent_decision"
        ]
        .value_counts()
        .reset_index()

    )


    decision_distribution.columns = [

        "agent_decision",

        "count"

    ]


    risk_distribution = (

        decisions[
            "financial_risk"
        ]
        .value_counts()
        .reset_index()

    )


    risk_distribution.columns = [

        "financial_risk",

        "count"

    ]


    return clean_json_data({

        "total_ai_decisions":
            int(total_decisions),

        "auto_resolved":
            int(auto_resolved),

        "escalated":
            int(escalated),

        "manual_review_required":
            int(manual_review),

        "average_confidence":
            round(
                float(average_confidence),
                4
            ),

        "decision_distribution":
            decision_distribution
            .to_dict(
                orient="records"
            ),

        "risk_distribution":
            risk_distribution
            .to_dict(
                orient="records"
            )

    })


# =================================================
# ALL AUDIT RECORDS
# =================================================

@app.get("/audit")

def get_audit_records():

    audit = pd.read_csv(
        AUDIT_PATH
    )


    return clean_json_data(

        audit
        .to_dict(
            orient="records"
        )

    )



# =================================================
# EXCEPTION RECORDS
# =================================================

@app.get("/exceptions")

def get_exceptions():

    exceptions = pd.read_csv(
        RECONCILIATION_PATH
    )


    exception_records = (

        exceptions[
            exceptions["status"]
            == "EXCEPTION"
        ]

    )


    records = (

        exception_records
        .to_dict(
            orient="records"
        )

    )


    return clean_json_data(
        records
    )

# =================================================
# EXCEPTION ANALYTICS
# =================================================

@app.get("/analytics/exceptions")
def get_exception_analytics():

    reconciliation = pd.read_csv(
        RECONCILIATION_PATH
    )


    exceptions = reconciliation[
        reconciliation["status"]
        == "EXCEPTION"
    ]


    exception_distribution = (
        exceptions["exception_type"]
        .value_counts()
        .reset_index()
    )


    exception_distribution.columns = [
        "exception_type",
        "count"
    ]


    total_exceptions = len(
        exceptions
    )


    return clean_json_data({

        "total_exceptions":
            int(total_exceptions),

        "exception_distribution":
            exception_distribution
            .to_dict(
                orient="records"
            )

    })

# =================================================
# EXCEPTION DETAILS
# =================================================

@app.get("/exceptions/{payment_id}")

def get_exception_details(
    payment_id: str
):

    reconciliation = pd.read_csv(
        RECONCILIATION_PATH
    )


    exception = reconciliation[

        (
            reconciliation[
                "payment_id"
            ]
            == payment_id
        )

        &

        (
            reconciliation[
                "status"
            ]
            == "EXCEPTION"
        )

    ]


    if exception.empty:

        return {

            "message":
                "Exception not found"

        }


    return clean_json_data(

        exception
        .iloc[0]
        .to_dict()

    )

# =================================================
# FINAL PROCESSING STATUS ANALYTICS
# =================================================

@app.get("/analytics/processing-status")
def get_processing_status_analytics():

    audit = pd.read_csv(
        AUDIT_PATH
    )


    processing_distribution = (

        audit[
            "final_processing_status"
        ]
        .value_counts()
        .reset_index()

    )


    processing_distribution.columns = [

        "final_processing_status",
        "count"

    ]


    total_records = len(
        audit
    )


    return clean_json_data({

        "total_records":
            int(total_records),

        "processing_distribution":

            processing_distribution
            .to_dict(
                orient="records"
            )

    })