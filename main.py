# Extract Schema 

from sqlalchemy import create_engine, inspect

db_url = 'sqlite://amazon.db'

engine = create_engine(db_url)
inspector = inspect
 
# Text to SQL (LLM with Ollama)

# Build StreamLit frontend 