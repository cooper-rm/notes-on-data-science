# data/

Three datasets, chosen so that between them they cover the distributional shapes the
posts need: well-behaved continuous, heavy-tailed, and categorical/ordinal.

Nothing here is committed. `data/raw/` is gitignored and rebuilt by
[../notebooks/01-data-download/01-download.ipynb](../notebooks/01-data-download/01-download.ipynb),
which pulls every file from its primary source.

---

## Fetching and loading

All I/O lives in `src/`, so notebooks stay thin — one call to download, one to load, no
parsing logic in the notebook itself.

**[`src/config.py`](../src/config.py)** — every URL, path, and query parameter. Change
scope here, never in a notebook.

| Name | Purpose |
|---|---|
| `RAW_DIR` | Where downloads land — `data/raw/` |
| `FRENCH_URL`, `BITFINEX_URL`, `HMDA_URL` | Source endpoints |
| `CRYPTO_SYMBOLS`, `CRYPTO_LIMIT` | Which symbols, how many candles |
| `HMDA_PARAMS` | Year, states, and action filter |
| `HEADERS` | User-Agent — the CFPB endpoint 403s `python-requests` |
| `FRENCH_FILE`, `CRYPTO_FILE`, `HMDA_FILE` | Output paths |

**[`src/data.py`](../src/data.py)** — paired download and load functions.

| Function | Does |
|---|---|
| `download_french()` | Unzips the Dartmouth archive, strips the preamble and copyright footer, parses dates, writes tidy CSV |
| `download_crypto()` | One request per symbol, reorders Bitfinex's `[ts, open, close, high, low, vol]` to conventional OHLC, concatenates long |
| `download_hmda()` | Follows the CFPB redirect to the generated extract, writes bytes as-is |
| `load_french()`, `load_crypto()` | Read back with `date` parsed |
| `load_hmda(usecols=None)` | Read back; pass `usecols` to avoid loading all 99 columns |

Downloads normalize on the way in, so the loaders are trivial and every notebook sees
the same shape. Each `download_*` is idempotent — safe to re-run, overwrites in place.

```python
from src import data

data.download_french()
french = data.load_french()
```

---

## `french_factors_daily.csv`

**Fama–French three-factor daily returns**, from the
[Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
at Dartmouth. Built on CRSP and maintained by Eugene Fama and Kenneth French — the file
the academic finance literature is written against.

**26,274 rows · 1926-07-01 → 2026-06-30** · `src.data.load_french()`

| Column | Meaning |
|---|---|
| `date` | Trading day |
| `mkt_rf` | Market return in excess of the risk-free rate |
| `smb` | Small Minus Big — the size factor |
| `hml` | High Minus Low — the value factor |
| `rf` | Risk-free rate, one-month Treasury bill |

**Values are percent, not decimals.** `0.09` means 0.09%. Divide by 100 before
compounding or annualizing — this fails silently rather than raising, and it is the most
common error made with this file.

Used for the continuous side: spread, shape, correlation matrices, Ledoit–Wolf shrinkage
(developed for exactly this problem), and partial correlation.

*Caveats.* Not independent observations — volatility clusters, so a standard deviation
over the full history summarizes a moving target. And a century spans the Depression,
Bretton Woods, and modern electronic markets; statistics computed across the whole span
average over market structures with little to do with each other.

---

## `crypto_daily.csv`

**Daily OHLCV candles for BTC/USD and ETH/USD** from the
[Bitfinex public API](https://docs.bitfinex.com/reference/rest-public-candles).
No authentication required.

**8,686 rows, long format — one row per symbol per day** · `src.data.load_crypto()`

| Symbol | Range | Days |
|---|---|---|
| `BTCUSD` | 2013-03-31 → present | 4,880 |
| `ETHUSD` | 2016-03-09 → present | 3,806 |

Columns: `date`, `symbol`, `open`, `high`, `low`, `close`, `volume`. Bitfinex returns
candles as `[timestamp, open, close, high, low, volume]` — close precedes high in the
raw payload; `src.data` reorders to conventional OHLC on download.

Used where fat tails are the point: kurtosis, extreme value theory, volatility
clustering, and **tail dependence via copulas**. The second symbol is the reason this
dataset has two — a single price history has no dependence structure to model. The
question is not how volatile each asset is alone, but whether they crash *together* more
often than their marginals imply.

*Caveats.* One exchange, not a consolidated tape. The joint history starts in 2016, not
2013, so ~3 years of BTC drops out of any paired computation. Daily candles hide
intraday extremes, which understates tail severity.

---

## `hmda_2023_ri.csv`

**Home Mortgage Disclosure Act loan applications**, published by the
[CFPB](https://ffiec.cfpb.gov/data-browser/). Lenders above a size threshold must report
every application they receive, making this a regulatory census rather than a sample.

**28,844 rows · 99 columns** — Rhode Island, 2023, originated or denied only ·
`src.data.load_hmda()`

| Column | Type | Role |
|---|---|---|
| `action_taken` | Binary | `1` originated, `3` denied — the outcome |
| `derived_race`, `derived_ethnicity`, `derived_sex` | Nominal | Applicant characteristics |
| `loan_purpose`, `lien_status`, `occupancy_type` | Nominal | Loan characteristics |
| `debt_to_income_ratio` | **Ordinal** | Ordered bands (`<20%`, `20%-<30%`, …) |
| `applicant_age` | **Ordinal** | Ordered bands (`35-44`, …) |
| `loan_amount`, `income`, `property_value` | Continuous | Hard right-skewed |

The ordinal columns are bands, **not numbers**. `astype(float)` either fails or silently
destroys the ordering that makes them useful.

Used for everything categorical: contingency tables, odds ratios, relative risk, lift,
phi, Cramér's V, and polychoric correlation. Also tetrachoric — denial is a threshold
applied to unobserved continuous creditworthiness, so the estimator's assumption matches
the actual data-generating process rather than being a convenient fiction.

*Caveats.* Applications, not people — anyone discouraged from applying never appears, so
denial rates describe the applicant pool, not the population. **No credit scores** in the
public file, so the most predictive underwriting variable is a non-random omitted
variable. Race and ethnicity are `derived_` fields with non-random missingness.

*Scope.* Defaults in [`../src/config.py`](../src/config.py). Rhode Island keeps this at
11 MB; size scales with state population and a full national year runs to several GB, so
add states individually rather than dropping the filter. The endpoint 403s the default
`python-requests` User-Agent, which is why `config.HEADERS` sets one.
