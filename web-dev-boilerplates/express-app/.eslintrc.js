module.exports = {
  env: {
    es6: true,
    node: true,
    // mocha: true, can be also set
  },
  plugins: ['security'],
  extends: ['eslint:recommended', 'airbnb-base', 'plugin:security/recommended'],
  parserOptions: {
    ecmaVersion: 2018,
  },
  globals: {
    describe: true,
    it: true,
  },
  rules: {
    indent: ['error', 2],
    'linebreak-style': ['error', 'unix'],
    semi: ['error', 'always'],
  },
};
