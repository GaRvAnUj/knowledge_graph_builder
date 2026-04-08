# Knowledge Graph Architecture & Visualization

## 1. Data Model Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH PUBLICATIONS GRAPH                   │
└─────────────────────────────────────────────────────────────────┘

NODE TYPES:
┌──────────────┐  ┌────────────┐  ┌───────────┐  ┌──────────────┐
│   Author     │  │   Paper    │  │   Field   │  │ University   │
│              │  │            │  │           │  │              │
│ name         │  │ title      │  │ name      │  │ name         │
│ email        │  │ year       │  │ description  ranking      │
│ research     │  │ abstract   │  │           │  │ country      │
│ Focus        │  │ doi        │  │           │  │              │
│              │  │ citations  │  │           │  │              │
└──────────────┘  └────────────┘  └───────────┘  └──────────────┘


RELATIONSHIP TYPES:

           Author
            / | \
           /  |  \
    WRITES/   |   \STUDIES
         /    |    \
        v    v      v
      Paper Field  University
        \    |     /
         \   |    /
    REFERENCES BELONGS_TO
         \   |   /
          \  |  /
           v v v

CO_AUTHORS_WITH (between Authors)
┌──────────┐  ────────────  ┌──────────┐
│ Author A │                │ Author B │
└──────────┘                └──────────┘
      |                           |
      └─── CO_AUTHORS_WITH ───────┘
```

---

## 2. Sample Extended Graph

```
                    ┌─────────────────┐
                    │ MIT             │
                    │ (University)    │
                    └────────┬────────┘
                             │
                    AFFILIATED_WITH
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      v                      v                      v
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│ Author 1     │  │ Author 2         │  │ Author 3     │
│ (Bengio)     │  │ (LeCun)          │  │ (Hinton)     │
└──┬───────────┘  └──────┬───────────┘  └────┬─────────┘
   │ WRITES             │ WRITES            │
   │                    │                   │
   ├────────────┬───────┘                   │
   │            │                           │
   v            v                           v
┌──────────────────────────┐    ┌──────────────────────────┐
│ Paper A                  │    │ Paper B                  │
│ "Learning RNN"           │    │ "ImageNet Classification"│
│ (2014)                   │    │ (2012)                   │
│ citations: 15000         │    │ citations: 103000        │
└──┬─────────────────────┬─┘    └──┬─────────────────────┬─┘
   │ BELONGS_TO          │         │ BELONGS_TO          │
   v                     v         v                     v
┌──────────────┐  ┌──────────────┐ ┌──────────────┐ ┌─────────────┐
│ Field: NLP   │  │ Field: DeepL │ │ Field: Comp. │ │ Field: DeepL│
│              │  │              │ │ Vision       │ │             │
└──────────────┘  └──────────────┘ └──────────────┘ └─────────────┘
   
REFERENCES (Citation Network):
Paper B ──REFERENCES──> Paper A
   (cites the work in A for methodological foundation)
```

---

## 3. Query Execution Paths

### Query Type 1: Direct Traversal (1 Hop)

```
Find: All papers by Christopher Manning

Path: Author[Manning] ──WRITES──> Paper

     ┌─────────────────┐
     │ Christopher     │
     │ Manning         │
     └────────┬────────┘
              │ WRITES
              ├──────────────┬──────────────┬──────────────┐
              v              v              v              v
         ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐
         │ Paper 1 │  │ Paper 2 │  │ Paper 3 │  │ Paper N  │
         └─────────┘  └─────────┘  └─────────┘  └──────────┘
```

### Query Type 2: Multi-Hop (2-3 Hops)

```
Find: NLP researchers at Stanford

Path: Field[NLP] <─STUDIES─ Author ─AFFILIATED_WITH─> University[Stanford]

     ┌──────────────┐
     │ Field: NLP   │
     └───────┬──────┘
             │ ←STUDIES (reverse)
             ├──────────┬──────────┬───────────┐
             v          v          v           v
        ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
        │Author1 │ │Author2 │ │Author3 │ │Author N│
        └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
            │ AFFILIATED_WITH
            │          (only Stanford matches filter)
            v
      ┌──────────────┐
      │ Stanford     │
      │ University   │
      └──────────────┘
```

### Query Type 3: Aggregation Pattern

```
Find: Papers per author (with statistics)

