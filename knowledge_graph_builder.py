"""
Neo4j Knowledge Graph Builder and Reasoner
Domain: Research Publications & NLP

This script:
1. Connects to Neo4j
2. Creates the graph schema
3. Imports sample data
4. Demonstrates reasoning queries
"""

import json
from neo4j import GraphDatabase
from typing import Dict, List
import os


class KnowledgeGraphManager:
    def __init__(self, uri: str, username: str, password: str):
        """Initialize connection to Neo4j database."""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.session = None

    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()

    def clear_database(self):
        """Clear all nodes and relationships from the database."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ Database cleared")

    def create_constraints(self):
        """Create unique constraints for node IDs."""
        queries = [
            "CREATE CONSTRAINT author_id IF NOT EXISTS FOR (a:Author) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT field_id IF NOT EXISTS FOR (f:Field) REQUIRE f.id IS UNIQUE",
            "CREATE CONSTRAINT university_id IF NOT EXISTS FOR (u:University) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT conference_id IF NOT EXISTS FOR (c:Conference) REQUIRE c.id IS UNIQUE",
        ]
        with self.driver.session() as session:
            for query in queries:
                try:
                    session.run(query)
                except:
                    pass  # Constraint might already exist
            print("✓ Constraints created")

    def import_data(self, data_file: str):
        """Import data from JSON file into Neo4j."""
        with open(data_file, 'r') as f:
            data = json.load(f)

        with self.driver.session() as session:
            # Create Universities
            for uni in data['universities']:
                session.run(
                    "CREATE (u:University {id: $id, name: $name, country: $country, ranking: $ranking})",
                    id=uni['id'], name=uni['name'], country=uni['country'], ranking=uni['ranking']
                )
            print(f"✓ Created {len(data['universities'])} universities")

            # Create Fields
            for field in data['fields']:
                session.run(
                    "CREATE (f:Field {id: $id, name: $name, description: $description})",
                    id=field['id'], name=field['name'], description=field['description']
                )
            print(f"✓ Created {len(data['fields'])} fields")

            # Create Authors
            for author in data['authors']:
                session.run(
                    "CREATE (a:Author {id: $id, name: $name, email: $email, researchFocus: $focus})",
                    id=author['id'], name=author['name'], email=author['email'], focus=author['researchFocus']
                )
            print(f"✓ Created {len(data['authors'])} authors")

            # Create Conferences
            for conf in data['conferences']:
                session.run(
                    "CREATE (c:Conference {id: $id, name: $name, year: $year, location: $location, acronym: $acronym})",
                    id=conf['id'], name=conf['name'], year=conf['year'], 
                    location=conf['location'], acronym=conf['acronym']
                )
            print(f"✓ Created {len(data['conferences'])} conferences")

            # Create Papers
            for paper in data['papers']:
                session.run(
                    """CREATE (p:Paper {id: $id, title: $title, year: $year, 
                       abstract: $abstract, doi: $doi, citations: $citations})""",
                    id=paper['id'], title=paper['title'], year=paper['year'],
                    abstract=paper['abstract'], doi=paper['doi'], citations=paper['citations']
                )
            print(f"✓ Created {len(data['papers'])} papers")

            # Create WRITES relationships (Author -> Paper)
            for paper in data['papers']:
                for author_id in paper['authors']:
                    session.run(
                        "MATCH (a:Author {id: $aid}) MATCH (p:Paper {id: $pid}) CREATE (a)-[:WRITES]->(p)",
                        aid=author_id, pid=paper['id']
                    )
            print(f"✓ Created WRITES relationships")

            # Create BELONGS_TO relationships (Paper -> Field)
            for paper in data['papers']:
                for field_id in paper['fields']:
                    session.run(
                        "MATCH (p:Paper {id: $pid}) MATCH (f:Field {id: $fid}) CREATE (p)-[:BELONGS_TO]->(f)",
                        pid=paper['id'], fid=field_id
                    )
            print(f"✓ Created BELONGS_TO relationships")

            # Create AFFILIATED_WITH relationships (Author -> University)
            for aff in data['affiliations']:
                session.run(
                    """MATCH (a:Author {id: $aid}) MATCH (u:University {id: $uid}) 
                       CREATE (a)-[:AFFILIATED_WITH {role: $role, startYear: $start, endYear: $end}]->(u)""",
                    aid=aff['authorId'], uid=aff['universityId'], role=aff['role'],
                    start=aff['startYear'], end=aff['endYear']
                )
            print(f"✓ Created AFFILIATED_WITH relationships")

            # Create STUDIES relationships (Author -> Field)
            for study in data['studies']:
                session.run(
                    "MATCH (a:Author {id: $aid}) MATCH (f:Field {id: $fid}) CREATE (a)-[:STUDIES {yearsExperience: $years}]->(f)",
                    aid=study['authorId'], fid=study['fieldId'], years=study['yearsExperience']
                )
            print(f"✓ Created STUDIES relationships")

            # Create REFERENCES relationships (Paper -> Paper)
            for ref in data['references']:
                session.run(
                    """MATCH (p1:Paper {id: $pid1}) MATCH (p2:Paper {id: $pid2}) 
                       CREATE (p1)-[:REFERENCES {context: $context}]->(p2)""",
                    pid1=ref['citingPaperId'], pid2=ref['citedPaperId'], context=ref['context']
                )
            print(f"✓ Created REFERENCES relationships")

            # Create CO_AUTHORS_WITH relationships (derived)
            session.run(
                """MATCH (a1:Author)-[:WRITES]->(paper:Paper)<-[:WRITES]-(a2:Author) 
                   WHERE a1.id < a2.id 
                   WITH a1, a2, COUNT(paper) as paperCount 
                   CREATE (a1)-[:CO_AUTHORS_WITH {paperCount: paperCount}]->(a2)"""
            )
            print(f"✓ Created CO_AUTHORS_WITH relationships (derived)")

    def query_reasoning_examples(self):
        """Execute example reasoning queries."""
        queries = {
            "Example 1: Find all NLP researchers": {
                "query": """
                MATCH (author:Author)-[:STUDIES]->(field:Field {name: "Natural Language Processing"})
                RETURN author.name, field.name, author.researchFocus
                ORDER BY author.name
                """,
                "description": "Direct: Find authors studying NLP"
            },
            "Example 2: Find NLP researchers by university affiliation": {
                "query": """
                MATCH (author:Author)-[:STUDIES]->(field:Field {name: "Natural Language Processing"})
                MATCH (author)-[:AFFILIATED_WITH]->(university:University)
                RETURN author.name, university.name, field.name
                ORDER BY university.name, author.name
                """,
                "description": "Reasoning: Combine STUDIES and AFFILIATED_WITH to get researchers' institutions"
            },
            "Example 3: Find collaboration networks in NLP": {
                "query": """
                MATCH (author:Author)-[:STUDIES]->(field:Field {name: "Natural Language Processing"})
                MATCH (author)-[co:CO_AUTHORS_WITH]->(coauthor:Author)
                MATCH (coauthor)-[:STUDIES]->(field)
                RETURN author.name, coauthor.name, co.paperCount as collaborations
                ORDER BY collaborations DESC
                """,
                "description": "Reasoning: Identify collaboration networks within NLP field"
            },
            "Example 4: Find researchers in same field but different universities": {
                "query": """
                MATCH (author1:Author)-[:STUDIES]->(field:Field)
                MATCH (author1)-[:AFFILIATED_WITH]->(uni1:University)
                MATCH (author2:Author)-[:STUDIES]->(field)
                MATCH (author2)-[:AFFILIATED_WITH]->(uni2:University)
                WHERE author1.id < author2.id AND uni1.id <> uni2.id
                RETURN field.name, author1.name, uni1.name, author2.name, uni2.name
                ORDER BY field.name, author1.name
                """,
                "description": "Reasoning: Find potential collaboration opportunities"
            },
            "Example 5: Most cited papers and their authors": {
                "query": """
                MATCH (paper:Paper)<-[:WRITES]-(author:Author)
                RETURN paper.title, paper.year, paper.citations, author.name
                ORDER BY paper.citations DESC
                LIMIT 10
                """,
                "description": "Impact analysis: Highly influential papers"
            },
            "Example 6: Citation network - papers that reference each other": {
                "query": """
                MATCH (p1:Paper)-[:REFERENCES]->(p2:Paper)
                RETURN p1.title as 'Citing Paper', p2.title as 'Cited Paper'
                """,
                "description": "Structural reasoning: Citation patterns in literature"
            },
            "Example 7: Author expertise paths (Multi-hop reasoning)": {
                "query": """
                MATCH path = (author:Author)-[:WRITES]->(:Paper)-[:BELONGS_TO]->(field:Field)
                WHERE author.name = 'Christopher Manning'
                WITH author, COLLECT(DISTINCT field.name) as fields
                RETURN author.name, fields
                """,
                "description": "Multi-hop: Find an author's expertise through their publications"
            },
            "Example 8: Discover emerging researchers": {
                "query": """
                MATCH (author:Author)-[:WRITES]->(paper:Paper)
                MATCH (paper)-[:BELONGS_TO]->(field:Field)
                WITH author, field, COUNT(paper) as papers, AVG(paper.year) as avgYear
                WHERE papers >= 2 AND avgYear >= 2020
                RETURN author.name, field.name, papers, avgYear
                ORDER BY avgYear DESC
                """,
                "description": "Insight discovery: Recent prolific researchers"
            },
            "Example 9: Academic lineage - all collaborators of a researcher": {
                "query": """
                MATCH (target:Author {name: 'Christopher Manning'})-[co:CO_AUTHORS_WITH*1..3]-(colleague:Author)
                RETURN DISTINCT colleague.name
                ORDER BY colleague.name
                """,
                "description": "Network traversal: Extended collaboration network (up to 3 hops)"
            },
            "Example 10: Cross-field expertise": {
                "query": """
                MATCH (author:Author)-[:STUDIES]->(field1:Field)
                MATCH (author)-[:STUDIES]->(field2:Field)
                WHERE field1.id <> field2.id
                RETURN author.name, field1.name, field2.name
                ORDER BY author.name
                """,
                "description": "Multi-field expertise: Authors studying multiple domains"
            }
        }

        print("\n" + "="*80)
        print("KNOWLEDGE GRAPH REASONING QUERIES")
        print("="*80)

        with self.driver.session() as session:
            for title, example in queries.items():
                print(f"\n{title}")
                print(f"Description: {example['description']}")
                print("-" * 80)
                try:
                    result = session.run(example['query'])
                    records = list(result)
                    if records:
                        print(f"Results ({len(records)} rows):")
                        for record in records:
                            print(f"  {dict(record)}")
                    else:
                        print("  [No results]")
                except Exception as e:
                    print(f"  Error executing query: {str(e)}")


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("NEO4J KNOWLEDGE GRAPH: Research Publications Domain")
    print("="*80 + "\n")

    # Configuration
    NEO4J_URI = "bolt://localhost:7687"
    USERNAME = "neo4j"
    PASSWORD = "PASSWORD" 

    # Get the data file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "sample_data.json")

    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return

    # Initialize manager
    manager = KnowledgeGraphManager(NEO4J_URI, USERNAME, PASSWORD)

    try:
        print("Connecting to Neo4j database...")
        # Test connection
        with manager.driver.session() as session:
            session.run("RETURN 1")
        print("✓ Connected successfully\n")

        # Clear and rebuild
        print("Step 1: Clearing database...")
        manager.clear_database()

        print("\nStep 2: Creating constraints...")
        manager.create_constraints()

        print("\nStep 3: Importing data...")
        manager.import_data(data_file)

        print("\nStep 4: Running reasoning queries...\n")
        manager.query_reasoning_examples()

        print("\n" + "="*80)
        print("✓ Knowledge Graph construction completed successfully!")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Neo4j database is running locally")
        print("  2. Correct credentials are provided (default: neo4j/password)")
        print("  3. Update NEO4J_URI if using non-default port")
    finally:
        manager.close()


if __name__ == "__main__":
    main()
