"""
Script to deploy database to Fly.io volume.
Can upload either the database file directly or CSV to load.
"""
import subprocess
import sys
import os
from pathlib import Path

APP_NAME = "hsd-ngo"
VOLUME_PATH = "/data"
DB_FILE = "hsd_ngo.db"
CSV_FILE = "data/tab-b-open-data-r020-hsdh-2014-2015.csv"

def run_command(cmd, check=True):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def upload_database():
    """Upload database file directly to Fly.io volume."""
    db_path = Path(DB_FILE)
    
    if not db_path.exists():
        print(f"Database file {DB_FILE} not found locally.")
        print("Attempting to load from CSV instead...")
        return False
    
    print(f"Found database file: {db_path} ({db_path.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"Uploading to Fly.io volume at {VOLUME_PATH}/{DB_FILE}...")
    
    # Use flyctl sftp to upload the file
    upload_cmd = f'flyctl ssh sftp shell -a {APP_NAME} -C "put {db_path} {VOLUME_PATH}/{DB_FILE}"'
    result = run_command(upload_cmd, check=False)
    
    if result.returncode == 0:
        print(f"✓ Successfully uploaded database to {VOLUME_PATH}/{DB_FILE}")
        return True
    else:
        print("Upload via SFTP failed, trying alternative method...")
        # Alternative: use flyctl ssh with cat
        print("Using alternative upload method...")
        with open(db_path, 'rb') as f:
            content = f.read()
        
        # Base64 encode and transfer
        import base64
        encoded = base64.b64encode(content).decode()
        
        # Split into chunks and upload
        chunk_size = 10000
        chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        
        print(f"Uploading in {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            cmd = f'flyctl ssh console -a {APP_NAME} -C "echo \'{chunk}\' | base64 -d >> {VOLUME_PATH}/{DB_FILE}.part"'
            run_command(cmd, check=False)
        
        # Combine parts
        run_command(f'flyctl ssh console -a {APP_NAME} -C "cat {VOLUME_PATH}/{DB_FILE}.part > {VOLUME_PATH}/{DB_FILE} && rm {VOLUME_PATH}/{DB_FILE}.part"', check=False)
        print("✓ Database uploaded (alternative method)")
        return True

def upload_csv_and_load():
    """Upload CSV file and load it into database on Fly.io."""
    csv_path = Path(CSV_FILE)
    
    if not csv_path.exists():
        print(f"CSV file {CSV_FILE} not found.")
        print("Please download it first using: python scripts/download_data.py")
        return False
    
    print(f"Found CSV file: {csv_path} ({csv_path.stat().st_size / 1024 / 1024:.2f} MB)")
    print("Uploading CSV and loading into database on Fly.io...")
    
    # Upload CSV to /tmp first
    print("Step 1: Uploading CSV file...")
    upload_cmd = f'flyctl ssh sftp shell -a {APP_NAME} -C "put {csv_path} /tmp/data.csv"'
    result = run_command(upload_cmd, check=False)
    
    if result.returncode != 0:
        print("SFTP upload failed, trying alternative...")
        # Alternative: use flyctl secrets or copy via console
        print("Please upload CSV manually or use: flyctl ssh console -a hsd-ngo")
        return False
    
    print("Step 2: Loading data into database...")
    # Run the load script on the machine
    load_script = f"""
import asyncio
import sys
sys.path.insert(0, '/app')
from scripts.load_data import load_csv_data
asyncio.run(load_csv_data('/tmp/data.csv'))
"""
    
    # Write script to temp file and execute
    run_command(
        f'flyctl ssh console -a {APP_NAME} -C "python3 -c \\"{load_script.replace(chr(10), "; ").replace('"', '\\"')}\\" "',
        check=False
    )
    
    # Better approach: copy load script and run it
    print("Copying load script...")
    run_command(f'flyctl ssh sftp shell -a {APP_NAME} -C "put scripts/load_data.py /tmp/load_data.py"', check=False)
    
    print("Running load script on Fly.io...")
    run_command(
        f'flyctl ssh console -a {APP_NAME} -C "cd /app && python3 /tmp/load_data.py /tmp/data.csv"',
        check=False
    )
    
    print("✓ Data loading initiated")
    return True

def main():
    """Main function."""
    print(f"Deploying data to Fly.io app: {APP_NAME}")
    print(f"Volume path: {VOLUME_PATH}")
    print("-" * 50)
    
    # Try to upload database file first
    if upload_database():
        print("\n✓ Database deployment complete!")
        print(f"App should now have data at: https://{APP_NAME}.fly.dev/")
        return
    
    # Fallback to CSV upload and load
    print("\nFalling back to CSV upload and load...")
    if upload_csv_and_load():
        print("\n✓ CSV uploaded and data loading initiated!")
        print("Check logs with: flyctl logs -a hsd-ngo")
        print(f"App should have data soon at: https://{APP_NAME}.fly.dev/")
    else:
        print("\n✗ Failed to deploy data")
        print("\nManual steps:")
        print(f"1. SSH into machine: flyctl ssh console -a {APP_NAME}")
        print(f"2. Upload database: flyctl ssh sftp shell -a {APP_NAME}")
        print(f"3. Or upload CSV and run: python scripts/load_data.py <csv_file>")

if __name__ == "__main__":
    main()

