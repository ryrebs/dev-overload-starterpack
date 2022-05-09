const path = require("path");

const CopyWebpackPlugin = require("copy-webpack-plugin");
var HtmlWebpackPlugin = require("html-webpack-plugin");
const CleanWebpackPlugin = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const merge = require("webpack-merge");
const webpack = require("webpack");

const APP_DIR = path.resolve(__dirname, "../src");

module.exports = env => {
  const { PLATFORM, VERSION } = env;

  return merge([
    {
      // full ES2015+ environment
      entry: ["@babel/polyfill", APP_DIR], // support async/await
      output: {
        filename:
          PLATFORM === "production" ? "[name].[contenthash].js" : "[name].js",
        path: path.resolve(__dirname, "../dist")
      },
      module: {
        rules: [
          {
            test: /\.js$/, // include these patterns
            exclude: /node_modules/,
            use: {
              // helper plugin
              // locates interpres .babelrc
              loader: "babel-loader"
            }
          },
          {
            test: /\.(scss|css)$/,
            use: [
              // extract css before
              // optimizing in production mode
              // else use style loader to inject styles directly to DOM
              // without optimizations
              PLATFORM === "production"
                ? MiniCssExtractPlugin.loader
                : "style-loader",
              "css-loader",
              "postcss-loader",
              "sass-loader"
            ]
          }
        ]
      },
      plugins: [
        new webpack.HashedModuleIdsPlugin(),
        new CleanWebpackPlugin(),
        // support for html
        new HtmlWebpackPlugin({
          template: "./src/index.html",
          filename: "./index.html"
        }),
        // define global constants at runtime
        new webpack.DefinePlugin({
          "process.env.VERSION": JSON.stringify(VERSION),
          "process.env.PLATFORM": JSON.stringify(PLATFORM)
        }),
        // copy files to build folder
        // copy files from static to dist
        // run `npm run prebuild`
        new CopyWebpackPlugin([{ from: "src/static" }])
      ]
    }
  ]);
};
