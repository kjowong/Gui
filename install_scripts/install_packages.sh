#!/usr/bin/env bash
# Installs nginx on my web server for Ubuntu 14.04. Adjustment needed to Ubuntu 16.04

# Create and change into directory where Guiscore will be stored
mkdir /www
cd /www

# Clone the project from Github
sudo git clone https://github.com/kjowong/Gui.git

# Importing public key for MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6

# Create file list for MongoDB for Ubuntu 14.04
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

# Update any necessary packages
sudo apt-get -y update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Upgrade versions if needed
sudo apt-get -y upgrade

# Install nginx
sudo apt-get -y install nginx

# Start up nginx
sudo service nginx start

# Start Mongodb
sudo service mongod start

# Install all Python setup tools
sudo apt-get install -y python-setuptools

# Install Pip
sudo easy_install pip

# Install Pip3
sudo apt-get install -y python3-pip

# Install Python Dev
sudo apt-get install -y python-pip python-dev nginx

# Install Pymongo package
sudo pip install pymongo

# Install Pyzomato package for Zomato API
sudo pip3 install pyzomato

# Install Geopy module
sudo pip3 install geopy

# Setup to install Node version 8+
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

# Install NodeJs
sudo apt-get install -y nodejs

# Install NPM
sudo npm install npm -g

# Change directory to Gui
cd /www/Gui

# Install Babel
sudo npm install --save-dev babel-core babel-loader babel-plugin-transform-class-properties babel-preset-react css-loader style-loader url-loader file-loader webpack

# Install React packages
sudo npm install --save react react-dom bootstrap

# Install React version 16
sudo npm install --save react@^16.0.0 react-dom@^16.0.0

# Install Babel CLI
sudo npm install --save-dev babel-cli

# Build npm package
sudo npm run build

# Install Flask
sudo pip3 install Flask

# Updates all packages
sudo apt-get update

# Install Gunicorn and Python
sudo apt-get install -y python python-pip python-virtualenv nginx gunicorn

# Install flask-cors module
sudo pip3 install flask-cors --upgrade

# Install Supervisor
sudo apt-get install -y supervisor

# Replace root to point to where JS package is at, /www/Gui/dist
sudo sed -i 's/\/var\/www\/html;/\/www\/Gui\/dist;/' /etc/nginx/sites-enabled/default

# Add new rewrite rule for location /api for users to be able to access site from the front-end
sudo sed -i '/^\tlocation \/ {$/i\\tlocation \/api { \n\t\trewrite /api(.*) \/$1 break; \n\t\tproxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \n\t\tproxy_set_header Host \$http_host; \n\t\t\proxy_pass http://api; \n\t}\n' /etc/nginx/sites-enabled/default

# Adding upstream for api
sudo sed '/^server {$/i\upstream api {\n\t\server 0.0.0.0:5000;\n}\n' /etc/nginx/sites-enabled/default

# Executing gunicorn commond in supervisor to start flask project
sudo echo "[program:flask_project] command = /usr/local/bin/gunicorn search:app -b 0.0.0.0:5000 directory = /www/Gui/web_flask user = ubuntu" | sudo tee -a /etc/supervisor/conf.d/myproject.conf

# Saving change to supervisor conf
sudo supervisorctl reread

# Updating supervisor if needed
sudo supervisorctl update

# Starting flask project via supervisor
sudo supervisorctl start flask_project

# Restarting nginx
sudo service nginx restart
