#!/usr/bin/env bash
# Sets up webservers for deployment: (Run script on both servers)
# If not done, does the following:
#     installs Nginx; creates folders /data/, /data/web_static/,
#     /data/web_static/releases/, /data/web_static/shared,
#     /data/web_static/releases/test
#     /data/web_static/releases/test/index.html (with some content)
# Create symbolic link /data/web_static/current to data/web_static/releases/test
#     delete and recreate symbolic link each time script's ran
# Recursively assign ownership of /data/ folder to user and group 'ubuntu'
# Update the Nginx config to serve content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static)
#     restart Nginx
# curl localhost/hbnb_static/index.html should return sample text"

# Install Nginx if it's not already installed
if [ ! -x /usr/sbin/nginx ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create the required directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "Test Page" | sudo tee /data/web_static/releases/test/index.html

# Create the symbolic link and give ownership to ubuntu user and group
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /data/;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}" | sudo tee /etc/nginx/sites-available/default

# Start Nginx
sudo service nginx start
