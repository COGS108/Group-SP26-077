"""Helpers for building the analysis panel and reusable EDA plots."""

import pandas as pd


def filter_life_outliers(life_df, n_std=1.5):
    """Drop extreme year-over-year life expectancy changes (data checkpoint rule)."""
    std = life_df["le_total_yoy_change"].std()
    return life_df[life_df["le_total_yoy_change"].abs() < n_std * std].copy()


def assign_dev_tier(gdp_per_capita):
    """Development tier from project hypothesis (USD, current prices)."""
    if pd.isna(gdp_per_capita):
        return pd.NA
    if gdp_per_capita >= 45_000:
        return "developed"
    if gdp_per_capita < 15_000:
        return "developing"
    return "transitional"


def build_analysis_panel(
    life_path="data/00-raw/life_expectancy.csv",
    health_path="data/00-raw/health_spending.csv",
    context_path="data/kaggle-dataset/context.csv",
    metadata_path="data/kaggle-dataset/country_metadata.csv",
):
    """Merge wrangled life expectancy, health spending, GDP, and geography."""
    life = pd.read_csv(life_path)
    health = pd.read_csv(health_path)
    context = pd.read_csv(context_path)
    metadata = pd.read_csv(metadata_path)

    drop_cols = ["region", "income_group", "iso2_code"]
    life = filter_life_outliers(life).drop(columns=drop_cols, errors="ignore")
    health = health.drop(columns=drop_cols, errors="ignore")

    # Health spending is only available from 2000 onward; keep all life years.
    panel = life.merge(
        health,
        on=["country_code", "country_name", "year"],
        how="left",
    )
    panel = panel.merge(
        context[
            [
                "country_code",
                "year",
                "gdp_per_capita_usd",
                "log_gdp_per_capita",
                "gdp_income_tier",
                "population_total",
            ]
        ],
        on=["country_code", "year"],
        how="left",
    )

    geo = (
        metadata[["country_name", "latitude", "longitude", "region", "income_group"]]
        .dropna(subset=["country_name", "latitude"])
        .drop_duplicates("country_name")
        .rename(columns={"region": "wb_region", "income_group": "wb_income_group"})
    )
    panel = panel.merge(geo, on="country_name", how="left")
    panel["dev_tier"] = panel["gdp_per_capita_usd"].map(assign_dev_tier)
    panel["abs_latitude"] = panel["latitude"].abs()
    panel["decade"] = (panel["year"] // 10) * 10
    return panel


def tier_order():
    return ["developing", "transitional", "developed"]
