import { persistCombineReducers } from "redux-persist";
import { connectRouter } from "connected-react-router";
import { createBrowserHistory } from "history";
import storage from "redux-persist/lib/storage";

const history = createBrowserHistory();

const persistConfig = {
  key: "main",
  storage,
  whitelist: [],
  blacklist: ["router"],
};
const reducers = {
  router: connectRouter(history),
};

export { history };
export default () => persistCombineReducers(persistConfig, reducers);
