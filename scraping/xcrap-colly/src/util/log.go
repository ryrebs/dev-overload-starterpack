package  util


import (
	"log"
	"os"
)

func LogInDev(msg string) {
	if os.Getenv("env") != "production" {
		log.Println(msg)
	}
}