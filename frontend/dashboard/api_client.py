import requests


# =================================================
# API BASE URL
# =================================================

BASE_URL = (
    "http://127.0.0.1:8000"
)


# =================================================
# GENERIC API REQUEST
# =================================================

def get_api_data(
    endpoint
):

    try:

        response = requests.get(

            f"{BASE_URL}{endpoint}",

            timeout=10

        )


        response.raise_for_status()


        return response.json()


    except requests.exceptions.RequestException as error:

        return {

            "error": str(
                error
            )

        }


# =================================================
# SYSTEM METRICS
# =================================================

def get_system_metrics():

    return get_api_data(
        "/metrics"
    )


# =================================================
# DASHBOARD KPIs
# =================================================

def get_dashboard_kpis():

    return get_api_data(
        "/dashboard/kpis"
    )


# =================================================
# EXCEPTIONS
# =================================================

def get_exceptions():

    return get_api_data(
        "/exceptions"
    )


# =================================================
# AI RESOLUTIONS
# =================================================

def get_ai_resolutions():

    return get_api_data(
        "/ai/resolutions"
    )


# =================================================
# AUDIT RECORDS
# =================================================

def get_audit_records():

    return get_api_data(
        "/audit"
    )