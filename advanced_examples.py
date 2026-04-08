"""
Advanced Knowledge Graph Examples and Extensions
Domain: Research Publications

This file contains example extensions, custom queries, and advanced techniques
for the knowledge graph project.
"""

# ============================================================================
# EXAMPLE 1: Custom Query Execution
# ============================================================================

def example_custom_query(driver):
    """Execute a custom query and pretty-print results."""
    
    with driver.session() as session:
        query = """
        MATCH (a:Author)-[:STUDIES]->(f:Field {name: "Natural Language Processing"})
        MATCH (a)-[:AFFILIATED_WITH]->(u:University)
        RETURN a.name as author, u.name as university, a.researchFocus
        ORDER BY u.name
        """
        
        result = session.run(query)
        
        print("\n", "="*60)
        print("NLP RESEARCHERS BY UNIVERSITY")
        print("="*60)
        for record in result:
            print(f"  {record['author']:25} | {record['university']:20} | {record['researchFocus']}")


# ============================================================================
# EXAMPLE 2: Parameterized Query with User Input
# ============================================================================

def example_find_author_papers(driver, author_name: str):
    """Find all papers by a specific author."""
    
    with driver.session() as session:
        query = """
        MATCH (a:Author {name: $author_name})-[:WRITES]->(p:Paper)
        RETURN p.title, p.year, p.citations, p.doi
        ORDER BY p.citations DESC
        """
        
        result = session.run(query, author_name=author_name)
        records = list(result)
        
        print(f"\n{'='*60}")
        print(f"PAPERS BY {author_name.upper()}")
        print(f"{'='*60}")
        
        if not records:
            print(f"  No papers found for author: {author_name}")
            return
        
        for i, record in enumerate(records, 1):
            print(f"\n  {i}. {record['p.title']}")
            print(f"     Year: {record['p.year']}, Citations: {record['p.citations']}")
            print(f"     DOI: {record['p.doi']}")


# ============================================================================
# EXAMPLE 3: Graph Statistics and Analytics
# ============================================================================

def example_graph_statistics(driver):
    """Get statistics about the graph structure."""
    
    with driver.session() as session:
        stats = {}
        
        # Count nodes by type
        queries = {
            'authors': 'MATCH (a:Author) RETURN COUNT(a)',
            'papers': 'MATCH (p:Paper) RETURN COUNT(p)',
            'fields': 'MATCH (f:Field) RETURN COUNT(f)',
            'universities': 'MATCH (u:University) RETURN COUNT(u)',
            'conferences': 'MATCH (c:Conference) RETURN COUNT(c)',
            'relationships': 'MATCH ()-[r]-() RETURN COUNT(r)',
        }
        
        for stat_name, query in queries.items():
            result = session.run(query)
            count = result.single()[0]
            stats[stat_name] = count
        
        print("\n", "="*60)
        print("GRAPH STATISTICS")
        print("="*60)
        for name, count in stats.items():
            print(f"  {name:25}: {count}")
        
        return stats


# ============================================================================
# EXAMPLE 4: Find Collaboration Opportunities
# ============================================================================

def example_collaboration_opportunities(driver, field_name: str):
    """Find potential collaborators in the same field at different institutions."""
    
    with driver.session() as session:
        query = """
        MATCH (a1:Author)-[:STUDIES]->(f:Field {name: $field_name})
        MATCH (a1)-[:AFFILIATED_WITH]->(u1:University)
        MATCH (a2:Author)-[:STUDIES]->(f)
        MATCH (a2)-[:AFFILIATED_WITH]->(u2:University)
        WHERE a1.id < a2.id AND u1.id <> u2.id
        RETURN a1.name as researcher1, u1.name as institution1,
               a2.name as researcher2, u2.name as institution2
        """
        
        result = session.run(query, field_name=field_name)
        records = list(result)
        
        print(f"\n{'='*80}")
        print(f"COLLABORATION OPPORTUNITIES IN {field_name.upper()}")
        print(f"{'='*80}")
        
        if not records:
            print(f"  No collaboration opportunities found in {field_name}")
            return
        
        for i, record in enumerate(records, 1):
            print(f"\n  {i}. {record['researcher1']:25} ({record['institution1']})")
            print(f"     +  {record['researcher2']:25} ({record['institution2']})")


# ============================================================================
# EXAMPLE 5: Impact Analysis
# ============================================================================

