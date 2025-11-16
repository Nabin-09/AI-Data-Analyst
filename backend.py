# Extract Schema 

from sqlalchemy import create_engine, inspect
import json
import sqlite3  
import warnings
import re
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater")

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

db_url = 'sqlite:///amazon.db'

def extract_schema(db_url): 
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]

    return json.dumps(schema)

def parse_sql_from_response(raw_response):
    """Extract SQL query from model response, removing thinking process"""
    # DeepSeek R1 often includes <think>...</think> tags
    # Remove thinking tags if present
    response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL)
    
    # Extract SQL query (look for SELECT, INSERT, UPDATE, DELETE)
    sql_pattern = r'(SELECT.*?;|INSERT.*?;|UPDATE.*?;|DELETE.*?;)'
    matches = re.findall(sql_pattern, response, re.IGNORECASE | re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # Fallback: return cleaned response
    return response.strip()

def text_to_sql(schema, prompt):
    SYSTEM_PROMPT = """
    You are an expert SQL query generator with deep knowledge of database design, optimization, and SQL syntax across multiple database systems. Given a database schema and a user prompt, generate a valid, efficient SQL query that precisely answers the prompt.

    **Core Requirements:**
    - Use ONLY the tables and columns explicitly provided in the schema
    - Ensure all SQL syntax is correct and follows standard SQL conventions
    - Output ONLY the SQL query—no explanations, markdown formatting, or additional text
    - Generate queries that are optimized for performance and readability

    **Query Construction Guidelines:**
    1. **Schema Adherence**: Reference only tables and columns that exist in the provided schema. Do not invent or assume additional tables or columns.

    2. **SQL Best Practices**:
    - Use proper JOIN syntax when combining tables
    - Apply appropriate WHERE clauses for filtering
    - Use aggregate functions (COUNT, SUM, AVG, etc.) when requesting summaries
    - Include ORDER BY when results need sorting
    - Add LIMIT/TOP clauses when the prompt requests a specific number of results
    - Use DISTINCT when duplicate elimination is required

    3. **Query Optimization**:
    - Select only necessary columns instead of using SELECT *
    - Use indexes efficiently by filtering on indexed columns when possible
    - Avoid redundant subqueries
    - Use appropriate join types (INNER, LEFT, RIGHT) based on the requirement

    4. **Common Patterns**:
    - For "latest" or "most recent" requests: ORDER BY date_column DESC LIMIT 1
    - For "top N" requests: ORDER BY relevant_column DESC LIMIT N
    - For counting: Use COUNT() with appropriate GROUP BY
    - For date ranges: Use BETWEEN or >= and <= operators
    - For pattern matching: Use LIKE with appropriate wildcards

    5. **Handling Ambiguity**:
    - If column names are unclear, use the most semantically appropriate column
    - For time-based queries without specified time zones, use the database's default
    - When multiple interpretations exist, choose the most common use case

    6. **Output Format**:
    - Return only the executable SQL query
    - Use consistent casing (prefer UPPERCASE for SQL keywords)
    - Format complex queries with appropriate line breaks for readability
    - End with a semicolon

    **Critical Constraints:**
    - Never use tables or columns not in the schema
    - Never include explanatory text before or after the query
    - Never use unsupported SQL features unless specified in the schema's database type
    - Always validate that joins reference valid foreign key relationships when possible

    Generate the SQL query now.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT),
        ('user', 'Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:')
    ])

    # FIX: Changed model name to 'deepseek-r1' (check with 'ollama list')
    model = OllamaLLM(model='deepseek-r1:8b')

    chain = prompt_template | model

    raw = chain.invoke({'schema': schema, 'user_prompt': prompt})
    
    # FIX: Parse SQL from response
    sql_query = parse_sql_from_response(raw)
    return sql_query

def get_data_from_database(prompt):
    """Execute SQL query with proper error handling"""
    try:
        schema = extract_schema(db_url)
        sql_query = text_to_sql(schema, prompt)
        
        print(f"Generated SQL: {sql_query}")  # Debug log
        
        db_path = 'amazon.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # FIX: Add error handling for SQL execution
        try:
            res = cur.execute(sql_query)
            results = res.fetchall()
            return {'success': True, 'data': results, 'query': sql_query}
        except sqlite3.Error as e:
            return {'success': False, 'error': str(e), 'query': sql_query}
        finally:
            # FIX: Always close connection
            cur.close()
            conn.close()
            
    except Exception as e:
        return {'success': False, 'error': f"System error: {str(e)}", 'query': None}
