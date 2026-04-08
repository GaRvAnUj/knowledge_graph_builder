# Knowledge Graph Reasoning: Research Publications Domain

## 📚 Project Overview

This project demonstrates **knowledge representation and reasoning using knowledge graphs** with Neo4j. The domain is **Research Publications & NLP**, featuring authors, papers, universities, conferences, and research fields.

### Key Concepts Demonstrated

1. **Entity-Relationship Modeling**: Structured data as nodes and relationships
2. **Direct Reasoning**: Single-hop queries along relationships
3. **Indirect Reasoning**: Multi-hop queries discovering hidden patterns
4. **Aggregation & Analytics**: Deriving insights from graph structure
5. **Pattern Discovery**: Finding collaborations, expertise, and knowledge transfer

---


## 🏗️ Domain Architecture

### Entities (Nodes)

| Entity | Properties | Example |
|--------|-----------|---------|
| **Author** | name, email, researchFocus | Alice Johnson, NLP |
| **Paper** | title, year, abstract, doi, citations | "Attention Is All You Need" (2017) |
| **Field** | name, description | Natural Language Processing |
| **University** | name, country, ranking | MIT, USA |
| **Conference** | name, year, location, acronym | ACL 2023, Toronto |

### Relationships (Edges)

| Relationship | Source → Target | Properties | Meaning |
|--------------|-----------------|-----------|---------|
| **WRITES** | Author → Paper | role | Who authored the paper |
| **BELONGS_TO** | Paper → Field | confidence | What field the paper covers |
| **AFFILIATED_WITH** | Author → University | role, years | Author's institutional affiliation |
| **STUDIES** | Author → Field | yearsExperience | Author's research expertise |
| **CO_AUTHORS_WITH** | Author → Author | paperCount | Collaboration frequency (derived) |
| **REFERENCES** | Paper → Paper | context | Citation relationship |

---

## 🚀 Quick Start Guide

### Step 1: Install Neo4j

**Option A: Download & Run Locally**
- Download from: https://neo4j.com/download/
- Or use Docker:
  ```bash
  docker run --name neo4j -p 7687:7687 -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes neo4j:latest
  ```

**Option B: Use Neo4j Cloud**
- Create free account at: https://neo4j.com/cloud/platform/aura/
- Get connection string from dashboard

### Step 2: Install Python Dependencies

```bash
pip install neo4j
```

### Step 3: Configure Connection

Edit `knowledge_graph_builder.py` and update:
```python
NEO4J_URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "your_password_here"  # Change to match your Neo4j setup
```

### Step 4: Run the Script

```bash
python knowledge_graph_builder.py
```

The script will:
1. Connect to Neo4j
2. Clear any existing data
3. Create unique constraints
4. Import all sample data
5. Run 10 example reasoning queries
6. Display results

---

## 🧠 Reasoning Examples

### Example 1: Direct Query
**Question**: "Who studies Natural Language Processing?"

```cypher
MATCH (a:Author)-[:STUDIES]->(f:Field {name: "Natural Language Processing"})
RETURN a.name
```

**Result**: Direct relationship traversal

---

### Example 2: Multi-Hop Reasoning
**Question**: "Find NLP researchers and their universities"

```cypher
MATCH (a:Author)-[:STUDIES]->(f:Field {name: "Natural Language Processing"})
MATCH (a)-[:AFFILIATED_WITH]->(u:University)
RETURN a.name, u.name
```

**Result**: Combines two relationships to answer a complex question

---

### Example 3: Collaboration Discovery
**Question**: "Find potential collaborators in the same field but different universities"

```cypher
MATCH (a1:Author)-[:STUDIES]->(field:Field)
MATCH (a1)-[:AFFILIATED_WITH]->(uni1:University)
MATCH (a2:Author)-[:STUDIES]->(field)
MATCH (a2)-[:AFFILIATED_WITH]->(uni2:University)
WHERE a1.id < a2.id AND uni1.id <> uni2.id
RETURN field.name, a1.name, uni1.name, a2.name, uni2.name
```

**Result**: Identifies cross-institutional collaboration opportunities

---

### Example 4: Citation Network Analysis
**Question**: "What papers reference 'Attention is All You Need'?"

```cypher
MATCH (citing:Paper)-[:REFERENCES]->(p:Paper {title: "Attention is All You Need"})
RETURN citing.title, citing.year
ORDER BY citing.year DESC
```

**Result**: Traces knowledge propagation through citations

---

### Example 5: Expert Discovery
**Question**: "Who are the emerging researchers in their field?"

```cypher
MATCH (a:Author)-[:WRITES]->(p:Paper)
WHERE p.year >= 2020
RETURN a.name, COUNT(p) as recent_papers, AVG(p.citations) as avg_citations
ORDER BY avg_citations DESC
```

**Result**: Identifies prolific recent researchers

---

## 📊 Query Categories (42 Examples Provided)

The `cypher_queries.txt` file contains 42 example queries organized by category:

