import json
import sys

from pathlib import Path
from statistics import mean


# ============================================================
# PROJECT PATH SETUP
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# IMPORT MODULES
# ============================================================

from src.controller.finance_controller import FinanceController

from src.metrics.performance_metrics import (
    run_performance_benchmark
)

from src.reports.exception_report import (
    build_exception_report
)

from src.validation.pipeline_validator import (
    main as validate_pipeline
)


# ============================================================
# FINAL CONTROLLER REPORT
# ============================================================

def build_final_report():

    print("\n" + "=" * 60)
    print("BUILDING FINAL CONTROLLER REPORT")
    print("=" * 60)


    # --------------------------------------------------------
    # STEP 1: FINANCE CONTROLLER
    # --------------------------------------------------------

    print("\nRunning finance controller...")

    controller = (
        FinanceController()
    )

    controller_summary = (
        controller.run()
    )


    # --------------------------------------------------------
    # STEP 2: PERFORMANCE BENCHMARK
    # --------------------------------------------------------

    print("\nRunning performance benchmark...")

    benchmark_data = (
        run_performance_benchmark()
    )


    processing_times = (
        benchmark_data[
            "processing_times"
        ]
    )

    throughputs = (
        benchmark_data[
            "throughputs"
        ]
    )

    benchmark_results = (
        benchmark_data[
            "results"
        ]
    )


    total_records = (
        len(
            benchmark_results
        )
    )


    matched_transactions = (
        len(
            benchmark_results[
                benchmark_results[
                    "status"
                ]
                == "MATCHED"
            ]
        )
    )


    exceptions_detected = (
        len(
            benchmark_results[
                benchmark_results[
                    "status"
                ]
                == "EXCEPTION"
            ]
        )
    )


    reference_recoveries = (
        len(
            benchmark_results[
                benchmark_results[
                    "exception_type"
                ]
                == "REFERENCE_MISMATCH"
            ]
        )
    )


    match_rate = (

        matched_transactions
        /
        total_records
        *
        100

        if total_records > 0

        else 0
    )


    exception_rate = (

        exceptions_detected
        /
        total_records
        *
        100

        if total_records > 0

        else 0
    )


    performance_metrics = {

        "benchmark_runs": (
            len(
                processing_times
            )
        ),

        "average_processing_time_seconds": (
            round(
                mean(processing_times),
                6
            )
        ),

        "fastest_processing_time_seconds": (
            round(
                min(processing_times),
                6
            )
        ),

        "slowest_processing_time_seconds": (
            round(
                max(processing_times),
                6
            )
        ),

        "average_throughput_records_per_second": (
            round(
                mean(throughputs),
                2
            )
        ),

        "best_throughput_records_per_second": (
            round(
                max(throughputs),
                2
            )
        ),

        "worst_throughput_records_per_second": (
            round(
                min(throughputs),
                2
            )
        ),

        "total_records_processed": (
            total_records
        ),

        "matched_transactions": (
            matched_transactions
        ),

        "exceptions_detected": (
            exceptions_detected
        ),

        "reference_linkages_recovered": (
            reference_recoveries
        ),

        "match_rate_percent": (
            round(
                match_rate,
                2
            )
        ),

        "exception_rate_percent": (
            round(
                exception_rate,
                2
            )
        )
    }


    # --------------------------------------------------------
    # STEP 3: EXCEPTION REPORT
    # --------------------------------------------------------

    print("\nBuilding exception report...")

    exception_report = (
        build_exception_report()
    )


    # --------------------------------------------------------
    # STEP 4: PIPELINE VALIDATION
    # --------------------------------------------------------

    print("\nValidating pipeline...")

    pipeline_valid = (
        validate_pipeline()
    )


    # --------------------------------------------------------
    # BUILD FINAL REPORT
    # --------------------------------------------------------

    final_report = {

        "project": (
            "MORTAL-FI"
        ),

        "report_type": (
            "FINAL_FINANCE_CONTROLLER_REPORT"
        ),

        "finance_controller": (
            controller_summary
        ),

        "performance_metrics": (
            performance_metrics
        ),

        "exception_summary": (
            exception_report
        ),

        "pipeline_integrity": (
            pipeline_valid
        )
    }


    # --------------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------------

    report_directory = (

        PROJECT_ROOT
        / "data"
        / "reports"

    )

    report_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    report_path = (

        report_directory
        / "final_controller_report.json"

    )


    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_report,
            file,
            indent=4,
            default=str
        )


    # --------------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL CONTROLLER REPORT")
    print("=" * 60)


    print(
        f"\nProject: "
        f"{final_report['project']}"
    )


    print(
        "\nPipeline Integrity: "
        f"{'VERIFIED' if pipeline_valid else 'FAILED'}"
    )


    print(
        "\n✓ Final report saved:"
    )

    print(
        report_path
    )


    return final_report


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    build_final_report()