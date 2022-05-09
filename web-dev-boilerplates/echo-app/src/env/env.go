package env

import (
	"os"
	"log"
	"github.com/joho/godotenv"
)

// Var defines environment variables
type Var struct {
	Port, Env, Secret string
}

// LoadEnv loads all environment variables in .env file
func LoadEnv() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
		log.Fatal("Error loading .env file")
	}
	// Make sure these env variables are present
	if (os.Getenv("PORT") == "" ||
		os.Getenv("SECRET_KEY") == ""){
		log.Fatal("None optional env variables: PORT, ENV, SECRET_KEY, CENTRIFUGO_ANONYMOUS_USER")
	}
}
