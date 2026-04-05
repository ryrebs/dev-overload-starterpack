# Understanding Hashing (HashMap / HashSet) from First Principles

---

## 1. Title

**Understanding Hashing (HashMap / HashSet) from First Principles**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Arrays and slices
- Basic time complexity (Big-O)
- Functions and structs in Go
- Basic memory concepts

---

## 3. Problem Definition

### The Core Problem

We want to **store and retrieve data quickly using a key**.

### Example

You want to store:

| Name | Age |
|------|-----|
| Alice | 25 |
| Bob | 30 |

Then quickly answer:
> “What is Alice’s age?”

### Input / Output

- Input: key-value pairs (e.g., `"Alice" → 25`)
- Output: fast lookup of value by key

---

## 🧠 4. First Principles Thinking

### Why Does This Problem Exist?

We need **fast lookup**.

If we use an array:

```go
[ ("Alice", 25), ("Bob", 30) ]
```

To find `"Alice"`:
- Check index 0 → maybe
- Check index 1 → maybe

This is **O(n)**.

---

### Why Is This Hard?

Because:
- Keys are arbitrary (strings, numbers)
- Arrays use **indexes (integers)**

👉 Problem:
> How do we convert a key → index?

---

### Naive Solution

Search linearly:
```go
for each item:
    if item.key == target:
        return value
```

❌ Problem:
- Too slow for large data

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Use Indexing (Fast)

Arrays are fast:
```go
arr[5] // O(1)
```

So we want:
> key → index → value

---

### Step 2: Introduce a Hash Function

We define:

```
hash(key) → integer index
```

Example:
```
hash("Alice") → 3
```

Now:
```go
arr[3] = 25
```

---

### ⚠️ Important Distinction

| Concept | Meaning |
|--------|--------|
| Key | "Alice" |
| Hash | some number (e.g., 12345) |
| Index | position in array (e.g., 3) |

👉 **Hash ≠ Index**
- Hash can be large
- Index is within array size

---

### Step 3: Compress Hash → Index

We use modulo:

```
index = hash(key) % array_size
```

⚠️ Hidden Detail:
- This **loses information**
- Many keys can map to same index

---

### Step 4: Collision Problem

Example:
```
hash("Alice") % 5 = 3
hash("Bob")   % 5 = 3
```

Now both want index 3.

👉 This is called a **collision**

---

### Step 5: Handle Collisions (Buckets)

Instead of storing one value:
```go
arr[3] = [ ("Alice", 25), ("Bob", 30) ]
```

👉 Each index holds a **list (bucket)**

---

### Key Insight

We transformed:
```
O(n) search → O(1) average lookup
```

---

## 🧠 6. Mental Model

Think of a **mailroom with lockers**:

- Key = person’s name
- Hash = locker number
- Bucket = list of letters in same locker

### Invariant

> All keys that hash to same index are stored together

### Why It Works

- Hash spreads keys “randomly”
- Buckets stay small (on average)

---

## 🔧 7. Algorithm Definition

### Insert

1. Compute hash of key
2. Convert to index
3. Go to bucket
4. Add (key, value)

---

### Lookup

1. Compute hash
2. Convert to index
3. Search bucket for key

---

### Pseudocode

```
function put(key, value):
    index = hash(key) % size
    bucket = table[index]

    for each (k, v) in bucket:
        if k == key:
            update value
            return

    append (key, value)

function get(key):
    index = hash(key) % size
    bucket = table[index]

    for each (k, v):
        if k == key:
            return v

    return not found
```

---

## 💻 8. Implementation (Golang)

