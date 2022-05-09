package scraper

import (
	"context"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const JOB_COLLECTION = "jobCollection"
const JOB_DATABASE = "jobs"

var collection *mongo.Collection

func CreateDBCollection() {
	log.Println("::::Creating Collection::::")
	URI := os.Getenv("MONGODB")

	if URI == "" {
		URI = "mongodb://server:serverpass@127.0.0.1:27017/jobs"
	}
	clientOpts := options.Client().ApplyURI(URI)
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	client, err := mongo.Connect(ctx, clientOpts)
	if err != nil {
		log.Fatalln(err)
	}
	collection = client.Database(JOB_DATABASE).Collection(JOB_COLLECTION)
	defer cancel()
}

func GetDefaultCollection() *mongo.Collection {
	if collection == nil {
		log.Println("::::No Collection::::")
		CreateDBCollection()
		return collection
	} else {
		log.Println("::::Collection Exists::::")
		return collection
	}
}

func InsertIntoCollection(items []interface{}, collection *mongo.Collection) {
	opts := options.InsertMany().SetOrdered(false)
	ctx, cancel := context.WithCancel(context.Background())
	collection.InsertMany(ctx, items, opts)
	defer cancel()
}

func DeleteMany(filter interface{}, collection *mongo.Collection) {
	filterBson, _ := bson.Marshal(filter)
	opts := options.Delete().SetCollation(&options.Collation{
		Locale: "en_US",
	})
	res, err := collection.DeleteMany(context.TODO(), filterBson, opts)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(res)
}
