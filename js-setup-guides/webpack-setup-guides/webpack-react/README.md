### Setup Webpack 4 and babel 7 for React

A. Install Dependencies

1. React

- react
- react-dom

2. Babel - js compiler for backwards compatibility

- "@babel/core" - core compiler
- "@babel/plugin-proposal-class-properties" - Coverts your class syntax into a function for browsers that don’t support class syntax
- "@babel/plugin-proposal-export-namespace-from" - export \* as ns from '../path/to/module';
- "@babel/plugin-proposal-throw-expressions" - new syntax for exceptions
- "@babel/plugin-syntax-dynamic-import" - helps with code splitting when using babel
- "@babel/polyfill" - full ES2015+ environment
- "@babel/preset-env" - collections of plugins for supporting latest JS
- "@babel/preset-react" - collections of plugins for react
- "babel-loader" - helper plugin for compiling

3. Webpack - Bundler and some other cool things

- "webpack"
- "webpack-cli"
- "webpack-dev-server" - to run a server for development
- "webpack-merge" - split webpack config
- "webpack-visualizer-plugin" - visual presentation when bundling

4. Other loaders and plugins

- "copy-webpack-plugin" - Copies files/folders to your build folder.
- "uglifyjs-webpack-plugin" - To minify JavaScript code for production (\*\*\* see Terser plugin)
- "css-loader" - css-loader interprets @import and url() like import/require() and will resolve them.
- "mini-css-extract-plugin" - extracts CSS into separate files. It creates a CSS file per JS file which contains CSS.
- "node-sass" - A dependency for sass-loader
- "optimize-css-assets-webpack-plugin" - To minify CSS code for production
- "style-loader" - Adds CSS to the DOM by injecting a <style> tag
- "sass-loader" - Loads a Sass/SCSS file and compiles it to CSS.
- "html-webpack-plugin" - generate HTML, supports on demand .css and .js files automatically added to your HTML files on demand
- "postcss-loader" - PostCSS is a tool for transforming styles with JS plugins. Used only auto prefixer
- "webpack-md5-hash" - generate hash with only changed files.

B. Installation

#### React

    npm i react react-dom

#### Webpack

    npm i --save-devwebpack webpack-cli webpack-dev-server webpack-merge webpack-visualizer-plugin

#### Babel

    npm i --save-dev @babel/core @babel/plugin-proposal-class-properties @babel/plugin-proposal-export-namespace-from @babel/plugin-proposal-throw-expressions @babel/plugin-syntax-dynamic-import @babel/polyfill @babel/preset-env @babel/preset-react babel-loader

#### Others

    npm i --save-dev copy-webpack-plugin uglifyjs-webpack-plugin css-loader mini-css-extract-plugin node-sass optimize-css-assets-webpack-plugin style-loader sass-loader html-webpack-plugin

C. Setup

1. Creating ./config and setting up base, prod and dev webpack config

2. Setup build scripts in package.json

D. Server support to serve production build of react

1. Add express server - point to the dist/ folder for the production build of the react app

2. Run prebuild and build

`npm run build` - Runs _prebuild_ , which is the webpack setup then runs the _build_ which the express node server.

E. Code Splitting

1. Check the new features: React lazy and React Suspense [Here](https://reactjs.org/docs/code-splitting.html)

2. See also [React Loadable](https://github.com/jamiebuilds/react-loadable)

---

Credits

[Original tutorial](https://medium.freecodecamp.org/how-to-combine-webpack-4-and-babel-7-to-create-a-fantastic-react-app-845797e036ff)
