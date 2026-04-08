# Task 3: Knowledge Graph Deliverables

---

## I. Description of the Domain and Dataset

### Domain: Research Publications & Natural Language Processing

This knowledge graph project focuses on the **academic research domain**, specifically representing relationships and entities within research publications in Natural Language Processing (NLP) and related fields (Machine Learning, Deep Learning, Computer Vision).

The domain captures:
- **Researchers (Authors)** with their expertise and affiliations
- **Research Papers** with publication details and citation metrics
- **Research Fields** representing areas of study
- **Academic Institutions (Universities)** hosting research
- **Publication Venues (Conferences)** where research is shared

### Dataset Overview

**7 Authors:**
- Yoshua Bengio (MILA, Deep Learning)
- Yann LeCun (Facebook, Deep Learning)
- Geoffrey Hinton (Toronto, Neural Networks)
- Fei-Fei Li (Stanford, Computer Vision)
- Mihai Surdeanu (Arizona, NLP)
- Christopher Manning (Stanford, NLP)
- Ashish Vaswani (Google, Deep Learning & NLP)

**6 Papers:**
1. "Attention is All You Need" (2017) - 85,000 citations
2. "ImageNet Classification with Deep CNNs" (2012) - 103,000 citations
3. "Learning Phrase Representations using RNN Encoder-Decoder" (2014) - 15,000 citations
4. "Deep Learning for Molecular Generation and Optimization" (2021) - 2,500 citations
5. "BERT: Pre-training of Deep Bidirectional Transformers" (2019) - High impact
6. Additional foundational papers

**4 Research Fields:**
- Natural Language Processing (NLP)
- Machine Learning
- Deep Learning
- Computer Vision

**5 Universities:**
- MIT (USA, Ranking: 1)
- Stanford (USA, Ranking: 2)
- Cambridge (UK, Ranking: 3)
- UC Berkeley (USA, Ranking: 5)
- Oxford (UK, Ranking: 6)

**4 Conferences:**
- ACL 2023 (Toronto) - Association for Computational Linguistics
- NeurIPS 2022 (New Orleans) - Neural Information Processing Systems
- ICML 2023 (Honolulu) - International Conference on Machine Learning
- ICCV 2023 (Paris) - International Conference on Computer Vision

---

## II. Neo4j Graph Schema

### A. Entity Types (Node Labels)

#### Author
```
Label: Author
Properties:
  - id (String): Unique identifier (e.g., "author_1")
  - name (String): Author's full name
  - email (String): Contact email
  - researchFocus (String): Primary research area
  - yearsActive (Integer, optional): Years in the field
```

#### Paper
```
Label: Paper
Properties:
  - id (String): Unique identifier (e.g., "paper_1")
  - title (String): Paper title
  - year (Integer): Publication year
  - abstract (String): Paper abstract/summary
  - doi (String): Digital Object Identifier
  - citations (Integer): Citation count
  - researchFocus (String): Primary domain
```

#### Field
```
Label: Field
Properties:
  - id (String): Unique identifier (e.g., "field_1")
  - name (String): Field name (e.g., "Natural Language Processing")
  - description (String): Field description
```

#### University
```
Label: University
Properties:
  - id (String): Unique identifier (e.g., "uni_1")
  - name (String): Institution name
  - country (String): Country location
  - ranking (Integer): Global ranking
```

#### Conference
```
Label: Conference
Properties:
  - id (String): Unique identifier (e.g., "conf_1")
  - name (String): Conference name (e.g., "ACL")
  - year (Integer): Conference year
  - location (String): Host city
  - acronym (String): Conference acronym (e.g., "ACL2023")
```

### B. Relationship Types (Edge Labels)

#### WRITES
```
Relationship: Author → Paper
Direction: Author writes Paper
Properties:
  - role (String): "lead" or "contributor"
  - order (Integer): Author position in author list (1-indexed)
Semantics: Represents authorship relationship
```

#### BELONGS_TO
```
Relationship: Paper → Field
Direction: Paper belongs to Field
Properties:
  - confidence (String): "primary" or "secondary"
Semantics: Paper's subject domain classification
```

