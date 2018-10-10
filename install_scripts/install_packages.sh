#!/usr/bin/env bash

# Update package function
UPDATE_PACKAGES () {
    apt-get -y update
}

# Install package updates and Git
if (! UPDATE_PACKAGES)
then
    echo "Unable to update packages"
    exit 1
else
    if (! apt-get install -y git)
    then
        echo "Unable to install Git, check script"
        exit 1
    else
        echo "Sucessfully installed Git"
    fi
fi

# Display script usage
echo "This script will install all the necessary packages for the Gui Score app"
echo "To use, please pass in the following parameters: Directory to store your app, Ubuntu Version"
echo "Example: sudo ./install_script DIRECTORY UBUNTU_VERSION"

# Grab first argument with desired web directory
WEB_DIRECTORY="$1"
echo $WEB_DIRECTORY

UBUNTU_VER="$2"
echo $UBUNTU_VER

# Used default values for web directory and ubuntu version if nothing is passed in
if [ ! $WEB_DIRECTORY ] &&  [ ! $UBUNTU_VER ]
then
    echo "No web directory passed in, proceed to default values /www and 14.04? y/n"
    read input
    if [ $input = "y" ]
    then
       WEB_DIRECTORY="/www"
       echo "Directory: $WEB_DIRECTORY"
       UBUNTU_VER="14.04"
       echo "Ubuntu ver: $UBUNTU_VER"
    else
       echo "Run script again with parameters"
       exit 1
    fi
fi


# Create directory if the directory doesn't exist
if [ ! -d $WEB_DIRECTORY ]
then
     mkdir $WEB_DIRECTORY
     echo "Created $WEB_DIRECTORY"
     cd $WEB_DIRECTORY
     echo "Changed directory to $WEB_DIRECTORY"
else
     echo "$WEB_DIRECTORY already exists"
     cd $WEB_DIRECTORY
     echo "Changed directory to $WEB_DIRECTORY"
fi

# Gui directory for web application
#GUI="Gui"
#DATE=$(date +%F-%T)
NEW_DIR="Gui"

# Attempt to clone the Gui Repo and return message if fail or success
if (! git clone "https://github.com/kjowong/Gui.git" $NEW_DIR )
    then
        echo >&2 "Failed to clone from Github, check errors"
        exit 1
else
    echo "Successfully cloned Gui Repo into directory $WEB_DIRECTORY"
fi

# Grab the Mongodb GBG Key, echo if failed and exit
if (! apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4)
then
    echo "Unable to grab Mongo public GPG key"
    exit 1
else
    echo "Successfully installed Mongo public GPG key"
fi

# Default values for Ubuntu and Amd version associated
UBUNTU_RELEASE="trusty"
AMD_VER="arch=amd64"

echo $UBUNTU_RELEASE
echo $AMD_VER

# Mongo list for specific Ubuntu version function
MONGO_LIST_CMD () {
    echo "deb [ $AMD_VER ] https://repo.mongodb.org/apt/ubuntu $UBUNTU_RELEASE/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
}

# Creating Mongo List for specific Ubuntu Version
if [ $UBUNTU_VER == "14.04" ]
then
    echo "hi"
    MONGO_LIST_CMD
    echo "Grabbed Mongo list for $UBUNTU_VER $UBUNTU_RELEASE"
elif [ $UBUNTU_VER = "16.04" ]
then
    UBUNTU_RELEASE="xenial"
    AMD_VER="arch=amd64,arm64"
    MONGO_LIST_CMD
elif [ $UBUNTU_VER = "18.04" ]
then
    UBUNTU_RELEASE="bionic"
    MONGO_LIST_CMD
else
    echo "Version does not exists, please check and update script"
    exit 1
fi

echo "Created file list for Ubuntu version $UBUNTU_VER with $AMD_VER"

# Update packages
if (! UPDATE_PACKAGES)
then
    echo "Unable to update packages, check apt-get command"
    exit 1
else
    echo "Successfully updated packages"
fi

# Install Mongo, default is latest
echo "Install latest Mongo version? y/n"

read mongo_input


if [ $mongo_input = "y" ]
then
    apt-get install -y mongodb-org
    echo "Installed latest Mongo Version"
else
    echo "Provide Mongo version, example 4.0.2"
    read mongo_ver
    MONGO_VER_CMD () {
        apt-get install -y mongodb-org=$mongo_ver mongodb-org-server=$mongo_ver mongodb-org-shell=$mongo_ver mongodb-org-mongos=$mongo_ver mongodb-org-tools=$mongo_ver
    }
    if (! MONGO_VER_CMD)
    then
        echo "Error occured in Mongo installation, check script"
        exit 1
    else
        echo "Successfully installed " $mongo_ver
    fi
