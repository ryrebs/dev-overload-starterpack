import React from "react";
import { Route, Switch, useHistory, useRouteMatch } from "react-router-dom";
import AdminComponent from "containers/Admin/Admin";
import UserComponent from "containers/User/User";
import Error404 from "core/components/errors";
import ProtectedRoutes from "core/container/Auth/ProtectedRoute/ProtectedRoute";

const ChildrenRoutes = () => {
  const { path } = useRouteMatch();
  return (
    <Switch>
      {true ? (
        <Route path={`${path}/admin`} component={AdminComponent} /> // admin routes
      ) : (
        <Route path={`${path}/user`} component={UserComponent} /> // non admin
      )}
      {/* Catch all routes on /member/!admin || !user */}
      <Route component={Error404} />
    </Switch>
  );
};

const LoginComponent = () => {
  return (
    <>
      <h1>Login Form</h1>
    </>
  );
};

const App = () => {
  const history = useHistory();
  return (
    <div>
      <Switch>
        {/* Root route for testing routes */}
        <Route
          exact
          path="/"
          render={() => (
            <>
              <button onClick={() => history.push("/member/admin")}>
                to admin
              </button>
              <button onClick={() => history.push("/  ")}>to login</button>
            </>
          )}
        />

        {/* Remove login route if authenticated */}
        {true ? null : ( // true - authenticated otherwise false
          <Route exact path="/login" component={LoginComponent} />
        )}

        {/* Protect all routes inside */}
        <ProtectedRoutes path="/member">
          <ChildrenRoutes />
        </ProtectedRoutes>

        {/* Catch all routes */}
        <Route component={Error404} />
      </Switch>
    </div>
  );
};

export default App;
