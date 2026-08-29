from src.metrics.metrics_engine import (
    MetricsEngine
)


# =================================================
# RUN CENTRALIZED METRICS
# =================================================

def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "RUNNING CENTRALIZED METRICS ENGINE"
    )

    print(
        "=" * 60
    )


    engine = (
        MetricsEngine()
    )


    # ---------------------------------------------
    # LOAD DATA
    # ---------------------------------------------

    engine.load_data()


    # ---------------------------------------------
    # BUILD METRICS
    # ---------------------------------------------

    metrics = (
        engine.build_metrics()
    )


    # ---------------------------------------------
    # DISPLAY METRICS
    # ---------------------------------------------

    engine.display_metrics(
        metrics
    )


    # ---------------------------------------------
    # SAVE METRICS
    # ---------------------------------------------

    engine.save_metrics(
        metrics
    )


if __name__ == "__main__":

    main()