# 🏥 Global Life Expectancy vs Healthcare Spending (1960-Present)

**Source**: World Bank Open Data API - https://data.worldbank.org
**API Key Required**: No - the World Bank API is free and open.
**Last Updated**: 2026-04-24

## World Bank Indicator Codes

| Indicator Code | Description | File |
|----------------|-------------|------|
| SP.DYN.LE00.IN | Life expectancy at birth, total (years) | life_expectancy.csv |
| SP.DYN.LE00.FE.IN | Life expectancy at birth, female (years) | life_expectancy.csv |
| SP.DYN.LE00.MA.IN | Life expectancy at birth, male (years) | life_expectancy.csv |
| SH.XPD.CHEX.GD.ZS | Current health expenditure (% of GDP) | health_spending.csv |
| SH.XPD.CHEX.PC.CD | Current health expenditure per capita (USD) | health_spending.csv |
| SH.MED.BEDS.ZS | Hospital beds per 1,000 people | hospital_capacity.csv |
| SH.MED.PHYS.ZS | Physicians per 1,000 people | hospital_capacity.csv |
| SH.MED.NUMW.P3 | Nurses and midwifery personnel per 1,000 | hospital_capacity.csv |
| SP.DYN.IMRT.IN | Infant mortality rate (per 1,000 live births) | infant_mortality.csv |
| SH.DYN.MORT | Under-5 mortality rate (per 1,000 live births) | infant_mortality.csv |
| SH.STA.MMRT | Maternal mortality ratio (per 100,000 live births) | infant_mortality.csv |
| NY.GDP.PCAP.CD | GDP per capita, current USD | context.csv |
| SP.POP.TOTL | Population, total | context.csv |

## Output Files

| File | Description |
|------|-------------|
| life_expectancy.csv | LE at birth (total/female/male), gender gap, YoY change — all countries |
| health_spending.csv | Health spend % GDP + per capita USD, spend tier, YoY change |
| hospital_capacity.csv | Beds/physicians/nurses per 1,000, total health workers, capacity tier |
| infant_mortality.csv | Infant, under-5, maternal mortality + YoY improvement + burden tier |
| context.csv | GDP per capita, population, log GDP, income tier |
| country_metadata.csv | ISO codes, World Bank region, income group, lat/lon |
| health_panel.csv | All indicators merged on country_code + year (primary analysis file) |
| ml_features.csv | Lag 1-5, rolling 3/5-year, dummies, regression + classification targets |

## Derived Columns (health_panel.csv)

| Column | Formula | Interpretation |
|--------|---------|----------------|
| life_expectancy_gender_gap | female_LE - male_LE | Positive = women live longer |
| le_per_gdp_point | life_expectancy_total / health_spend_pct_gdp | Life-years per % of GDP spent on health |
| le_per_1k_spend | life_expectancy_total / (health_spend_per_capita_usd / 1000) | Life-years per $1,000 per capita health spend |
| le_spend_residual | Actual LE - OLS predicted LE from log(spend) | Positive = outperforms spending level |
| efficiency_score | le_per_1k_spend normalised 0-100 within each year | 100 = most efficient country that year |

## ML Targets (ml_features.csv)

| Column | Type | Description |
|--------|------|-------------|
| target_le_next_year | float | Life expectancy next year (regression) |
| target_le_change_next_year | float | Change in life expectancy next year |
| target_le_improves | int | 1 if LE improves next year, else 0 (classification) |
| target_le_5yr | float | Life expectancy 5 years ahead (long-horizon regression) |
| target_le_gain_5yr | float | LE gain over next 5 years |
| target_im_next_year | float | Infant mortality next year (regression) |
| target_im_improvement | float | Infant mortality reduction next year (positive = improving) |

## Key Historical Health Events

| Period | Event | Impact on Data |
|--------|-------|----------------|
| 1960s–1980s | Green Revolution + basic healthcare expansion | Rapid LE gains in low-income countries |
| 1981–2000 | HIV/AIDS epidemic in Sub-Saharan Africa | LE reversed by 5-15 years in hardest-hit nations |
| 1990s | Post-Soviet health system collapse | Sharp LE drops in Eastern Europe/Central Asia |
| 2000s | PEPFAR, Global Fund, MDGs | LE rebounds; infant mortality falls sharply in Africa |
| 2020–2022 | COVID-19 pandemic | Global LE dropped ~1.8 years (largest decline since WWII) |

## Source & License
World Bank Open Data — https://data.worldbank.org
API endpoint: https://api.worldbank.org/v2/
License: CC BY 4.0 — https://datacatalog.worldbank.org/public-licenses