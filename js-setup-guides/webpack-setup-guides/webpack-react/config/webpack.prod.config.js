var merge = require("webpack-merge");

// Plugins
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
var OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
var UglifyJsPlugin = require("uglifyjs-webpack-plugin");
var Visualizer = require("webpack-visualizer-plugin");

// Configs
var commonConfig = require("./webpack.common.config");

// prod setup , optimizations
const prodConfiguration = () => {
  return merge([
    {
      optimization: {
        runtimeChunk: "single",
        splitChunks: {
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: "vendors",
              chunks: "all"
            }
          }
        },
        // splits common code into chunks
        // and generates a vendor.js file
        // deny access to source map or don't deploy source map
        // to production
        minimizer: [new UglifyJsPlugin({ sourceMap: true })]
      },
      plugins: [
        new MiniCssExtractPlugin({
          filename: "[name].[contenthash].css"
        }),
        new OptimizeCssAssetsPlugin(),
        new Visualizer({ filename: "./statistics.html" })
      ]
    },
    {
      mode: "production",
      devtool: "source-map"
    }
  ]);
};

module.exports = env => {
  return merge(commonConfig(env), prodConfiguration());
};