fi

# Function to upgrade any packages, if necessary
UPGRADE_PACKAGES () {
    apt-get -y upgrade
}

# Upgrade packages if needed
if (! UPGRADE_PACKAGES)
then
    echo "Unable to upgrade packages"
    exit 1
else
    echo "Successfully upgraded packages"
fi

# Install nginx
if (! apt-get -y install nginx)
then
    echo "Unable to install Nginx, check apt-get command"
    exit 1
else
    echo "Successfully installed Nginx"
fi

# Start Nginx server
if (! service nginx start)
then
    echo "Unable to start Nginx, check script"
    exit 1
else
    echo "Successfully started nginx"
fi

# Start mongodb database
if (! service mongod start)
then
    if (! service mongod stop)
    then
        echo "Check mongodb status" && service mongod status
        exit 1
    else
        service mongod start
        echo "Successfully started mongod"
    fi
else
    echo "Successfully started mongodb"
fi

# Install Python Tools
if (! apt-get install -y python-setuptools)
then
    echo "Unable to install Python tools, check apt-get command"
    exit 1
else
    echo "Successfully installed Python tools"
fi

# Install pip
if (! easy_install pip)
then
    echo "Unable to install Pip, check apt-get command"
    exit 1
else
    echo "Successfully installed Pip"
fi

# Install pip3
if (! apt-get install -y python3-pip)
then
    echo "Unable to install Python3 and pip3 tools, check apt-get command"
    exit 1
else
    echo "Successfully installed Python3 and pip3"
fi

# Install Python Dev
if (! apt-get install -y python-dev )
then
    echo "Unable to install python dev"
    exit 1
else
    echo "Successfully installed python dev"
fi


# Install Pymongo package
if (! pip install pymongo )
then
    echo "Unable to install pymongo"
    exit 1
else
    echo "Successfully installed pymongo"
fi

# Install Pyzomato package for Zomato API
if (! pip3 install pyzomato )
then
    echo "Unable to install Zomato API"
    exit 1
else
    echo "Successfully installed Zomato API"
fi

# Install Geopy module
if (! pip3 install geopy )
then
    echo "Unable to install Geopy Module"
    exit 1
else
    echo "Successfully installed Geopy Module"
fi

# Set Node Version to install - use default if no version is passed
NODE_VER=8
echo "Install Default Node Version 8? y/n"
read node_input

if [ $node_input == "y" ]
then
    curl -sL https://deb.nodesource.com/setup_$NODE_VER.x | sudo -E bash -
