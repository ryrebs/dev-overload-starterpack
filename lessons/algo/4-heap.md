# Understanding Heap (Priority Queue) from First Principles (Deep Execution-Level Guide)

---

## 1. Title

**Understanding Heap (Priority Queue) from First Principles: From Arrays to Logarithmic Power**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Arrays and slices
- Basic tree concepts
- Index arithmetic
- Big-O notation

---

## 3. Problem Definition

---

### The Core Problem

We want to:

> Efficiently get the **smallest (or largest)** element repeatedly while also allowing insertions.

---

### Example

Input stream:
```
[5, 3, 8, 1]
```

We want:
```
getMin() → 1
insert(2)
getMin() → 2
```

---

### Input / Output

- Input:
  - Dynamic set of numbers
- Output:
  - Fast:
    - insert
    - extract-min / extract-max

---

## 🧠 4. First Principles Thinking

---

### Why Does This Problem Exist?

Many systems need:
- scheduling (next task)
- shortest path (smallest distance)
- prioritization

---

### Naive Solution

Keep array sorted:

```go
sort every insert → O(n log n)
```

OR

```go
scan min every time → O(n)
```

---

### Why This Fails

| Operation | Cost |
|----------|------|
| Insert | O(n) |
| Get min | O(n) |

👉 Too slow

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Only Care About the Top

We don’t need full sorting.

We only need:
> “smallest element at top”

---

### Step 2: Use Tree Structure

We want:
```
parent ≤ children
```

---

### Step 3: Represent Tree as Array

---

### ⚠️ Key Mapping (VERY IMPORTANT)

| Tree Concept | Array Index |
|-------------|------------|
| root | 0 |
| left child | 2*i + 1 |
| right child | 2*i + 2 |
| parent | (i-1)/2 |

---

### 🔍 Why This Works

Because:
- tree is **complete binary tree**
- stored compactly

---

### Step 4: Insert Operation

Add at end:
```
[3, 5, 8, 1]
           ↑ new
```

Now fix heap property.

---

### Step 5: Bubble Up

Compare with parent:
- swap if smaller

---

### Step 6: Remove Root

Replace root with last element:
```
[1, 3, 8, 5] → remove 1
→ [5, 3, 8]
```

Then fix downward.

---

### Step 7: Bubble Down

Swap with smaller child.

---

## 🧠 6. Mental Model

---

### Think of Heap as a “Priority Funnel”

- smallest always floats to top
- new elements rise or sink

---

### Invariant

> Every parent ≤ its children

---

### Why This Guarantees Correctness

- smallest element must be root
- structure ensures logarithmic operations

---

## 🔧 7. Algorithm Definition

---

### Insert

```
append value
while value < parent:
    swap
```

---

### Extract Min

```
save root
move last element to root
remove last

while node > child:
    swap with smaller child
```

---

## 💻 8. Implementation (Golang)

---

```go
package main

import "fmt"

type MinHeap struct {
	data []int
}

// Insert element
func (h *MinHeap) Insert(val int) {
	h.data = append(h.data, val)

	i := len(h.data) - 1

	// Bubble up
	for i > 0 {
		parent := (i - 1) / 2

		if h.data[parent] <= h.data[i] {
			break
		}

		h.data[parent], h.data[i] = h.data[i], h.data[parent]
		i = parent
	}
}

// Extract min
func (h *MinHeap) ExtractMin() int {
	if len(h.data) == 0 {
		return -1
	}

	min := h.data[0]

	last := h.data[len(h.data)-1]
	h.data[0] = last
	h.data = h.data[:len(h.data)-1]

	h.heapifyDown(0)

	return min
}

// Heapify down
func (h *MinHeap) heapifyDown(i int) {
	for {
		left := 2*i + 1
		right := 2*i + 2
		smallest := i

		if left < len(h.data) && h.data[left] < h.data[smallest] {
			smallest = left
		}

		if right < len(h.data) && h.data[right] < h.data[smallest] {
			smallest = right
		}

		if smallest == i {
			break
		}

		h.data[i], h.data[smallest] = h.data[smallest], h.data[i]
		i = smallest
	}
}

func main() {
	h := MinHeap{}

	h.Insert(5)
	h.Insert(3)
	h.Insert(8)
	h.Insert(1)

	fmt.Println(h.ExtractMin()) // 1
	fmt.Println(h.ExtractMin()) // 3
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Insert 5

```
[5]
```

---

### Insert 3

```
[5, 3]
compare 3 < 5 → swap

[3, 5]
```

---

### Insert 8

```
[3, 5, 8]
(no swap needed)
```

---

### Insert 1

```
[3, 5, 8, 1]

compare with parent (5)
→ swap → [3, 1, 8, 5]

compare with parent (3)
→ swap → [1, 3, 8, 5]
```

---

### Extract Min

```
remove 1

replace with last:
[5, 3, 8]

heapify:
5 > 3 → swap

[3, 5, 8]
```

---

## ⏱️ 10. Complexity Analysis

---

### Height of Heap

```
log₂(n)
```

---

### Operations

| Operation | Time |
|----------|------|
| Insert | O(log n) |
| Extract | O(log n) |
| Peek | O(1) |

---

### Space

```
O(n)
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ Frequent min/max queries  
✅ Streaming data  
✅ Scheduling  

---

### When NOT to Use

❌ Need sorted order  
❌ Need fast search for arbitrary elements  

---

### Alternatives

| Structure | Use |
|----------|-----|
| Sorted array | small data |
| BST | ordered operations |
| HashMap | lookup |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Wrong index math

```
left = 2*i + 1
right = 2*i + 2
```

---

### ❌ Forgetting heapify after removal

→ breaks heap

---

### ❌ Confusing heap with sorted array

Heap is:
> partially ordered

---

## 🌍 13. Real-World Usage

---

### Dijkstra’s Algorithm

- always pick smallest distance

---

### Task Scheduling

- priority queues

---

### Operating Systems

- CPU scheduling

---

### Streaming Data

- top K elements

---

## 🚀 14. Variations and Extensions

---

### Max Heap

reverse comparisons

---

### k-th Smallest

use heap of size k

---

### Median Finder

two heaps

---

### Priority Queue with Objects

store struct with priority

---

## 🔁 15. Recap (Feynman Compression)

A heap is a special tree stored in an array where the smallest (or largest) element is always at the top. It allows fast insertion and removal by maintaining a simple parent-child relationship using swaps.

---

## 🧩 16. Exercises

---

### Easy

1. Implement MaxHeap  
2. Peek minimum element  

---

### Medium

3. Find k smallest elements  

---

### Real-World Challenge

4. Build task scheduler:
   - tasks with priority
   - always execute highest priority  

---

## 🧠 Final Insight

You might think a heap is “just a tree”

But actually it is:

> A **carefully constrained array** that encodes a tree using index math

And its power comes from:
- minimal structure
- maximum efficiency