def example_impact_analysis(driver):
    """Analyze paper impact metrics."""
    
    with driver.session() as session:
        # Most cited papers
        query = """
        MATCH (p:Paper)<-[:WRITES]-(a:Author)
        RETURN p.title, p.citations, p.year, a.name
        ORDER BY p.citations DESC
        LIMIT 5
        """
        
        result = session.run(query)
        records = list(result)
        
        print("\n", "="*80)
        print("MOST CITED PAPERS")
        print("="*80)
        
        for i, record in enumerate(records, 1):
            print(f"\n  {i}. {record['p.title']}")
            print(f"     Author: {record['a.name']}")
            print(f"     Citations: {record['p.citations']} (Published: {record['p.year']})")


# ============================================================================
# EXAMPLE 6: Knowledge Transfer Analysis
# ============================================================================

def example_knowledge_transfer(driver):
    """Analyze knowledge transfer through citations and citations."""
    
    with driver.session() as session:
        query = """
        MATCH (source:Author)-[:WRITES]->(p1:Paper)-[:REFERENCES*1..2]->(p2:Paper)<-[:WRITES]-(target:Author)
        WHERE source.id <> target.id
        RETURN DISTINCT source.name as from_author, target.name as to_author
        LIMIT 10
        """
        
        result = session.run(query)
        records = list(result)
        
        print("\n", "="*80)
        print("KNOWLEDGE TRANSFER PATHS (Citation Network)")
        print("="*80)
        
        if not records:
            print("  No knowledge transfer paths found")
            return
        
        for i, record in enumerate(records, 1):
            print(f"  {i}. {record['from_author']:25} ──> {record['to_author']}")


# ============================================================================
# EXAMPLE 7: Add New Data Dynamically
# ============================================================================

def example_add_new_author(driver, author_data: dict):
    """Add a new author to the graph."""
    
    with driver.session() as session:
        query = """
        CREATE (a:Author {
            id: $id,
            name: $name,
            email: $email,
            researchFocus: $focus
        })
        RETURN a
        """
        
        result = session.run(query, **author_data)
        
        print("\n✓ Author added successfully")
        print(f"  {author_data['name']} ({author_data['email']})")


def example_create_collaboration(driver, author1_id: str, author2_id: str, paper_count: int):
    """Create a CO_AUTHORS_WITH relationship between two authors."""
    
    with driver.session() as session:
        query = """
        MATCH (a1:Author {id: $author1})
        MATCH (a2:Author {id: $author2})
        CREATE (a1)-[:CO_AUTHORS_WITH {paperCount: $count}]->(a2)
        RETURN a1.name, a2.name, $count as collaborations
        """
        
        result = session.run(query, author1=author1_id, author2=author2_id, count=paper_count)
        record = result.single()
        
        print(f"\n✓ Collaboration created: {record['a1.name']} ←→ {record['a2.name']} ({record['collaborations']} papers)")


# ============================================================================
# EXAMPLE 8: Export Results
# ============================================================================

def example_export_to_csv(driver, query: str, output_file: str):
    """Execute query and export results to CSV."""
    
    import csv
    
    with driver.session() as session:
        result = session.run(query)
        
        # Get column names from first record
        records = list(result)
        if not records:
            print("No results to export")
            return
        
        keys = list(records[0].keys())
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for record in records:
                writer.writerow(dict(record))
        
        print(f"\n✓ Results exported to {output_file}")
        print(f"  Rows: {len(records)}, Columns: {len(keys)}")


# ============================================================================
# EXAMPLE 9: Recommendation Engine
# ============================================================================

def example_paper_recommendations(driver, paper_title: str, limit: int = 5):
    """Recommend papers based on a given paper."""
    
    with driver.session() as session:
        query = """
        MATCH (p:Paper {title: $title})-[:BELONGS_TO]->(f:Field)
        MATCH (recommended:Paper)-[:BELONGS_TO]->(f)
        WHERE recommended.title <> $title
        RETURN recommended.title, recommended.citations, recommended.year
        ORDER BY recommended.citations DESC
        LIMIT $limit
        """
        
        result = session.run(query, title=paper_title, limit=limit)
        records = list(result)
        
        print(f"\n{'='*80}")
        print(f"RECOMMENDED PAPERS SIMILAR TO: {paper_title}")
        print(f"{'='*80}")
        
        if not records:
            print("No recommendations found")
            return
        
        for i, record in enumerate(records, 1):
            print(f"  {i}. {record['recommended.title']}")
            print(f"     Citations: {record['recommended.citations']}, Year: {record['recommended.year']}")


