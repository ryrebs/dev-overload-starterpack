import React from "react";
import { Provider } from "react-redux";
import { ConnectedRouter } from "connected-react-router";
import { PersistGate } from "redux-persist/integration/react";
import Container from "./containers";
import setupStore from "./core/store";
import setUpApi from "./core/service/api";
import "./utils/i18n";
import "./App.scss";
import AuthContextProvider from "./core/context/Auth/AuthContextProvider";

setUpApi();
const { store, persistor, history } = setupStore();

export default () => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedRouter history={history}>
        <AuthContextProvider>
          <Container />
        </AuthContextProvider>
      </ConnectedRouter>
    </PersistGate>
  </Provider>
);
