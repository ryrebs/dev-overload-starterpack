package main

import (
	"log"
	"sort"
)

// recursion
var RECURSE_LIMIT = 1000
var guard = 1

func BinarySearchRc(target *int, searchSpace []int) int {
	sortedSearchSpace := sort.IntSlice(searchSpace)
	sortedSearchSpace.Sort()

	// We guard the recursion and set max recursion
	if guard <= RECURSE_LIMIT {
		guard += 1
	} else {
		return -1
	}
	middleIndex := len(sortedSearchSpace) / 2

	// Check if target is in the middle
	middleNum := sortedSearchSpace[middleIndex]
	if middleNum == *target {
		return sortedSearchSpace[middleIndex]
	}

	// Check if the seach space is already empty
	if len(sortedSearchSpace) == 1 {
		return -1
	}

	// Check if target is lower or greater than middle
	if *target < middleNum {
		// get lower part of array
		return BinarySearchRc(target, sortedSearchSpace[:middleIndex])
	} else if *target > middleNum {
		// get upper
		return BinarySearchRc(target, sortedSearchSpace[middleIndex:])
	} else {
		return -1
	}
}

// Implement not recursion
func BinarySearch(target int, searchSpace []int) int {

	sortedSearchSpace := sort.IntSlice(searchSpace)
	sortedSearchSpace.Sort()

	var left = 0
	var right = len(sortedSearchSpace) - 1

	for left <= right {
		// Get the middle
		middleIdx := (left + right) / 2
		var middleNum = sortedSearchSpace[middleIdx]

		if target == middleNum {
			return middleIdx
		}
		// We move our searchspace to the right of the middle num
		if target > middleNum {
			left = middleIdx + 1
		} else {
			// We move searchspace to the left
			right = middleIdx - 1
		}
	}
	return -1
}

func bsearch() {

	// not exist
	target := 999
	srSpace := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
	targetFound := BinarySearchRc(&target, srSpace)
	log.Println(targetFound < 0)

	// exist
	target2 := 9
	srSpace2 := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
	targetFound2 := BinarySearchRc(&target2, srSpace2)
	log.Println(targetFound2 > -1)

	target3 := 9
	srSpace3 := []int{9, 5, 2, 10, 1, 11}
	targetFound3 := BinarySearchRc(&target3, srSpace3)
	log.Println(targetFound3 > -1)

	found := BinarySearch(target2, srSpace2)
	log.Println(found > -1)

	found2 := BinarySearch(target, srSpace)
	log.Println(found2 < 0)

	found3 := BinarySearch(0, []int{1})
	log.Println(found3 < 0)

	found4 := BinarySearch(0, []int{})
	log.Println(found4 < 0)

	found5 := BinarySearch(0, []int{-1, -3, 5, 0, 10})
	log.Println(found5 > -1)

	found6 := BinarySearch(-3, []int{-1, -3, 5, 0, 10})
	log.Println(found6 > -1)

}
