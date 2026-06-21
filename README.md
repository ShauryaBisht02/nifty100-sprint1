# Nifty 100 Financial Intelligence Platform

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/.env.template .env
```

## Usage
```bash
make load       # Run ETL pipeline
make ratios     # Compute KPIs
make test       # Run test suite
make report     # Generate PDF reports
make dashboard  # Start Streamlit app
make api        # Start FastAPI server
make clean      # Clean cache files
```

## Project Structure
- `data/raw/` — Core Excel datasets (READ ONLY)
- `data/supporting/` — Supplementary datasets
- `src/etl/` — ETL pipeline
- `src/analytics/` — KPI computation
- `src/dashboard/` — Streamlit app
- `src/api/` — FastAPI server
- `reports/` — Generated PDFs and charts
- `tests/` — pytest test suite