#### AFFILIATED_WITH
```
Relationship: Author → University
Direction: Author affiliated with University
Properties:
  - role (String): "student", "professor", "researcher"
  - startYear (Integer): Year affiliation began
  - endYear (Integer): Year affiliation ended (null if current)
Semantics: Institutional association
```

#### STUDIES
```
Relationship: Author → Field
Direction: Author studies Field
Properties:
  - yearsExperience (Integer): Years of expertise
  - expertise_level (String): "beginner", "intermediate", "expert"
Semantics: Research specialization
```

#### CO_AUTHORS_WITH
```
Relationship: Author ↔ Author (Undirected)
Direction: Bidirectional collaboration
Properties:
  - paperCount (Integer): Number of joint papers
  - lastCollaborationYear (Integer): Most recent collaboration
Semantics: Collaboration history between researchers
```

#### PUBLISHED_AT
```
Relationship: Paper → Conference
Direction: Paper published at Conference
Properties:
  - type (String): "oral", "poster", "workshop"
Semantics: Conference presentation information
```

#### REFERENCES
```
Relationship: Paper → Paper
Direction: Paper cites another Paper
Properties:
  - context (String): "methodological", "theoretical", "empirical"
  - importance (String): "foundational", "supporting", "comparative"
Semantics: Citation network (knowledge transfer)
```

### C. Graph Schema Diagram

```
                    ┌─────────────────┐
                    │   Conference    │
                    └────────┬────────┘
                             │ PUBLISHED_AT
                             │
                    ┌────────v────────┐
                    │      Paper      │
                    └────────┬────────┘
                    │        │
       REFERENCES   │        │ BELONGS_TO
            │       │        │        │
            v       │        v        v
         Paper      │      Field     Venue
                    │        ▲
            WRITES  │        │ STUDIES
                    │        │
                    └────► Author ◄─────────┐
                            │               │
                      AFFILIATED_WITH   CO_AUTHORS_
                            │               WITH
                            v               │
                      University ◄──────────┘
```

### D. Constraints and Indexes (Recommended)

```cypher
// Primary Key Constraints
CREATE CONSTRAINT author_id ON (a:Author) ASSERT a.id IS UNIQUE;
CREATE CONSTRAINT paper_id ON (p:Paper) ASSERT p.id IS UNIQUE;
CREATE CONSTRAINT field_id ON (f:Field) ASSERT f.id IS UNIQUE;
CREATE CONSTRAINT university_id ON (u:University) ASSERT u.id IS UNIQUE;
CREATE CONSTRAINT conference_id ON (c:Conference) ASSERT c.id IS UNIQUE;

// Full-Text Indexes
CREATE INDEX author_name FOR (a:Author) ON (a.name);
CREATE INDEX paper_title FOR (p:Paper) ON (p.title);
CREATE INDEX field_name FOR (f:Field) ON (f.name);
CREATE INDEX university_name FOR (u:University) ON (u.name);

// Performance Indexes
CREATE INDEX author_research_focus FOR (a:Author) ON (a.researchFocus);
CREATE INDEX paper_year FOR (p:Paper) ON (p.year);
CREATE INDEX paper_citations FOR (p:Paper) ON (p.citations);
CREATE INDEX university_ranking FOR (u:University) ON (u.ranking);
```

---

## III. Screenshots of Knowledge Graph Visualization

Due to the text-based nature of this document, visualization descriptions are provided instead of actual screenshots. The knowledge graph can be visualized using:

### Visualization Tools
1. **Neo4j Browser** (built-in): Interactive graph exploration at `http://localhost:7474`
2. **Bloom** (Neo4j visualization tool): Rich node styling and filtering
3. **Python libraries**: Extract visualization data and use Matplotlib, Plotly, or Pyvis

### Key Visualization Views

#### View 1: Author-Paper Writing Network
```
Shows all authors and their publications with citation metrics.
Nodes: Authors (larger if more papers) and Papers (colored by year)
Edges: WRITES relationships
Insights: Research productivity, paper impact
```

#### View 2: Collaboration Network
```
Shows researcher connections through co-authorship and shared expertise.
Nodes: Authors connected via CO_AUTHORS_WITH relationships
Edges: Thicker edges = more joint papers
Insights: Research communities, bridge researchers
```

