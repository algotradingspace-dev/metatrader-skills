---
name: forex-fundamentals-reference
description: 'Forex macroeconomic indicator reference for interpreting CPI, GDP, NFP, PMI, rate decisions, unemployment, trade balance, current account, housing, wages, confidence, and survey releases across USD, EUR, GBP, GER, JPY, CAD, AUD, NZD, CHF, and CNY. Use when: a user asks what an indicator means; wants trading interpretation for a calendar release; compares macro drivers across currencies; or asks about items like NFP, CPI, PMI, GDP, unemployment, trade balance, or rate decisions. Trigger on: NFP, CPI, GDP, PMI, unemployment, trade balance, current account, rate decision, inflation, payrolls, confidence, and queries like USD CPI, AUD employment, or what does this indicator mean.'
---

# Forex Fundamentals Reference

Use this skill when the user needs trading-oriented meaning for macro releases rather than platform mechanics or MQL5 APIs.

## Included Chunks

- `FX-USD` United States Macro Releases
- `FX-EUR` Eurozone Macro Releases
- `FX-GBP` United Kingdom Macro Releases
- `FX-GER` Germany as Eurozone Lead Economy
- `FX-JPY` Japan Macro Releases
- `FX-CAD` Canada Macro Releases
- `FX-AUD` Australia Macro Releases
- `FX-NZD` New Zealand Macro Releases
- `FX-CHF` Switzerland Macro Releases
- `FX-CNY` China Macro Releases

## When to Use

- Explaining what a calendar release means for a currency
- Interpreting inflation, growth, labor, trade, or confidence indicators
- Ranking which releases usually move a currency most
- Translating calendar labels like NFP, CPI, PMI, PPI, or current account into trading context
- Comparing macro drivers across major and commodity-linked FX pairs

---

### CHUNK FX-USD: United States Macro Releases

**Source family:** `fundamental-economic_indicators_usa*.md`

USD releases cover the broadest set of market-moving indicators: labor (`nonfarm_payrolls`, `jobless_claims`, `average_hourly_earnings`), inflation (`cpi`, `ppi`, `gdp_deflator`), growth (`gdp`, `personal_income`, `personal_spending`), activity (`ism`, regional Fed surveys, `retail_sales`), housing (`housing_starts`, `new_home_sales`, `existing_home_sales`, `building_permits`), trade/current-account flow, and Fed policy via `federal_funds_rate`. In practice, traders treat payrolls, CPI, and Fed-rate expectations as the highest-value USD catalysts. `PMI` and `ISM` readings above `50` imply expansion, while falling core inflation or softer labor data usually lowers Fed-tightening expectations.

**High-value releases:** `nonfarm_payrolls`, `cpi`, `federal_funds_rate`, `retail_sales`, `ism`, `gdp`

**References:** `fundamental-economic_indicators_usa.md`, `usa-atlanta_fed_index.md`, `usa-average_hourly_earnings.md`, `usa-average_workweek.md`, `usa-beige_book.md`, `usa-building_permits.md`, `usa-business_inventories.md`, `usa-capacity_utilization.md`, `usa-chicago_pmi.md`, `usa-construction_spending.md`, `usa-consumer_confidence.md`, `usa-consumer_credit.md`, `usa-core_consumer_price_index.md`, `usa-core_retail_sales.md`, `usa-current_account.md`, `usa-durable_goods_orders.md`, `usa-existing_home_sales.md`, `usa-export_prices.md`, `usa-factory_orders.md`, `usa-federal_budget.md`, `usa-federal_funds_rate.md`, `usa-gdp.md`, `usa-gdp_deflator.md`, `usa-help_wanted_index.md`, `usa-housing_starts.md`, `usa-import_prices.md`, `usa-initial_jobless_claims.md`, `usa-ism_index.md`, `usa-leading_indicators.md`, `usa-money_supply.md`, `usa-new_home_sales.md`, `usa-nonfarm_payrolls.md`, `usa-personal_income.md`, `usa-personal_spending.md`, `usa-philadelphia_fed_index.md`, `usa-producer_price_index.md`, `usa-productivity.md`, `usa-real_earnings.md`, `usa-redbook.md`, `usa-retail_sales.md`, `usa-trade_balance.md`, `usa-unit_labor_cost.md`, `usa-university_of_michigan_consumer_confidence.md`, `usa-unemployment_rate.md`, `usa-wholesale_inventories.md`

