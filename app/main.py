from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from app.engine import recommend_distribution
from app.models import DistributionRequest, ProductSizeDemand, StoreProfile


def _request_from_json(payload: dict) -> DistributionRequest:
    stores = []
    for store_payload in payload.get("stores", []):
        assortment = [ProductSizeDemand(**item) for item in store_payload.get("assortment", [])]
        stores.append(
            StoreProfile(
                store_id=store_payload["store_id"],
                capacity_units=store_payload["capacity_units"],
                demand_index=store_payload.get("demand_index", 1.0),
                assortment=assortment,
            )
        )

    return DistributionRequest(
        stores=stores,
        planning_horizon_days=payload.get("planning_horizon_days", 14),
        service_level=payload.get("service_level", 0.95),
        custom_factors=payload.get("custom_factors"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Store product-size distribution planner")
    parser.add_argument("input_json", type=Path, help="Path to a JSON planning payload.")
    args = parser.parse_args()

    with args.input_json.open("r", encoding="utf-8") as f:
        raw_payload = json.load(f)

    request = _request_from_json(raw_payload)
    response = recommend_distribution(request)
    print(json.dumps(asdict(response), indent=2))


if __name__ == "__main__":
    main()
