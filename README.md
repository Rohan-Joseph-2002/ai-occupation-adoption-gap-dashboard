# AI Occupation Adoption Gap Dashboard

Portfolio analytics project for the occupation-level gap between `theoretical AI capability` and `observed AI use`.

## Purpose

This repository presents a narrow workforce-analytics question:

`Which occupations have high theoretical AI capability but low observed AI use?`

The repo is structured as a reproducible dashboard project:

- Python and Streamlit present the implemented interactive dashboard
- DuckDB SQL builds reproducible dashboard views from derived CSV inputs
- Python validation scripts compare SQL outputs against R-produced answer-key files from the upstream analysis repo
- A later Tableau version will use the same derived inputs and analytical views
- Generated screenshots, exports, and logs stay under `output/`, matching the analysis repo's reproducibility style

This repository does not rebuild the research pipeline. It consumes derived outputs from `ai-occupation-adoption-gap-analysis`.

## Key Definitions

- `Observed AI Use`: occupation-level observed work use of AI from Anthropic's public labor-market release.
- `Theoretical AI Capability`: occupation-level estimate of what current AI systems appear capable of supporting from the public GPTs-are-GPTs release.
- `Adoption Gap`: `theoretical_exposure - observed_exposure`.
- `Opportunity Role`: a high-capability occupation with a large adoption gap.
- `Major Group`: the broad two-digit SOC occupation family used for grouped dashboard summaries.
- `Modeling Sample`: complete-case occupation sample used for regression-linked dashboard views.

## Data Access Notes

Raw public inputs are not stored in this dashboard repository. They are acquired and processed by the upstream analysis repository:

`../ai-occupation-adoption-gap-analysis`

This dashboard repository stores only selected derived CSV extracts under `input/derived_data/`. Those files are copied from the upstream analysis repo's `output/derived_data/` directory.

Public source links:

