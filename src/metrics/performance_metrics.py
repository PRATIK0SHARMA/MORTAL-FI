from time import perf_counter
from statistics import mean

from src.reconciliation.loader import load_all_data
from src.reconciliation.engine import ReconciliationEngine


# =================================================
# PERFORMANCE METRICS ENGINE
# =================================================

BENCHMARK_RUNS = 5


def run_single_benchmark(data):

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

        end_time
        -
        start_time

    )


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


    return {

        "processing_time": processing_time,

        "throughput": throughput,

        "results": results
    }


# =================================================
# RUN PERFORMANCE BENCHMARK
# =================================================

def run_performance_benchmark():

    print("\n" + "=" * 60)
    print("RECONCILIATION PERFORMANCE BENCHMARK")
    print("=" * 60)


    # ---------------------------------------------
    # LOAD DATA ONCE
    # ---------------------------------------------

    data = load_all_data()


    benchmark_results = []


    # ---------------------------------------------
    # RUN MULTIPLE BENCHMARKS
    # ---------------------------------------------

    print("\nRunning benchmark iterations...\n")


    for run_number in range(
        1,
        BENCHMARK_RUNS + 1
    ):

        benchmark = (
            run_single_benchmark(
                data
            )
        )


        benchmark_results.append(
            benchmark
        )


        print(

            f"Run {run_number}: "

            f"{benchmark['processing_time']:.6f} seconds | "

            f"{benchmark['throughput']:.2f} records/second"

        )


    # ---------------------------------------------
    # EXTRACT VALUES
    # ---------------------------------------------

    processing_times = [

        result["processing_time"]

        for result
        in benchmark_results

    ]


    throughputs = [

        result["throughput"]

        for result
        in benchmark_results

    ]


    # ---------------------------------------------
    # USE LAST RESULT FOR BUSINESS METRICS
    # ---------------------------------------------

    results = (
        benchmark_results[-1]["results"]
    )


    total_records = len(
        results
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
    # PERFORMANCE SUMMARY
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)


    print(
        f"Benchmark Runs: "
        f"{BENCHMARK_RUNS}"
    )

    print(
        f"Average Processing Time: "
        f"{mean(processing_times):.6f} seconds"
    )

    print(
        f"Fastest Processing Time: "
        f"{min(processing_times):.6f} seconds"
    )

    print(
        f"Slowest Processing Time: "
        f"{max(processing_times):.6f} seconds"
    )

    print(
        f"Average Throughput: "
        f"{mean(throughputs):.2f} records/second"
    )

    print(
        f"Best Throughput: "
        f"{max(throughputs):.2f} records/second"
    )

    print(
        f"Worst Throughput: "
        f"{min(throughputs):.2f} records/second"
    )


    # ---------------------------------------------
    # BUSINESS METRICS
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("RECONCILIATION METRICS")
    print("=" * 60)


    print(
        f"Total Records Processed: "
        f"{total_records}"
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


    return {

        "results": results,

        "processing_times": processing_times,

        "throughputs": throughputs
    }


# =================================================
# MAIN
# =================================================

if __name__ == "__main__":

    run_performance_benchmark()