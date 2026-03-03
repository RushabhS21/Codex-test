# Store Product Distribution Planner

This is a starter application for deciding **which product sizes** and **how many units** should be distributed to each store.

It is built so you can plug in more factors later (for example: weather, local events, promotions, demographics, and regional trends).

## What it does now

- Accepts per-store assortment data (product, size, recent sales, inventory).
- Scores each product-size line using:
  - sales velocity,
  - inventory gap,
  - seasonality multiplier,
  - strategic priority multiplier,
  - store demand index,
  - optional custom multipliers.
- Splits each store's available capacity into recommended units by score.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run planner from JSON

```bash
python -m app.main sample_payload.json
```

## Example request (`sample_payload.json`)

```json
{
  "planning_horizon_days": 14,
  "service_level": 0.95,
  "custom_factors": {
    "promo_week": 1.15
  },
  "stores": [
    {
      "store_id": "NYC-001",
      "capacity_units": 180,
      "demand_index": 1.2,
      "assortment": [
        {
          "product_id": "DENIM-100",
          "size": "30",
          "recent_sales_units": 80,
          "on_hand_units": 18,
          "lead_time_days": 7,
          "seasonality_multiplier": 1.1,
          "strategic_weight": 1.2
        },
        {
          "product_id": "DENIM-100",
          "size": "32",
          "recent_sales_units": 65,
          "on_hand_units": 22,
          "lead_time_days": 7,
          "seasonality_multiplier": 1.1,
          "strategic_weight": 1.0
        }
      ]
    }
  ]
}
```

## Next factors you can add later

- Weather forecasts and climate profiles.
- Upcoming promotions/discount depth.
- Calendar effects (holidays, paydays, school season).
- Lost-sales / stockout history.
- Product substitution affinity.
- Margin-aware optimization.

## Run tests

```bash
pytest
```
