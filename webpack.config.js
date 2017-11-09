const webpack = require('webpack');
const path = require('path');

const config = {
  entry: path.resolve('src/scripts.js'),
  output: {
    path: path.resolve('dist'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
	  test: /.js$/,
	  exclude: path.resolve(__dirname, 'node_modules/'),
      	  loader: 'babel-loader'
      },
      {
      	  test: /\.css$/,
	  loader: 'style-loader!css-loader'
      },
      {
	  test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
        loader: 'url-loader',
	  options: {
	  	limit: 10000
	  }
      }
    ]
  },
  externals: {
    jquery: 'jQuery'
  }
};

module.exports = config;
