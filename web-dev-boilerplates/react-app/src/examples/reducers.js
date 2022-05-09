import { createSlice, createSelector } from "@reduxjs/toolkit";

/** Sample root reducer
 *  const reducers = {
 *   profile: profileReducer,
 *   router: connectRouter(history),
 * };
 */

/** Creating selectors */
const isProfileFoundSelector = createSelector(
  (state) => state.profile,
  (profile) =>
    profile["profile/update"].name != null &&
    profile["profile/update"].url != null,
);

const userUrlSelector = createSelector(
  (state) => state.profile,
  (profile) => profile["profile/update"].url,
);

export { isProfileFoundSelector, userUrlSelector };

/** Creating reducers */
const reducerDefaultObjectBuilder = () => {
  return {
    loading: false,
    error: false,
    response: null,
    errorMsg: "",
  };
};

const initialState = {
  "users/update": reducerDefaultObjectBuilder(),
};
/* eslint-disable no-param-reassign */
const mapResponseToState = (stateKey, state, action) => {
  state[stateKey].loading = action.payload.loading;
  state[stateKey].error = action.payload.error;
  state[stateKey].errorMsg = action.payload.errorMsg;
  state[stateKey].response = action.payload.response;
};

const adminSlice = createSlice({
  name: "adminSlice",
  initialState,
  reducers: {
    updateReducerAction: (state, action) =>
      mapResponseToState("users/update", state, action),
  },
});

const { actions, reducer } = adminSlice;

const { updateReducerAction } = actions;

export { updateReducerAction, reducer };
