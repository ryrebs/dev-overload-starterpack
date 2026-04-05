# Understanding Aho–Corasick from First Principles (Ultra Deep Execution-Level Guide)

---

## 1. Title

**Understanding Aho–Corasick from First Principles: Matching Multiple Patterns in Linear Time**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Strings and arrays
- Trie (prefix tree)
- BFS (queue)
- Basic understanding of KMP (helpful but not required)

---

## 3. Problem Definition

---

### The Core Problem

We want to:

> Find **multiple patterns** inside a text efficiently.

---

### Example

```
Text: "ushers"
Patterns: ["he", "she", "his", "hers"]
```

---

### Output

```
"she" at index 1
"he" at index 2
"hers" at index 2
```

---

### Input / Output

- Input:
  - list of patterns
  - text string
- Output:
  - all matches with positions

---

## 🧠 4. First Principles Thinking

---

### Why Does This Problem Exist?

In real systems:
- we search many patterns at once
- e.g., keywords, virus signatures

---

### Naive Approach

For each pattern:
```
run KMP or naive search
```

---

### Complexity

```
O(k * n)
```

where:
- k = number of patterns
- n = text length

---

### ❌ Problem

Too slow when:
```
k is large (e.g., thousands)
```

---

### Hidden Inefficiency

We repeatedly scan:
```
same text multiple times
```

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Combine Patterns

Instead of separate searches:

> Put all patterns into one structure

---

### Step 2: Use Trie

Insert:

```
he, she, his, hers
```

---

### Structure

```
        root
       /   \
      h     s
     / \     \
    e   i     h
        |     |
        s     e
             / \
            r   (end)
            |
            s
```

---

### ⚠️ Disambiguation

| Term | Meaning |
|------|--------|
| Trie node | character node |
| Path | prefix |
| isEnd | pattern ends here |

---

### Step 3: Problem Still Exists

Trie helps:
```
match prefixes
```

But mismatch still:
```
forces restart
```

---

### Step 4: Borrow Idea from KMP

👉 Introduce:
```
failure links
```

---

### Step 5: Failure Link Meaning

If mismatch:

```
jump to longest valid suffix
```

---

### Example

For "she":

```
failure("she") → "he"
```

---

### 🔥 Key Insight

> Reuse previous partial matches

---

### Step 6: Build Failure Links Using BFS

- start from root
- propagate fallback links

---

## 🧠 6. Mental Model

---

### Aho-Corasick = “Trie + KMP”

- Trie → structure
- Failure links → recovery

---

### Invariant

At each step:
```
current node = longest valid suffix match
```

---

### Analogy

Like:
```
walking in trie,
if you fail → follow fallback path
```

---

### Why It Works

Because:
- failure links preserve information
- no need to restart matching

---

## 🔧 7. Algorithm Definition

---

### Build Trie

```
insert all patterns
```

---

### Build Failure Links

```
use BFS
set root children → root
propagate links
```

---

### Search

```
for each char in text:
    follow trie edges
    if mismatch → follow failure link

    if node has output:
        report matches
```

---

## 💻 8. Implementation (Golang)

---

```go
package main

import (
	"container/list"
	"fmt"
)

type Node struct {
	children map[rune]*Node
	fail     *Node
	output   []string
}

func NewNode() *Node {
	return &Node{
		children: make(map[rune]*Node),
	}
}

// Build Trie
func buildTrie(patterns []string) *Node {
	root := NewNode()

	for _, p := range patterns {
		node := root
		for _, ch := range p {
			if node.children[ch] == nil {
				node.children[ch] = NewNode()
			}
			node = node.children[ch]
		}
		node.output = append(node.output, p)
	}

	return root
}

// Build Failure Links
func buildFailure(root *Node) {
	queue := list.New()

	// Initialize root children
	for _, child := range root.children {
		child.fail = root
		queue.PushBack(child)
	}

	for queue.Len() > 0 {
		current := queue.Remove(queue.Front()).(*Node)

		for ch, next := range current.children {
			failNode := current.fail

			for failNode != nil && failNode.children[ch] == nil {
				failNode = failNode.fail
			}

			if failNode == nil {
				next.fail = root
			} else {
				next.fail = failNode.children[ch]
				next.output = append(next.output, next.fail.output...)
			}

			queue.PushBack(next)
		}
	}
}

// Search
func search(text string, root *Node) {
	node := root

	for i, ch := range text {
		for node != root && node.children[ch] == nil {
			node = node.fail
		}

		if node.children[ch] != nil {
			node = node.children[ch]
		}

		if len(node.output) > 0 {
			for _, match := range node.output {
				fmt.Printf("Found %s at index %d\n", match, i-len(match)+1)
			}
		}
	}
}

func main() {
	patterns := []string{"he", "she", "his", "hers"}
	root := buildTrie(patterns)

	buildFailure(root)

	text := "ushers"
	search(text, root)
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Text: "ushers"

---

### Step-by-step

---

#### i=0 → 'u'

```
no match → stay at root
```

---

#### i=1 → 's'

```
move to 's'
```

---

#### i=2 → 'h'

```
move to 'sh'
```

---

#### i=3 → 'e'

```
move to 'she'
output: ["she", "he"]
```

---

### ⚠️ Hidden Insight

You might think:
> only "she" matches

But actually:
> failure link gives "he"

---

#### i=4 → 'r'

```
follow failure → match continues
```

---

#### i=5 → 's'

```
match "hers"
```

---

## ⏱️ 10. Complexity Analysis

---

### Build Trie

```
O(sum of pattern lengths)
```

---

### Build Failure Links

```
O(total nodes)
```

---

### Search

Each character processed once:

```
O(n)
```

---

### Total

```
O(n + total pattern length)
```

---

### Space

```
O(total nodes)
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ multiple pattern search  
✅ large text  
✅ many keywords  

---

### When NOT to Use

❌ single pattern → use KMP  
❌ very small input  

---

### Alternatives

| Algorithm | Use |
|----------|-----|
| KMP | single pattern |
| Rabin-Karp | hashing |
| Naive | simple |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Forgetting failure links

---

### ❌ Not merging outputs

---

### ❌ Infinite loop on fail

---

### ❌ Wrong root handling

---

## 🌍 13. Real-World Usage

---

### Search Engines

- keyword matching

---

### Antivirus Software

- signature detection

---

### Spam Filters

- detecting phrases

---

### DNA Analysis

- multiple sequence matching

---

## 🚀 14. Variations and Extensions

---

### Case-insensitive matching

---

### Unicode support

---

### Streaming input

---

### Weighted matches

---

## 🔁 15. Recap (Feynman Compression)

Aho-Corasick builds a trie of patterns and uses failure links to efficiently match multiple patterns in a single pass through the text.

---

## 🧠 Final Insight

You might think Aho-Corasick is:
> “just Trie + KMP”

But actually it is:

> A **system that preserves partial matches across multiple patterns simultaneously**

Where:
- trie organizes patterns
- failure links reuse work
- search becomes linear