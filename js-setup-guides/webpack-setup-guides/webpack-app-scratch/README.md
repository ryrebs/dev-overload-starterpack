### Setup react from the scratch with webpack

*Note:*   This setup is for learning purposes only. Not suitable for production for obvious reasons.

#### Table of Contents

A. [Setup](#Setup)

B. [Config](#Config)

C. [Setting up Babel](#Setting-up-Babel)

D. [Setting up React](#Setting-up-React)

E. [Install a web server](#Install-a-web-server)

#### Webpack

    A javascript module bundler. ( That's it... =D )

Usage:

1. Bundler

2. Can do transpilation by using babel-loaders

3. Watch changes

4. Run a development server

5. File splitting

6. Process css (Sass to css and others..)

7. Tree shaking  (removing dead code)

And others....

Terms:

1. *Loaders* are special modules webpack uses to 'load' other modules. (Process before bundling.) 

2. *Plugins* are used to have additional processing like bundling or minifying your files. (Process at the end of bundling process)

3. *Preset* is a set of plugins for Babel.

### Setup

1. Create src folder

    mkdir -p src

2. Handle project dependencies with

    npm init -y

3. Install webpack tools

    npm i webpack --save-dev

    npm i webpack-cli --save-dev

4. Add build scripts to package.json

5. Running `npm run build` needs to have  an entry point so create your entry point:

    `src/index.js`

    Webpack 4's entry point is by defaault src/index.js

6. After a succesful build it will create a folder and file:

    dist/main.js

### Config

1. Setup mode development and production on package.json

    "dev": "webpack --mode development",
    "build": "webpack --mode production"

2.  Running build spits a minified version of your app bundled in file.While running dev gives unbundled.

    Production benefits:

        1. minified
        
        2. scope hoisting
        
        3. tree shaking

        others...

3. Overriding script output by:

        "scripts": {
            "dev": "webpack --mode development ./foo/src/js/index.js --output ./foo/main.js",
            "build": "webpack --mode production ./foo/src/js/index.js --output ./foo/main.js"
        }
    

### Setting up Babel

    Babel - ES6 a javascript specifications, so when a browser runs a js program it must
    support a specific version of js. When writing modern js,some old browsers need to understand it.
    so Babel does the transformations.

Install packages:


    1. babel core

    2. babel loader
    
    3. babel preset env for compiling Javascript ES6 code down to ES5

`npm i @babel/core babel-loader @babel/preset-env --save-dev`

4. Add .babelrc

        {
            "presets": [
                "@babel/preset-env"
            ]
        }

5. Set up the babel-loader in a webpack.config.js
    
    
        module.exports = {
            module: {
            rules: [
                {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
                }
            ]
            }
        };

### Setting up React

1. Install react related packages as dev

    npm i react react-dom --save-dev

2. Install babel preset for react

    npm i @babel/preset-react --save-dev

3. Update .babelrc with

     "@babel/preset-react"
    
4. Add html plugins

    npm i html-webpack-plugin html-loader --save-dev

5. Build the app

    npm run build

6. Open dist/index.html - and you can see the react app.

7. Add css plugin and loader

    npm i mini-css-extract-plugin css-loader --save-dev

8. Update webpack.config.js with:

    Html and css's plugin and loader:

    const HtmlWebPackPlugin = require("html-webpack-plugin");
    const MiniCssExtractPlugin = require("mini-css-extract-plugin");


     {
            test: /\.html$/,
            use: [
              {
                loader: "html-loader",
                options: { minimize: true }
              }
            ]
          },
    {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"]
    }

     plugins: [
        new HtmlWebPackPlugin({
            template: "./src/index.html",
            filename: "./index.html"
        }),
        new MiniCssExtractPlugin({
            filename: "[name].css",
            chunkFilename: "[id].css"
          })
    ],

### Install a web server

1. npm i webpack-dev-server

2. Update webpack.config.js

        devServer: {
            contentBase: path.join(__dirname, 'index.html'),
            compress: true,
            port: 9000
        }

3. Update scripts

    "start": "webpack-dev-server"

4. Run server

    npm run start
---

Ref:

Guides taken from:

[How to set up React, webpack, and Babel 7 from scratch (2019)](https://www.valentinog.com/blog/react-webpack-babel/)

[Webpack wiki](https://github.com/webpack/docs/wiki/usage)

[React Handbook](https://medium.freecodecamp.org/the-react-handbook-b71c27b0a795)