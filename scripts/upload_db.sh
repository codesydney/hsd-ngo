#!/bin/bash
# Upload database using flyctl ssh console with cat
# This method works even when machine is stopped (auto-starts)

APP_NAME="hsd-ngo"
DB_FILE="hsd_ngo.db"
VOLUME_PATH="/data"

echo "Uploading $DB_FILE to Fly.io..."
echo "This will auto-start the machine if needed..."

# Use flyctl ssh console with cat to upload
cat "$DB_FILE" | flyctl ssh console -a $APP_NAME -C "cat > $VOLUME_PATH/$DB_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Upload complete!"
    echo "Verifying..."
    flyctl ssh console -a $APP_NAME -C "ls -lh $VOLUME_PATH/$DB_FILE && file $VOLUME_PATH/$DB_FILE"
    echo ""
    echo "✓ Database deployed successfully!"
    echo "App URL: https://$APP_NAME.fly.dev/"
else
    echo "✗ Upload failed"
    exit 1
fi

