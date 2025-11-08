"""
Script to download the CSV data file.
"""
import urllib.request
from pathlib import Path

CSV_URL = "https://data.nsw.gov.au/data/dataset/0d915408-0026-44f7-a477-5f29ad7708ea/resource/0ad7196f-f7e8-45fd-957d-79394255b0ef/download/tab-b-open-data-r020-hsdh-2014-2015.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "tab-b-open-data-r020-hsdh-2014-2015.csv"

def download_csv():
    """Download the CSV file."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading CSV from {CSV_URL}...")
    print(f"Saving to {OUTPUT_FILE}...")
    
    urllib.request.urlretrieve(CSV_URL, OUTPUT_FILE)
    
    print(f"✓ Successfully downloaded {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"\nNext step: Run 'python scripts/load_data.py {OUTPUT_FILE}' to load the data")

if __name__ == "__main__":
    download_csv()

