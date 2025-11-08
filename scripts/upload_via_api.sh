#!/bin/bash
# Upload database via HTTP API endpoint
# This works even when machine is auto-stopped

APP_NAME="hsd-ngo"
DB_FILE="hsd_ngo.db"
ADMIN_TOKEN="${ADMIN_TOKEN:-change-me-in-production}"

if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found"
    exit 1
fi

echo "Uploading $DB_FILE via API..."
echo "This will wake up the machine automatically..."

# Upload via curl
curl -X POST "https://$APP_NAME.fly.dev/admin/upload-db?token=$ADMIN_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@$DB_FILE"

echo ""
echo ""
echo "✓ Upload complete!"
echo "Check the app at: https://$APP_NAME.fly.dev/"

