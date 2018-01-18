<img src="https://i.imgur.com/nS2XeUj.png" width="50" height=auto />

# Gui Score: Web Application

## Description

The purpose of this web application is to provide users with a composite score for the top restaurants in the area, with the user providing their zip code and price range desired (optional). 

##### Currently for San Francisco Only

## Environment

* __OS:__ Ubuntu 14.04 LTS
* __frontend-language:__ Reactjs v16.0
* __backend-language:__ Python 3.4.3
* __web server:__ nginx/1.4.6
* __application server:__ Flask v0.12.2
* __web server gateway:__ gunicorn (version 19.7.1)
* __database:__ mongod v3.4.9
* __module_bunlder:__ webpack v3.8.1
* __react_compiler:__ babel v1.4.0

## Repository Breakdown
Summary of what repository contains:

|   **Item**    |  **Decription**                       |
|---------------|---------------------------------------|
| README.md   | Readme file           |
| package.json      | contains requirements and configuration for Reactjs v16 frontend         |
| .babelrc     | contains configuration for Babel            |
| **web_flask** | contain flask application to run mongodb database |
| **src**     | contains React scripts for for front-end |
| **dist** | contains **static** directory, bundle.js and index.html |
| **backend**     | contains backend modules in Python 3.4 |
| **install_scripts**     | contains script to install all dependencies and packages |

## Environment Setup
To setup the proper environment to deploy this application, run the following scripts:

## Data Flow
<img src="https://i.imgur.com/bTAqgZq.jpg" width="950" height=auto />

## Web Flask Files
`search.py` - contains all routes for web application:
* `/search/<zip_code>` -> returns all records with the provied zip code
* `/search/<zip_code>/<price>` -> returns all records with the provide price range under the provided zip code

## Src Files
`scripts.js` - Reactjs code that pulls from RESTful API created by Flask and displays the content dynamtically.

## Dist Files
Static Directory:
* CSS directory with stylesheets
* SCSS directory with scss stylesheets
* img directory with all images
* Js directory with bootstrap css functionality
* Vendor directory with bootstrap style dependencies

Other Files:
* `index/html` - HTML markup file
* `bundle.js` - script file that contains the bundle created with webpack

## Backend
* `database.py` - Functionn that takes in what was returned from `new_yelp.py` and creates a database
* `foursquare_remove_trucks.py` - Function that calls the FourSquare Api and returns a list of restaurants to pass to `match_list.py`(currently does not support food trucks with no location)
* `match_list.py` - Function that takes in both lists from FourSquare and Zomato to find a match, returns a list to pass to `new_yelp.py`
* `new_yelp.py` - Function that takes in the matched list, calls the yelp api to create a new composite score
* `price_coord_passer.py` - Function that takes in the arguments passed by the user (zip code and price) to pass to FourSquare API
* `query_listing.py` - Function that queries the database based on the user's inputs: Either just a zip code or if they included price
* `zomato_name_addr.py` - Function that calls the Zomato API and returns a list of restaurants to pass to `match_list.py`
* `zomato_tips.py` - Function that calls the Zomato API and grabs the tips provided in regards to the zip code

## Install_Scripts
* `install_packages.sh` - script to install all packages necessary

To use the script, run it like so
```
./install_packages.sh
```

## Testing
To be added

## Notes
This project is for educational purposes only

## To-Dos
User Authentication

## Known Bugs
There are no known bugs at the time.

## Authors

* Kimberly Wong, [kjowong](https://github.com/kjowong) | [@kjowong](https://twitter.com/kjowong) | [Email](kjowong@gmail.com)
* Spencer Cheng, [spencerhcheng](github.com/spencerhcheng) | [@spencerhcheng](https://twitter.com/spencerhcheng) | [Email](136@holbertonschool.com)


#### Feedback and contributors welcomed. Reach out to either authors.
