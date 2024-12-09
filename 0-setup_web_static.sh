#!/usr/bin/bash

# Update package list and install Nginx if not already installed
if ! command -v nginx > /dev/null 2>&1; then
    echo "Installing Nginx..."
    sudo apt update
    sudo apt install nginx -y
else
    echo "Nginx is already installed."
fi

# Define the required directories
directories=(
    "/data/"
    "/data/web_static/"
    "/data/web_static/releases/"
    "/data/web_static/shared/"
    "/data/web_static/releases/test/"
)

# Create directories if they do not exist
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Creating directory: $dir"
        sudo mkdir -p "$dir"
    else
        echo "Directory already exists: $dir"
    fi
done

# Create a fake HTML file in the test directory
sudo tee /data/web_static/releases/test/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Welcome to web_static!</h1>
</body>
</html>
EOF

# Create or update the symbolic link
symlink="/data/web_static/current"
target="/data/web_static/releases/test/"

if [ -L "$symlink" ]; then
    echo "Removing existing symbolic link: $symlink"
    sudo rm "$symlink"
fi

echo "Creating new symbolic link: $symlink -> $target"
sudo ln -s "$target" "$symlink"

# Give ownership of /data/ to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
nginx_conf="/etc/nginx/sites-available/default"

if grep -q "/hbnb_static" "$nginx_conf"; then
    echo "Nginx configuration already updated for /hbnb_static."
else
    echo "Updating Nginx configuration for /hbnb_static..."
    sudo sed -i '/server_name _;/a \
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
        try_files $uri $uri/ =404;
    }' "$nginx_conf"
fi

# Restart Nginx to apply changes
echo "Restarting Nginx..."
sudo service nginx restart

echo "Setup complete!"
