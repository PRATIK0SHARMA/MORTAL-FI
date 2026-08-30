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