package main

import (
	"net/http" 
	"log"
)


func main(){
	dist := http.FileServer(http.Dir("./dist"))
	http.Handle("/", dist)
	log.Fatal(http.ListenAndServe("127.0.0.1:8000", nil))
}