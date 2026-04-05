package main

import "log"

func partition(left, right int, arr []int) int {

	// left is the lowest or first item in the array
	// right is the end of the array

	// Using lomotu partition
	// pivot is always chosen at the end
	pvIdx := right
	i := left     // index for switching
	j := left + 1 // traverses the array

	for j < pvIdx {
		if arr[j] <= arr[pvIdx] {
			// swap i j
			// j should be on the left
			// increment switche idx
			i = i + 1
			arr[i], arr[j] = arr[j], arr[i]
		}
		j++
	}

	// Place pivot the pivot after the lowest num.
	i = i + 1
	arr[i], arr[pvIdx] = arr[pvIdx], arr[i]
	return i
}

func quickSort(left, right int, arr []int) {

	if left == right {
		return
	}

	// partition and get middle Idx
	// this will put small numbers on the left and large numbers on the right
	// of the pivot
	pvIdx := partition(left, right, arr)

	// sort lower
	quickSort(left, pvIdx-1, arr)

	// sort upper
	quickSort(pvIdx, right, arr)

}

func tQuickSort() {
	arr := []int{3, 7, 6, 1, 5}
	left := -1
	right := len(arr) - 1
	quickSort(left, right, arr)
	log.Println(arr)

	arr2 := []int{3, 7, 6, 1, 5, -1, 8, 0, 10, 10, 11, 100, 7}
	left2 := -1
	right2 := len(arr2) - 1
	quickSort(left2, right2, arr2)
	log.Println(arr2)

	arr3 := []int{-1, 0, -2, -4, -5, -7}
	left3 := -1
	right3 := len(arr3) - 1
	quickSort(left3, right3, arr3)
	log.Println(arr3)

	arr4 := []int{3, 3, 3, 1, 1, 1, 1, 2}
	left4 := -1
	right4 := len(arr4) - 1
	quickSort(left4, right4, arr4)
	log.Println(arr4)

	arr5 := []int{3}
	left5 := -1
	right5 := len(arr5) - 1
	quickSort(left5, right5, arr5)
	log.Println(arr5)

	arr6 := []int{1, 2, 3, 4, 5}
	left6 := -1
	right6 := len(arr6) - 1
	quickSort(left6, right6, arr6)
	log.Println(arr6)

	arr7 := []int{5, 4, 3, 2, 1}
	left7 := -1
	right7 := len(arr7) - 1
	quickSort(left7, right7, arr7)
	log.Println(arr7)
}
