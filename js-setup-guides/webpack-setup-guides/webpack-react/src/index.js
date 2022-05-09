import React from "react";
import ReactDOM from "react-dom";

import "./styles.scss";

import Foo from "./Foo";

class App extends React.Component {
  state = {
    CaptainKirkBio: {}
  };

  componentDidMount() {
    console.log("process.env.VERSION", process.env.VERSION);
    console.log("process.env.PLATFORM", process.env.PLATFORM);
    console.log("process.env.NODE_ENV", process.env.NODE_ENV);

    // code splitting via dynamic import
    // Load ./Foo file and named it `Foo
    import(/* webpackChunkName: 'Foo' */ "./Foo").then(Foo => {
      console.log("Foo is loaded: ", Foo);
      this.setState({ Foo: Foo.default });
    });

    this.onGetKirkBio();
  }

  onGetKirkBio = async () => {
    try {
      const result = await fetch(
        "http://stapi.co/api/v1/rest/character/search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: {
            title: "James T. Kirk",
            name: "James T. Kirk"
          }
        }
      );
      const resultJSON = await result.json();
      const character = resultJSON.characters[0];
      this.setState({ CaptainKirkBio: character });
    } catch (error) {
      console.log("error", error);
    }
  };

  render() {
    const { CaptainKirkBio } = this.state;
    return (
      <div className="app">
        <div className="div box" />
        <img
          alt="header"
          src="/dist/images/header.jpg"
          className="app-header"
        />
        <p>
          We are a most promising species, Mr. Spock, as predators go. Did you
          know that? I frequently have my doubts. I dont. Not any more. And
          maybe in a thousand years or so, we will be able to prove it.
        </p>
        <p>- Captain Kirk</p>
        <section>
          {Object.values(CaptainKirkBio).length === 0 ? (
            <p>Loading User Information</p>
          ) : (
            <p style={{ wordBreak: "break-all" }}>
              {JSON.stringify(CaptainKirkBio)}
            </p>
          )}
        </section>
        {/* Code splitting demo */}
        {Foo ? <Foo /> : <p>Foo is loading</p>}
      </div>
    );
  }
}

// attach script to this element
// which during bundling js files are automatically added
// set up in webpack config.js
ReactDOM.render(<App />, document.getElementById("app"));
