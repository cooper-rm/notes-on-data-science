# Notes on Data Science

Companion code for **[Notes on Data Science](https://medium.com/)** — a blog that breaks
down data science from the ground up, one concept at a time.

Every post has a notebook here. If you came from an article and want to run the code, 
poke at the numbers, or check my work, you're in the right place.

## Who's writing this

I'm Morgan — bachelor's in computer science, master's in data science.

Most explanations of this material stop at what a method computes. The harder and more
useful questions are when to reach for it, what it quietly assumes, and what it hides
when those assumptions break. That's what I write about.

Every post starts from first principles and ends somewhere you can actually use. The
notebooks are here so you never have to take my word for any of it — run them, change
the numbers, watch where the conclusions bend.

Found a mistake? Open an issue. I'd rather be corrected than wrong.

## Posts

| # | Post | Notebook |
|---|------|----------|
| 01 | Measures of Central Tendency | [notebooks/descriptive-statistics/01-univariate/01-measures-of-central-tendency.ipynb](notebooks/descriptive-statistics/01-univariate/01-measures-of-central-tendency.ipynb) |

## Running the code

```bash
git clone https://github.com/<your-username>/notes-on-data-science.git
cd notes-on-data-science
conda env create -f environment.yml
conda activate notes-on-ds
jupyter lab
```

Then run [notebooks/01-data-download/01-download.ipynb](notebooks/01-data-download/01-download.ipynb)
first — it pulls every dataset the other notebooks use into `data/raw/`. Nothing is
vendored, so the data is always fetched from the primary source.

## Data

| Dataset | Source | Used for |
|---|---|---|
| Fama–French daily factors | Dartmouth (Kenneth French Data Library) | Continuous distributions, correlation structure, shrinkage |
| BTC / ETH daily candles | Bitfinex public API | Heavy tails, volatility, tail dependence |
| HMDA mortgage applications | CFPB | Categorical and ordinal structure, contingency tables |

See [data/README.md](data/README.md) for columns, ranges, and the caveats each one
carries.

## Layout

```
notebooks/     one notebook per post, grouped by topic
src/           shared helpers the notebooks import
data/raw/      downloaded datasets (gitignored)
```

## License

Code is [MIT](LICENSE). Post text belongs to the Medium articles.
