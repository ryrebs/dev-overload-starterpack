package test

import (
	"encoding/json"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"sample/server/env"
	"sample/server/route"
	"strings"
	"testing"
	"time"

	"github.com/joho/godotenv"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

var userJSON = `{"name": "testUser", "email": "asdasd@gmail.com"}`

type userToken struct {
	Token string
}

func loadEnvTest() *env.Var {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal(err)
		log.Fatal("Error loading .env file")
	}

	port := os.Getenv("PORT")
	environ := os.Getenv("ENV")
	secret := os.Getenv("SECRET_KEY")

	return &env.Var{
		Port:   port,
		Env:    environ,
		Secret: secret,
	}
}

func TestAuthentication(t *testing.T) {

	// Setup
	envVar := loadEnvTest()
	e := echo.New()
	req := httptest.NewRequest(http.MethodPost, "/authenticate", strings.NewReader(userJSON))
	req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// A User DOES NOT exist
	// Assert Test user does not exist
	if assert.NoError(t, route.AuthenticateHandler(c)) {
		assert.Equal(t, http.StatusBadRequest, rec.Code)
		assert.NotEmpty(t, rec.Body.String())
	}

	// A User DOES exist
	// Assert a user exist and does have a token
	var token userToken
	var s string
	s = rec.Body.String()
	_ = json.Unmarshal([]byte(s), &token)
	if token.Token != "" {
		// Assert token has correct signing method
		parsedToken, err := jwt.Parse(token.Token, func(token *jwt.Token) (interface{}, error) {
			_, ok := token.Method.(*jwt.SigningMethodHMAC)
			assert.True(t, ok)
			return []byte(envVar.Secret), nil
		})
		assert.Nil(t, err)

		// Assert token has correct claims
		claims, ok := parsedToken.Claims.(jwt.MapClaims)
		assert.True(t, ok)
		assert.True(t, parsedToken.Valid)
		assert.Equal(t, claims["sub"], "testUser")

		// Assert test token has expiration time of 30mins
		if m, ok := claims["exp"].(string); ok {
			p, _ := time.Parse(time.RFC3339, m)
			assert.WithinDuration(t, time.Now().Add(time.Minute*30), p, 10*time.Minute)
		}
	}
}
