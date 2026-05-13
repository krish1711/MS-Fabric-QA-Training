import json
import os
from decimal import Decimal
from pathlib import Path


def load_results():
    base_dir = Path(__file__).resolve().parents[1]
    configured_path = os.environ.get("OBSERVED_RESULTS_PATH")
    results_path = Path(configured_path) if configured_path else base_dir / "observed_results.json"
    with results_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_decimal(value):
    return Decimal(str(value))


def test_pipeline_statuses_and_duration_pattern():
    data = load_results()
    pipeline = data["pipeline"]

    assert pipeline["run_1_status"] == "Failed"
    assert pipeline["run_2_status"] == "Succeeded"
    assert pipeline["fast_activity_status"] == "Succeeded"
    assert pipeline["slow_activity_status"] == "Succeeded"
    assert pipeline["threshold_activity_initial_status"] == "Failed"
    assert pipeline["threshold_activity_rerun_status"] == "Succeeded"
    assert pipeline["fast_duration_seconds"] > 0
    assert pipeline["slow_duration_seconds"] > pipeline["fast_duration_seconds"]
    assert pipeline["slow_activity_longer_than_fast"] is True


def test_warehouse_kpis():
    data = load_results()
    warehouse = data["warehouse"]

    assert warehouse["factsales_count"] == 10
    assert as_decimal(warehouse["total_sales"]) == Decimal("5070.00")
    assert warehouse["order_count"] == 10
    assert as_decimal(warehouse["average_order_value"]) == Decimal("507.00")


def test_region_totals():
    data = load_results()
    region_totals = data["warehouse"]["region_totals"]

    assert region_totals["East"]["order_count"] == 2
    assert as_decimal(region_totals["East"]["total_sales"]) == Decimal("1590.00")

    assert region_totals["North"]["order_count"] == 3
    assert as_decimal(region_totals["North"]["total_sales"]) == Decimal("1530.00")

    assert region_totals["South"]["order_count"] == 2
    assert as_decimal(region_totals["South"]["total_sales"]) == Decimal("390.00")

    assert region_totals["West"]["order_count"] == 3
    assert as_decimal(region_totals["West"]["total_sales"]) == Decimal("1560.00")
