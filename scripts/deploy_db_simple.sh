#!/bin/bash
# Simple script to upload database file to Fly.io volume

APP_NAME="hsd-ngo"
DB_FILE="hsd_ngo.db"
VOLUME_PATH="/data"

if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file $DB_FILE not found"
    echo "Please ensure the database file exists in the current directory"
    exit 1
fi

echo "Uploading $DB_FILE to Fly.io volume..."
echo "File size: $(du -h $DB_FILE | cut -f1)"

# Use flyctl ssh sftp to upload
echo "Connecting to Fly.io machine..."
flyctl ssh sftp shell -a $APP_NAME <<EOF
put $DB_FILE $VOLUME_PATH/$DB_FILE
ls -lh $VOLUME_PATH/$DB_FILE
quit
EOF

if [ $? -eq 0 ]; then
    echo "✓ Successfully uploaded database to $VOLUME_PATH/$DB_FILE"
    echo "App should now have data at: https://$APP_NAME.fly.dev/"
else
    echo "✗ Upload failed. Trying alternative method..."
    
    # Alternative: use flyctl ssh console with base64
    echo "Using base64 transfer method..."
    flyctl ssh console -a $APP_NAME -C "cat > $VOLUME_PATH/$DB_FILE" < $DB_FILE
    
    if [ $? -eq 0 ]; then
        echo "✓ Database uploaded successfully"
        echo "App should now have data at: https://$APP_NAME.fly.dev/"
    else
        echo "✗ Upload failed. Please try manually:"
        echo "  flyctl ssh console -a $APP_NAME"
        echo "  Then upload via SFTP or copy the file"
    fi
fi

