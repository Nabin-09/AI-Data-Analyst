# backend.py - Complete Updated Code

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
    """Extract database schema and return as JSON"""
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
    """Generate SQL query from natural language prompt"""
    SYSTEM_PROMPT = SYSTEM_PROMPT = """
    You are an expert SQL query generator for SQLite databases. Given a database schema and a user prompt, generate a valid, efficient SQLite query that precisely answers the prompt.

    **CRITICAL: You MUST generate SQLite syntax ONLY. This is NOT MySQL, PostgreSQL, or MS SQL Server.**

    **SQLite-Specific Syntax Rules:**
    - For random ordering: Use RANDOM() NOT RAND()
    - For string concatenation: Use || NOT CONCAT()
    - For LIMIT with OFFSET: LIMIT x OFFSET y
    - Date functions: date(), datetime(), strftime()
    - No UNSIGNED, ENUM, or SET data types
    - Use AUTOINCREMENT not AUTO_INCREMENT

    **Core Requirements:**
    - Use ONLY the tables and columns explicitly provided in the schema
    - Ensure all SQL syntax is correct SQLite syntax
    - Output ONLY the SQL query—no explanations, markdown, or additional text
    - Generate queries optimized for SQLite performance

    **Query Construction Guidelines:**
    1. **Schema Adherence**: Reference only tables and columns in the provided schema

    2. **SQLite Best Practices**:
    - Use proper JOIN syntax (INNER JOIN, LEFT JOIN, etc.)
    - Apply WHERE clauses for filtering
    - Use aggregate functions: COUNT(), SUM(), AVG(), MIN(), MAX()
    - For random results: ORDER BY RANDOM()
    - Add LIMIT for top N results
    - Use DISTINCT to eliminate duplicates

    3. **Common Patterns**:
    - Latest record: ORDER BY date_column DESC LIMIT 1
    - Top N: ORDER BY column DESC LIMIT N
    - Random N: ORDER BY RANDOM() LIMIT N
    - Counting: COUNT(*) with GROUP BY
    - Date ranges: WHERE date BETWEEN 'start' AND 'end'
    - Pattern matching: WHERE column LIKE '%pattern%'

    4. **Output Format**:
    - Return ONLY the executable SQLite query
    - Use UPPERCASE for SQL keywords
    - End with a semicolon
    - No explanations or comments

    **Example:**
    Schema: customers (id, name, email, created_at)
    Prompt: "Show me 10 random customer names"
    Output: SELECT name FROM customers ORDER BY RANDOM() LIMIT 10;

    Generate the SQLite query now.
    """
    

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT),
        ('user', 'Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:')
    ])

    # Use faster model (change to 'phi3' if deepseek-r1:8b is too slow)
    model = OllamaLLM(model='deepseek-r1:8b', timeout=30)

    chain = prompt_template | model

    try:
        raw = chain.invoke({'schema': schema, 'user_prompt': prompt})
        sql_query = parse_sql_from_response(raw)
        return sql_query
    except Exception as e:
        return f"-- Error generating query: {str(e)}"

def get_data_from_database(prompt):
    """Execute SQL query with proper error handling and return column names"""
    try:
        schema = extract_schema(db_url)
        sql_query = text_to_sql(schema, prompt)
        
        print(f"Generated SQL: {sql_query}")  # Debug log
        
        db_path = 'amazon.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        try:
            res = cur.execute(sql_query)
            results = res.fetchall()
            
            # Get column names from cursor description
            column_names = [description[0] for description in cur.description] if cur.description else []
            
            return {
                'success': True, 
                'data': results, 
                'columns': column_names,
                'query': sql_query
            }
        except sqlite3.Error as e:
            return {
                'success': False, 
                'error': str(e), 
                'query': sql_query, 
                'columns': [], 
                'data': []
            }
        finally:
            cur.close()
            conn.close()
            
    except Exception as e:
        return {
            'success': False, 
            'error': f"System error: {str(e)}", 
            'query': None, 
            'columns': [], 
            'data': []
        }
