from time import perf_counter

from src.reconciliation.loader import load_all_data
from src.reconciliation.engine import ReconciliationEngine


# =================================================
# PERFORMANCE METRICS ENGINE
# =================================================

def run_performance_benchmark():

    print("\n" + "=" * 60)
    print("RECONCILIATION PERFORMANCE BENCHMARK")
    print("=" * 60)


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    data = load_all_data()


    # ---------------------------------------------
    # CREATE ENGINE
    # ---------------------------------------------

    engine = ReconciliationEngine(

        orders=data["orders"],

        payments=data["payments"],

        settlements=data["settlements"]
    )


    # ---------------------------------------------
    # START TIMER
    # ---------------------------------------------

    start_time = perf_counter()


    # ---------------------------------------------
    # RUN RECONCILIATION
    # ---------------------------------------------

    results = engine.run()


    # ---------------------------------------------
    # STOP TIMER
    # ---------------------------------------------

    end_time = perf_counter()


    processing_time = (
        end_time - start_time
    )


    # ---------------------------------------------
    # CALCULATE METRICS
    # ---------------------------------------------

    total_records = len(
        results
    )

    throughput = (

        total_records
        /
        processing_time

        if processing_time > 0

        else 0
    )


    matched_count = len(

        results[
            results["status"]
            == "MATCHED"
        ]

    )


    exception_count = len(

        results[
            results["status"]
            == "EXCEPTION"
        ]

    )


    reference_recovery_count = len(

        results[
            results["exception_type"]
            == "REFERENCE_MISMATCH"
        ]

    )


    match_rate = (

        matched_count
        /
        total_records
        *
        100
    )


    exception_rate = (

        exception_count
        /
        total_records
        *
        100
    )


    # ---------------------------------------------
    # PRINT METRICS
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)

    print(
        f"Total Records Processed: "
        f"{total_records}"
    )

    print(
        f"Processing Time: "
        f"{processing_time:.6f} seconds"
    )

    print(
        f"Throughput: "
        f"{throughput:.2f} records/second"
    )

    print(
        f"Matched Transactions: "
        f"{matched_count}"
    )

    print(
        f"Exceptions Detected: "
        f"{exception_count}"
    )

    print(
        f"Reference Recoveries: "
        f"{reference_recovery_count}"
    )

    print(
        f"Match Rate: "
        f"{match_rate:.2f}%"
    )

    print(
        f"Exception Rate: "
        f"{exception_rate:.2f}%"
    )


    return results


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":

    run_performance_benchmark()