else
    echo "Input Node version to install"
    read node_ver_input
    if (! curl -sL https://deb.nodesource.com/setup_$node_ver_input.x | sudo -E bash -)
    then
        echo "Unable to install Node version $node_ver_input, check script"
        exit 1
    else
        echo "Successfully installed Node version $node_ver_input"
    fi
fi

# Install Node
if (! apt-get install -y nodejs)
then
    echo "Unable to install Node, check script"
    exit 1
else
    echo "Successfully installed Node"
fi

# Install npm globally
if (! npm install npm -g)
then
    echo "Unable to install npm, check script"
    exit 1
else
    echo "Successfully installed npm packages"
fi

# Move to the Gui directory
pushd $NEW_DIR

# Install Babel function
INSTALL_BABEL () {
    npm install --save-dev babel-core babel-loader babel-plugin-transform-class-properties babel-preset-react css-loader style-loader url-loader file-loader webpack
}

# Install Babel packages
if (! INSTALL_BABEL)
then
    echo "Unable to install Babel"
    exit 1
else
    echo "Successfully install Babel"
fi

# Install React and packages, option to use version 16 or latest
echo "Specify React version to install, example: 16.0.0 - compatible with up to version 16"
read react_ver
if (! npm install --save react@^$react_ver react-dom@^$react_ver bootstrap)
then
    echo "Unable to install React, React-Dom and Bootstrap at version $react_ver, proceed with version 16 or latest? 16/latest"
    read react_input
    if [ react_input == "16" ]
    then
        npm install --save react@^16.0.0 react-dom@^16.0.0 bootstrap
        echo "Installed React version 16"
    else
        npm install --save react react-dom bootstrap
        echo "Installed latest React version"
    fi
else
    echo "Successfully installed React, React-Dom and Bootstrap"
fi

# Install Babel CLI
if (! npm install --save-dev babel-cli)
then
    echo "Unable to install Babel CLI, check script"
    exit 1
else
    echo "Successfully installed Babel CLI"
fi

# Build npm package
if (! npm run build)
then
    echo "Unable to build package, check script"
    exit 1
else
    echo "Successfully built npm package"
fi

# Install Flask with pip3
if (! pip3 install Flask)
then
    echo "Unable to install Flask, check script"
    exit 1
else
    echo "Successfully installed Flask"
fi

# Update packages
UPDATE_PACKAGES

# Install Gunicorn and Python virtualenv
if (! apt-get install -y python-virtualenv gunicorn)
then
    echo "Unable to install Python Virtual Env and/or Gunicorn, check script"
    exit 1
else
    echo "Successfully installed Python Virtual Env and Gunicorn"
fi

# Install Flask-cors with pip3
if (! pip3 install flask-cors --upgrade )
then
    echo "Unable to install Flask-cors, check script"
    exit 1
else
    echo "Successfully installed Flask-cors"
fi

# Install supervisor
if (! apt-get install -y supervisor)
then
    echo "Unable to install supervisor, check script"
    exit 1
else
    echo "Successfully installed supervisor"
fi

# Commenting out first match of root destination that originally points to nginx html
if (! sed -i '0,/root/ s//#/' /etc/nginx/sites-enabled/default) 
then
    echo "Unable to comment out root line in Nginx default file"
    exit 1
else
    echo "Successfully commented out first match of root line in Nginx default file"
fi

# Replace commented out root line with root destination to point to Gui React package
if (! sed -i '0,/#.*;$/ s//root \'"$WEB_DIRECTORY"'\/'"$NEW_DIR"'\/dist;/' /etc/nginx/sites-enabled/default)
then
    echo "Unable to replace root to point to correct React package"
    exit 1
else
    echo "Successfully replaced root to point to React package"
fi

# Adding rewrite rule for location /api for users to access and interact the application from the front-end
LOCATION="api"
ADD_LOCATION_FUNC () {
    sed -i '/^\tlocation \/ {$/i\\tlocation \/'"$LOCATION"' { \n\t\trewrite /'"$LOCATION"'(.*) \/$1 break; \n\t\tproxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \n\t\tproxy_set_header Host \$http_host; \n\t\t\proxy_pass http://'"$LOCATION"'; \n\t}\n' /etc/nginx/sites-enabled/default
}
echo "Proceed with default rewrite rule location /api? y or specify new location, for example: api"
read location_input

if [ location_input == "y" ]
then
    if (! ADD_LOCATION_FUNC )
    then
        echo "Unable to add rewrite rule, check script"
        exit 1
    else
        echo "Successfully added rewrite rule"
    fi
else
    LOCATION=$location_input
    if (! ADD_LOCATION_FUNC )
    then
        echo "Unable to add rewrite rule, check script"
        exit 1
    else
        echo "Successfully added rewrite rule"
    fi
fi

# Adding upstream for api
if (! sed -i '/^server {$/i\upstream '"$LOCATION"' {\n\t\server 0.0.0.0:5000;\n}\n' /etc/nginx/sites-enabled/default)
then
    echo "Unable to add upstream for $LOCATION, check script"
    exit 1
else
    echo "Successfully added upstream for $LOCATION"
fi

GUNICORN_PATH="$(which gunicorn)" 
# Executes Gunicorn command in supervisor to start flask project
GUNICORN () {
    echo -e "[program:flask_project]\ncommand=$GUNICORN_PATH search:app -b 0.0.0.0:5000 ;\ndirectory=$WEB_DIRECTORY/$NEW_DIR/web_flask ;\nuser=ubuntu ;" | sudo tee -a /etc/supervisor/conf.d/myproject.conf
}

if (! GUNICORN)
then
    echo "Unable to execute gunicorn on supervisor, check script"
    exit 1
else
    echo "Successfully executed Gunicorn in supervisor"
fi

# Save changes to supervisor configuration
if (! supervisorctl reread)
then
    echo "Unable to save changes to supervisor conf file, check script"
    exit 1
else
    echo "Successfully saved changes to supervisor conf file"
fi

# Update supervisor if needed
if (! supervisorctl update)
then
    echo "Unable to update supervisor, check script"
    exit 1
else
    echo "Successfully updated supervisor"
fi

# Start the flask proejct with supervisor
if (! supervisorctl start flask_project)
then
    echo "Unable to start the flask project with supervisor, check script"
    exit 1
else
    echo "Successfully started the flask project with supervisor"
fi

# Restarting nginx
if (! service nginx restart)
then
    echo "Unable to restart nginx, check script"
    exit 1
else
    echo "Sucessfully started nginx"
fi

echo "Gui has been deployed"

# Pop out of current directory Gui
popd
