# Research Design

## Thesis
Portfolios formed with long-short pairs of securities experience significant idiosyncratic returns because investors overreact to short-term news, causing stock prices to deviate from their fair values.

## Construction

After the market close of time t-1, where t is the first of the month.

1. Filter US equity market data on share code (10, 11) and exchange code (1, 2, 3).
2. Generate 48 momentum return features from (t-n to t-2).
3. Generate 78 firm characteristic features using COMPUSTAT data.
4. Normalize all features using cross-sectional means and standard deviations.
5. Apply principal component analysis to reduce the dimensionality of features.
6. Assign each stock to a cluster via K-Means Clustering, DB-SCAN, or another clustering algorithm.
7. Within each cluster:
   - Pair the stock with the highest one-month momentum with the stock with the lowest one-month momentum.
   - Repeat for all stocks in the cluster.
8. Construct an equal-weighted long (lower pair) short (higher pair) portfolio with pairs whose one-month momentum spread is greater than the cross-sectional deviation.

Execute trades at the market open of time t.

## Assumptions
1. **Momentum return features** are statistically powerful at predicting future returns.
2. **Firm characteristics** are statistically powerful at predicting future returns.
3. **Stock pairings**: The pairs identified based on one-month momentum spreads will experience a predictable reversal or continuation in returns, allowing for profitable long-short positioning.
4. **Investor Overreaction**: Market participants will continue to overreact to short-term news, causing price deviations that can be exploited.
5. **Sector Neutrality**: By clustering stocks, sector-specific risks are assumed to be minimized, allowing idiosyncratic performance to drive returns.
6. **Cross-sectional deviations** in momentum are meaningful predictors of mean reversion or momentum continuation within clusters.
7. **Liquidity Assumption**: There is sufficient liquidity for both long and short trades to be executed without significant slippage.
8. **Low Transaction Costs**: Transaction costs do not significantly impact the net returns of the portfolio.

## Experiments

To validate each assumption in the trading strategy, we propose the following statistical tests:

1. **Momentum return features**: Run linear regressions of next-month returns on past-month momentum features to verify predictive power and statistical significance.

2. **Firm characteristics**: Use a multiple regression analysis of next-month returns on firm characteristics to assess the predictive strength of these variables.

3. **Stock pairings**: Perform a paired t-test on returns within identified pairs to check for significant differences, validating that high-momentum and low-momentum stocks perform distinctly.

4. **Investor Overreaction**: Run linear regression on short good news and long bad news strategy returns surrounding earnings releases, and other news events to test the mean reverting nature of investor overreaction.

5. **Sector neutrality**: Conduct an ANOVA test on returns across clusters to ensure that intra-cluster returns are more similar than inter-cluster returns, confirming that clustering reduces sector-specific risks.

6. **Cross-sectional deviations in momentum**: Test the significance of cross-sectional standard deviations in momentum features by regressing portfolio returns on this measure to validate it as a predictive factor.

## Further Questions:
- What is the relationship between returns for extreme news and mild news?
- Do stocks revert following increases in volume relative to the market?

## Misc.

### Types of news:
- Earnings surprise
- Product releases
- News events
- Competitor news