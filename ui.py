import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from agent.agent import agent

# Load env
load_dotenv()

DB_URL = os.getenv("DB_URL")

# ----------------- DATABASE -----------------
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

st.set_page_config(page_title="Candy Cloud Chat", layout="wide")

# Inject Pastel Animated CSS (Green + Blue + Lavender Blend)
candy_css = """
<style>

@keyframes candyGradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        120deg,
        #ccffe0,
        #bfe7ff,
        #e3caff,
        #ffd6ea,
        #d6ffe9
    );
    background-size: 500% 500%;
    animation: candyGradient 15s ease-in-out infinite;
    padding-top: 20px;
}

.chat-box {
    padding: 15px 20px;
    border-radius: 18px;
    margin-bottom: 15px;
    max-width: 78%;
    font-size: 16px;
    line-height: 1.5;
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.60);
    border: 2px solid rgba(255, 255, 255, 0.45);
    box-shadow: 0 4px 12px rgba(150, 180, 255, 0.25);
}

.user-box {
    border-left: 5px solid #8bd8b3;
}

.agent-box {
    border-left: 5px solid #9f8bff;
}

h1, .section-title {
    color: #6a5da8 !important;
    text-shadow: 0px 1px 3px rgba(255, 255, 255, 0.5);
    font-weight: 700;
}

textarea, input[type="text"] {
    border-radius: 15px !important;
    background: rgba(255, 255, 255, 0.88) !important;
    border: 2px solid #d4c3ff !important;
    font-size: 16px !important;
    padding: 10px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #b8f1d1, #c7b6ff);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 16px;
    box-shadow: 0px 3px 10px rgba(150, 120, 255, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #a4ebc3, #b9a7ff);
    transform: translateY(-2px);
    transition: 0.2s ease-in-out;
}

</style>
"""
st.markdown(candy_css, unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.markdown("<h1 style='text-align:center;'>🤖 Chat Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6a5da8;'>Ask questions • View chat history </p>", unsafe_allow_html=True)
st.divider()


# ----------------- USER INPUT -----------------
st.markdown("<h3 class='section-title'>💬 Ask something:</h3>", unsafe_allow_html=True)

user_input = st.text_input(" ", placeholder="Type your question here...")

if st.button("Send"):
    if user_input.strip():
        response = agent(user_input)

        st.markdown("<h3 class='section-title'>🤖 Agent Response</h3>", unsafe_allow_html=True)

        st.markdown(
            f"<div class='chat-box agent-box'>{response}</div>",
            unsafe_allow_html=True
        )

    else:
        st.warning("Please type something!")


st.divider()


# ----------------- CHAT HISTORY -----------------
chats = fetch_last_5_chats()

if isinstance(chats, str):
    st.error(chats)

elif len(chats) > 0:
    st.markdown("<h3 class='section-title'>🕒 Recent Conversations</h3>", unsafe_allow_html=True)

    for user_query, agent_answer, created_at in chats:
        st.markdown(
            f"<div class='chat-box user-box'><b>🧑 User:</b><br>{user_query}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='chat-box agent-box'><b>🤖 Agent:</b><br>{agent_answer}</div>",
            unsafe_allow_html=True
        )

else:
    st.markdown("<p style='opacity:0.6; text-align:center;'>No recent chat history.</p>", unsafe_allow_html=True)
