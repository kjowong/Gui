#!/usr/bin/env bash
# Installs nginx on my web server

mkdir /www
cd /www
sudo git clone https://github.com/kjowong/Gui.git
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get -y update
sudo apt-get install -y mongodb-org
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo service nginx start
sudo service mongod start
sudo apt-get install -y python-setuptools
sudo easy_install pip
sudo apt-get install -y python3-pip
sudo apt-get install -y python-pip python-dev nginx
sudo pip install pymongo
sudo pip3 install pyzomato
sudo pip3 install geopy
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install npm -g
cd /www/Gui
npm install --save-dev babel-core babel-loader babel-plugin-transform-class-properties babel-preset-react css-loader style-loader url-loader file-loader webpack
npm install --save react react-dom bootstrap
npm install --save react@^16.0.0 react-dom@^16.0.0
npm install --save-dev babel-cli
npm run build
sudo pip3 install Flask
sudo apt-get update
sudo apt-get install -y python python-pip python-virtualenv nginx gunicorn
pip3 install flask-cors --upgrade
sudo apt-get install -y supervisor

sudo sed "s#root /usr/share/nginx/html;#root /www/Gui/dist;" /etc/nginx/sites-enabled/default
sudo sed -i "41i \ \tlocation /api { rewrite /api(.*) /$1  break; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header Host $http_host; proxy_pass http://api; }" /etc/nginx/sites-enabled/default
sudo sed -i "19i upstream api { /tserver 0.0.0.0:5000;
}" /etc/nginx/sites-enabled/default
sudo echo "[program:flask_project] command = gunicorn search:app -b localhost:5000 directory = /www/Gui/web_flask user = ubuntu" | sudo tee -a /etc/supervisor/conf.d/myproject.conf

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start flask_project
sudo service nginx restart