# ============================================================================
# EXAMPLE 10: Community Detection (Simple)
# ============================================================================

def example_find_communities(driver):
    """Identify research communities based on collaborations."""
    
    with driver.session() as session:
        query = """
        MATCH (a1:Author)-[:CO_AUTHORS_WITH]-(a2:Author)
        WITH a1, a2, COUNT(*) as strength
        WHERE strength >= 1
        RETURN a1.name, COLLECT(DISTINCT a2.name) as collaborators, 
               COUNT(DISTINCT a2) as team_size
        ORDER BY team_size DESC
        LIMIT 5
        """
        
        result = session.run(query)
        records = list(result)
        
        print(f"\n{'='*80}")
        print("RESEARCH COMMUNITIES (By Co-authorship)")
        print(f"{'='*80}")
        
        for i, record in enumerate(records, 1):
            collab_str = ", ".join(record['collaborators'][:3])
            if len(record['collaborators']) > 3:
                collab_str += f", ... +{len(record['collaborators']) - 3} others"
            
            print(f"\n  {i}. {record['a1.name']} (team size: {record['team_size']})")
            print(f"     Collaborators: {collab_str}")


# ============================================================================
# MAIN EXECUTION EXAMPLES
# ============================================================================

def main_examples():
    """Run all example functions."""
    
    from neo4j import GraphDatabase
    
    # Connect to database
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    
    try:
        print("\n" + "="*80)
        print("KNOWLEDGE GRAPH - ADVANCED EXAMPLES")
        print("="*80)
        
        # Run examples
        example_graph_statistics(driver)
        example_custom_query(driver)
        example_find_author_papers(driver, "Christopher Manning")
        example_collaboration_opportunities(driver, "Natural Language Processing")
        example_impact_analysis(driver)
        example_knowledge_transfer(driver)
        example_find_communities(driver)
        
        # Example: Export query results
        export_query = """
        MATCH (a:Author)-[:WRITES]->(p:Paper)
        RETURN a.name as author, p.title as paper_title, p.year as year, p.citations as citations
        ORDER BY p.citations DESC
        """
        example_export_to_csv(driver, export_query, "query_results.csv")
        
        # Example: Paper recommendations
        example_paper_recommendations(driver, "Attention is All You Need", limit=3)
        
    finally:
        driver.close()


# ============================================================================
# TEMPLATE: Creating a Custom Analysis Function
# ============================================================================

def template_custom_analysis(driver, query_param: str = None):
    """
    Template for creating custom analysis functions.
    
    Args:
        driver: Neo4j driver instance
        query_param: Optional parameter for the query
    """
    
    with driver.session() as session:
        # Your custom Cypher query
        query = """
        MATCH (a:Author)-[:STUDIES]->(f:Field)
        WHERE f.name CONTAINS $search
        RETURN a.name, f.name, a.researchFocus
        LIMIT 10
        """
        
        # Execute query with parameters
        result = session.run(query, search=query_param or "")
        
        # Process results
        print(f"\n{'='*60}")
        print(f"CUSTOM ANALYSIS RESULTS")
        print(f"{'='*60}")
        
        for record in result:
            print(f"  Author: {record['a.name']}")
            print(f"  Field: {record['f.name']}")
            print(f"  Focus: {record['a.researchFocus']}")
            print()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def pretty_print_record(record, title: str = None):
    """Pretty print a single database record."""
    if title:
        print(f"\n{title}")
        print("-" * len(title))
    for key, value in dict(record).items():
        print(f"  {key}: {value}")


def format_results_table(records: list, columns: list):
    """Format results as a table."""
    
    if not records:
        print("No records found")
        return
    
    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for record in records:
        for col in columns:
            widths[col] = max(widths[col], len(str(record.get(col, ""))))
    
    # Print header
    header = " | ".join(f"{col.ljust(widths[col])}" for col in columns)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for record in records:
        row = " | ".join(f"{str(record.get(col, '')).ljust(widths[col])}" for col in columns)
        print(row)


# ============================================================================
# If running this file directly
# ============================================================================

if __name__ == "__main__":
    main_examples()
