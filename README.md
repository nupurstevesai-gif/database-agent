Root Files:

.env - Stores sensitive information (never commit to git)
.gitignore - Tells git what files to ignore
requirements.txt - Lists all Python packages needed
README.md - Project description and setup instructions
app.py - Main Streamlit application (what you run)

Folders:

tools/ - Contains all tool definitions

Separates web search from database operations
Easy to add more tools later


agent/ - Contains agent orchestration logic

LangGraph workflow lives here
Keeps agent logic separate from UI