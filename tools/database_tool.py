from langchain.tools import tool
import psycopg2
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
DB_URL = os.getenv("DB_URL")


@tool
def save_chat_tool(user_query: str, agent_answer: str) -> str:
    """
    Save a chat entry into PostgreSQL.
    
    Inputs:
        user_query: The user's question
        agent_answer: The AI's response

    Returns:
        Status message confirming insert result.
    """
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO chat_history (user_query, agent_answer)
            VALUES (%s, %s)
        """, (user_query, agent_answer))

        conn.commit()
        cur.close()
        conn.close()

        return "Chat saved successfully."

    except Exception as e:
        return f"DB Error (save): {str(e)}"



@tool
def fetch_chats_tool(limit: int = 5) -> str:
    """
    Fetch last N chats from PostgreSQL.
    
    Inputs:
        limit: Number of rows to return (default 5)

    Returns:
        Chat history records formatted as text.
    """
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT user_query, agent_answer, created_at
            FROM chat_history
            ORDER BY created_at DESC
            LIMIT %s;
        """, (limit,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        # Format output for the agent
        output = ""
        for user_q, agent_ans, ts in rows:
            output += f"[{ts}]\nUSER: {user_q}\nAGENT: {agent_ans}\n\n"

        return output if output else "No chat history found."

    except Exception as e:
        return f"DB Error (fetch): {str(e)}"
