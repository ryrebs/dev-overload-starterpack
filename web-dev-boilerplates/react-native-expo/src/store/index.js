import { createStore, applyMiddleware } from "redux";
import createSagaMiddleware from "redux-saga";
// import { composeWithDevTools } from "redux-devtools-extension/developmentOnly";
import rootSaga from "./saga";
import { persistStore } from "redux-persist";
import createRootReducer from "./reducer";

export default () => {
  const sagaMiddleware = createSagaMiddleware();
  // eslint-disable-next-line no-undef
  const middlewares = [sagaMiddleware];
  const store = createStore(
    createRootReducer(),
    // composeWithDevTools(applyMiddleware(...middlewares)),
    applyMiddleware(...middlewares)
  );
  const persistor = persistStore(store);
  sagaMiddleware.run(rootSaga);

  return { store, persistor };
};

export { store, persistor };
