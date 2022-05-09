### React with redux minimal boilerplate

Libraries:

1. @reduxjs/toolkit - for redux setup.
2. connected-react-router - for dispatching router action inside saga.
3. redux-saga - async side effects.
4. axios - for http requests.
5. husky - code checks
6. redux-devtools-extension
7. redux-persist - persisting to local storage
8. react-i18next - internationalization
9. i18next-browser-languagedetector - detecting browser language
10. react-router-dom - navigation
11. pm2 - running production server

A. Install dependencies:

```
npm i connected-react-router \
                axios \
                history \
                i18next \
                i18next-browser-languagedetector \
                sass \
                prop-types \
                react-i18next \
                react-redux \
                react-router-dom \
                redux-devtools-extension \
                redux-persist \
                redux-saga \
                @reduxjs/toolkit \
                pm2
```

B. Copy these folder to new project:

    components/

    containers/

    example/

    service/

    store/

    utils/

C. Replace new App.js content