- Anthropic observed-use file: [job_exposure.csv](https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main/labor_market_impacts/job_exposure.csv)
- Anthropic task-level companion file: [task_penetration.csv](https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main/labor_market_impacts/task_penetration.csv)
- OpenAI occupation-level capability file: [occ_level.csv](https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/occ_level.csv)
- OpenAI-linked BLS occupation controls: [occupations_onet_bls_matched.csv](https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/occupations_onet_bls_matched.csv)
- O*NET database text release: [db_30_2_text.zip](https://www.onetcenter.org/dl_files/database/db_30_2_text.zip)

## Implemented Data Sources

The current dashboard uses derived files built from:

- Anthropic `job_exposure.csv` for observed AI use
- OpenAI `gpts_are_gpts_occ_level.csv` for theoretical AI capability
- OpenAI `occupations_onet_bls_matched.csv` for employment and wage controls
- O*NET database text release for work activities, work context, and job zones

## Current Workflow

1. `scripts/setup_env.py`
   - Creates standard project directories
   - Copies `.env.example` to `.env` when needed
   - Optionally installs Python dependencies
2. `scripts/check_env.py`
   - Validates runtime settings, required input files, and Python package imports
3. `scripts/001_copy_analysis_outputs.py`
   - Copies selected derived outputs from the upstream analysis repo into `input/derived_data/`
4. `sql/00_load.sql`
   - Loads the master and modeling CSVs into DuckDB tables
5. `sql/01_kpis.sql` through `sql/05_top_observed_use.sql`
   - Reproduce KPI, group summary, opportunity ranking, gap-band, and observed-use views
6. `scripts/002_validate_sql.py`
   - Executes the SQL files and validates outputs against answer-key CSVs
7. `app/streamlit_app.py`
   - Runs the Streamlit dashboard entrypoint
8. `tableau/`
   - Holds notes for the Tableau companion dashboard that will use the same derived inputs

## Repository Structure

```text
ai-occupation-adoption-gap-dashboard/
├── README.md
├── LICENSE
├── NOTICE
├── pyproject.toml
├── .gitignore
├── .env.example
├── requirements.txt
├── app/
│   └── streamlit_app.py
├── docs/
│   └── images/
│       └── .gitkeep
├── input/
│   ├── derived_data/
│   └── reference/
│       └── .gitkeep
├── output/
│   ├── screenshots/
│   │   └── .gitkeep
│   ├── exports/
│   │   └── .gitkeep
│   └── logs/
│       └── .gitkeep
├── sql/
│   ├── 00_load.sql
│   ├── 01_kpis.sql
│   ├── 02_group_means.sql
│   ├── 03_opportunity_rank.sql
│   ├── 04_gap_bands.sql
│   └── 05_top_observed_use.sql
├── scripts/
│   ├── setup_env.py
│   ├── check_env.py
│   ├── 001_copy_analysis_outputs.py
│   ├── 002_validate_sql.py
│   └── run_app.py
├── notebooks/
│   └── validate_sql.ipynb
├── tests/
│   ├── test_data_schema.py
│   └── test_sql_outputs.py
├── tableau/
│   └── README.md
└── src/
    ├── dashboard/
    │   ├── charts.py
    │   ├── data.py
    │   ├── metrics.py
    │   └── sql.py
    └── project/
        ├── env.py
        ├── io.py
        ├── logger.py
        ├── paths.py
        ├── settings.py
        └── utils.py
```

## Tracking Policy

- `.env` is local-only and ignored; `.env.example` is tracked as the committed template.
- `input/derived_data/` contains selected dashboard-ready derived extracts copied from the analysis repo.
- `input/reference/` is scaffold-only unless later documentation assets are needed.
- `output/screenshots/`, `output/exports/`, and `output/logs/` keep only `.gitkeep` in git. Generated app captures, exports, and Markdown run logs stay local.
- `docs/images/` is reserved for curated screenshots that should appear in the README or portfolio write-up.
- Notebook checkpoint folders and Python caches are ignored.

## Setup

Create the local project directories, create `.env` from `.env.example` when needed, and install Python requirements:

```bash
python3 scripts/setup_env.py --create-venv --install-requirements
source .venv/bin/activate
```

If you do not want a repo-local virtual environment, run:

```bash
python3 scripts/setup_env.py --install-requirements
```

On first run, `scripts/setup_env.py` creates `.env` from `.env.example` if `.env` does not already exist. The default configuration expects the upstream analysis repo at:

```text
../ai-occupation-adoption-gap-analysis
```

Edit `.env` only when you need to override the upstream repo path, Streamlit host, Streamlit port, or dashboard thresholds:

```text
ANALYSIS_REPO_PATH=../ai-occupation-adoption-gap-analysis
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501
CAPABILITY_THRESHOLD=0.50
TOP_ROLE_COUNT=15
```

Validate the local environment:

```bash
python3 scripts/check_env.py
```

Run the unit tests:

```bash
python3 -m pytest
```

## Run The Streamlit App

1. Refresh the dashboard input extracts from the upstream analysis repo:

```bash
python3 scripts/001_copy_analysis_outputs.py
```

2. Validate the SQL layer against the copied answer-key CSVs:

```bash
python3 scripts/002_validate_sql.py
```

3. Launch the Streamlit dashboard:

```bash
python3 scripts/run_app.py
```

The launcher runs:

```bash
python3 -m streamlit run app/streamlit_app.py \
  --server.address localhost \
  --server.port 8501 \
  --server.headless true \
  --browser.gatherUsageStats false
```

Open the app at:

```text
http://localhost:8501
```

Leave the terminal running while using the dashboard. Stop the app with `Ctrl+C`.

If port `8501` is already in use, set a different port in `.env`:

```text
STREAMLIT_PORT=8502
```

Then rerun:

```bash
python3 scripts/run_app.py
```

## Current Inputs

Main dashboard input files:

- Derived file: `input/derived_data/occupation_analysis_dataset.csv`
- Derived file: `input/derived_data/modeling_dataset.csv`
- Derived file: `input/derived_data/major_group_summary.csv`
- Derived file: `input/derived_data/top_gap_occupations.csv`
- Derived file: `input/derived_data/low_gap_high_capability_occupations.csv`
- Derived file: `input/derived_data/top_observed_use_occupations.csv`
- Derived file: `input/derived_data/model_coefficients.csv`
- Derived file: `input/derived_data/variable_codebook.csv`
- Derived file: `input/derived_data/source_manifest.csv`

## Current SQL Outputs

SQL files map to dashboard views and keep the analytical logic inspectable:

| SQL file | Dashboard view | Query pattern |
| --- | --- | --- |
| `sql/00_load.sql` | DuckDB input tables | CSV loading into reusable tables |
| `sql/01_kpis.sql` | Headline KPI band | Aggregate summary metrics |
| `sql/02_group_means.sql` | Group-level exposure and gap comparison | Grouped means by SOC major group |
| `sql/03_opportunity_rank.sql` | High-capability, high-gap role ranking | CTE, ordered ranking, within-group window rank |
| `sql/04_gap_bands.sql` | Adoption-gap quartiles and labels | `NTILE` quartiles and `CASE` banding |
| `sql/05_top_observed_use.sql` | Occupations where AI use is already highest | Ordered top-N query with tie-breaking |

`scripts/002_validate_sql.py` validates SQL outputs against:

- `input/derived_data/major_group_summary.csv`
- `input/derived_data/top_gap_occupations.csv`
- `input/derived_data/top_observed_use_occupations.csv`

The gap-band query is validated against independently computed pandas output for quartile assignment, band labels, and adoption-gap values.

## Streamlit Dashboard

The Streamlit app turns the modeling dataset into an interactive occupation-level view.

Sidebar controls let the user filter by occupation group, minimum theoretical capability, and occupation title search. Those filters update the KPI cards, scatter plot, and ranked bar charts together.

The headline cards summarize the filtered occupations:

- Occupations analysed
- Mean observed AI use
- Mean theoretical AI capability
- Mean adoption gap

The scatter plot places theoretical AI capability on the x-axis and observed AI use on the y-axis. Each point is an occupation, colored by group. The diagonal parity line marks where observed use would equal theoretical capability; occupations below that line have more apparent unrealized AI headroom.

The lower charts provide two complementary rankings:

- `Highest-opportunity roles`: high-capability occupations with the largest adoption gaps.
- `Where AI is already embedded`: occupations with the highest observed AI use.

Together, the dashboard separates roles where AI use is already visible from roles where the measured capability-use gap is still large.

## Tableau Companion

A Tableau version is planned as a companion dashboard over the same derived inputs. The Tableau notes live in `tableau/` and will be updated with workbook details, screenshots, and a Tableau Public link once that dashboard is built.

## Current Results Snapshot

On the current public-data run:

- The master occupation dataset contains `709` occupations across `22` major groups
- The modeling/display sample contains `693` occupations
- Master-sample mean observed AI use is `0.082`
- Master-sample mean theoretical AI capability is `0.548`
- Master-sample mean adoption gap is `0.466`
- Modeling-sample mean observed AI use is `0.081`
- Modeling-sample mean theoretical AI capability is `0.547`
- Modeling-sample mean adoption gap is `0.466`
- Modeling-sample median adoption gap is `0.478`

The highest-gap occupations in the current run include:

- Cost Estimators
- Insurance Appraisers, Auto Damage
- Interior Designers
- Legal Secretaries and Administrative Assistants
- Pediatricians, General

The highest observed-use occupations include:

- Computer Programmers
- Customer Service Representatives
- Data Entry Keyers
- Market Research Analysts and Marketing Specialists
- Medical Transcriptionists

## Validation Status

Current validation commands pass:

```bash
python3 scripts/check_env.py
python3 scripts/002_validate_sql.py
python3 -m pytest
```

The SQL validation confirms:

- KPI query matches the modeling dataset
- Major-group means match `major_group_summary.csv`
- Opportunity ranking matches `top_gap_occupations.csv`
- Gap-band query matches expected quartiles, labels, and gap values
- Observed-use ranking matches `top_observed_use_occupations.csv`

## Limitations

- This is a descriptive dashboard, not a causal design.
- The dashboard depends on derived outputs from the upstream analysis repo.
- The occupation sample is limited to the overlap across the public Anthropic, OpenAI, O*NET, and BLS-linked files.
- Theoretical capability and observed use come from different public releases and should be interpreted as distinct constructs rather than interchangeable measures.
- The Streamlit app is implemented locally; curated screenshots, live deployment links, and the Tableau Public link will be added as the presentation layer is finalized.