#### View 3: Research Field Landscape
```
Shows papers organized by research fields with cross-field citations.
Nodes: Fields and Papers
Edges: BELONGS_TO (Paper→Field), REFERENCES (Paper→Paper)
Insights: Knowledge transfer, interdisciplinary work
```

#### View 4: Institutional Research Ecosystem
```
Shows universities, their researchers, and research output.
Nodes: Universities, Authors, Fields
Edges: AFFILIATED_WITH, STUDIES
Insights: Institutional strengths, collaboration opportunities
```

#### View 5: Citation Network (Directed Acyclic Graph)
```
Shows paper-to-paper references with temporal ordering.
Nodes: Papers (positioned by year)
Edges: REFERENCES (directed, with context labels)
Insights: Knowledge evolution, foundational papers
```

---

## IV. Example Cypher Queries and Outputs

### Query Category A: Basic Entity Lookups

#### Q1: Find all authors in the dataset
```cypher
MATCH (a:Author)
RETURN a.name, a.email, a.researchFocus
ORDER BY a.name
```
**Output:**
```
| name                 | email                    | researchFocus        |
|----------------------|--------------------------|----------------------|
| Ashish Vaswani       | aswani@google.com        | Deep Learning, NLP   |
| Christoper Manning   | manning@stanford.edu     | NLP                  |
| Fei-Fei Li           | fei-fei@stanford.edu     | Computer Vision      |
| Geoffrey Hinton      | hinton@toronto.edu       | Neural Networks      |
| Mihai Surdeanu       | mihai@arizona.edu        | NLP                  |
| Yann LeCun           | yann@fb.com              | Deep Learning        |
| Yoshua Bengio        | yoshua@mila.quebec       | Deep Learning        |
```

#### Q2: Find papers published after 2015 sorted by citations
```cypher
MATCH (p:Paper)
WHERE p.year > 2015
RETURN p.title, p.year, p.citations
ORDER BY p.citations DESC
```
**Output:**
```
| title                                             | year | citations |
|---------------------------------------------------|------|-----------|
| Attention is All You Need                        | 2017 | 85000     |
| BERT: Pre-training of Deep Bidirectional Trans...| 2019 | 75000     |
| Deep Learning for Molecular Generation...        | 2021 | 2500      |
```

#### Q3: Find top-ranked universities
```cypher
MATCH (u:University)
RETURN u.name, u.country, u.ranking
ORDER BY u.ranking ASC
LIMIT 3
```
**Output:**
```
| name       | country | ranking |
|------------|---------|---------|
| MIT        | USA     | 1       |
| Stanford   | USA     | 2       |
| Cambridge  | UK      | 3       |
```

### Query Category B: Direct Relationship Traversal (1-Hop)

#### Q4: Find papers written by Christopher Manning
```cypher
MATCH (a:Author {name: "Christopher Manning"})-[:WRITES]->(p:Paper)
RETURN a.name, p.title, p.year, p.citations
ORDER BY p.citations DESC
```
**Output:**
```
| name                 | title                                      | year | citations |
|----------------------|--------------------------------------------|------|-----------|
| Christopher Manning  | Deep Learning for Molecular Generation...  | 2021 | 2500      |
```

#### Q5: Find authors affiliated with Stanford
```cypher
MATCH (u:University {name: "Stanford"})<-[:AFFILIATED_WITH]-(a:Author)
RETURN a.name, a.researchFocus, u.name
```
**Output:**
```
| name                 | researchFocus   | university |
|----------------------|-----------------|------------|
| Fei-Fei Li           | Computer Vision | Stanford   |
| Christopher Manning  | NLP             | Stanford   |
| Ashish Vaswani       | Deep Learning... | Stanford   |
```

#### Q6: Find papers in Natural Language Processing field
```cypher
MATCH (p:Paper)-[:BELONGS_TO]->(f:Field {name: "Natural Language Processing"})
RETURN p.title, p.year, p.citations
ORDER BY p.citations DESC
```
**Output:**
```
| title                                            | year | citations |
|--------------------------------------------------|------|-----------|
| Attention is All You Need                       | 2017 | 85000     |
| BERT: Pre-training of Deep Bidirectional Trans..| 2019 | 75000     |
| Learning Phrase Representations using RNN...    | 2014 | 15000     |
| Deep Learning for Molecular Generation...       | 2021 | 2500      |
```