---

### CHUNK FX-EUR: Eurozone Macro Releases

**Source family:** `fundamental-economic_indicators_euro*.md`

EUR traders focus on inflation (`consumer_price_index`, `labor_cost_index`), growth (`gdp`), activity surveys (`pmi_manufacturing`, `pmi_services`, `purchasing_managers_index`), sentiment (`zew_survey`, `economic_sentiment`, `consumer_confidence_indicator`, `industrial_confidence`, `retail_trade_confidence`), money/credit (`money_supply_growth`), and ECB policy transmission (`refinancing_tender_rate`). The most tradable pattern is simple: inflation and survey momentum drive ECB expectations; `PMI` above `50` signals expansion and below `50` signals contraction. Balance-of-payments and current-account data matter more for medium-horizon structural flow analysis than intraday reactions.

**High-value releases:** `consumer_price_index`, `pmi_manufacturing`, `gdp`, `refinancing_tender_rate`, `zew_survey`

**References:** `fundamental-economic_indicators_euro.md`, `euro-balance_of_payments.md`, `euro-capital_and_financial_account.md`, `euro-consumer_confidence_indicator.md`, `euro-consumer_price_index.md`, `euro-current_account.md`, `euro-economic_sentiment.md`, `euro-gdp.md`, `euro-industrial_confidence.md`, `euro-labor_cost_index.md`, `euro-money_supply_growth.md`, `euro-pmi_manufacturing.md`, `euro-pmi_services.md`, `euro-purchasing_managers_index.md`, `euro-refinancing_tender_rate.md`, `euro-retail_trade_confidence.md`, `euro-unemployment_rate.md`, `euro-zew_survey.md`

---

### CHUNK FX-GBP: United Kingdom Macro Releases

**Source family:** `fundamental-economic_indicators_uk*.md`

GBP trades off BoE policy, growth, inflation, wages, and business surveys. The main clusters are GDP, inflation (`retail_price_index`, `producer_price_index_input`, `producer_price_index_output`), labor (`average_earning_growth`, `unemployment`, `unit_wage_costs`), surveys (`cbi_*`, `pmi`), money and credit (`m4`, `net_consumer_credit`), housing (`major_banks_mortgage_approvals`, `rightmove_hpi`), and external balance (`current_account`, `non_eu_trade_balance`, `balance_of_payments`). BoE minutes and repo-rate expectations often dominate near-term GBP pricing, while wages and PMI data help traders judge persistent inflation and growth.

**High-value releases:** `repo_rate`, `bank_of_england_minutes`, `average_earning_growth`, `gdp`, `pmi`

**References:** `fundamental-economic_indicators_uk.md`, `uk-average_earning_growth.md`, `uk-balance_of_payments.md`, `uk-bank_of_england_minutes.md`, `uk-cbi_distributive_trades.md`, `uk-cbi_industrial_orders.md`, `uk-cbi_industrial_trends.md`, `uk-current_account.md`, `uk-gdp.md`, `uk-industrial_output.md`, `uk-m4.md`, `uk-major_banks_mortgage_approvals.md`, `uk-manufacturing_output.md`, `uk-net_consumer_credit.md`, `uk-non-eu_trade_balance.md`, `uk-pmi.md`, `uk-producer_price_index_input.md`, `uk-producer_price_index_output.md`, `uk-psncr.md`, `uk-r_repo_rate.md`, `uk-retail_price_index.md`, `uk-retail_sales.md`, `uk-rightmove_hpi.md`, `uk-unemployment.md`, `uk-unit_wage_costs.md`

---

### CHUNK FX-GER: Germany as Eurozone Lead Economy

**Source family:** `fundamental-economic_indicators_germany*.md`

Germany matters because it often leads the broader euro-area cycle. The most watched releases are `ifo_survey`, `manufacturing_orders`, `industrial_production`, `gdp`, `trade_balance`, `current_account`, and `zew`. Traders use German business and factory data as an early read on Eurozone industrial momentum. Strong German export and factory numbers usually support EUR when they imply firmer regional growth and less pressure for ECB easing.

**High-value releases:** `ifo_survey`, `manufacturing_orders`, `industrial_production`, `trade_balance`, `zew`

