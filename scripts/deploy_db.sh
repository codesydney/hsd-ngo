#!/bin/bash
# Deploy database to Fly.io volume
# Usage: ./scripts/deploy_db.sh

APP_NAME="hsd-ngo"
DB_FILE="hsd_ngo.db"
VOLUME_PATH="/data"

echo "=========================================="
echo "Fly.io Database Deployment Script"
echo "=========================================="
echo "App: $APP_NAME"
echo "Database: $DB_FILE"
echo "Volume: $VOLUME_PATH"
echo ""

# Check if database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "❌ Error: Database file '$DB_FILE' not found in current directory"
    echo ""
    echo "Options:"
    echo "1. Generate database locally first:"
    echo "   python scripts/download_data.py"
    echo "   python scripts/load_data.py data/tab-b-open-data-r020-hsdh-2014-2015.csv"
    echo ""
    echo "2. Or upload CSV and load on Fly.io:"
    echo "   See scripts/deploy_csv.sh"
    exit 1
fi

DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
echo "✓ Found database file: $DB_FILE ($DB_SIZE)"
echo ""

# Check if flyctl is available
if ! command -v flyctl &> /dev/null; then
    echo "❌ Error: flyctl not found"
    echo "Install from: https://fly.io/docs/getting-started/installing-flyctl/"
    exit 1
fi

# Check if logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "❌ Error: Not logged into Fly.io"
    echo "Run: flyctl auth login"
    exit 1
fi

echo "Uploading database to Fly.io volume..."
echo "This may take a few minutes for large files..."
echo ""

# Method 1: Try SFTP upload
echo "Method 1: Attempting SFTP upload..."
flyctl ssh sftp shell -a $APP_NAME <<SFTP_EOF
put $DB_FILE $VOLUME_PATH/$DB_FILE
ls -lh $VOLUME_PATH/$DB_FILE
quit
SFTP_EOF

SFTP_SUCCESS=$?

if [ $SFTP_SUCCESS -eq 0 ]; then
    echo ""
    echo "✓ Successfully uploaded database via SFTP"
    echo ""
    echo "Verifying upload..."
    flyctl ssh console -a $APP_NAME -C "ls -lh $VOLUME_PATH/$DB_FILE && file $VOLUME_PATH/$DB_FILE"
    
    echo ""
    echo "=========================================="
    echo "✓ Deployment Complete!"
    echo "=========================================="
    echo "Database is now available at: $VOLUME_PATH/$DB_FILE"
    echo "App URL: https://$APP_NAME.fly.dev/"
    echo ""
    echo "You may need to restart the app:"
    echo "  flyctl apps restart $APP_NAME"
    exit 0
fi

# Method 2: Alternative using flyctl ssh console with base64
echo ""
echo "SFTP upload failed, trying alternative method..."
echo "Method 2: Using base64 transfer (this may take longer)..."

# Split file into chunks and upload
CHUNK_SIZE=1000000  # 1MB chunks
TEMP_DIR=$(mktemp -d)
SPLIT_FILE="$TEMP_DIR/db_chunk"

echo "Splitting database into chunks..."
split -b $CHUNK_SIZE "$DB_FILE" "$SPLIT_FILE"

echo "Uploading chunks..."
CHUNK_COUNT=0
for chunk in "$SPLIT_FILE"*; do
    CHUNK_COUNT=$((CHUNK_COUNT + 1))
    echo "  Uploading chunk $CHUNK_COUNT..."
    base64 "$chunk" | flyctl ssh console -a $APP_NAME -C "base64 -d >> $VOLUME_PATH/$DB_FILE.part$CHUNK_COUNT" 2>/dev/null
done

echo "Combining chunks on Fly.io..."
flyctl ssh console -a $APP_NAME -C "cat $VOLUME_PATH/$DB_FILE.part* > $VOLUME_PATH/$DB_FILE && rm -f $VOLUME_PATH/$DB_FILE.part* && ls -lh $VOLUME_PATH/$DB_FILE"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo "Database is now available at: $VOLUME_PATH/$DB_FILE"
echo "App URL: https://$APP_NAME.fly.dev/"
echo ""
echo "You may need to restart the app:"
echo "  flyctl apps restart $APP_NAME"

