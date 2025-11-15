# main.py
from sqlalchemy import create_engine, inspect
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db_url = 'sqlite:///amazon.db'

# Extract Schema Function (your existing code)
def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
    
    return json.dumps(schema)

# Initialize Gemini LLM
def initialize_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key,
        temperature=0,
        convert_system_message_to_human=True
    )
    return llm

# Create SQL Database Chain
def create_sql_chain(db_url):
    llm = initialize_llm()
    db = SQLDatabase.from_uri(db_url)
    
    # Custom prompt template
    prompt_template = """You are an expert SQL query generator for an Amazon database.
    
Given an input question, create a syntactically correct SQLite query to run.
The database has the following tables and columns:
{table_info}

Question: {input}

Only return the SQL query without any explanation or markdown formatting.
SQL Query:"""
    
    prompt = PromptTemplate(
        input_variables=["input", "table_info"],
        template=prompt_template
    )
    
    db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        prompt=prompt,
        verbose=True,
        return_intermediate_steps=True
    )
    
    return db_chain

# Query execution function
def execute_query(question, db_chain):
    try:
        response = db_chain(question)
        return response
    except Exception as e:
        return {"error": str(e)}

# Streamlit Frontend
def main():
    st.set_page_config(page_title="AI Data Analyst", page_icon="📊")
    
    st.title("🤖 AI Data Analyst - Text to SQL")
    st.write("Ask questions about your Amazon database in natural language!")
    
    # Display schema
    with st.expander("View Database Schema"):
        schema = extract_schema(db_url)
        st.json(schema)
    
    # Initialize DB chain
    db_chain = create_sql_chain(db_url)
    
    # User input
    question = st.text_input("Ask your question:", 
                             placeholder="e.g., How many customers are there?")
    
    submit = st.button("Generate & Execute Query")
    
    if submit and question:
        with st.spinner("Processing your question..."):
            result = execute_query(question, db_chain)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                # Display SQL query
                if "intermediate_steps" in result:
                    sql_query = result["intermediate_steps"][0]
                    st.subheader("Generated SQL Query:")
                    st.code(sql_query, language="sql")
                
                # Display results
                st.subheader("Query Results:")
                st.write(result["result"])
    
    # Example queries
    st.sidebar.header("Example Questions")
    st.sidebar.write("- How many customers are in the database?")
    st.sidebar.write("- Show me all orders from the orders table")
    st.sidebar.write("- What are the total order items?")
    st.sidebar.write("- List the first 5 customers")

if __name__ == "__main__":
    main()