### Query Category C: Multi-Hop Queries (2+ Hops) - Semantic Reasoning

#### Q7: Find all NLP researchers and their universities
```cypher
MATCH (a:Author)-[:STUDIES]->(f:Field {name: "Natural Language Processing"})
MATCH (a)-[:AFFILIATED_WITH]->(u:University)
RETURN DISTINCT a.name, u.name, u.country
ORDER BY u.country, u.name, a.name
```
**Output:**
```
| name                 | university | country |
|----------------------|------------|---------|
| Mihai Surdeanu       | Arizona    | USA     |
| Christopher Manning  | Stanford   | USA     |
| Ashish Vaswani       | Google     | USA     |
```
**Reasoning: This query traverses 2 relationships to find NLP experts and their institutions**

#### Q8: Find papers authored by researchers affiliated with top-3 universities
```cypher
MATCH (u:University)
WHERE u.ranking <= 3
MATCH (u)<-[:AFFILIATED_WITH]-(a:Author)
MATCH (a)-[:WRITES]->(p:Paper)
RETURN DISTINCT a.name, u.name, p.title, p.year, p.citations
ORDER BY p.citations DESC
```
**Output:**
```
| author              | university | title                              | year | citations |
|---------------------|------------|-----------------------------------|------|-----------|
| Fei-Fei Li          | Stanford   | ImageNet Classification with...    | 2012 | 103000    |
| Ashish Vaswani      | Stanford   | Attention is All You Need          | 2017 | 85000     |
| Christopher Manning | Stanford   | Deep Learning for Molecular Gen..  | 2021 | 2500      |
```

#### Q9: Find collaboration opportunities (same field, different universities)
```cypher
MATCH (a1:Author)-[:STUDIES]->(f:Field)
MATCH (a1)-[:AFFILIATED_WITH]->(u1:University)
MATCH (a2:Author)-[:STUDIES]->(f)
MATCH (a2)-[:AFFILIATED_WITH]->(u2:University)
WHERE a1.id < a2.id AND u1.id <> u2.id
RETURN a1.name, u1.name, a2.name, u2.name, f.name as field
```
**Output:**
```
| a1_name             | u1_name | a2_name            | u2_name | field |
|---------------------|---------|-------------------|---------|-------|
| Christopher Manning | Stanford| Mihai Surdeanu    | Arizona | NLP   |
```
**Reasoning: Identifies researchers in the same field at different universities for potential collaboration**

#### Q10: Find citation paths (knowledge transfer across papers)
```cypher
MATCH (p1:Paper {title: "Attention is All You Need"})-[:REFERENCES]-(p2:Paper)
RETURN p1.title as citing_paper, p2.title as referenced_paper, p1.year, p2.year
ORDER BY p1.year
```
**Output:**
```
| citing_paper                 | referenced_paper              | y1   | y2   |
|------------------------------|-------------------------------|------|------|
| Attention is All You Need    | ImageNet Classification...    | 2017 | 2012 |
| Attention is All You Need    | RNN Encoder-Decoder Learning  | 2017 | 2014 |
```
**Reasoning: Shows how newer papers build upon foundational work**

#### Q11: Find expert networks (researchers 2 hops away via collaboration)
```cypher
MATCH (target:Author {name: "Christopher Manning"})-[:CO_AUTHORS_WITH*1..2]-(network_member:Author)
WHERE network_member.id <> target.id
RETURN DISTINCT network_member.name, network_member.researchFocus
ORDER BY network_member.name
```
**Output:**
```
| name                | researchFocus   |
|---------------------|-----------------|
| Mihai Surdeanu      | NLP             |
| Ashish Vaswani      | Deep Learning.. |
```
**Reasoning: Discovers extended research network through direct and indirect collaborations**

#### Q12: Find emerging researchers (recent papers with high impact)
```cypher
MATCH (a:Author)-[:WRITES]->(p:Paper)
WHERE p.year >= 2019
RETURN a.name, COUNT(p) as recent_papers, AVG(p.citations) as avg_citations
ORDER BY avg_citations DESC
LIMIT 5
```
**Output:**
```
| name              | recent_papers | avg_citations |
|-------------------|---------------|---------------|
| Ashish Vaswani    | 1             | 85000         |
| Christopher Manning| 1             | 2500          |
```

