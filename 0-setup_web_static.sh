#!/usr/bin/bash
sudo apt-get update
# Creating directories to store static files
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")

# Checking whether nginx is installed, if not, installs it
if ! command -v nginx >/dev/null 2>&1; then
    sudo apt install nginx -y
fi

# Iterate over the list to create directories
for dir in "${directories[@]}"; do
    # Create directory if it doesn't exist
    sudo mkdir -p "$dir"
done
sudo chown -R ubuntu:ubuntu /data/
# Create a basic HTML page
echo "<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>

        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>

    </body>
</html>" > /data/web_static/releases/test/index.html


LINK_PATH="/data/web_static/current"
TARGET_PATH="/data/web_static/releases/test/"

# Check if the symbolic link or file exists
if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
    rm -rf "$LINK_PATH"
fi

sudo ln -s "$TARGET_PATH" "$LINK_PATH"

# Change ownership of the /data/ directory to ubuntu user and group (recursively)
sudo chown -R ubuntu:ubuntu /data/

# Create or update the Nginx configuration for serving static files
echo "
server {
    listen 80;
    server_name mydomainname.tech;

    # Other configurations ...

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
        try_files \$uri \$uri/ =404;
    }

    # Other configurations ...
}
" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx to apply the changes
sudo service nginx reload
sudo service nginx restart
