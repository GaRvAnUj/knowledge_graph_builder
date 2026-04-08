# Neo4j Knowledge Graph - Quick Start Guide

## Prerequisites

- Python 3.8+ with `neo4j` package installed
- Neo4j database running locally on port 7687
- Credentials: username `neo4j` / your password

---

## Quick Start

### 1. Start the Application

```bash
python knowledge_graph_builder.py
```

### 2. View Neo4j Browser

Open your web browser and navigate to:
```
http://localhost:7474
```

Login with:
- **Username**: neo4j
- **Password**: 2026#Isend

---

## Port Reference

| Port | Purpose | URL/Connection |
|------|---------|-----------------|
| **7687** | Bolt Protocol (Python connections) | `bolt://localhost:7687` |
| **7474** | Neo4j Browser (Web UI) | `http://localhost:7474` |

---

## Useful Neo4j Commands

### Graph Exploration

```cypher
// View all nodes and relationships (limit 25)
MATCH (n) RETURN n LIMIT 25

// Count all nodes by type
MATCH (n) RETURN labels(n) as label, COUNT(*) as count

// See all authors
MATCH (a:Author) RETURN a.name, a.researchFocus ORDER BY a.name

// See all research fields
MATCH (f:Field) RETURN f.name, f.description

// See all papers with their citations
MATCH (p:Paper) RETURN p.title, p.year, p.citations ORDER BY p.citations DESC
```

### Relationship Queries

```cypher
// Find who works at which university
MATCH (a:Author)-[:AFFILIATED_WITH]->(u:University) 
RETURN a.name, u.name ORDER BY u.name, a.name

// Show author collaboration networks
MATCH (a1:Author)-[:CO_AUTHORS_WITH]->(a2:Author) 
RETURN a1.name, a2.name, COUNT(*) as collaborations

// Find papers by specific author
MATCH (a:Author {name: "Christopher Manning"})-[:WRITES]->(p:Paper) 
RETURN p.title, p.year ORDER BY p.year DESC

// See what fields an author studies
MATCH (a:Author {name: "Christopher Manning"})-[:STUDIES]->(f:Field) 
RETURN f.name, f.description
```

### Advanced Queries

```cypher
// Find most cited papers in NLP field
MATCH (p:Paper)-[:BELONGS_TO]->(f:Field {name: "Natural Language Processing"}) 
RETURN p.title, p.citations, p.year ORDER BY p.citations DESC LIMIT 10

// Find all co-authors of Christopher Manning (up to 3 hops)
MATCH (target:Author {name: "Christopher Manning"})-[co:CO_AUTHORS_WITH*1..3]-(colleague:Author) 
RETURN DISTINCT colleague.name

// Find papers that reference each other (citation network)
MATCH (p1:Paper)-[:REFERENCES]->(p2:Paper) 
RETURN p1.title as 'Citing Paper', p2.title as 'Cited Paper'

// Find research collaborations happening at the same university
MATCH (a1:Author)-[:AFFILIATED_WITH]->(u:University)<-[:AFFILIATED_WITH]-(a2:Author) 
WHERE a1.id < a2.id 
RETURN a1.name, a2.name, u.name
```

### Statistics & Analytics

```cypher
// Total counts in the graph
MATCH (a:Author) WITH COUNT(a) as authors
MATCH (p:Paper) WITH COUNT(p) as papers, authors
MATCH (f:Field) WITH COUNT(f) as fields, papers, authors
RETURN {authors: authors, papers: papers, fields: fields}

// Average citations per paper
MATCH (p:Paper) RETURN AVG(p.citations) as avg_citations, MAX(p.citations) as max_citations

// Authors with most papers
MATCH (a:Author)-[:WRITES]->(p:Paper) 
RETURN a.name, COUNT(p) as paper_count ORDER BY paper_count DESC

// Most prolific year
MATCH (p:Paper) RETURN p.year, COUNT(p) as paper_count ORDER BY paper_count DESC
```

### Database Management

```cypher
// Clear entire database (WARNING: Deletes everything!)
MATCH (n) DETACH DELETE n

// Show all constraints
CALL db.constraints()

// Show property keys
CALL db.propertyKeys()

// Show all relationship types
CALL db.relationshipTypes()

// Database size and memory info
CALL db.store.stats()
```

---

## Tips

- **Run script again**: Re-running `python knowledge_graph_builder.py` will clear and rebuild the entire graph
- **Custom queries**: Write your own Cypher queries directly in the Neo4j Browser
- **Export data**: Use `MATCH` queries to export results as CSV or JSON
- **Visualize**: Neo4j Browser automatically visualizes relationships and paths
- Add new query categories
- Implement additional reasoning logic

### 4. Enhance Reasoning

Create new queries that:
- Find collaboration patterns
- Predict future collaborations
- Identify research gaps
- Recommend papers to read

---

## Common Tasks

### Reset the Database

```bash
python knowledge_graph_builder.py
# Script automatically clears old data
```

### Export Query Results

Modify script to save results:
```python
results = []
for record in result:
    results.append(dict(record))

import json
with open('query_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Run Individual Query

```python
with driver.session() as session:
    result = session.run("""
        MATCH (a:Author)-[:STUDIES]->(f:Field {name: "Natural Language Processing"})
        RETURN a.name, f.name
    """)
    for record in result:
        print(f"{record['a.name']} studies {record['f.name']}")
```

---

## Performance Optimization

### For Larger Datasets

1. **Create Indexes**:
```cypher
CREATE INDEX author_name FOR (a:Author) ON a.name
CREATE INDEX paper_year FOR (p:Paper) ON p.year
```

2. **Use EXPLAIN/PROFILE**:
```cypher
PROFILE MATCH (a:Author)-[:WRITES]->(p:Paper) RETURN * LIMIT 10
```

3. **Batch Imports**:
Split large data into chunks and import gradually

---

## Resources

- **Neo4j Docs**: https://neo4j.com/docs/
- **Cypher Guide**: https://neo4j.com/docs/cypher-manual/current/
- **Python Driver**: https://neo4j.com/docs/api/python-driver/current/
- **Tutorial**: https://neo4j.com/graphacademy/
- **Sample Datasets**: https://github.com/neo4j-examples

---

## Support

If you encounter issues:

1. Check Neo4j server logs
2. Verify connection settings
3. Review error messages in Python output
4. Check Neo4j documentation

---

**Last Updated**: April 2026
**Version**: 1.0
