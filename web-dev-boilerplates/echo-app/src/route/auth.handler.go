package route

import (
	"net/http"
	"os"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
	"github.com/labstack/echo/v4"
)

// AuthenticateHandler - handles /authenticate route
// @tags Auth
// @Summary Creates token for subscribers
// @Description TODO
// @Accept  json
// @Produce  json
// @Param id formData string true "id of connecting client"
// @Header 200 {string} Token
// @Router /authenticate [post]
func AuthenticateHandler(c echo.Context) (err error) {
	errorRes := &ErrorUser{
		Status: 404,
		Msg:    "",
	}
	user := &GenericUser{
		err: map[string]string{
			"ID": "name - is required and length greater than 5",
		},
	}
	if err = c.Bind(user); err != nil {
		return
	}
	if err = Validate(user); err != nil {
		errorRes.Msg = ExtractError(user, err)
		return c.JSON(http.StatusNotFound, errorRes)
	}
	if CheckExistingUser(user) {
		tokenString := CreateToken(user.ID, os.Getenv("SECRET_KEY"))
		return c.JSON(http.StatusOK, struct {
			Token string `json:"token"`
		}{
			Token: tokenString,
		})
	}
	errorRes.Msg = "User Not Found!"
	errorRes.Status = http.StatusBadRequest
	return c.JSON(http.StatusBadRequest, errorRes)

}

// CheckUser - check for existing users
func CheckExistingUser(u *GenericUser) bool {
	// TODO: Add user retrieval logic
	if u.ID == os.Getenv("KNOWN_USER") {
		return true
	} else {
		return false
	}
}

// CreateToken - creates the token for the specified user
func CreateToken(id string, secret string) (tokenString string) {
	timeNow := time.Now()
	timeNowUTC := timeNow.UTC()
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": id,
		"exp": timeNowUTC.Add(time.Minute * 30).Unix()})
	tokenString, _ = token.SignedString([]byte(secret))
	return
}
