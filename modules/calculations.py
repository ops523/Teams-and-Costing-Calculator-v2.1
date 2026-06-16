# modules/calculations.py

import math


PRINTING_RATE = 2.75
MEDIA_RATE = 5.50
PACKING_RATE = 0.25

GUM_RATE = 156
GUM_KG_PER_1000_SQFT = 5


def calculate_project(
    project_sqft,
    wall_size,
    avg_sqft_per_team,
    efficiency_pct,
    travel_days_per_month,
    risk_buffer_pct,
    daily_team_cost,
    wall_rental_per_wall,
    margin_pct,
    mode,
    project_days=None,
    team_count=None
):

    effective_daily_prod = (
        avg_sqft_per_team *
        efficiency_pct / 100
    )

    if mode == "deadline":

        travel_days = (
            project_days / 30
        ) * travel_days_per_month

        productive_days = (
            project_days - travel_days
        )

        productive_days *= (
            1 - risk_buffer_pct / 100
        )

        productive_days = max(
            productive_days,
            1
        )

        capacity_per_team = (
            effective_daily_prod *
            productive_days
        )

        team_count = math.ceil(
            project_sqft /
            capacity_per_team
        )

    else:

        raw_days = (
            project_sqft /
            (
                effective_daily_prod *
                team_count
            )
        )

        travel_days = (
            raw_days / 30
        ) * travel_days_per_month

        project_days = math.ceil(
            raw_days +
            travel_days
        )

        productive_days = (
            project_days -
            travel_days
        )

    utilization_pct = (
        productive_days /
        project_days
    ) * 100

    total_walls = math.ceil(
        project_sqft /
        wall_size
    )

    execution_cost = (
        daily_team_cost *
        project_days *
        team_count
    )

    wall_rental_cost = (
        total_walls *
        wall_rental_per_wall
    )

    printing_cost = (
        project_sqft *
        PRINTING_RATE
    )

    media_cost = (
        project_sqft *
        MEDIA_RATE
    )

    packing_cost = (
        project_sqft *
        PACKING_RATE
    )

    gum_qty = (
        project_sqft /
        1000
    ) * GUM_KG_PER_1000_SQFT

    gum_cost = (
        gum_qty *
        GUM_RATE
    )

    material_cost = (
        printing_cost +
        media_cost +
        packing_cost +
        gum_cost
    )

    grand_total = (
        execution_cost +
        wall_rental_cost +
        material_cost
    )

    client_quote = (
        grand_total *
        (1 + margin_pct / 100)
    )

    execution_only_cost_per_sqft = (
        execution_cost +
        wall_rental_cost
    ) / project_sqft

    all_inclusive_cost_per_sqft = (
        grand_total /
        project_sqft
    )

    return {

        "team_count": team_count,
        "project_days": project_days,
        "productive_days": productive_days,
        "travel_days": travel_days,
        "utilization_pct": utilization_pct,
        "effective_daily_prod": effective_daily_prod,

        "total_walls": total_walls,

        "execution_cost": execution_cost,
        "wall_rental_cost": wall_rental_cost,

        "printing_cost": printing_cost,
        "media_cost": media_cost,
        "packing_cost": packing_cost,

        "gum_qty": gum_qty,
        "gum_cost": gum_cost,

        "material_cost": material_cost,

        "grand_total": grand_total,

        "client_quote": client_quote,

        "execution_only_cost_per_sqft":
            execution_only_cost_per_sqft,

        "all_inclusive_cost_per_sqft":
            all_inclusive_cost_per_sqft
    }
