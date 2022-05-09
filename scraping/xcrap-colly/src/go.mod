module scraper/backend

go 1.14

replace scraper/backend/route => ./route

replace scraper/backend/env => ./env

replace scraper/backend/docs => ./docs

replace scraper/backend/scheduler => ./scheduler

replace scraper/backend/util => ./util

require (
	github.com/PuerkitoBio/goquery v1.5.1 // indirect
	github.com/alecthomas/template v0.0.0-20190718012654-fb15b899a751
	github.com/antchfx/htmlquery v1.2.3
	github.com/antchfx/xmlquery v1.2.4 // indirect
	github.com/carlescere/scheduler v0.0.0-20170109141437-ee74d2f83d82
	github.com/centrifugal/centrifuge-go v0.5.0
	github.com/centrifugal/gocent v2.1.0+incompatible
	github.com/dgrijalva/jwt-go v3.2.0+incompatible
	github.com/go-playground/validator/v10 v10.2.0
	github.com/go-redis/redis v6.15.7+incompatible // indirect
	github.com/gocolly/colly v1.2.0
	github.com/gocolly/colly/v2 v2.0.1
	github.com/gocolly/redisstorage v0.0.0-20190812112800-1745c5e6d0ba
	github.com/golang/protobuf v1.4.0 // indirect
	github.com/joho/godotenv v1.3.0
	github.com/labstack/echo/v4 v4.1.16
	github.com/onsi/ginkgo v1.12.0 // indirect
	github.com/onsi/gomega v1.9.0 // indirect
	github.com/stretchr/testify v1.4.0
	github.com/swaggo/echo-swagger v1.0.0
	github.com/swaggo/swag v1.6.3
	go.mongodb.org/mongo-driver v1.4.1
	golang.org/x/net v0.0.0-20200425230154-ff2c4b7c35a0
	google.golang.org/appengine v1.6.6 // indirect
)
