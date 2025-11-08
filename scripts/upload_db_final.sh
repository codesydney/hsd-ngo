#!/bin/bash
# Final database upload script using API endpoint
# This handles large files better

APP_NAME="hsd-ngo"
DB_FILE="hsd_ngo.db"
ADMIN_TOKEN="${ADMIN_TOKEN:-hsd-ngo-upload-2024}"

if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found"
    exit 1
fi

echo "=========================================="
echo "Uploading database to Fly.io"
echo "=========================================="
echo "File: $DB_FILE ($(du -h $DB_FILE | cut -f1))"
echo "App: $APP_NAME"
echo ""

# Upload with increased timeout
echo "Uploading (this may take a few minutes for large files)..."
RESPONSE=$(curl -X POST "https://$APP_NAME.fly.dev/admin/upload-db?token=$ADMIN_TOKEN" \
  -F "file=@$DB_FILE" \
  --max-time 600 \
  -w "\nHTTP_CODE:%{http_code}" \
  2>&1)

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "=========================================="
    echo "✓ Database uploaded successfully!"
    echo "=========================================="
    echo "App URL: https://$APP_NAME.fly.dev/"
    echo ""
    echo "The app should now have all data loaded."
else
    echo "✗ Upload failed with HTTP $HTTP_CODE"
    echo "Response: $BODY"
    echo ""
    echo "Alternative: Try uploading via SSH when machine is running:"
    echo "  flyctl ssh console -a $APP_NAME"
    echo "  Then use SFTP or copy the file"
    exit 1
fi

