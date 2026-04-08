# Knowledge Graph Schema: Research Publications

## Domain: Academic Research Publications & NLP

### Entities (Nodes)

1. **Author**
   - Properties: name, email, url, researchFocus
   - Example: Alice Johnson, NLP specialist

2. **Paper**
   - Properties: title, year, abstract, doi, citations
   - Example: "Transformers: Attention Is All You Need"

3. **Field**
   - Properties: name, description
   - Example: Natural Language Processing, Machine Learning

4. **University**
   - Properties: name, country, ranking
   - Example: MIT, USA

5. **Conference**
   - Properties: name, year, location, acronym
   - Example: ACL 2023, Toronto

6. **Venue** (for publications)
   - Properties: name, type (journal/conference), issn
   - Example: Proceedings of ACL

### Relationships (Edges)

1. **WRITES** - Author to Paper
   - Properties: role (lead, contributor)

2. **BELONGS_TO** - Paper to Field
   - Properties: confidence (primary/secondary)

3. **AFFILIATED_WITH** - Author to University
   - Properties: role (student, professor, researcher), startYear, endYear

4. **CO_AUTHORS_WITH** - Author to Author (derived from collaboration)
   - Properties: paperCount, lastCollaborationYear

5. **PUBLISHED_AT** - Paper to Conference
   - Properties: type (oral, poster, workshop)

6. **PUBLISHED_IN** - Paper to Venue
   - Properties: volume, issue, pages

7. **STUDIES** - Author to Field
   - Properties: yearsExperience

8. **REFERENCES** - Paper to Paper
   - Properties: context (methodological, theoretical, empirical)

9. **HOSTED_BY** - Conference to University
   - Properties: hostYear

### Graph Reasoning Examples

- Find authors in the same field across different universities (indirect relationships)
- Identify collaboration networks and bridges between research groups
- Discover emerging topics based on citation patterns
- Find experts who didn't collaborate but work on related topics