Author ──WRITES──> Paper
 ├─ COUNT(Papers)
 ├─ AVG(Citations)
 └─ MAX(Year)

     ┌──────────────┐
     │ Author Name  │
     └────────┬─────┘
              │ WRITES (count all)
              ├─ Count: 5 papers
              ├─ Avg Citations: 25000
              └─ Latest: 2023
```

### Query Type 4: Pattern Discovery (Complex)

```
Find: Researchers in same field at different universities (collaboration potential)

     ┌──────────────┐
     │  Field: NLP  │
     └──────┬───────┘
            │ ↑ (STUDIES relationship)
      ┌─────┘ └─────────────────────────┐
      │                                  │
    Author1                           Author2
      │                                 │
      │ AFFILIATED_WITH         AFFILIATED_WITH
      │ (different unis)         (different unis)
      v                            v
    Uni1                          Uni2

Filter: uni1.id <> uni2.id (different universities)
Result: Suggests potential collaboration
```

---

## 4. Relationship Semantics

### Direct Relationships

```
WRITES: Author → Paper
  ├─ Role: lead, contributor
  └─ Meaning: The author is responsible for this publication

BELONGS_TO: Paper → Field  
  ├─ Confidence: primary, secondary
  └─ Meaning: The paper contributes to this field of study

AFFILIATED_WITH: Author → University
  ├─ Role: professor, student, researcher
  ├─ StartYear, EndYear
  └─ Meaning: Author worked/studied at this institution

STUDIES: Author → Field
  ├─ YearsExperience
  └─ Meaning: Author has expertise in this field
```

### Derived Relationships

```
CO_AUTHORS_WITH: Author ↔ Author
  ├─ PaperCount
  └─ Meaning: These authors have collaborated on N papers
  ├─ Derivation: MATCH (a1)-[:WRITES]->(p)<-[:WRITES]-(a2)
  └─ Value: Quickly find collaboration frequency
```

### Citation Relationships

```
REFERENCES: Paper → Paper
  ├─ Context: methodological, theoretical, empirical
  └─ Meaning: The citing paper builds on/references the cited paper
  ├─ Forward: Find impact/influence
  └─ Backward: Find foundational work
```

---

## 5. Graph Algorithm Examples

### Centrality Measures

```
DEGREE CENTRALITY: Most connected authors

Author1 ────┬──────────┬──────────┬──────────┐
            v          v          v          v
        Paper1     Paper2     Paper3     Paper4
        
Count: 4 relationships = High degree

Author2 ────┬──────────┐
            v          v
        Paper1     Paper2
        
Count: 2 relationships = Lower degree
```

### Path Finding

```
SHORTEST PATH: Collaboration distance between two authors

Manning ──CO_AUTHOR──> A ──CO_AUTHOR──> B ──CO_AUTHOR──> Li
└─────────────────────────────────────────────────────┘
              Distance: 3 hops
```

### Community Detection

```
CLUSTERING: Research communities

Cluster 1:              Cluster 2:
Author A ◄──CO_AUTH──► Author D ◄──CO_AUTH──► Author E
    ▲                       ▼
    └──────CO_AUTH──────────┘

Strong internal connections
Weak external connections = Different research communities
```

---

## 6. Performance Characteristics

### Query Complexity by Hops

```
1 Hop   (Direct):      ████  Fast       O(n)
2 Hops  (1 Indirection): ████████  Moderate O(n²)
3 Hops  (2 Indirections): ████████████  Slower   O(n³)
4+ Hops (Many):          ████████████████ Very Slow O(n⁴+)
```

### Optimization Strategies

```
Without Index:
┌─────────────────────────────────────────┐
│ Scan all 1000 authors for name="Manning" │
│ Check each for WRITES relationship        │
│ Find matches → Result                     │
│ Time: Slow (Full table scan)              │
└─────────────────────────────────────────┘

With Index on Author(name):
┌──────────────────────┐
│ Direct lookup in B-tree │
│ Get Manning node ID: 42  │
│ Traverse WRITES from 42  │
│ Find matches → Result    │
│ Time: Fast (Direct lookup)
└──────────────────────┘
```

---

## 7. Data Model Normalization

### Why this structure?

```
NOT NORMALIZED (Problems):
┌────────────────────────────────────────────────────┐
│ Author Table                                       │
├───┬──────────┬───────┬──────────────┬─────────────┤
│ID │ Name     │ Papers│ Universities│ Fields     │
├───┼──────────┼───────┼──────────────┼─────────────┤
│1  │ Manning  │ [1,2,3] │[Stanford]  │[NLP, ML]  │
│2  │ Li       │ [4,5]  │[Stanford]   │[Vision]   │
└───┴──────────┴───────┴──────────────┴─────────────┘