**References:** `fundamental-economic_indicators_germany.md`, `germany-balance_of_trade.md`, `germany-current_account.md`, `germany-gdp.md`, `germany-ifo_survey.md`, `germany-import_prices.md`, `germany-industrial_production.md`, `germany-m3.md`, `germany-manufacturing_orders.md`, `germany-manufacturing_production.md`, `germany-producer_price_index.md`, `germany-retail_sales.md`, `germany-unemployment.md`, `germany-wholesale_index.md`, `germany-zew.md`

---

### CHUNK FX-JPY: Japan Macro Releases

**Source family:** `fundamental-economic_indicators_jp*.md`

JPY trading blends growth, inflation, trade, and survey interpretation with the market's broader risk and yield backdrop. Important releases include `gdp`, `cpi`, `trade_balance`, `tankan_survey`, `machinery_orders`, `industrial_production_index`, `retail_sales`, and `unemployment`. Japan data often matters less in isolation than US-rate or risk-tone shifts, but `Tankan`, GDP, and CPI are still key for judging BoJ policy drift and whether domestic demand is stabilizing.

**High-value releases:** `tankan_survey`, `gdp`, `cpi`, `trade_balance`, `machinery_orders`

**References:** `fundamental-economic_indicators_jp.md`, `jp-all-industry_activity_index.md`, `jp-balance_of_payments.md`, `jp-consumer_price_index.md`, `jp-corporate_goods_price_index.md`, `jp-gdp.md`, `jp-industrial_production_index.md`, `jp-leading_and_coincident_indices.md`, `jp-machinery_orders.md`, `jp-retail_sales.md`, `jp-tankan_survey.md`, `jp-tertiary_industry_index.md`, `jp-trade_balance.md`, `jp-unemployment_rate.md`, `jp-wholesale_price_index.md`

---

### CHUNK FX-CAD: Canada Macro Releases

**Source family:** `fundamental-economic_indicators_canada*.md`

CAD is highly sensitive to growth, labor, inflation, trade, and Bank of Canada policy, with added spillover from oil and US demand. `gdp`, employment, `cpi`, `ivey_pmi`, `trade_balance`, and rate decisions are the core releases. Housing and wholesale/manufacturing figures help explain domestic momentum, while `current_account` and trade speak to external demand. Strong GDP and employment usually reinforce BoC-tightening expectations and support CAD, especially when oil is firm.

**High-value releases:** `gdp`, `interest_rate_decision`, `cpi`, `payroll_employment`, `ivey_pmi`, `trade_balance`

**References:** `fundamental-economic_indicators_canada.md`, `canada-average_weekly_earnings.md`, `canada-balance_of_payments.md`, `canada-building_permits.md`, `canada-capacity_utilization.md`, `canada-consumer_price_index.md`, `canada-core_consumer_price_index.md`, `canada-current_account.md`, `canada-gdp.md`, `canada-housing_starts.md`, `canada-interest_rate_decision.md`, `canada-international_security.md`, `canada-ivey_pmi.md`, `canada-labor_productivity.md`, `canada-leading_indicators_index.md`, `canada-manufacturing_survey_shipments.md`, `canada-new_housing_price_index.md`, `canada-new_vehicle_sales.md`, `canada-overnight_rate_target.md`, `canada-payroll_employment.md`, `canada-producer_price_index.md`, `canada-raw_materials_price_index.md`, `canada-retail_sales.md`, `canada-retail_sales_ex_vehicles.md`, `canada-trade_balance.md`, `canada-unit_labor_cost.md`, `canada-unemployment_rate.md`, `canada-wholesale_inventories.md`, `canada-wholesale_sales.md`

---

### CHUNK FX-AUD: Australia Macro Releases

**Source family:** `fundamental-economic_indicators_australia*.md`

AUD reacts most to RBA policy, inflation, labor, trade, confidence, and China-linked growth proxies. The highest-value releases are `rba_interest_rate_decision`, `consumer_price_index`, `trade_balance`, `unemployment_rate`, `retail_sales`, and the Westpac and NAB confidence gauges. Because AUD is a commodity and carry-sensitive currency, traders also pay close attention to housing, credit, and business-survey data that can change RBA expectations.

**High-value releases:** `rba_interest_rate_decision`, `consumer_price_index`, `trade_balance`, `unemployment_rate`, `retail_sales`, `westpac_consumer_confidence`

