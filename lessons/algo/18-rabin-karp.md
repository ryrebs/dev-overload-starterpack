
# Understanding Rabin–Karp from First Principles (Ultra Deep Execution-Level Guide)

---

## 1. Title

**Understanding Rabin–Karp from First Principles: Turning String Matching into Hash Comparison**

---

## 2. Who This Is For

**Skill Level:** Intermediate  
**Prerequisites:**
- Strings and arrays
- Basic hashing concepts
- Modular arithmetic (important)
- Loops and indexing

---

## 3. Problem Definition

---

### The Core Problem

We want to:

> Find all occurrences of a **pattern** inside a **text efficiently**

---

### Example

```
Text:    "ababcabcab"
Pattern: "abcab"
```

Output:
```
Index: 2
```

---

### Input / Output

- Input:
  - text string (length n)
  - pattern string (length m)
- Output:
  - indices where pattern appears

---

## 🧠 4. First Principles Thinking

---

### Naive Approach

At every position:
```
compare pattern character by character
```

---

### Complexity

```
O(n * m)
```

---

### ❌ Problem

Repeated comparisons:

```
same substring checked multiple times
```

---

### Key Observation

> Substrings overlap heavily

---

## 🧭 5. Build the Intuition (Step-by-Step)

---

### Step 1: Replace String Comparison

Instead of:
```
compare strings directly
```

We:
```
compare hash values
```

---

### ⚠️ Disambiguation

| Term | Meaning |
|------|--------|
| String comparison | char-by-char |
| Hash | numeric representation |
| Collision | different strings → same hash |

---

### Step 2: Hash Function

Example:

```
"abc" → hash value
```

---

### Step 3: Sliding Window

We compute:
```
hash of each substring of length m
```

---

### ❌ Problem

Recomputing hash each time:
```
O(m) per window → O(n*m)
```

---

### Step 4: Rolling Hash

Instead of recomputing:

```
reuse previous hash
```

---

### Formula

```
hash_next = (hash_prev - left_char * power) * base + new_char
```

---

### ⚠️ Critical Disambiguation

| Term | Meaning |
|------|--------|
| base | multiplier (e.g., 31) |
| power | base^(m-1) |
| modulo | prevent overflow |

---

### 🔥 Key Insight

> Shift window efficiently using math

---

## 🧠 6. Mental Model

---

### Rabin-Karp = “Sliding Fingerprint”

- each substring → fingerprint
- compare fingerprints instead of full strings

---

### Invariant

> Hash represents substring uniquely (with high probability)

---

### Why It Works

- rolling hash avoids recomputation
- hash comparison is O(1)

---

## 🔧 7. Algorithm Definition

---

### Pseudocode

```
compute patternHash
compute first window hash

for i in range:
    if hashes match:
        verify string

    update hash using rolling formula
```

---

## 💻 8. Implementation (Golang)

---

```go
package main

import "fmt"

func rabinKarp(text, pattern string) []int {
	n := len(text)
	m := len(pattern)

	if m > n {
		return []int{}
	}

	base := 31
	mod := 1000000007

	patternHash := 0
	windowHash := 0
	power := 1

	// compute base^(m-1)
	for i := 0; i < m-1; i++ {
		power = (power * base) % mod
	}

	// initial hash
	for i := 0; i < m; i++ {
		patternHash = (patternHash*base + int(pattern[i])) % mod
		windowHash = (windowHash*base + int(text[i])) % mod
	}

	result := []int{}

	for i := 0; i <= n-m; i++ {

		if patternHash == windowHash {
			// verify to avoid collision
			match := true
			for j := 0; j < m; j++ {
				if text[i+j] != pattern[j] {
					match = false
					break
				}
			}
			if match {
				result = append(result, i)
			}
		}

		if i < n-m {
			// remove left char
			windowHash = (windowHash - int(text[i])*power%mod + mod) % mod

			// add new char
			windowHash = (windowHash*base + int(text[i+m])) % mod
		}
	}

	return result
}

func main() {
	text := "ababcabcab"
	pattern := "abcab"

	fmt.Println(rabinKarp(text, pattern))
}
```

---

## 🧪 9. Walkthrough Example (Execution-Level)

---

### Input

```
text = "ababc"
pattern = "abc"
```

---

### Step 1: Compute Initial Hash

```
patternHash("abc")
windowHash("aba")
```

---

### Step 2: Slide Window

```
remove 'a'
add 'c'
```

---

### Rolling Hash Update

```
windowHash = (oldHash - 'a'*power) * base + 'c'
```

---

### ⚠️ Hidden Insight

You might think:
> subtraction removes value

Actually:
> we remove weighted contribution

---

### Internal State

| Window | Hash |
|--------|------|
| "aba" | H1 |
| "bab" | H2 |
| "abc" | H3 |

Match at:
```
i = 2
```

---

## ⏱️ 10. Complexity Analysis

---

### Time

- Hash computation: O(n)
- Verification (rare): O(m)

---

### Average

```
O(n + m)
```

---

### Worst Case

```
O(n * m) (many collisions)
```

---

### Space

```
O(1)
```

---

## ⚖️ 11. Tradeoffs and Alternatives

---

### When to Use

✅ multiple pattern searches  
✅ large text  
✅ substring detection  

---

### When NOT to Use

❌ very small inputs  
❌ collision-sensitive systems  

---

### Alternatives

| Algorithm | Use |
|----------|-----|
| KMP | deterministic |
| Naive | simple |
| Boyer-Moore | practical speed |

---

## ⚠️ 12. Common Mistakes

---

### ❌ Ignoring modulo

→ overflow

---

### ❌ Not verifying matches

→ false positives

---

### ❌ Wrong power calculation

---

### ❌ Negative hash values

---

## 🌍 13. Real-World Usage

---

### Plagiarism Detection

- substring matching

---

### Search Engines

- pattern scanning

---

### Malware Detection

- signature matching

---

### Bioinformatics

- DNA sequence matching

---

## 🚀 14. Variations and Extensions

---

### Multiple Patterns

---

### Double Hashing

- reduce collisions

---

### 2D Rabin-Karp

- matrix matching

---

## 🔁 15. Recap (Feynman Compression)

Rabin-Karp converts strings into numbers (hashes) and compares hashes instead of characters. Using a rolling hash, it efficiently updates the hash for each substring, allowing fast pattern matching.

---

## 🧠 Final Insight

You might think Rabin-Karp is:
> “just hashing”

But actually it is:

> A **mathematical optimization of sliding window comparison**

Where:
- structure replaces brute force
- math replaces repetition
