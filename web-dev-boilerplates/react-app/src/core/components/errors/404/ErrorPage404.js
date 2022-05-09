import React from "react";
import { withRouter } from "react-router-dom";
import "./styles.scss";

export default withRouter(() => {
  return (
    <div className="errorContainer">
      <h1 className="errorHeader">Ooops!</h1>
      <div className="messageContainer">
        The page you are looking for might have been removed, had its name
        changes, or is temporarily unavailable.
      </div>
    </div>
  );
});
