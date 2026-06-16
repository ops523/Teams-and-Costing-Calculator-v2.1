import math
import pandas as pd


def build_scenario_comparison(
    base_teams,
    project_sqft,
    effective_daily_prod,
    travel_days_per_month,
    daily_team_cost,
    wall_rental_cost,
    material_cost,
    margin_pct
):

    scenarios = {
        "Lean": max(1, math.floor(base_teams * 0.8)),
        "Base": base_teams,
        "Aggressive": math.ceil(base_teams * 1.2)
    }

    rows = []

    for name, teams in scenarios.items():

        raw_days = (
            project_sqft /
            (
                effective_daily_prod *
                teams
            )
        )

        travel_days = (
            raw_days / 30
        ) * travel_days_per_month

        total_days = math.ceil(
            raw_days +
            travel_days
        )

        execution_cost = (
            daily_team_cost *
            total_days *
            teams
        )

        grand_total = (
            execution_cost +
            wall_rental_cost +
            material_cost
        )

        quote = (
            grand_total *
            (
                1 +
                margin_pct / 100
            )
        )

        rows.append({

            "Scenario": name,

            "Teams": teams,

            "Days Required":
                total_days,

            "Execution Cost":
                round(execution_cost),

            "Grand Total":
                round(grand_total),

            "Client Quote":
                round(quote),

            "Cost Per Sq Ft":
                round(
                    grand_total /
                    project_sqft,
                    2
                )

        })

    return pd.DataFrame(rows)
