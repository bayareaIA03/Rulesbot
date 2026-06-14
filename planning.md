# RulesBot — Planning Doc

Use this file to record your design decisions as you work through the lab.
There are no wrong answers — write enough that you could explain your reasoning to another group.

---

## Chunking Strategy

**Chunk size:**


**Overlap:**


**Why this strategy fits rule book text:**


---

## Retrieval Observations

After implementing retrieval, try these test queries and record what comes back:

| Query | Top result game | Does it make sense? |
|-------|----------------|---------------------|
| "How do you win?" | | |
| "What happens when you roll a 7?" | | |
| "Can two players share a route?" | | |

**Anything surprising?**


---

## Response Quality

After implementing generation, try 2–3 questions and assess the answers:

| Query | Answer accurate? | Properly grounded? | Cited the right game? |
|-------|-----------------|-------------------|----------------------|
| | | | |
| | | | |

**What would you change about the prompt to improve grounding?**

## Domain

Student reviews of professors at CSU East Bay

I chose this domain because official course catalogs explain what each CS class covers, but they usually do not explain what students actually experience with each professor. Student reviews can help answer practical questions about teaching style, workload, exam difficulty, grading fairness, feedback quality, and whether students recommend taking a class with that professor.

This information is hard to find because it is spread across different places like Rate My Professors, Reddit threads, forums, and informal student conversations. My system will make that information searchable so students can ask plain-language questions and get grounded answers based on the documents I collected.

---