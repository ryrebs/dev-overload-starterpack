# Express rest api structure boilerplate

## Getting started

1. Clone the repo

2. Install dependencies `npm install`

3. Compile and run `npm start`

## Features

1. es6 import and class properties

2. Sample todo CRUD operation using LokiJS as Database

3. Validation Joi

4. Husky for pre commit scripts

5. Pm2 node process manager for monitoring node applications

6. Testing with mocha

7. Documentation through ApiDoc

#### Scripts

Production:

`npm run start:prod`

Development:

`npm run start`

Linting:

`yarn lint`

`yarn lint:fix`

`yarn lint:watch`

Testing:

`yarn test`

Coverage(Sample only):

`yarn coverage`

    "coverage": "nyc report --reporter=text-lcov | coveralls",
    "postcoverage": "opn coverage/index.html",

Documentations:

`yarn docs`

#### Dependencies:

1. morgan - HTTP request logger middleware for node.js
2. helmet - Helmet helps you secure your Express apps by setting various HTTP headers. It's not a silver bullet, but it can help!
3. Mocha - testing framework for JS
4. Supertests - client side testing library for node
5. Pm2 - Advanced, production process manager for Node.js
6. cors - Enable cors on express
7. Compresssion - Node.js compression middleware.
8. http-status - Utility to interact with HTTP status code.

#### Dev Dependencies:

10. apidoc - inline docs for Restful web api
11. Istanbul - Code coverage with coveralls (See docs for usage, Not installed as package)
12. nyc - Istanbul cli
13. opn - open files automatically - crossplatform
14. Eslint - Ecma script standards linting
15. DotEnv - setting envirsonment variables as config file
16. Cross-env - setting env in cross platform, overrides set .env variables
17. Dotenv-safe - .env loader like Dotenv but allows you to have two .env one for your repo (.env.example) and one for your actual prod setup.
18. nodemon - monitor changes and restarts your app
19. prettier - (not installed as cli)code formatter, can be used as a cli (prettier used .prettierrc.yaml) or plugin for vscode, which also respects .prettierrc.yaml and .prettierignore
20. Chai - a BDD / TDD assertion library for node
21. husky - Husky can prevent bad git commit, git push and more 🐶 woof!
22. coveralls - provides historical coverage (Not installed / CI purposes)
23. eslint-plugin-prettier - Runs Prettier as an ESLint rule and reports differences as individual ESLint issues.
24. eslint-config-prettier - Turns off all rules that are unnecessary or might conflict with Prettier