Problems:
- Arrays as properties (not scalable)
- Difficult to query relationships
- Data duplication
- Can't efficiently aggregate


GRAPH MODEL (Solutions):
Author ──WRITES──> Paper ──BELONGS_TO──> Field
   │                                       │
   └─────── AFFILIATED_WITH ───────> University
              STUDIES
              │
              v
            Field

Solutions:
✓ Natural representation of relationships
✓ Efficient path queries
✓ No data duplication
✓ Easy aggregation and traversal
✓ Scalable to large networks
```

---

## 8. Query Execution Example

```
Query: "Find NLP researchers at Stanford and their papers"

Execution Plan:

Step 1: Find Field node
┌────────────────────────────┐
│ MATCH f:Field {name: "NLP"}│ ← Index lookup: O(1)
└────────────────────────────┘
            │
            v
       ┌──────────┐
       │ Field:NLP│
       └────┬─────┘

Step 2: Find authors studying this field
┌────────────────────────────┐
│ User.STUDIES → Author      │ ← Edge traversal: O(k)
└────────────────────────────┘
            │
       ┌────┴────┬────────┬────────┐
       v         v        v        v
    Author1  Author2  Author3  Author4

Step 3: Filter by university
┌──────────────────────────────────────────┐
│ Author.AFFILIATED_WITH → University      │ ← Edge traversal: O(m)
│ WHERE university.name = "Stanford"       │
└──────────────────────────────────────────┘
       │
    Author1  Author3

Step 4: Find their papers
┌──────────────────────────┐
│ Author.WRITES → Paper    │ ← Edge traversal: O(p)
└──────────────────────────┘
       │
    ┌──┴──┬──┐
    v  v  v  v
 Paper1 Paper2 Paper3 Paper4

Result: 4 papers by 2 NLP researchers at Stanford

Execution Time: milliseconds (with indexes)
```

---

## 9. Expansion Possibilities

### Current Schema
```
5 Node Types × 6 Relationship Types = Foundation
```

### Possible Extensions

```
Add Conference Management:
Conference ──HOSTS──> Venue (Location)
         ├──ACCEPTS──> Paper
         └──HELD_IN──> Year

Add Publication Details:
Paper ──PUBLISHED_IN──> Journal
     ├──HAS_ISSUE──> Issue
     └──CITES_IN──> DOI

Add Author Collaboration Details:
Author ──COLLABORATED_ON──> Project
      ├──MENTORED_BY──> Author
      └──MEMBER_OF──> ResearchGroup

Add Subject Hierarchy:
Field ──PARENT_OF──> Subfield
    ├──RELATED_TO──> Field
    └──OVERLAPS_WITH──> Field
```

---

## 10. Visual Query Explanation

### Example: "Emergent Researchers in Machine Learning"

```
PATTERN:
Author ──WRITES──> Paper (year >= 2020) ──BELONGS_TO──> Field[ML]
                       ▲
                   High citations (avg >= 1000)

VISUAL:
                   ┌─────────────────┐
                   │ Field: ML       │
                   └────────┬────────┘
                            │ ↑ (BELONGS_TO)
                   ┌────────┘ └───────────┐
                   │                      │
              Paper1 (high-cited)     Paper2 (high-cited)
              (2020-2023)            (2020-2023)
                   │                      │
                   └────────┬─────────────┘
                            │ ← WRITES (reverse)
                            │
                       ┌────┴────┐
                       │ Author 1 │  <- RESULT
                       │ Author 2 │  <- RESULT
                       └──────────┘

Reasoning:
1. Find ML field
2. Get papers that BELONG_TO it
3. Filter for recent (2020+)
4. Aggregate citations
5. Find authors with high-avg-citations
= Emerging researchers
```

---

This visualization helps understand:
- How data is connected
- How queries traverse relationships
- Performance characteristics
- Scalability considerations
- Future expansion options
