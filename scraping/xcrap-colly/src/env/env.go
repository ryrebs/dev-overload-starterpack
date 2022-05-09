package env

import (
	"os"
	"log"
	"github.com/joho/godotenv"
)

// Var defines environment variables
type Var struct {
	Port, Env, Secret, RedisHost, RedisPass string
}

// LoadEnv loads all environment variables in .env file
func LoadEnv() {
	// Load env variables when in development
	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
		log.Fatal("Error loading .env file")
	}

	log.Println(""+os.Getenv("CENTRIFUGO_API_HOST"))
	// Make sure these env variables are present
	if (os.Getenv("PORT") == "" ||
		os.Getenv("SECRET_KEY") == "" ||
		os.Getenv("CENTRIFUGO_ANONYMOUS_USER") == ""){
		log.Fatal("None optional env variables: PORT, ENV, SECRET_KEY, CENTRIFUGO_ANONYMOUS_USER")
	}
}
