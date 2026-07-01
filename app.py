"""
Australia Skilled Migration Pathway Dashboard
Built by Shanmuga Priya Gnanasekaran

Source data: Department of Home Affairs, "Australian Migration Statistics 2024-25"
statistical package (data.gov.au), Creative Commons Attribution 2.5 Australia.
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

st.set_page_config(
    page_title="Australia Skilled Migration Pathway Dashboard",
    page_icon="🧭",
    layout="wide",
)


@st.cache_data
def load_data():
    program = pd.read_csv(os.path.join(DATA_DIR, "1_migration_program_outcome_by_year.csv"))
    by_category = pd.read_csv(os.path.join(DATA_DIR, "2_migration_program_by_category.csv"))
    countries = pd.read_csv(os.path.join(DATA_DIR, "3_top_citizenship_countries_by_pathway.csv"))
    occupations = pd.read_csv(os.path.join(DATA_DIR, "4_top_occupations_by_pathway.csv"))
    temp_visas = pd.read_csv(os.path.join(DATA_DIR, "5_temporary_visas_by_category.csv"))
    return program, by_category, countries, occupations, temp_visas


program, by_category, countries, occupations, temp_visas = load_data()

PATHWAYS = ["Employer Sponsored", "Regional", "State/Territory Nominated"]
LATEST_YEAR = program["year"].iloc[-1]

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Australia Skilled Migration Pathway Dashboard")
st.markdown(
    """
Built by an international graduate on a Subclass 485 visa, for anyone trying to
make sense of where Australia's skilled migration program is actually heading.

This dashboard tracks the three main skilled visa pathways (Employer Sponsored,
Regional, and State/Territory Nominated), the occupations getting the most grants
under each, and where applicants are coming from, using official Department of
Home Affairs figures, not forum guesswork.
"""
)

st.caption(
    "Source: Department of Home Affairs, Australian Migration Statistics "
    f"(data.gov.au). Figures shown up to {LATEST_YEAR}. Data refreshes annually "
    "when Home Affairs publishes the new statistical package."
)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
latest = program[program["year"] == LATEST_YEAR].iloc[0]
prev_year_rows = program[program["year"] != LATEST_YEAR]
prev = prev_year_rows.iloc[-1] if len(prev_year_rows) else None

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total migration program", f"{int(latest['total']):,}", f"{LATEST_YEAR}")
col2.metric(
    "Skill stream places",
    f"{int(latest['skill_stream']):,}",
    f"{int(latest['skill_stream']) - int(prev['skill_stream']):+,}" if prev is not None else None,
)
skill_share = latest["skill_stream"] / latest["total"] * 100
col3.metric("Skill stream share of program", f"{skill_share:.0f}%")
family_share = latest["family_stream"] / latest["total"] * 100
col4.metric("Family stream share", f"{family_share:.0f}%")

st.divider()

# ---------------------------------------------------------------------------
# Program composition over time
# ---------------------------------------------------------------------------
st.subheader("Migration program composition, 1984-85 to today")
prog_long = program.melt(
    id_vars="year",
    value_vars=["skill_stream", "family_stream", "child_stream", "special_eligibility"],
    var_name="stream",
    value_name="count",
)
prog_long["stream"] = prog_long["stream"].str.replace("_", " ").str.title()
fig = px.area(
    prog_long,
    x="year",
    y="count",
    color="stream",
    title="Where migration places have gone, by stream",
)
fig.update_layout(xaxis_title="Program year", yaxis_title="Places granted", legend_title="Stream")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Pathway breakdown for latest year
# ---------------------------------------------------------------------------
st.subheader(f"Skilled visa pathways, {LATEST_YEAR}")
pathway_rows = by_category[
    (by_category["year"] == LATEST_YEAR) & (by_category["category"].isin(PATHWAYS + [
        "Skilled Independent", "Global Talent (Independent)", "Business Innovation & Investment",
        "Distinguished Talent", "National Innovation", "Skilled Regional",
    ]))
]
fig2 = px.bar(
    pathway_rows.sort_values("count", ascending=True),
    x="count",
    y="category",
    orientation="h",
    title=f"Places granted by skilled visa category, {LATEST_YEAR}",
)
fig2.update_layout(xaxis_title="Places granted", yaxis_title="")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Occupations explorer
# ---------------------------------------------------------------------------
st.subheader("Which occupations are actually getting through")
st.markdown(
    "Top 10 nominated occupations (by ANZSCO Unit Group) for primary applicants, "
    "by pathway. **ICT Business and Systems Analysts** and **Software and "
    "Applications Programmers** are highlighted since they're the closest match "
    "to Business Analyst and Salesforce Developer roles."
)

pathway_choice = st.selectbox("Choose a pathway", PATHWAYS)
occ_subset = occupations[occupations["pathway"] == pathway_choice]
highlight_occs = ["ICT Business and Systems Analysts", "Software and Applications Programmers"]

fig3 = px.line(
    occ_subset,
    x="year",
    y="count",
    color="occupation",
    title=f"Top nominated occupations over time, {pathway_choice}",
    markers=True,
)
for trace in fig3.data:
    if trace.name in highlight_occs:
        trace.line.width = 4
    else:
        trace.line.width = 1
        trace.opacity = 0.35
st.plotly_chart(fig3, use_container_width=True)

latest_occ = occ_subset[occ_subset["year"] == occ_subset["year"].max()].sort_values("count", ascending=False)
st.dataframe(latest_occ[["occupation", "count"]].reset_index(drop=True), use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Citizenship country explorer
# ---------------------------------------------------------------------------
st.subheader("Where applicants are coming from")
country_pathway = st.selectbox("Choose a pathway ", PATHWAYS, key="country_pathway")
country_year = st.select_slider(
    "Year",
    options=sorted(countries[countries["pathway"] == country_pathway]["year"].unique()),
    value=sorted(countries[countries["pathway"] == country_pathway]["year"].unique())[-1],
)
country_subset = countries[
    (countries["pathway"] == country_pathway) & (countries["year"] == country_year) & (countries["country"] != "Other")
].sort_values("count", ascending=False).head(15)

fig4 = px.bar(
    country_subset,
    x="count",
    y="country",
    orientation="h",
    title=f"Top citizenship countries, {country_pathway}, {country_year}",
)
fig4.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Places granted", yaxis_title="")
st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.markdown(
    """
**About this project**

I'm on a Subclass 485 (Temporary Graduate) visa myself, having completed a Master
of Business Analytics at Deakin University. I built this because the actual
official numbers on skilled migration are scattered across dense PDF reports,
while most of what circulates in international student communities is anecdotal.
This pulls the real Home Affairs figures into one place.

Data source: [Australian Migration Statistics, Department of Home Affairs](https://data.gov.au/data/dataset/australian-migration-statistics)
(Creative Commons Attribution 2.5 Australia).
"""
)