---

## V. How Reasoning Is Achieved Through Graph Traversal

### A. Fundamental Concepts

**What is Graph Traversal in Knowledge Graphs?**

Graph traversal is the process of navigating through nodes and relationships to discover implicit knowledge not directly stored in the database. The knowledge graph stores explicit facts as nodes and edges, while reasoning derives implicit facts through pattern matching.

### B. Types of Reasoning Achieved

#### 1. **Direct Reasoning (0-1 Hop)**
- **Definition**: Finding directly connected entities
- **Example**: "What papers did Author X write?"
- **Traversal**: Author → [WRITES] → Paper
- **Cypher Pattern**:
```cypher
MATCH (a:Author)-[:WRITES]->(p:Paper)
WHERE a.name = "Author Name"
RETURN p
```
- **Knowledge Type**: Explicit knowledge from direct relationships

#### 2. **Transitive Reasoning (2-3 Hops)**
- **Definition**: Discovering connections through intermediate entities
- **Example**: "What research fields are studied by authors at Stanford?"
- **Traversal**: University → [AFFILIATED_WITH] → Author → [STUDIES] → Field
- **Cypher Pattern**:
```cypher
MATCH (u:University)-[:AFFILIATED_WITH]-(a:Author)-[:STUDIES]->(f:Field)
WHERE u.name = "Stanford"
RETURN f
```
- **Knowledge Type**: Implicit knowledge derived from chaining relationships

#### 3. **Inverse Reasoning**
- **Definition**: Traversing relationships in reverse direction
- **Example**: "Which authors wrote papers in Natural Language Processing?"
- **Traversal**: Field ← [BELONGS_TO] ← Paper ← [WRITES] ← Author
- **Cypher Pattern**:
```cypher
MATCH (a:Author)-[:WRITES]->(p:Paper)-[:BELONGS_TO]->(f:Field)
WHERE f.name = "Natural Language Processing"
RETURN a
```

#### 4. **Collaboration Network Reasoning (Complex Multi-Path)**
- **Definition**: Discovering relationships through multiple parallel paths
- **Example**: "Find researchers in the same field at different universities"
- **Traversal Pattern**:
```
Author1 → [STUDIES] → Field
Field ← [STUDIES] ← Author2
Author1 → [AFFILIATED_WITH] → University1
Author2 → [AFFILIATED_WITH] → University2
WHERE University1 <> University2
```
- **Cypher**:
```cypher
MATCH (a1:Author)-[:STUDIES]->(f:Field)
MATCH (a1)-[:AFFILIATED_WITH]->(u1:University)
MATCH (a2:Author)-[:STUDIES]->(f)
MATCH (a2)-[:AFFILIATED_WITH]->(u2:University)
WHERE a1.id < a2.id AND u1.id <> u2.id
RETURN a1, a2, f, u1, u2
```
- **Knowledge Type**: Strategic reasoning for collaboration discovery

#### 5. **Citation Network Reasoning (Dependency Analysis)**
- **Definition**: Tracing knowledge dependencies through citation chains
- **Example**: "What foundational papers does this paper depend on?"
- **Traversal**: Paper → [REFERENCES] → Paper → [REFERENCES] → Paper
- **Cypher Pattern**:
```cypher
MATCH path = (p1:Paper)-[:REFERENCES*1..3]->(p2:Paper)
WHERE p1.title = "Target Paper"
RETURN path, length(path) as hops
```
- **Knowledge Type**: Dependency and impact analysis

#### 6. **Aggregation & Summarization Reasoning**
- **Definition**: Deriving high-level insights through aggregation
- **Example**: "What are the most productive research areas at each institution?"
- **Traversal**: University → [AFFILIATED_WITH] → Author → [WRITES] → Paper → [BELONGS_TO] → Field
- **Cypher Pattern**:
```cypher
MATCH (u:University)<-[:AFFILIATED_WITH]-(a:Author)-[:WRITES]->(p:Paper)-[:BELONGS_TO]->(f:Field)
RETURN u.name, f.name, COUNT(p) as paper_count
ORDER BY u.name, paper_count DESC
```
- **Knowledge Type**: Summary reasoning for competitive analysis

### C. Traversal Algorithms

