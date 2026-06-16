# app.py

import streamlit as st
import pandas as pd
from datetime import timedelta

from modules.calculations import calculate_project
from modules.scenarios import create_what_if_analysis
from modules.scheduling import create_schedule
from modules.exports import create_excel_export
from modules.scenario_comparison import build_scenario_comparison

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Wall Project Cost Calculator",
    page_icon="assets/logo.png",
    layout="wide"
)

# --------------------------------------------------
# LOGO
# --------------------------------------------------

try:
    logo_col1, logo_col2, logo_col3 = st.columns([1,2,1])

    with logo_col2:
        st.image(
            "assets/logo.png",
            width=100
        )
except:
    pass

st.title("Wall Project Cost Calculator V2.1")
st.caption(
    "Project Planning • Team Requirement • Cost Estimation"
)

# --------------------------------------------------
# MODE
# --------------------------------------------------

mode = st.radio(
    "Calculation Mode",
    [
        "Fixed Deadline Mode",
        "Fixed Team Mode"
    ],
    horizontal=True
)

# --------------------------------------------------
# PROJECT INPUTS
# --------------------------------------------------

st.header("Project Inputs")

c1, c2, c3 = st.columns(3)

with c1:

    project_sqft = st.number_input(
        "Project Total Sq Ft",
        min_value=1.0,
        value=50000.0
    )

    wall_size = st.number_input(
        "Per Wall Size (Sq Ft)",
        min_value=1.0,
        value=100.0
    )

with c2:

    avg_sqft_per_team = st.number_input(
        "Target Sq Ft Per Team Per Day",
        min_value=1.0,
        value=500.0
    )

    efficiency_pct = st.number_input(
        "Team Efficiency %",
        min_value=1.0,
        max_value=100.0,
        value=85.0
    )

with c3:

    travel_days_per_month = st.number_input(
        "Travel Days Per Month",
        min_value=0.0,
        value=5.0
    )

    risk_buffer_pct = st.number_input(
        "Risk Buffer %",
        min_value=0.0,
        value=0.0
    )

# --------------------------------------------------
# DATES / TEAMS
# --------------------------------------------------

st.header("Project Duration")

d1, d2 = st.columns(2)

with d1:

    start_date = st.date_input(
        "Project Start Date"
    )

with d2:

    if mode == "Fixed Deadline Mode":

        end_date = st.date_input(
            "Project End Date",
            value=start_date + timedelta(days=30)
        )

        project_days = (
            end_date - start_date
        ).days + 1

        team_count_input = None

    else:

        team_count_input = st.number_input(
            "Number of Teams",
            min_value=1,
            value=5
        )

        project_days = None

# --------------------------------------------------
# TEAM COSTS
# --------------------------------------------------

st.header("Daily Team Cost")

a1, a2, a3 = st.columns(3)

with a1:

    salary_cost = st.number_input(
        "Salary Cost",
        min_value=0.0,
        value=2000.0
    )

    food_cost = st.number_input(
        "Food Cost",
        min_value=0.0,
        value=500.0
    )

with a2:

    travel_cost = st.number_input(
        "Travel/Fuel Cost",
        min_value=0.0,
        value=400.0
    )

    stay_cost = st.number_input(
        "Stay Cost",
        min_value=0.0,
        value=1000.0
    )

with a3:

    bike_cost = st.number_input(
        "Bike Rental Cost",
        min_value=0.0,
        value=0.0
    )

    misc_cost = st.number_input(
        "Misc Cost",
        min_value=0.0,
        value=200.0
    )

daily_team_cost = (
    salary_cost +
    food_cost +
    travel_cost +
    stay_cost +
    bike_cost +
    misc_cost
)

# --------------------------------------------------
# WALL RENTAL
# --------------------------------------------------

wall_rental_per_wall = st.number_input(
    "Wall Rental Cost Per Wall",
    min_value=0.0,
    value=0.0
)

# --------------------------------------------------
# CLIENT MARGIN
# --------------------------------------------------

margin_pct = st.number_input(
    "Client Margin %",
    min_value=0.0,
    value=20.0
)

# --------------------------------------------------
# WHAT IF SETTINGS
# --------------------------------------------------

max_teams = st.number_input(
    "Maximum Teams for What-If Analysis",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

# --------------------------------------------------
# CALCULATE
# --------------------------------------------------

results = calculate_project(

    project_sqft=project_sqft,
    wall_size=wall_size,
    avg_sqft_per_team=avg_sqft_per_team,
    efficiency_pct=efficiency_pct,
    travel_days_per_month=travel_days_per_month,
    risk_buffer_pct=risk_buffer_pct,
    daily_team_cost=daily_team_cost,
    wall_rental_per_wall=wall_rental_per_wall,
    margin_pct=margin_pct,

    mode=(
        "deadline"
        if mode == "Fixed Deadline Mode"
        else "teams"
    ),

    project_days=project_days,
    team_count=team_count_input
)

# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

st.header("Project Summary")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Teams Required",
    results["team_count"]
)

k2.metric(
    "Project Days",
    results["project_days"]
)

