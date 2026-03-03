from __future__ import annotations

import math
from typing import Dict, List

from app.models import (
    AllocationRecommendation,
    DistributionRequest,
    DistributionResponse,
    ProductSizeDemand,
    StoreRecommendation,
)


def _base_demand_score(
    item: ProductSizeDemand,
    planning_horizon_days: int,
    service_level: float,
    demand_index: float,
    global_multiplier: float,
) -> float:
    daily_sales = item.recent_sales_units / max(1.0, item.lead_time_days)
    projected_demand = daily_sales * planning_horizon_days
    safety_stock = projected_demand * (service_level - 0.5)
    inventory_gap = max(0.0, projected_demand + safety_stock - item.on_hand_units)

    return (
        inventory_gap
        * item.seasonality_multiplier
        * item.strategic_weight
        * demand_index
        * global_multiplier
    )


def recommend_distribution(payload: DistributionRequest) -> DistributionResponse:
    global_multiplier = 1.0
    notes: List[str] = []

    if payload.custom_factors:
        for _, factor_value in payload.custom_factors.items():
            global_multiplier *= factor_value
        notes.append("Applied custom factors as a global multiplier.")

    store_recommendations: List[StoreRecommendation] = []

    for store in payload.stores:
        raw_scores: Dict[str, float] = {}

        for item in store.assortment:
            key = f"{item.product_id}::{item.size}"
            raw_scores[key] = _base_demand_score(
                item,
                payload.planning_horizon_days,
                payload.service_level,
                store.demand_index,
                global_multiplier,
            )

        score_sum = sum(raw_scores.values())
        allocations: List[AllocationRecommendation] = []

        if score_sum == 0:
            for item in store.assortment:
                allocations.append(
                    AllocationRecommendation(
                        product_id=item.product_id,
                        size=item.size,
                        recommended_units=0,
                        score=0.0,
                    )
                )
            notes.append(
                f"Store {store.store_id} has no detected inventory gaps; all recommendations are 0."
            )
        else:
            remainder = store.capacity_units
            scored_items = sorted(
                store.assortment,
                key=lambda x: raw_scores[f"{x.product_id}::{x.size}"],
                reverse=True,
            )

            for i, item in enumerate(scored_items):
                key = f"{item.product_id}::{item.size}"
                share = raw_scores[key] / score_sum

                if i == len(scored_items) - 1:
                    units = remainder
                else:
                    units = min(remainder, max(0, math.floor(store.capacity_units * share)))

                remainder -= units
                allocations.append(
                    AllocationRecommendation(
                        product_id=item.product_id,
                        size=item.size,
                        recommended_units=units,
                        score=round(raw_scores[key], 3),
                    )
                )

        total_recommended_units = sum(x.recommended_units for x in allocations)
        store_recommendations.append(
            StoreRecommendation(
                store_id=store.store_id,
                total_recommended_units=total_recommended_units,
                allocations=allocations,
            )
        )

    return DistributionResponse(
        planning_horizon_days=payload.planning_horizon_days,
        service_level=payload.service_level,
        store_recommendations=store_recommendations,
        notes=notes,
    )
