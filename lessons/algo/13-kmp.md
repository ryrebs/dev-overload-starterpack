

# Understanding KMP (Knuth-Morris-Pratt) from First Principles (Master-Level Deep Execution Guide)

---

## 1. Title

**Understanding KMP from First Principles: How to Turn Pattern Matching from Repetition into Memory**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Strings and arrays
- Index-based iteration
- Basic pattern matching
- Understanding of loops and conditionals

---

## 3. Problem Definition

---

### The Core Problem

We want to:

> Efficiently find a pattern inside a text **without re-checking characters unnecessarily**

---

### Example

```
Text:    "aaacaaaaac"
Pattern: "aaaa"
```

---

### Expected Output

```
Matches at indices: [3, 4]
```

---

### Input / Output

- Input:
  - text string (length n)
  - pattern string (length m)
- Output:
  - all match starting indices

---

## 🧠 4. First Principles Thinking

---

### Naive Algorithm

At every position:

```
try to match pattern
```

---

### Example Breakdown

```
Text:    aaacaaaaac
Pattern: aaaa
```

Matching:

```
aaaa vs aaac → mismatch at last char
```

---

### What Happens Next?

Naive approach:
```
shift by 1 → restart from scratch
```

---

### ❌ Core Problem

We already know:
```
first 3 characters matched
```

But we:
```
throw away that knowledge
```

---

### Complexity

```
O(n * m)
```

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Ask Key Question

> When mismatch happens, how much do we already know?

---

### Step 2: Analyze Pattern Internally

Pattern:
```
aaaa
```

Observation:
```
prefix = suffix = "aaa"
```

---

### ⚠️ Disambiguation

| Term | Meaning |
|------|--------|
| Prefix | start of string |
| Suffix | end of string |
| Proper prefix | not full string |
| LPS[i] | longest prefix = suffix up to i |

---

### Step 3: Build LPS Table

---

#### Pattern: "aaaa"

```
Index:   0 1 2 3
Char:    a a a a
LPS:     0 1 2 3
```

---

### Step 4: What LPS Means

At index 3:
```
LPS[3] = 3
```

Meaning:
```
first 3 chars = last 3 chars
```

---

### Step 5: Use This Information

Instead of restarting:
```
jump to LPS value
```

---

### 🔥 Critical Insight

> We reuse matched prefix instead of re-checking

---

## 🧠 6. Mental Model

---

### KMP = "Sliding Pattern with Memory"

- text pointer always moves forward
- pattern pointer jumps intelligently

---

### Invariant

> All matched characters before mismatch are still valid information

---

### Analogy

Think of:
```
pattern = elastic band
```

When mismatch:
- it snaps back to valid prefix

---

## 🔧 7. Algorithm Definition

---

### Step 1: Build LPS

```
length = 0
i = 1

while i < m:
    if match:
        length++
        lps[i] = length
        i++
    else:
        if length != 0:
            length = lps[length-1]
        else:
            lps[i] = 0
            i++
```

---

### Step 2: Search

```
i = 0 (text)
j = 0 (pattern)

while i < n:
    if match:
        i++, j++

    if j == m:
        record match
        j = lps[j-1]

    else if mismatch:
        if j != 0:
            j = lps[j-1]
        else:
            i++
```

---

## 💻 8. Implementation (Golang)

---

```go
package main

import "fmt"

// Build LPS array
func buildLPS(pattern string) []int {
	lps := make([]int, len(pattern))
	length := 0

	for i := 1; i < len(pattern); {
		if pattern[i] == pattern[length] {
			length++
			lps[i] = length
			i++
		} else {
			if length != 0 {
				length = lps[length-1]
			} else {
				lps[i] = 0
				i++
			}
		}
	}
	return lps
}

// KMP search
func kmp(text, pattern string) []int {
	lps := buildLPS(pattern)
	result := []int{}

	i, j := 0, 0

	for i < len(text) {
		if text[i] == pattern[j] {
			i++
			j++
		}

		if j == len(pattern) {
			result = append(result, i-j)
			j = lps[j-1]
		} else if i < len(text) && text[i] != pattern[j] {
			if j != 0 {
				j = lps[j-1]
			} else {
				i++
			}
		}
	}

	return result
}

func main() {
	text := "aaacaaaaac"
	pattern := "aaaa"

	fmt.Println(kmp(text, pattern))
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Input

```
Text:    aaacaaaaac
Pattern: aaaa
```

---

### LPS

```
[0,1,2,3]
```

---

### Step-by-step Matching

---

#### Step 1

```
i=0,j=0 → match
i=1,j=1 → match
i=2,j=2 → match
i=3,j=3 → mismatch (c vs a)
```

---

#### Instead of Restarting

```
j = lps[2] = 2
```

---

#### Continue

```
reuse previous match
```

---

### ⚠️ Hidden Flow

We:
- preserved partial match
- avoided re-checking

---

## ⏱️ 10. Complexity Analysis

---

### Time

- LPS build: O(m)
- Search: O(n)

Total:
```
O(n + m)
```

---

### Why Linear?

Each character:
- visited at most twice

---

### Space

```
O(m)
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ large text  
✅ repeated patterns  
✅ substring search  

---

### When NOT to Use

❌ tiny inputs  
❌ simple matching  

---

### Alternatives

| Algorithm | Use |
|----------|-----|
| Naive | small data |
| Rabin-Karp | hashing |
| Boyer-Moore | practical speed |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Misunderstanding LPS

---

### ❌ Off-by-one errors

---

### ❌ Restarting instead of fallback

---

### ❌ Ignoring partial matches

---

## 🌍 13. Real-World Usage

---

### Text Editors

- search feature

---

### DNA Analysis

- sequence matching

---

### Security

- pattern detection

---

### Log Analysis

- substring scanning

---

## 🚀 14. Variations and Extensions

---

### Multiple pattern search

---

### Streaming KMP

---

### Wildcard matching

---

## 🔁 15. Recap (Feynman Compression)

KMP avoids rechecking characters by remembering how much of the pattern has already matched. Using the LPS array, it jumps intelligently instead of restarting, achieving linear time complexity.

---

## 🧩 16. Exercises

---

### Easy

1. Build LPS array  
2. Find first occurrence  

---

### Medium

3. Count overlapping matches  

---

### Real-World Challenge

4. Build text search tool:
   - highlight all matches  
   - support large files  

---

## 🧠 Final Insight

You might think KMP is:
> “just faster matching”

But actually it is:

> A transformation from **stateless matching → stateful matching**

Where:
- memory replaces repetition
- structure replaces brute force

Master this → you understand efficient string processing deeply 🚀
