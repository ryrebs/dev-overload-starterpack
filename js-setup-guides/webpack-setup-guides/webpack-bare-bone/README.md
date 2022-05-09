### Setting up webpack

A. Setup

1. Initialize project folder

   npm init -y

2. Setup package.json - allow webpack to handle dependency

3. Install dependency

   npm i lodash

4. Bundle initialize files , install webpack and/or webpack-cli if necessary and package.json

   npx webpack

   or

   npx webpack --config webpack.config.js

   or

   npm run build

5. dist folder will be the production build

B. Asset management

1. Install

   npm install --save-dev style-loader css-loader

2. Adjust webpack config accordingly

3. Allow loading styles like this

   import './style.css'

4. Allow loading other files

   npm install --save-dev file-loader

5. Setup file loader

6. Setup data loading

   npm install --save-dev csv-loader xml-loader

C. Output Management

7. Setup output management to make sure updated files are still reference
   correctly and change package.json accordingly

   npm install --save-dev html-webpack-plugin

8. Clean up dist - delete before creating new files

   npm install --save-dev clean-webpack-plugin

D. Development

9. Using source map to refer original files after bundling,
   useful in debugging error in bundled file

   devtool: 'inline-source-map',

10. Using watch for watching changes ang re compile

    "watch": "webpack --watch",

11. Using webpack dev server install and change webpack.config
    * Bundles are in memory

    devServer: {
        contentBase: './dist'
    },

E. Hot Module Replacement

12. Updating module at runtime using Hot Module Replacement,
    automatically updates loaded depedency via runtime

12. HMR styles

    npm install --save-dev style-loader css-loader

F. Tree Shaking

13. Tree shaking - removing dead code - (ES2015 module's import and export syntax)

    A dead code is something  exported but not used, since using import { a } from "file"
    does take b if b is export in "file" thus takes up space. See reference guide below.

G. Production Setup

14. Setup Splitting

    npm install --save-dev webpack-merge

15. Separate prod and dev webpack config

16. Enable source (not the inline one)

H. Production mode cli options

1. --optimize-minimize flag will include the TerserPlugin behind the scenes. (Default in production mode)

2. --define process.env.NODE_ENV="'production'" same as DefinePlugin

References:

[Webpack getting started](https://webpack.js.org/guides/getting-started)
