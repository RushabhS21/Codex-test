from app.engine import recommend_distribution
from app.models import DistributionRequest, ProductSizeDemand, StoreProfile


def test_recommendations_respect_capacity():
    payload = DistributionRequest(
        planning_horizon_days=14,
        service_level=0.95,
        stores=[
            StoreProfile(
                store_id="S1",
                capacity_units=120,
                demand_index=1.1,
                assortment=[
                    ProductSizeDemand(
                        product_id="TEE-001",
                        size="M",
                        recent_sales_units=70,
                        on_hand_units=10,
                        seasonality_multiplier=1.2,
                        strategic_weight=1.0,
                    ),
                    ProductSizeDemand(
                        product_id="TEE-001",
                        size="L",
                        recent_sales_units=50,
                        on_hand_units=8,
                        seasonality_multiplier=1.0,
                        strategic_weight=1.1,
                    ),
                ],
            )
        ],
    )

    result = recommend_distribution(payload)
    rec = result.store_recommendations[0]

    assert rec.total_recommended_units == 120
    assert len(rec.allocations) == 2


def test_zero_gap_returns_zero_allocations():
    payload = DistributionRequest(
        stores=[
            StoreProfile(
                store_id="S2",
                capacity_units=80,
                assortment=[
                    ProductSizeDemand(
                        product_id="HOOD-010",
                        size="S",
                        recent_sales_units=0,
                        on_hand_units=100,
                    )
                ],
            )
        ]
    )

    result = recommend_distribution(payload)
    rec = result.store_recommendations[0]

    assert rec.total_recommended_units == 0
    assert rec.allocations[0].recommended_units == 0
