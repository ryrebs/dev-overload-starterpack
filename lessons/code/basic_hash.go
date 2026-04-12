package main

import (
	"fmt"
)

// Basic hash calculation for understanding the whole concept
func getHash(key string) int{
	hash := 0
	for _, ch :=  range key {
		// Get unicode value as integer
		hash += int(ch)
	}
	return hash
}

type Entry struct {
		Key string	
}

func main() {
	// We want fast storage and lookup
	// O(1) compare with array O(n)
	
	// calc hash
	sample1 := "tester"
	sampleHashed1 := getHash(sample1)

	sample2 := "dev"
	sampleHashed2 := getHash(sample2)

	// 663
	fmt.Println(sampleHashed1)

	// 319
	fmt.Println(sampleHashed2)


	// Bucket size
	bucketSize := 5

	// We store it in an Array
	hashMap := &struct{
		Buckets [][]Entry
	}{
		Buckets: make([][]Entry, bucketSize),
	}

	// We want store values inside a bucket 
	// so if the same keys (collisions) resolves to the same index
	// we store the data in the bucket[index]
	// where bucket[index] contains a list of data

	// We need to make sure index is within hash map size
	sampleHashIndex1 := sampleHashed1 % bucketSize
	sampleHashIndex2 := sampleHashed2 % bucketSize


	// Store data at index
	bucket := hashMap.Buckets[sampleHashIndex1]
	hashMap.Buckets[sampleHashIndex1] = append(bucket, Entry{sample1})

	bucket = hashMap.Buckets[sampleHashIndex2]
	hashMap.Buckets[sampleHashIndex2] = append(bucket, Entry{sample2})

	fmt.Println(hashMap) // &{[[] [] [] [{tester}] [{dev}]]}

	// Average case lookup is O(1) 1 item per bucket
	//  OR the item in bucket does not grow with N
	// WHY???
	// We resize the bucket to redistribute the items
	// We make a good hashing function to distribute the items evenly
	// So the goal is O(1 + k)
	// WE need to consider load factor, lf = n / bucket_size for resizing

	// Worst case is O(n) all items are in the same bucket
	// SO as n grows k grows (k the no. of items)

}
