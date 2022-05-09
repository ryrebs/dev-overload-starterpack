import React from "react";
import ReactDOM from "react-dom";
import './style.css'

const App = () => {
  return (
    <div>
      <p>React here!</p>
      <h3>I'm I reloading? really?</h3>
    </div>
  );
};
export default App;

ReactDOM.render(<App />, document.getElementById("app"));