k3.metric(
    "Utilization %",
    f"{results['utilization_pct']:.1f}%"
)

k4.metric(
    "Gum Required",
    f"{results['gum_qty']:.1f} Kg"
)

k5.metric(
    "Grand Total",
    f"₹{results['grand_total']:,.0f}"
)

# --------------------------------------------------
# TEAM DETAILS
# --------------------------------------------------

team_df = pd.DataFrame({

    "Metric": [

        "Team Count",
        "Project Days",
        "Productive Days",
        "Travel Days",
        "Utilization %",
        "Effective Sq Ft Per Day"

    ],

    "Value": [

        results["team_count"],
        results["project_days"],
        round(results["productive_days"],1),
        round(results["travel_days"],1),
        round(results["utilization_pct"],1),
        round(results["effective_daily_prod"],1)

    ]
})

st.header("A) Team Details")
st.dataframe(
    team_df,
    use_container_width=True
)

# --------------------------------------------------
# MATERIAL COSTING
# --------------------------------------------------

material_df = pd.DataFrame({

    "Item":[

        "Printing",
        "Media",
        "Packing & Logistics",
        "Gum"

    ],

    "Quantity":[

        f"{project_sqft:,.0f} Sq Ft",
        f"{project_sqft:,.0f} Sq Ft",
        f"{project_sqft:,.0f} Sq Ft",
        f"{results['gum_qty']:,.2f} Kg"

    ],

    "Rate":[

        "₹2.75 / Sq Ft",
        "₹5.50 / Sq Ft",
        "₹0.25 / Sq Ft",
        "₹156 / Kg"

    ],

    "Cost":[

        results["printing_cost"],
        results["media_cost"],
        results["packing_cost"],
        results["gum_cost"]

    ]

})

st.header("B) Material Costing")
st.dataframe(
    material_df,
    use_container_width=True
)

# --------------------------------------------------
# WHAT IF ANALYSIS
# --------------------------------------------------

what_if_df = create_what_if_analysis(

    max_teams=max_teams,

    project_sqft=project_sqft,

    effective_daily_prod=
        results["effective_daily_prod"],

    travel_days_per_month=
        travel_days_per_month,

    daily_team_cost=
        daily_team_cost
)

scenario_df = build_scenario_comparison(

    base_teams=
        results["team_count"],

    project_sqft=
        project_sqft,

    effective_daily_prod=
        results["effective_daily_prod"],

    travel_days_per_month=
        travel_days_per_month,

    daily_team_cost=
        daily_team_cost,

    wall_rental_cost=
        results["wall_rental_cost"],

    material_cost=
        results["material_cost"],

    margin_pct=
        margin_pct
)

st.header("C) What-If Analysis")
st.dataframe(
    what_if_df,
    use_container_width=True,
    height=500
)
st.header("D) Scenario Comparison")

st.dataframe(
    scenario_df,
    use_container_width=True
)

# --------------------------------------------------
# PROJECT SCHEDULE
# --------------------------------------------------

schedule_df = create_schedule(
    start_date,
    results["project_days"],
    results["travel_days"]
)

st.header("D) Project Schedule")
st.dataframe(
    schedule_df,
    use_container_width=True
)

# --------------------------------------------------
# COST SUMMARY
# --------------------------------------------------

summary_df = pd.DataFrame({

    "Cost Head":[

        "Execution Team Cost",
        "Wall Rental Cost",

        "Printing Cost",
        "Media Cost",
        "Packing & Logistics Cost",

        "Gum Quantity (Kg)",
        "Gum Cost",

        "Grand Total",

        "Cost Per Sq Ft Execution Only",

        "Cost Per Sq Ft All Inclusive",

        "Client Quote"

    ],

    "Amount":[

        results["execution_cost"],
        results["wall_rental_cost"],

        results["printing_cost"],
        results["media_cost"],
        results["packing_cost"],

        results["gum_qty"],
        results["gum_cost"],

        results["grand_total"],

        results[
            "execution_only_cost_per_sqft"
        ],

        results[
            "all_inclusive_cost_per_sqft"
        ],

        results["client_quote"]

    ]

})

st.header("E) Final Cost Summary")
st.dataframe(
    summary_df,
    use_container_width=True
)

# --------------------------------------------------
# EXCEL EXPORT
# --------------------------------------------------

inputs_df = pd.DataFrame({

    "Parameter":[

        "Project Sq Ft",
        "Wall Size",
        "Efficiency %",
        "Travel Days / Month",
        "Risk Buffer %",
        "Margin %"

    ],

    "Value":[

        project_sqft,
        wall_size,
        efficiency_pct,
        travel_days_per_month,
        risk_buffer_pct,
        margin_pct

    ]

})

excel_file = create_excel_export(

    inputs_df,
    team_df,
    material_df,
    what_if_df,
    scenario_df,
    schedule_df,
    summary_df
)

st.download_button(

    label="📥 Download Excel Report",

    data=excel_file,

    file_name=
        "wall_project_costing_v21.xlsx",

    mime=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
