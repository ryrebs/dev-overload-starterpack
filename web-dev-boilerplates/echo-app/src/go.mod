module sample/server

go 1.13

require (
	github.com/alecthomas/template v0.0.0-20190718012654-fb15b899a751
	github.com/dgrijalva/jwt-go v3.2.0+incompatible
	github.com/go-playground/validator/v10 v10.2.0
	github.com/joho/godotenv v1.3.0
	github.com/labstack/echo v3.3.10+incompatible
	github.com/labstack/echo/v4 v4.1.15
	github.com/stretchr/testify v1.4.0
	github.com/swaggo/echo-swagger v0.0.0-20191205130555-62f81ea88919
	github.com/swaggo/swag v1.6.3
)

replace sample/server/route => ./route

replace sample/server/env => ./env

replace sample/server/docs => ./docs