1. **Basic Queries** (Q1-Q4): Simple entity lookups
2. **Relationship Traversal** (Q5-Q8): Direct connections
3. **Multi-Hop Queries** (Q9-Q12): Indirect reasoning
4. **Collaboration Networks** (Q13-Q16): Finding connected researchers
5. **Citation Networks** (Q17-Q20): Knowledge flow analysis
6. **Aggregation & Analytics** (Q21-Q25): Insights from structure
7. **Expert Finding** (Q26-Q29): Domain specialists
8. **Advanced Reasoning** (Q30-Q34): Complex patterns
9. **Graph Properties** (Q35-Q38): Network analysis
10. **Parameterized Queries** (Q39-Q42): For applications

---

## 🔍 Key Reasoning Techniques

### 1. Path Traversal
Find indirect connections through multiple hops:
```cypher
MATCH (a1:Author)-[:CO_AUTHORS_WITH*1..3]-(colleague:Author)
```

### 2. Aggregation with Grouping
Summarize related nodes:
```cypher
MATCH (a:Author)-[:WRITES]->(p:Paper)
RETURN a.name, COUNT(p) as papers
```

### 3. Filtering on Derived Properties
Find special nodes based on relationships:
```cypher
MATCH (a:Author)-[r]-()
RETURN a.name, COUNT(r) as connections
ORDER BY connections DESC
```

### 4. Multiple Pattern Matching
Combine different relationship types:
```cypher
MATCH (a:Author)-[:STUDIES]->(f:Field)
MATCH (a)-[:AFFILIATED_WITH]->(u:University)
```

### 5. Implicit Relationship Detection
Identify patterns through analysis:
```cypher
// Find researchers in same field but different universities
WHERE uni1.id <> uni2.id
```

---

## 💡 Real-World Applications

### 1. **Academic Research**
- Identify collaboration opportunities
- Find subject matter experts
- Discover citation patterns
- Track knowledge dissemination

### 2. **Knowledge Discovery**
- Find emerging research areas
- Identify interdisciplinary bridges
- Predict future collaborations

### 3. **Recruitment**
- Find experts in specific domains
- Identify rising talent
- Understand expertise networks

### 4. **Grant Allocation**
- Analyze research communities
- Identify impactful researchers
- Track research trends

---

## 🛠️ Customization Guide

### Add New Data

1. **Add to sample_data.json**:
   ```json
   {
     "id": "author_8",
     "name": "Your Name",
     "email": "your@email.com",
     "researchFocus": "Your Focus"
   }
   ```

2. **Extend relationships** by adding to respective arrays

3. **Re-run the script**: `python knowledge_graph_builder.py`

### Modify Schema

To add new node types:

1. Update SCHEMA.md
2. Add creation code to `knowledge_graph_builder.py`:
   ```python
   for item in data['new_type']:
       session.run(
           "CREATE (n:NewType {id: $id, name: $name})",
           id=item['id'], name=item['name']
       )
   ```

### Create Custom Queries

Write Cypher queries in Neo4j Browser:
```
http://localhost:7474
```

---

## 📈 Performance Tips

### For Large Graphs

1. **Create Indexes**:
   ```cypher
   CREATE INDEX ON :Author(id)
   CREATE INDEX ON :Paper(year)
   ```

2. **Use LIMIT for exploration**:
   ```cypher
   MATCH (...) RETURN ... LIMIT 100
   ```

3. **Profile queries**:
   ```cypher
   PROFILE MATCH (...) RETURN ...
   ```

---

## 🔗 Resources

- **Neo4j Documentation**: https://neo4j.com/docs/
- **Cypher Manual**: https://neo4j.com/docs/cypher-manual/
- **Colab Notebook**: Google Colab for cloud-based execution
- **Graph Databases**: "Learning Neo4j" book

---

## 📝 Example Output

When you run the script, you'll see:

```
================================================================================
NEO4J KNOWLEDGE GRAPH: Research Publications Domain
================================================================================

Connecting to Neo4j database...
✓ Connected successfully

Step 1: Clearing database...
✓ Database cleared

Step 2: Creating constraints...
✓ Constraints created

Step 3: Importing data...
✓ Created 5 universities
✓ Created 4 fields
✓ Created 7 authors
...

Step 4: Running reasoning queries...

Example 1: Find all NLP researchers
Description: Direct: Find authors studying NLP
Results (3 rows):
  {'name': 'Christopher Manning', 'field': 'Natural Language Processing', ...}
  ...

✓ Knowledge Graph construction completed successfully!
```

---

## 🤝 Contributing

To extend this project:

1. Add more sample data
2. Create domain-specific queries
3. Implement visualization
4. Add real data sources (arXiv, DBLP, etc.)

---

## 📄 License

Educational project for knowledge graph demonstration.

---

## ❓ FAQ

**Q: Can I use this with real academic data?**
A: Yes! Replace sample_data.json with real data from DBLP, arXiv, or other sources.

**Q: How do I visualize the graph?**
A: Neo4j Browser shows interactive visualization at `http://localhost:7474`

**Q: What's the difference between STUDIES and WRITES relationships?**
A: STUDIES = expertise in a field; WRITES = actually published papers

**Q: Can I run this on Neo4j Cloud?**
A: Yes! Update NEO4J_URI with your Aura connection string.

---

**Last Updated**: April 2026
**Author**: AI Assistant
**Domain**: Research Publications & NLP
