package route

import (
	"github.com/go-playground/validator/v10"
)


var validate *validator.Validate

type ErrorUser struct {
	Status int    `json:"status"`
	Msg  string 	`json:"msg"`
}

type User interface {
	validate() error
	extractValidationError(error) string
}

type GenericUser struct {
	ID  string `json:"name" validate:"required"`
	err map[string]string
}

func (u *GenericUser) validate() (err error) {
	validate = validator.New()
	if err = validate.Struct(u); err != nil {
		return
	}
	return nil
}

func (u *GenericUser) extractValidationError(err error) (errs string){
	allErrors := ""
	e := map[string]string{
		"gt": " should be greater than 5.",
		"required": " should not be empty.",
	}
	for _, errss := range err.(validator.ValidationErrors) {
		msg, ok := e[errss.Tag()]
		if ok {allErrors = allErrors + errss.Field() + msg + "\n"}
	}
	return allErrors
}


func ExtractError(user User, err error) (errs string){
	errs = user.extractValidationError(err)
	return 
}

func Validate(user User) (err error) {
	if err = user.validate(); err != nil {
		return
	}
	return nil
}