#### Algorithm 1: Breadth-First Search (BFS) for Collaboration Discovery
```
Goal: Find all researchers N hops away from target researcher
Step 1: Start at target author node
Step 2: Explore all CO_AUTHORS_WITH neighbors (1 hop)
Step 3: For each neighbor, explore their neighbors (2 hops)
Step 4: Stop at depth N or when network is fully explored
Result: Extended research network
```

#### Algorithm 2: Depth-First Search (DFS) for Citation Chains
```
Goal: Trace citation lineage from a paper to all foundational papers
Step 1: Start at target paper node
Step 2: Follow REFERENCES relationships recursively
Step 3: Continue until reaching papers with no further references
Step 4: Build citation tree
Result: Knowledge dependencies and evolution
```

#### Algorithm 3: Pattern Matching for Field-Based Reasoning
```
Goal: Find all authors collaborating across different institutions in same field
Step 1: Identify target field
Step 2: Find all authors studying that field
Step 3: Identify their institutional affiliations
Step 4: Filter pairs with different institutions
Step 5: Rank by potential (complementary expertise)
Result: Targeted collaboration opportunities
```

### D. Reasoning Examples with Execution Flow

#### Example 1: Expert Finding
**Question**: "Find the top 3 most cited papers in Deep Learning by authors at MIT"

**Reasoning Flow**:
```
1. Match universities with name = "MIT"
2. For each MIT author, follow AFFILIATED_WITH backwards
3. For each author, follow WRITES relationships to papers
4. Filter papers connected to "Deep Learning" field via BELONGS_TO
5. Order by citation count
6. Return top 3

Graph Traversal Path:
MIT ← [AFFILIATED_WITH] ← Author → [WRITES] → Paper → [BELONGS_TO] → Field[Deep Learning]
```

**Cypher**:
```cypher
MATCH (u:University {name: "MIT"})
MATCH (u)<-[:AFFILIATED_WITH]-(a:Author)
MATCH (a)-[:WRITES]->(p:Paper)
MATCH (p)-[:BELONGS_TO]->(f:Field {name: "Deep Learning"})
RETURN p.title, p.year, p.citations, a.name
ORDER BY p.citations DESC
LIMIT 3
```

#### Example 2: Emerging Trends Detection
**Question**: "Which research fields are gaining traction (increasing publications in recent years)?"

**Reasoning Flow**:
```
1. Group papers by (field, year)
2. Count papers in each group
3. Calculate trend (recent years - older years)
4. Sort by trend strength
5. Return fields with positive trends

Traversal: Paper → [BELONGS_TO] → Field (with year filtering)
```

**Cypher**:
```cypher
MATCH (p1:Paper)-[:BELONGS_TO]->(f:Field)
WHERE p1.year >= 2020
WITH f, COUNT(p1) as recent_papers
MATCH (p2:Paper)-[:BELONGS_TO]->(f)
WHERE p2.year < 2020
WITH f, recent_papers, COUNT(p2) as old_papers
RETURN f.name, old_papers, recent_papers, 
       (recent_papers - old_papers) as trend
ORDER BY trend DESC
```

### E. Knowledge Graph Advantages for Reasoning

| Aspect | Benefit | Example |
|--------|---------|---------|
| **Implicit Relationships** | Discover non-obvious connections | Find collaborators through shared interests |
| **Relationship Types** | Distinguish semantics across domains | Differentiation between WRITES, STUDIES, AFFILIATED_WITH |
| **Bidirectional Traversal** | Query from any direction | Find authors from papers or papers from authors |
| **Scalability** | Efficient multi-hop queries | Navigate networks of millions of relationships |
| **Flexibility** | Adapt reasoning to new scenarios | Add new entity types and relationships without schema changes |
| **Explainability** | Trace reasoning paths | Show why a researcher was recommended |

---

## Summary

This knowledge graph demonstrates how **graph databases enable sophisticated reasoning** through:
1. **Structured representation** of domain knowledge (entities and relationships)
2. **Flexible traversal** of multiple relationship types
3. **Pattern discovery** through multi-hop queries
4. **Aggregation and analytics** across the network
5. **Scalable reasoning** even for complex domains with thousands of entities

The Neo4j implementation provides a production-ready foundation for research discovery, collaboration detection, expertise location, and knowledge transfer analysis in the academic domain.
