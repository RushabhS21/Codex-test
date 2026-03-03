from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class ProductSizeDemand:
    product_id: str
    size: str
    recent_sales_units: int
    on_hand_units: int
    lead_time_days: int = 7
    seasonality_multiplier: float = 1.0
    strategic_weight: float = 1.0


@dataclass(slots=True)
class StoreProfile:
    store_id: str
    capacity_units: int
    demand_index: float = 1.0
    assortment: List[ProductSizeDemand] = field(default_factory=list)


@dataclass(slots=True)
class DistributionRequest:
    stores: List[StoreProfile]
    planning_horizon_days: int = 14
    service_level: float = 0.95
    custom_factors: Optional[Dict[str, float]] = None


@dataclass(slots=True)
class AllocationRecommendation:
    product_id: str
    size: str
    recommended_units: int
    score: float


@dataclass(slots=True)
class StoreRecommendation:
    store_id: str
    total_recommended_units: int
    allocations: List[AllocationRecommendation]


@dataclass(slots=True)
class DistributionResponse:
    planning_horizon_days: int
    service_level: float
    store_recommendations: List[StoreRecommendation]
    notes: List[str]
