import { persistCombineReducers } from "redux-persist";
import createSecureStore from "redux-persist-expo-securestore";

const storage = createSecureStore();
const persistConfig = {
  key: "main",
  storage,
  // whitelist/blacklist list of reducer Array<string> where string is the key
  whitelist: [],
};
const reducers = {};

export default () => persistCombineReducers(persistConfig, reducers);
