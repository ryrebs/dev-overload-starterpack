### echo-app

### Documentation

Add docs dependencies:

`go get github.com/swaggo/swag/cmd/swag`

`go get -u github.com/swaggo/echo-swagger`

Generate/update docs with:

`/bin/swag init -generalInfo ./src/server.go -output ./src/docs`

Run by running the app Api docs: `http://localhost:8000/swagger/index.html`
