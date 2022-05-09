import {
  fork,
  call,
  put,
  take,
  delay,
  all,
  debounce,
  actionChannel,
  spawn,
} from "redux-saga/effects";
import { channel, buffers } from "redux-saga";
import { createAction } from "@reduxjs/toolkit";

/**
 *  Sample dispatching requests
 *   @param payload: Object
 *  addRequestAction(payload)
 */
/** -- Sample action that changes the reducer */
export const addRequestAction = (payload) => ({
  type: "REQUEST",
  method: () => {}, // http method
  route: "/post/route",
  resultReducerAction: () => {}, // fn is a reducer action
  payload,
});

/** Requests are intercepted by saga,
 *  either create a request that changes
 *  the reducer and dispatched from saga or
 *  just create an action to be intercepted by saga
 */
/** sample action to be intercepted by saga */
export const refreshUserAfterDeleteAction = createAction(
  "REQUEST_REFRESH_USER_AFTER_DELETE"
);

/** App Sagas that handles type *REQUEST* */
export function* retry(count, msDelay, method, route, payload) {
  let error;
  for (let i = 0; i < count; i += 1) {
    try {
      const res = yield call(method, route, payload);
      return res;
    } catch (err) {
      if (i < count - 1) {
        yield delay(msDelay);
      }
      error = err;
    }
  }
  /** Throw the final catched error so
   * reducers that rely on error responses
   * can received the response data */
  throw error;
}

export function* checkTokenExpiration(response) {
  if (
    response.message.includes("Expired") ||
    response.message.includes("Invalid")
  )
    yield put(
      tokenExpiredReducerAction({ error: true, errorMsg: response.message })
    );
}

export function* returnErrorResponseAction(err, action) {
  const { response } = err;
  yield call(checkTokenExpiration, response);
  yield put(
    action({
      loading: false,
      response,
      error: true,
      errorMsg: err.message || "",
    })
  );
}

function* handler(action) {
  const { resultReducerAction } = action;
  const { method, payload, route } = action;
  try {
    let result;
    if (payload) result = yield retry(2, 4000, method, route, payload);
    else result = yield retry(2, 4000, method, route);
    const { response } = result;
    yield put(
      resultReducerAction({
        loading: false,
        error: false,
        errorMsg: "",
        response,
      })
    );
  } catch (err) {
    yield call(returnErrorResponseAction, err, resultReducerAction);
  }
}

function* requestHandler(chan) {
  while (true) {
    const apiAction = yield take(chan);
    yield call(handler, apiAction);
  }
}

function* requestFlow() {
  // create 5 workers
  // to handle 5 request max
  const chan = yield call(channel);
  for (let i = 0; i < 5; i += 1) {
    yield fork(requestHandler, chan);
  }
  while (true) {
    const requestAction = yield take("REQUEST");
    const { resultReducerAction } = requestAction;

    // First reducer mutation
    // Note: Response is null
    yield put(
      resultReducerAction({
        loading: true,
        error: false,
        errorMsg: "",
        response: null,
      })
    );
    yield put(chan, requestAction);
  }
}

/** Delay the search request to an api for 1 second */
function* searchRequest() {
  yield debounce(1000, "SEARCH_REQUEST", handler);
}

/** Queue up to 5 request and handle each one of them in order */
function* requestQueue() {
  const requestChan = yield actionChannel("REQUEST_QUEUE", buffers.sliding(5));
  while (true) {
    const requestAction = yield take(requestChan);
    const { startReducerAction } = requestAction;
    yield put(startReducerAction());
    yield call(handler, requestAction);
  }
}

/** Start request saga */
function* requestSaga() {
  yield all([call(requestFlow), call(searchRequest), call(requestQueue)]);
}

export default function* rootSaga() {
  const sagas = [requestSaga];
  yield all(
    sagas.map((saga) =>
      // eslint-disable-next-line func-names
      spawn(function* () {
        while (true) {
          try {
            yield call(saga);
            break;
          } catch (e) {
            console.error(e);
          }
        }
      })
    )
  );
}
