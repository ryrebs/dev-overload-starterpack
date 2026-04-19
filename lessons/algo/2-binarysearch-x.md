
# Understanding Binary Search from First Principles

---

## 1. Title

**Understanding Binary Search from First Principles (with Deep Execution Insight)**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Arrays / slices
- Loops and conditionals
- Basic Big-O understanding
- Integer arithmetic

---

## 3. Problem Definition

### The Core Problem

We want to **find the position of a target value in a sorted array efficiently**.

---

### Example

```go
arr := []int{1, 3, 5, 7, 9, 11}
target := 7
```

Output:
```
index = 3
```

---

### Inputs / Outputs

- Input:
  - Sorted array of integers
  - Target value
- Output:
  - Index of target OR -1 if not found

---

## 🧠 4. First Principles Thinking

---

### Why Does This Problem Exist?

Searching is fundamental:
- databases
- search engines
- memory lookup

---

### Naive Solution: Linear Search

```go
for i := 0; i < len(arr); i++ {
    if arr[i] == target {
        return i
    }
}
```

---

### Why Is This Inefficient?

Worst case:
- You scan **every element**

Time:
```
O(n)
```

---

### What Makes This Problem Interesting?

👉 The array is **sorted**

This gives us **information we are not using yet**

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Use Sorted Order

Instead of checking everything:

👉 Check the **middle**

---

### Step 2: Key Insight

If:
```
arr[mid] < target
```

Then:
> Target MUST be on the RIGHT

Because array is sorted.

---

### ⚠️ Disambiguation

| Concept | Meaning |
|--------|--------|
| mid | index in array |
| arr[mid] | value at that index |

👉 Do NOT confuse:
- index vs value

---

### Step 3: Eliminate Half

Each step:
- Remove half the array

---

### Step 4: Repeat

Keep narrowing:
```
left → mid → right
```

---

### Step 5: Stop Condition

When:
```
left > right
```

👉 Search space is empty

---

## 🧠 6. Mental Model

---

### Think of It Like Guessing a Number

Range: 1–100

Ask:
- Is it > 50?
- Then > 75?
- Then < 62?

👉 You **cut possibilities in half each time**

---

### Invariant (VERY IMPORTANT)

At every step:

> If the target exists, it MUST be inside [left, right]

---

### Why This Guarantees Correctness

We:
- never discard the correct region
- always shrink the search space

---

## 🔧 7. Algorithm Definition

---

### Steps

1. Initialize:
   ```
   left = 0
   right = n - 1
   ```

2. While left ≤ right:
   - Compute mid
   - Compare arr[mid] with target
   - Adjust bounds

---

### ⚠️ Critical Detail: Mid Calculation

```
mid = left + (right - left)/2
```

---

### Why NOT `(left + right)/2`?

You might think:
> “They are the same”

But actually:
- `(left + right)` can overflow

---

### Pseudocode

```
while left <= right:
    mid = left + (right - left) / 2

    if arr[mid] == target:
        return mid
    else if arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

return -1
```

---

## 💻 8. Implementation (Golang)

```go
package main

import "fmt"

func binarySearch(arr []int, target int) int {
	left := 0
	right := len(arr) - 1

	for left <= right {
		// Prevent overflow
		mid := left + (right-left)/2

		// Debug understanding:
		// left, mid, right represent CURRENT search window

		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			// Eliminate LEFT side including mid
			left = mid + 1
		} else {
			// Eliminate RIGHT side including mid
			right = mid - 1
		}
	}

	return -1
}

func main() {
	arr := []int{1, 3, 5, 7, 9, 11}

	fmt.Println(binarySearch(arr, 7))  // 3
	fmt.Println(binarySearch(arr, 4))  // -1
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Input

```go
arr = [1, 3, 5, 7, 9, 11]
target = 9
```

---

### Step 1

```
left = 0
right = 5

mid = 0 + (5-0)/2 = 2
arr[mid] = 5
```

Comparison:
```
5 < 9 → go right
```

Update:
```
left = 3
```

---

### Step 2

```
left = 3
right = 5

mid = 3 + (5-3)/2 = 4
arr[mid] = 9
```

Found!

---

### Internal State Evolution

| Step | left | mid | right | value |
|------|------|-----|-------|-------|
| 1 | 0 | 2 | 5 | 5 |
| 2 | 3 | 4 | 5 | 9 |

---

### ⚠️ Hidden Flow Explanation

When we do:
```
left = mid + 1
```

We are:
- **discarding left half INCLUDING mid**

Why include mid?
- Because we already KNOW it's not the target

---

## ⏱️ 10. Complexity Analysis

---

### Time Complexity

Each step:
```
n → n/2 → n/4 → ...
```

After k steps:
```
n / (2^k) = 1
```

Solve:
```
k = log₂(n)
```

---

### Final

| Case | Time |
|------|------|
| Best | O(1) |
| Average | O(log n) |
| Worst | O(log n) |

---

### Space Complexity

```
O(1)
```

(no extra memory)

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ Sorted data  
✅ Fast lookup needed  
✅ Static dataset  

---

### When NOT to Use

❌ Unsorted data  
❌ Frequent insertions  

---

### Alternatives

| Algorithm | Time | Use Case |
|----------|------|---------|
| Linear Search | O(n) | small data |
| Hashing | O(1) avg | key lookup |
| Binary Search Tree | O(log n) | dynamic sorted |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Infinite Loop

Using:
```
while left < right
```

👉 Misses edge case

---

### ❌ Wrong Mid Update

```
left = mid
```

👉 Infinite loop

Correct:
```
left = mid + 1
```

---

### ❌ Forgetting Sorted Requirement

Binary search ONLY works on sorted arrays.

---

### ❌ Off-by-One Errors

Most bugs come from:
- boundaries
- incorrect updates

---

## 🌍 13. Real-World Usage

---

### Databases

- Index lookup (B-Trees use binary search internally)

---

### Search Engines

- Finding position in sorted index

---

### Systems Programming

- Memory lookup tables

---

### Libraries

Go’s `sort.Search` uses binary search internally

---

## 🚀 14. Variations and Extensions

---

### Find First Occurrence

Modify:
```
if arr[mid] == target:
    move left
```

---

### Find Last Occurrence

Move right instead.

---

### Lower Bound

First element ≥ target

---

### Upper Bound

First element > target

---

### Binary Search on Answer

Used in:
- optimization problems
- scheduling

---

## 🔁 15. Recap (Feynman Compression)

Binary search works by repeatedly cutting a sorted array in half. At each step, it compares the middle element with the target and eliminates half of the search space. This leads to very fast lookup in logarithmic time.

---

## 🧩 16. Exercises

---

### Easy

1. Implement binary search recursively  
2. Find if element exists in sorted array  

---

### Medium

3. Find first occurrence of a duplicate element  

---

### Real-World Challenge

4. Given sorted logs of timestamps:
   - Find earliest event ≥ target time  
   - Implement efficient lookup system  

---

## 🧠 Final Insight

You might think binary search is just:
> “divide and conquer”

But actually it is:

> Maintaining a **correct shrinking boundary** where the answer MUST exist

Everything depends on:
- correct invariant
- precise boundary updates

Break either → algorithm fails.