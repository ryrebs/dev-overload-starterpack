package test

import (
	"encoding/json"
	"scraper/backend/env"
	"scraper/backend/route"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
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

	// setup
	secret := os.Getenv("SECRET_KEY")
	e := echo.New()
	req := httptest.NewRequest(http.MethodPost, "/authenticate", strings.NewReader(userJSON))
	req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	authHandler := route.AuthenticateHandler(c)

	if assert.NoError(t, authHandler) {
		assert.Equal(t, http.StatusOK, rec.Code)
		assert.NotEmpty(t, rec.Body.String())
	}
	var token userToken
	var s string
	s = rec.Body.String()
	jsonerr := json.Unmarshal([]byte(s), &token)

	assert.Nil(t, jsonerr)

	parsedToken, err := jwt.Parse(token.Token, func(token *jwt.Token) (interface{}, error) {
		_, ok := token.Method.(*jwt.SigningMethodHMAC)
		assert.True(t, ok)
		return []byte(secret), nil
	})

	assert.Nil(t, err)

	claims, ok := parsedToken.Claims.(jwt.MapClaims)

	assert.True(t, ok)
	assert.True(t, parsedToken.Valid)
	assert.Equal(t, claims["sub"], "testUser")

	// test token expiration time is 30mins
	if m, ok := claims["exp"].(string); ok {
		p, _ := time.Parse(time.RFC3339, m)
		assert.WithinDuration(t, time.Now().Add(time.Minute*30), p, 10*time.Minute)
	}

}
