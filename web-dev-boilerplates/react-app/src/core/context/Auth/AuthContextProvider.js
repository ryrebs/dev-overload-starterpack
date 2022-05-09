import React from "react";
import PropTypes from "prop-types";

export const AuthContext = React.createContext({});

const AuthContextProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [authSuccess, setAuthSuccess] = React.useState(null);

  const onLogIn = (user, pass) => {
    if (user === "admin@gmail.com" && pass === "admin") {
      setAuthSuccess(true);
      setIsLoggedIn(true);
    } else setAuthSuccess(false);
  };

  return (
    <AuthContext.Provider value={{ onLogIn, isLoggedIn, authSuccess }}>
      {children}
    </AuthContext.Provider>
  );
};

AuthContextProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthContextProvider;
