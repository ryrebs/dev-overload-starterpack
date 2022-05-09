import React from "react";
import { Route, Redirect } from "react-router-dom";
/** Accessing protected routes
 *  should wait for authentication service
 *  before deciding which route to show.
 */

// TODO: fix eslint errors
/* eslint-disable react/prop-types */
/* eslint-disable no-constant-condition */
/* eslint-disable react/button-has-type */
const DEFAULT_REDIRECT_TO = "/login";

const ProtectedRoutesComponent = ({ children }) => {
  // not loading
  // authenticated
  if (true)
    if (true)
      /** Children  is either nested routes or component  or */
      return <>{children}</>;
    /** Unauthenticated request should redirect to login */ else
      return (
        <Redirect
          to={{
            exact: true,
            pathname: DEFAULT_REDIRECT_TO,
          }}
        />
      );
  /* eslint-disable no-else-return */ else {
    /** Create loader while waiting for authentication */
    return <h1>Loading...</h1>;
  }
};

const ProtectedRoutes = ({ children, ...args }) => {
  if (args)
    // Render a nested route with base path and/or other args.
    return (
      // eslint-disable-next-line react/jsx-props-no-spreading
      <Route {...args}>
        <ProtectedRoutesComponent>{children}</ProtectedRoutesComponent>
      </Route>
    );
  // Render a nested route.
  return <ProtectedRoutesComponent>{children}</ProtectedRoutesComponent>;
};

export default ProtectedRoutes;
