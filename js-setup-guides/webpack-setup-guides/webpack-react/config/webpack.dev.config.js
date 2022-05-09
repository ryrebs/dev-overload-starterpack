const merge = require("webpack-merge");
const common = require("./webpack.common.config");

// dev setup
const devConfiguration = () => {
  return merge([
    {
      mode: "development",
      devtool: "inline-source-map"
    }
  ]);
};

module.exports = env => merge(common(env), devConfiguration);
