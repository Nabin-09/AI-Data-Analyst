

# 🤖 AI Database Analyzer

![Python](http://github.com/Nabin-09/AI-Data-Analyst/blob/main/images/Screenshot%202025-11-16%20135209.png?raw=1) **Transform natural language questions into SQL queries and analyze your database instantly using AI.**

An intelligent database analysis tool that converts plain English questions into SQL queries, executes them, and presents results in a beautiful interactive dashboard. Powered by DeepSeek-R1 running locally via Ollama.

![AI Database Analyzer Demo](https://github.com/Nabin-09/AI-Data-Analyst/blob/main/images/Screenshot%202025-11-16%20135218.png?raw=1) 🌟 Features

- 🗣️ **Natural Language to SQL**: Ask questions in plain English, get SQL queries automatically
- 🤖 **Local AI Model**: Uses DeepSeek-R1 via Ollama (100% free, runs offline)
- 📊 **Interactive Results**: Beautiful data tables with download capabilities
  - 🔍 **Query Transparency**: See the generated SQL query for every analysis
  - 💾 **CSV Export**: Download query results as CSV files
- ⚡ **SQLite Support**: Works with SQLite databases out of the box
- 🎨 **Modern UI**: Clean, responsive Streamlit interface

***

## 🚀 Demo

**Example Questions You Can Ask:**

- "Show me the top 10 products by revenue"
- "Compare sales performance across different categories"
- "Find customers who made purchases in the last 30 days"
            - "Calculate the average order value by month"  
- "List the 5 best-selling products this year"

![Query Results](images/Screenshot%202025- 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.13 |
| **AI Model** | DeepSeek-R1 (8B) via Ollama |
| **LLM Framework** | LangChain |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |
| **Package Manager** | uv |

***

## 📋 Prerequisites

- Python 3.10 or higher (recommended: 3.13)
- Ollama installed ([Download here](https://ollama.ai))
- 8GB+ RAM (for running DeepSeek-R1)
- SQLite database file

***

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nabin-09/AI-Data-Analyst.git
cd AI-Data-Analyst
```

### 2. Install Ollama and Download Model

```bash
# Install Ollama (Windows)
# Download from https://ollama.ai/download

# Pull the DeepSeek-R1 model
ollama pull deepseek-r1:8b
```

### 3. Set Up Python Environment

**Using uv (Recommended)**:

```bash
# Install uv
pip install uv

# Install Python 3.13
uv python install 3.13

# Pin project to Python 3.13
uv python pin 3.13

# Install dependencies
uv pip install streamlit langchain-ollama sqlalchemy pandas
```

**Using pip**:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit langchain-ollama sqlalchemy pandas
```

### 4. Prepare Your Database

Place your SQLite database file (`amazon.db` or your own) in the project root directory.

---

## 🎯 Usage

### Run the Application

```bash
streamlit run frontend.py
```

The app will open in your browser at `http://localhost:8501`

### Example Workflow

1. **Enter your question** in natural language
2. **Click "Analyze"** to generate SQL query
3. **View results** in an interactive table
4. **Download CSV** if needed
5. **Check generated SQL** in the expander

***

## 📁 Project Structure

```
AI-Data-Analyst/
├── backend.py              # Database logic and AI integration
├── frontend.py             # Streamlit UI
├── amazon.db              # SQLite database (example)
├── images/                # Screenshots
│   ├── Screenshot 2025-11-16 135209.png
│   └── Screenshot 2025-11-16 135218.png
├── .python-version        # Python version specification
├── pyproject.toml         # Project metadata
├── uv.lock               # Dependency lock file
└── README.md             # This file
```

***

## 🔧 How It Works

### Architecture

```
User Query → LangChain → DeepSeek-R1 → SQL Query → SQLite → Results → Streamlit UI
```

### Workflow

1. **Schema Extraction**: Automatically extracts database schema using SQLAlchemy
2. **Prompt Engineering**: Sends schema + user question to DeepSeek-R1
3. **SQL Generation**: AI model generates SQLite-compatible query
4. **Query Execution**: Executes query safely with error handling
5. **Result Presentation**: Displays data in pandas DataFrame with column names
6. **Export Option**: Allows CSV download of results

***

## 🚀 Future Improvements

### Short-term Enhancements

- [ ] **Multi-database Support**: PostgreSQL, MySQL, MongoDB integration
- [ ] **Query History**: Save and reuse previous queries
- [ ] **Data Visualization**: Auto-generate charts for numerical results
- [ ] **Query Optimization**: Suggest index creation for slow queries
- [ ] **Error Suggestions**: AI-powered error resolution hints

### Medium-term Features

- [ ] **Natural Language Insights**: Generate business insights from results
- [ ] **Advanced Analytics**: Statistical analysis, trend detection
- [ ] **Custom Dashboards**: Save and share custom analysis views
- [ ] **Collaboration**: Multi-user support with shared queries
- [ ] **API Integration**: RESTful API for programmatic access

### Long-term Vision

- [ ] **AutoML Integration**: Automatic predictive modeling
- [ ] **Real-time Monitoring**: Live database change alerts
- [ ] **Cloud Deployment**: AWS/Azure hosting with authentication
- [ ] **Enterprise Features**: Role-based access, audit logs
- [ ] **Multi-modal Analysis**: Image, text, and structured data analysis

***

## 🐛 Known Issues & Limitations

### Current Limitations

1. **Model Speed**: DeepSeek-R1 is slower (10-15 tokens/sec) - consider switching to Phi3 for faster responses
2. **SQLite Only**: Currently supports SQLite; other databases require code modifications
3. **No Authentication**: Single-user mode only
4. **Limited Error Recovery**: Manual intervention needed for some errors

### Workarounds

- **Slow responses**: Use `phi3` model instead (`ollama pull phi3`)
- **Complex queries**: Break into simpler sub-queries
- **MySQL syntax errors**: System prompt now enforces SQLite syntax

***

## 🔐 Security Considerations

- ⚠️ **SQL Injection**: Generated queries are validated but not 100% safe for production
- ⚠️ **No Access Control**: Anyone with access can query entire database
- ⚠️ **Local Only**: Not production-ready for public deployment

**Recommendations for Production**:
- Implement query whitelisting
- Add user authentication (OAuth, JWT)
- Use read-only database connections
- Add rate limiting
- Implement comprehensive logging

***

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

***

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - For local LLM inference
- [DeepSeek AI](https://www.deepseek.com/) - For the R1 reasoning model
- [LangChain](https://langchain.com/) - For LLM orchestration
- [Streamlit](https://streamlit.io/) - For the amazing web framework

***

## 📧 Contact

**Nabin** - [@Nabin-09](https://github.com/Nabin-09)

**Project Link**: [https://github.com/Nabin-09/AI-Data-Analyst](https://github.com/Nabin-09/AI-Data-Analyst)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

***
