# NSW Human Services Data Hub - NGO Providers Explorer

A FastAPI-based web application for exploring NGO providers and services across New South Wales, using data from the [Human Services Data Hub – NGO Providers 2014‑15](https://data.nsw.gov.au/data/dataset/human-services-data-hub-ngo-providers-2014-15).

## Features

- 🔍 Search providers by name, program, or location
- 🏥 Filter by Local Health District
- 🏛️ Filter by Commissioning Agency
- 📊 Browse paginated provider listings
- 📱 Mobile-first responsive design
- 🎨 Clean black and white Vibecamp design system

## Project Structure

```
hsd-ngo/
├── app/
│   ├── models/          # Database models
│   ├── controllers/     # Business logic
│   ├── routes/          # API routes
│   ├── templates/       # Jinja2 templates
│   ├── static/          # Static files (CSS, images)
│   └── database.py      # Database configuration
├── scripts/
│   └── load_data.py     # CSV data loader
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── fly.toml            # Fly.io deployment config
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Data

Download the CSV file from:
https://data.nsw.gov.au/data/dataset/0d915408-0026-44f7-a477-5f29ad7708ea/resource/0ad7196f-f7e8-45fd-957d-79394255b0ef/download/tab-b-open-data-r020-hsdh-2014-2015.csv

### 3. Load Data

```bash
python scripts/load_data.py tab-b-open-data-r020-hsdh-2014-2015.csv
```

### 4. Run Application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Web Routes
- `GET /` - Home page with search and stats
- `GET /providers` - Browse providers with filters and pagination

### API Routes
- `GET /api/v1/providers` - List providers (JSON)
- `GET /api/v1/providers/{id}` - Get provider by ID
- `GET /api/v1/filters` - Get available filter values

## Deployment

### Fly.io

1. Create volume:
```bash
fly volumes create hsd_ngo_data --size 10 --region lax
```

2. Deploy:
```bash
fly deploy
```

3. Load data (after deployment):

**Option A: Upload existing database file (fastest)**
```bash
# If you have hsd_ngo.db locally:
./scripts/deploy_db.sh
```

**Option B: Upload CSV and load on Fly.io**
```bash
# Upload CSV and load script
flyctl ssh sftp shell -a hsd-ngo
# Then upload CSV and run load_data.py
```

## Data Attribution

Data sourced from [Human Services Data Hub – NGO Providers 2014‑15](https://data.nsw.gov.au/data/dataset/human-services-data-hub-ngo-providers-2014-15), Government of New South Wales, licensed under [Creative Commons Attribution (CC BY 3.0 AU)](https://creativecommons.org/licenses/by/3.0/au/).

## License

This project is open source. The data is licensed under CC BY 3.0 AU.

---

A [Vibecamp](https://vibecamp.au/) Creation
