#!/usr/bin/env bash

# Updates system packages to ensure the package lists are up to date
sudo apt-get update

# Creating directories to store static files
# A set of directories is created to store static content for the web server
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")

# Checking whether nginx is installed, if not, installs it
# If Nginx is not already installed, it will be installed using apt
if ! command -v nginx >/dev/null 2>&1; then
    sudo apt install nginx -y
fi

# Iterate over the list to create directories
# Loops through the list of directories and creates them if they don't exist
for dir in "${directories[@]}"; do
    # Create directory if it doesn't exist
    sudo mkdir -p "$dir"
done

# Change ownership of the /data/ directory to ubuntu user and group (recursively)
# Ensures that the ubuntu user has the correct ownership of the directories
sudo chown -R ubuntu:ubuntu /data/

# Create a basic HTML page
# Generates a simple HTML page and stores it in the /data/web_static/releases/test/index.html file
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
# Removes any existing link or file at /data/web_static/current before creating a new symbolic link
if [ -L "$LINK_PATH" ] || [ -e "$LINK_PATH" ]; then
    rm -rf "$LINK_PATH"
fi

# Creates a symbolic link to the /data/web_static/releases/test/ directory
# Points /data/web_static/current to the newly created test release
sudo ln -s "$TARGET_PATH" "$LINK_PATH"

# Change ownership of the /data/ directory to ubuntu user and group (recursively)
# Ensures that the ubuntu user has ownership of the directories and files
sudo chown -R ubuntu:ubuntu /data/

# Create or update the Nginx configuration for serving static files
# Configures Nginx to serve static content from /data/web_static/current/ when the URL path /hbnb_static is requested
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
# Reloads and restarts Nginx to apply the updated configuration
sudo service nginx reload
sudo service nginx restart
