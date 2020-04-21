
Step by step instructions:

Install Django & create requirements.txt

requirements.txt:
```
asgiref==3.2.4
Django==3.0.4
django-extensions==2.2.8
django-rest-framework==0.1.0
django-webpack-loader==0.7.0
djangorestframework==3.11.0
pytz==2019.3
six==1.14.0
sqlparse==0.3.1
```

Now : 

pip install -r requirements.txt

Add to following to settings.py

```
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['0.0.0.0']
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'), 
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets')
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
```
And add these too:
```
INSTALLED_APPS = [
    'hello_world',
    'webpack_loader',
    'rest_framework',
    'django_extensions',

```

Run npm init, should have these packages:
```
Update package.json
{
  "name": “<NAME”>,
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
        "start": "./node_modules/.bin/webpack --config webpack.config.js --watch"
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "babel": "^6.23.0",
    "babel-loader": "^8.0.6",
    "@babel/plugin-proposal-class-properties": "^7.8.3",
    "react": "^16.13.0",
    "webpack": "^4.42.0",
    "webpack-bundle-tracker": "^0.4.3",
    "webpack-cli": "^3.3.11",
    "@babel/core": "^7.8.4",
    "@babel/preset-env": "^7.8.4",
    "@babel/preset-react": "^7.8.3",
    "autoprefixer": "^9.7.3",
    "babel-core": "^6.26.3",
    "clean-webpack-plugin": "^3.0.0",
    "css-loader": "^3.4.2",
    "csv-loader": "^3.0.2",
    "file-loader": "^5.0.2",
    "html-webpack-plugin": "^3.2.0",
    "mini-css-extract-plugin": "^0.9.0",
    "node-sass": "^4.13.1",
    "papaparse": "^5.1.1",
    "postcss-loader": "^3.0.0",
    "sass-loader": "^8.0.2",
    "style-loader": "^1.1.2",
    "webpack-dev-server": "^3.10.3",
    "xml-loader": "^1.2.1"
  },
  "dependencies": {
    "prop-types": "^15.7.2",
    "react": "^16.12.0",
    "react-dom": "^16.12.0",
    "react-promise": "^3.0.2"
  }
}
```
Add a webpack.config.js file
```
const path = require('path');
var BundleTracker = require('webpack-bundle-tracker');
var webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: 'development',
    context: __dirname,
    entry: './assets/js/index', 
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: "[name]-[hash].js",
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.(scss)$/,
                use: [
                    {
                        loader: 'style-loader', // inject CSS to page
                    },
                    {
                        loader: 'css-loader', // translates CSS into CommonJS modules
                    },
                    {
                        loader: 'postcss-loader', // Run postcss actions
                        options: {
                            plugins: function () { // postcss plugins, can be exported to postcss.config.js
                                return [
                                    require('autoprefixer')
                                ];
                            }
                        }
                    },
                    {
                        loader: 'sass-loader' // compiles Sass to CSS
                    }
                ]
            },
        ]
    }
    ,
    resolve: {
        extensions: ['*', '.jsx', '.js'],
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new HtmlWebpackPlugin({ // plugin for inserting scripts into html
        }),
        new MiniCssExtractPlugin({ // plugin for controlling how compiled css will be outputted and named
            filename: "css/[name].css",
            chunkFilename: "css/[id].css"
        })
    ]
};
```

Add a 'hello world' react component to : assets/js/index.js:

```
import React, {useCallback, useRef} from "react";
import {render} from "react-dom";

const App = () => {
    return (<div>Hello World!</div>)
}
render(<App/>, document.getElementById('app'));
```

Add a template file
```
{% load static %}
{% load render_bundle from webpack_loader %}
<!DOCTYPE html>
<html lang="en">
 <body>
  <div id="app"></div>
  {% render_bundle 'main' %}
 </body>
</html>
```

Add .babelrc
```
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ],
  "plugins": [
    [
      "@babel/plugin-proposal-class-properties",
      {
        "loose": true
      }
    ]
  ]
}

```
---
Run web pack in watch mode
```
npm run start
``` 
 
Now kick off Runserver!
```
python manage.py runserver
```

The docker way
---
With docker: from within this folder:
``` 
docker-compose up
```

Both should run the app on: http://0.0.0.0:8000/

To view Django admin to see successfully uploaded data:

```
python manage.py createsuperuser
``` 
And then visit: http://0.0.0.0:8000/admin/