```go
package main

import (
	"fmt"
)

// KeyValue pair
type Entry struct {
	Key   string
	Value int
}

// HashMap structure
type HashMap struct {
	Buckets [][]Entry
	Size    int
}

// Create new HashMap
func NewHashMap(size int) *HashMap {
	buckets := make([][]Entry, size)
	return &HashMap{
		Buckets: buckets,
		Size:    size,
	}
}

// Simple hash function
func (hm *HashMap) hash(key string) int {
	hash := 0
	for _, ch := range key {
		hash += int(ch)
	}
	return hash % hm.Size
}

// Put key-value
func (hm *HashMap) Put(key string, value int) {
	index := hm.hash(key)

	bucket := hm.Buckets[index]

	// Check if key exists
	for i, entry := range bucket {
		if entry.Key == key {
			// Update existing
			hm.Buckets[index][i].Value = value
			return
		}
	}

	// Add new entry
	hm.Buckets[index] = append(bucket, Entry{key, value})
}

// Get value
func (hm *HashMap) Get(key string) (int, bool) {
	index := hm.hash(key)
	bucket := hm.Buckets[index]

	for _, entry := range bucket {
		if entry.Key == key {
			return entry.Value, true
		}
	}

	return 0, false
}

func main() {
	hm := NewHashMap(5)

	hm.Put("Alice", 25)
	hm.Put("Bob", 30)

	val, ok := hm.Get("Alice")
	if ok {
		fmt.Println("Alice:", val)
	}
}
```

---

## 🧪 9. Walkthrough Example

Insert `"Alice"`

### Step-by-step:

1. Compute hash:
```
"A" + "l" + "i" + "c" + "e"
= 65 + 108 + 105 + 99 + 101 = 478
```

2. Index:
```
478 % 5 = 3
```

3. Insert:
```
Buckets:
[ [], [], [], [("Alice",25)], [] ]
```

---

Insert `"Bob"`

```
66 + 111 + 98 = 275
275 % 5 = 0
```

```
[ [("Bob",30)], [], [], [("Alice",25)], [] ]
```

---

### Internal State

| Index | Bucket |
|------|--------|
| 0 | Bob |
| 3 | Alice |

---

## ⏱️ 10. Complexity Analysis

### Time Complexity

#### Average Case

- Insert: O(1)
- Lookup: O(1)

Why?
- Buckets are small

---

#### Worst Case

All keys collide:

```
O(n)
```

👉 Hash function quality matters

---

### Space Complexity

- O(n) for storing elements
- Extra space for buckets

---

## ⚖️ 11. Tradeoffs and Alternatives

### When to Use

✅ Fast lookups  
✅ Unique key mapping  
✅ Frequency counting  

---

### When NOT to Use

❌ Need ordered data  
❌ Need range queries  

---

### Alternatives

| Structure | Use Case |
|----------|--------|
| Array | Small, index-based |
| TreeMap | Sorted keys |
| Trie | Prefix matching |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Confusing Hash and Index

You might think:
> “hash gives position”

Actually:
> hash must be reduced → index

---

### ❌ Ignoring Collisions

Without buckets:
- Data gets overwritten

---

### ❌ Poor Hash Function

Bad:
```
hash = len(key)
```

👉 Causes many collisions

---

### ❌ Forgetting Update Logic

Must handle:
```
existing key → update value
```

---

## 🌍 13. Real-World Usage

---

### Databases

- Key-value stores (Redis)
- Indexing records

---

### Caching

```
userID → session data
```

---

### Compilers

- Symbol tables

---

### Networking

- Routing tables

---

## 🚀 14. Variations and Extensions

---

### HashSet

Only store keys:

```go
map[string]bool
```

---

### Open Addressing

Instead of buckets:
- Probe next slot

---

### Dynamic Resizing

When load factor increases:
- Resize array
- Rehash all keys

---

### Frequency Counter

```
"apple" → 3
```

---

## 🔁 15. Recap (Feynman Compression)

Hashing converts a key into an array index using a hash function. Since multiple keys may map to the same index, we store them in buckets. This allows us to achieve fast (average O(1)) insertion and lookup.

---

## 🧩 16. Exercises

---

### Easy

1. Implement a HashSet using the above structure  
2. Count frequency of characters in a string  

---

### Medium

3. Find first non-repeating character using a hash map  

---

### Real-World Challenge

4. Design a simple cache system:
   - Key → value
   - Limit size
   - Remove least-used items  

---

## 🧠 Final Insight

You might think hashing is just a “map,” but it's actually:

> A clever way to trade **memory + randomness** for **speed**

And the entire system depends on:
- good hashing
- collision handling
- maintaining small buckets
