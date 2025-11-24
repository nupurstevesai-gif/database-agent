import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from agent.agent import agent

load_dotenv()

DB_URL = os.getenv("DB_URL")

def fetch_last_5_chats():
    """Fetch the last 5 chats from PostgreSQL."""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT user_query, agent_answer, created_at
            FROM chat_history
            ORDER BY created_at DESC
            LIMIT 5;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    except Exception as e:
        return f"DB Error: {str(e)}"


# ----------------- STREAMLIT UI -----------------

st.set_page_config(page_title="Chat Dashboard", layout="wide")
st.title("Chat Dashboard")

st.divider()

# Input box
user_input = st.text_input("Ask me anything:")

# When Send button clicked
if st.button("Send"):
    if user_input.strip():
        response = agent(user_input)  # agent writes to DB internally
        
        # Show current answer immediately
        st.markdown("### 🤖 Agent:")
        st.write(response)
    else:
        st.warning("Please type something!")

st.divider()

# ---------------- SHOW LAST 5 CHATS ----------------

chats = fetch_last_5_chats()

if isinstance(chats, str):
    st.error(chats)   # DB error
else:
    if len(chats) == 0:
        pass  # Show nothing if DB has no rows
    else:
        st.markdown("## 🕒 Recent Chats")

        for user_query, agent_answer, created_at in chats:
            st.markdown(f"**🧑 User:** {user_query}")
            st.markdown(f"**🤖 Agent:** {agent_answer}")
            st.markdown("---")