**References:** `fundamental-economic_indicators_australia.md`, `aud-balance_of_payments.md`, `aud-building_approvals.md`, `aud-construction_work_done.md`, `aud-consumer_price_index.md`, `aud-export_price_index.md`, `aud-gdp.md`, `aud-home_loans.md`, `aud-house_price_index.md`, `aud-import_price_index.md`, `aud-labour_price_index.md`, `aud-nab_business_confidence.md`, `aud-new_motor_vehicle_sales.md`, `aud-private_sector_credit.md`, `aud-producer_price_index.md`, `aud-purchasing_managers_index.md`, `aud-r_retail_sales.md`, `aud-rba_interest_rate_decision.md`, `aud-service_pmi.md`, `aud-trade_balance.md`, `aud-unemployment_rate.md`, `aud-westpac_coincident_index.md`, `aud-westpac_consumer_confidence.md`, `aud-westpac_leading_index.md`

---

### CHUNK FX-NZD: New Zealand Macro Releases

**Source family:** `fundamental-economic_indicators_new_zealand*.md`

NZD follows the same commodity-cycle logic as AUD but with a smaller domestic economy and heavier agriculture influence. Traders focus on `rbnz_meeting_announcement`, `cpi`, `gdp`, `trade_balance`, `nbnz_business_confidence`, employment, and food-price inflation. Business-confidence and trade numbers often matter disproportionately because they give an early read on export demand and domestic activity in a small open economy.

**High-value releases:** `rbnz_meeting_announcement`, `cpi`, `gdp`, `trade_balance`, `nbnz_business_confidence`

**References:** `fundamental-economic_indicators_new_zealand.md`, `nzd-average_hourly_earnings.md`, `nzd-balance_of_payments.md`, `nzd-building_permits.md`, `nzd-consumer_price_index.md`, `nzd-food_price_index.md`, `nzd-gdp.md`, `nzd-labour_cost_index.md`, `nzd-manufacturing_activity.md`, `nzd-nbnz_business_confidence.md`, `nzd-producer_input_prices.md`, `nzd-producer_output_prices.md`, `nzd-purchasing_managers_index.md`, `nzd-rbnz_meeting_announcement.md`, `nzd-retail_sales.md`, `nzd-trade_balance.md`, `nzd-unemployment_rate.md`

---

### CHUNK FX-CHF: Switzerland Macro Releases

**Source family:** `fundamental-economic_indicators_switzerland*.md`

CHF is a safe-haven currency, so domestic data interacts with global risk sentiment and SNB policy. Key releases include `snb_3-month_libor_range`, `snb_policy`, `consumer_price_index`, `kof_leading_indicator`, `gdp`, `trade_balance`, and `unemployment_rate`. In practice, CHF traders use Swiss data mostly to refine policy expectations and assess whether the SNB has room to tolerate or resist currency strength.

**High-value releases:** `snb_policy`, `3-month_libor_range`, `consumer_price_index`, `kof_leading_indicator`, `trade_balance`

**References:** `fundamental-economic_indicators_switzerland.md`, `switzerland-3-month_libor_range.md`, `switzerland-consumer_price_index.md`, `switzerland-gdp.md`, `switzerland-industrial_production.md`, `switzerland-kof_leading_indicator.md`, `switzerland-producer_price_index.md`, `switzerland-purchasing_managers_index.md`, `switzerland-retail_sales.md`, `switzerland-snb_policy.md`, `switzerland-trade_balance.md`, `switzerland-unemployment_rate.md`, `switzerland-zew_survey.md`

---

### CHUNK FX-CNY: China Macro Releases

**Source family:** `fundamental-economic_indicators_china*.md`

China releases in this corpus are narrower, but they still matter because they influence commodity demand, regional growth, and global risk sentiment. The core releases are `gross_domestic_product`, `industrial_production`, `retail_sales`, `consumer_price_index`, and `producer_price_index`. Traders rarely use these as standalone CNY triggers in retail FX, but they are high-value context for AUD, NZD, CAD, and broader risk-on or risk-off positioning.

**High-value releases:** `gross_domestic_product`, `industrial_production`, `retail_sales`, `consumer_price_index`, `producer_price_index`

**References:** `fundamental-economic_indicators_china.md`, `china-customer_price_index.md`, `china-gross_domestic_product.md`, `china-industrial_production.md`, `china-producer_price_index.md`, `china-retail_sales.md`
