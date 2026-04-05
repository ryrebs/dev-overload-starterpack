You are an expert in algorithms, data structures, and computer science education.

Your task is to create a **high-quality, deeply structured tutorial** about the following algorithm:

Dijkstra

The tutorial must:

* be technically correct and aligned with standard CS knowledge
* include working, runnable code
* teach from first principles (not memorization)
* build deep intuition and problem-solving ability
* reflect how algorithms are used in real-world systems

---

## 🎯 PRIMARY GOAL

By the end of this tutorial, the reader should be able to:

1. Understand the problem the algorithm solves
2. Derive the algorithm from first principles
3. Implement it from scratch (without copying)
4. Analyze its time and space complexity
5. Recognize when to use (and not use) it
6. Adapt it to variations of the problem

---

## 🧩 STRUCTURE (FOLLOW EXACTLY)

### 1. Title

Clear and specific (e.g., “Understanding Dijkstra’s Algorithm from First Principles”).

---

### 2. Who This Is For

* skill level (e.g., beginner/intermediate)
* required background (arrays, recursion, graphs, etc.)

---

### 3. Problem Definition

* describe the problem in plain language
* include a small concrete example
* define inputs and outputs clearly

---

## 🧠 4. First Principles Thinking

Explain:

* Why does this problem exist?
* What makes it hard?
* What would a naive solution look like?
* Why does the naive solution fail or scale poorly?

---

## 🧭 5. Build the Intuition (Step-by-Step)

Derive the algorithm logically:

* Start from naive thinking
* Gradually refine the idea
* Introduce key insights one at a time
* Show how each insight improves the solution

DO NOT jump directly to the final algorithm.

---

## 🧠 6. Mental Model

Explain how to think about the algorithm:

* what is happening at each step?
* what invariant is maintained?
* what guarantees correctness?

Use analogies if helpful.

---

## 🔧 7. Algorithm Definition

Present the final algorithm:

* clear step-by-step logic
* pseudocode (clean and readable)

---

## 💻 8. Implementation (Runnable Code)

Provide:

* clean, idiomatic code (Python preferred unless specified)
* no shortcuts or magic
* comments explaining key parts

---

## 🧪 9. Walkthrough Example

Take a sample input and:

* walk through the algorithm step-by-step
* show intermediate states
* explain decisions

---

## ⏱️ 10. Complexity Analysis

Explain:

* time complexity (best, average, worst)
* space complexity

Derive it step-by-step (not just state it).

---

## ⚖️ 11. Tradeoffs and Alternatives

Explain:

* when this algorithm is ideal
* when it is not
* alternative approaches
* comparison with similar algorithms

---

## ⚠️ 12. Common Mistakes

* typical implementation bugs
* edge cases
* incorrect assumptions

---

## 🌍 13. Real-World Usage

Explain how this algorithm appears in:

* real systems
* industry applications
* practical scenarios

---

## 🚀 14. Variations and Extensions

Include:

* modified versions of the problem
* how the algorithm adapts
* related problems

---

## 🔁 15. Recap (Feynman Compression)

Explain the entire algorithm simply in a few sentences as if teaching a beginner.

---

## 🧩 16. Exercises

Include:

* 2 easy problems
* 1 medium problem
* 1 real-world-style challenge

---

## 🧠 LEARNING DESIGN RULES

You MUST apply:

* First Principles Thinking
* Feynman Technique (simple → technical → example)
* Progressive Disclosure (build gradually)
* Worked Example + Variation
* Error-based learning (show failure cases)

---

## ⚙️ TECHNICAL REQUIREMENTS

* Code must be correct and runnable
* Avoid deprecated patterns
* Use clean structure and naming
* Prefer clarity over cleverness

---

## 🚫 DO NOT:

* jump directly to the final solution
* skip intuition
* provide only code without explanation
* assume prior deep knowledge
* overload with unnecessary theory

---

## OUTPUT QUALITY

The tutorial should feel like:

* a great professor teaching step-by-step
* combined with a senior engineer showing practical use

---

Language: Golang
Difficulty: Intermediate
Include visual intuition: Yes

## 🧠 DEEP UNDERSTANDING ENFORCEMENT (MANDATORY)

The tutorial MUST explicitly address and clarify hidden or subtle points that learners commonly misunderstand.

For every key concept or line of code, you MUST:

1. **Disambiguate Similar Concepts**
   - Clearly distinguish between related ideas (e.g., hash vs index, bucket vs value, reassignment vs accumulation)
   - Explicitly state what each term means in context

2. **Execution-Level Walkthrough**
   - Show step-by-step state changes with actual values
   - Demonstrate how variables evolve over time
   - Do not skip intermediate computations

3. **Explain “Why This Works”**
   - For every critical line or formula, explain:
     - what it does
     - why it is necessary
     - what would break if removed

4. **Expose Common Misconceptions**
   - Include statements like:
     - “You might think X, but actually Y”
   - Correct misunderstandings before they form

5. **Reveal Hidden Information Flow**
   - Explain how information is preserved or transformed (e.g., how reassignment still accumulates)
   - Show where information is lost (e.g., modulo compression)

6. **Internal State Visualization**
   - Show what data structures actually contain at runtime
   - Use concrete examples (arrays, buckets, memory layout)

7. **No Conceptual Jumps Allowed**
   - Do NOT skip from idea → result
   - Every transformation must be explained

Failure to include these will result in an incomplete tutorial.

Now create the tutorial and format it inside 4 backticks to avoid leaking markdown format outside, create each algorithm on difference markdown file