
# Understanding LRU / LFU Cache from First Principles (Deep Execution-Level Guide)

---

## 1. Title

**Understanding LRU & LFU Cache from First Principles: Designing O(1) Memory Systems**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- HashMaps
- Doubly Linked Lists
- Pointers and structs in Go
- Time complexity basics

---

## 3. Problem Definition

---

### The Core Problem

We want to:

> Store data with **fast access (O(1))** while limiting memory size.

---

### Example

Cache size = 2

Operations:

```
put(1, A)
put(2, B)
get(1) → A
put(3, C) → evict?
```

👉 Which one do we remove?

---

### Input / Output

- Input:
  - key-value operations
- Output:
  - fast get/put + eviction policy

---

## 🧠 4. First Principles Thinking

---

### Why Does This Problem Exist?

Memory is limited:
- RAM
- CPU cache
- disk cache

---

### Naive Solution

Store everything:
```
map[key] = value
```

❌ Problem:
- memory grows infinitely

---

### Add Limit

When full:
```
remove random item
```

❌ Problem:
- removes useful data

---

## 🧭 5. Build the Intuition

---

### Key Idea

We need:
> A rule to decide what to remove

---

### Strategy 1: LRU (Least Recently Used)

Remove:
> item not used recently

---

### Strategy 2: LFU (Least Frequently Used)

Remove:
> item used least times

---

### Step 1: Need Fast Lookup

```
map[key] → node
```

---

### Step 2: Need Order Tracking

We need:
- recency order (LRU)
- frequency order (LFU)

---

### ⚠️ Disambiguation

| Concept | Meaning |
|--------|--------|
| Cache | storage |
| Eviction | removal |
| Recency | last access time |
| Frequency | number of accesses |

---

## 🧠 6. Mental Model

---

### LRU = "Recently Touched Moves to Front"

Think:
```
Most recent ←→ Least recent
```

---

### Data Structure

```
HashMap + Doubly Linked List
```

---

### Why BOTH?

| Structure | Role |
|----------|------|
| HashMap | O(1) lookup |
| DLL | maintain order |

---

### Invariant

> Head = most recently used  
> Tail = least recently used  

---

## 🔧 7. Algorithm Definition

---

### LRU Operations

---

#### GET

```
if key not found → return -1

move node to front
return value
```

---

#### PUT

```
if key exists:
    update value
    move to front

else:
    if full:
        remove tail

    insert new node at front
```

---

## 💻 8. Implementation (Golang)

---

```go
package main

import "fmt"

type Node struct {
	key, value int
	prev, next *Node
}

type LRUCache struct {
	capacity int
	cache    map[int]*Node
	head     *Node
	tail     *Node
}

func Constructor(capacity int) LRUCache {
	head := &Node{}
	tail := &Node{}
	head.next = tail
	tail.prev = head

	return LRUCache{
		capacity: capacity,
		cache:    make(map[int]*Node),
		head:     head,
		tail:     tail,
	}
}

// Remove node from list
func (l *LRUCache) remove(node *Node) {
	node.prev.next = node.next
	node.next.prev = node.prev
}

// Insert node after head
func (l *LRUCache) insert(node *Node) {
	node.next = l.head.next
	node.prev = l.head
	l.head.next.prev = node
	l.head.next = node
}

func (l *LRUCache) Get(key int) int {
	if node, ok := l.cache[key]; ok {
		l.remove(node)
		l.insert(node)
		return node.value
	}
	return -1
}

func (l *LRUCache) Put(key int, value int) {
	if node, ok := l.cache[key]; ok {
		node.value = value
		l.remove(node)
		l.insert(node)
		return
	}

	if len(l.cache) == l.capacity {
		// remove LRU (tail.prev)
		lru := l.tail.prev
		l.remove(lru)
		delete(l.cache, lru.key)
	}

	node := &Node{key: key, value: value}
	l.cache[key] = node
	l.insert(node)
}

func main() {
	cache := Constructor(2)

	cache.Put(1, 10)
	cache.Put(2, 20)

	fmt.Println(cache.Get(1)) // 10

	cache.Put(3, 30) // evicts key 2

	fmt.Println(cache.Get(2)) // -1
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Initial

```
capacity = 2
list: head <-> tail
map: {}
```

---

### Put(1,10)

```
list: head <-> 1 <-> tail
map: {1}
```

---

### Put(2,20)

```
list: head <-> 2 <-> 1 <-> tail
```

---

### Get(1)

Move 1 to front:

```
list: head <-> 1 <-> 2 <-> tail
```

---

### Put(3,30)

Evict tail.prev → 2

```
list: head <-> 3 <-> 1 <-> tail
```

---

### Internal State Visualization

| Key | Position |
|-----|--------|
| 3 | most recent |
| 1 | older |
| 2 | removed |

---

## ⏱️ 10. Complexity Analysis

---

### Time

| Operation | Complexity |
|----------|------------|
| Get | O(1) |
| Put | O(1) |

---

### Why O(1)?

- HashMap → direct access
- DLL → constant pointer updates

---

### Space

```
O(capacity)
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ limited memory systems  
✅ caching layers  
✅ frequently reused data  

---

### When NOT to Use

❌ need exact ordering  
❌ no memory constraint  

---

### Alternatives

| Strategy | Behavior |
|---------|--------|
| FIFO | remove oldest inserted |
| Random | simple but inefficient |
| LFU | remove least used |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Forgetting to update order on GET

→ breaks LRU logic

---

### ❌ Not removing from map

→ memory leak

---

### ❌ Pointer mistakes

→ broken linked list

---

## 🌍 13. Real-World Usage

---

### Web Browsers

- cache pages

---

### Databases

- query caching

---

### Operating Systems

- page replacement

---

### Distributed Systems

- Redis uses LRU/LFU

---

## 🚀 14. Variations and Extensions

---

### LFU Cache

Track:
```
frequency count
```

More complex:
- hashmap + frequency buckets

---

### TTL Cache

Expire after time

---

### ARC Cache

Adaptive strategy

---

## 🔁 15. Recap (Feynman Compression)

A cache stores limited data and must decide what to remove. LRU removes the least recently used item using a combination of a hashmap and a doubly linked list to achieve O(1) operations.

---

## 🧩 16. Exercises

---

### Easy

1. Implement LRU without linked list  
2. Simulate cache operations  

---

### Medium

3. Implement LFU cache  

---

### Real-World Challenge

4. Build a web cache:
   - key = URL
   - value = HTML
   - eviction = LRU  

---

## 🧠 Final Insight

You might think cache is just:
> “store and remove”

But actually it is:

> A **carefully synchronized system of memory + time + structure**

Where correctness depends on:
- keeping order accurate
- maintaining O(1) guarantees

