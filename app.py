import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import uuid
import time
from prompts import SYSTEM_PROMPT, MOCK_INTERVIEW_PROMPT

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="NEXA AI", page_icon="assets/logo.png", layout="centered")

MODES = ["💬 Ask Nexa", "🧩 DSA Practice", "📘 Concept Explainer", "🎤 Mock Interview", "❓ Question Generator"]

# ---------- 1. Initialize chat storage (runs once) ----------
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}     # {chat_id: {"title", "mode", "messages"}}
    st.session_state.current_chat_id = None

def create_new_chat(mode=MODES[0]):
    chat_id = str(uuid.uuid4())
    st.session_state.all_chats[chat_id] = {"title": "New chat", "mode": mode, "messages": []}
    st.session_state.current_chat_id = chat_id

# if there are no chats yet, create the very first one
if st.session_state.current_chat_id is None:
    create_new_chat()

current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# ---------- 2. Sidebar ----------
st.sidebar.title("NEXA AI")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    create_new_chat()
    st.rerun()

st.sidebar.divider()

# mode selector - now comes BEFORE recent chats
mode = st.sidebar.selectbox("Choose a mode", MODES, index=MODES.index(current_chat["mode"]))
current_chat["mode"] = mode

if mode == "📘 Concept Explainer":
    topic = st.sidebar.selectbox("Subject", ["OS", "DBMS", "Computer Networks", "OOPs", "Data Structures", "Algorithms"])
if mode == "🎤 Mock Interview":
    role = st.sidebar.text_input("Target role", "Software Engineer")
if mode == "❓ Question Generator":
    qtopic = st.sidebar.text_input("Topic", "Arrays")
    n = st.sidebar.slider("How many questions?", 1, 10, 5)

st.sidebar.divider()
st.sidebar.caption("Recent chats")

for chat_id in reversed(list(st.session_state.all_chats.keys())):
    chat = st.session_state.all_chats[chat_id]
    is_active = chat_id == st.session_state.current_chat_id
    label = ("📍 " if is_active else "") + chat["title"]
    if st.sidebar.button(label, key=f"select_{chat_id}", use_container_width=True):
        st.session_state.current_chat_id = chat_id
        st.rerun()

st.sidebar.divider()
if st.sidebar.button("🗑️ Delete this chat"):
    del st.session_state.all_chats[st.session_state.current_chat_id]
    if st.session_state.all_chats:
        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
    else:
        create_new_chat()
    st.rerun()

# ---------- 3. Hero section (only when this chat is empty) ----------
if not current_chat["messages"]:
    st.markdown(
        """
        <div style='text-align:center; margin-top:-20px;'>

        </div>
        """,
        unsafe_allow_html=True
    )

    logo_col1, logo_col2, logo_col3 = st.columns([1.5, 1, 1.5])
    with logo_col2:
        st.image("assets/logo.png", width=140)

    st.markdown(
        """
        <h1 style='text-align:center; margin-top:10px; margin-bottom:0;'>
            NEXA AI
        </h1>

        <p style='text-align:center; color:#94A3B8; font-size:16px; margin-top:5px;'>
            Your AI Placement Mentor
        </p>

        <p style='text-align:center; color:#64748B; font-size:14px; margin-top:-5px;'>
            Master DSA • DBMS • OS • CN • Interviews
        </p>
        """,
        unsafe_allow_html=True
    )

# ---------- 4. Show this chat's messages ----------
for msg in current_chat["messages"]:
    avatar = "assets/user.png" if msg["role"] == "user" else "assets/logo.png"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------- 5. Build the right prompt depending on mode ----------
def get_contextual_prompt(user_input):
    if mode == "🧩 DSA Practice":
        return f"Help with this DSA problem. Explain approach, complexity, then code:\n\n{user_input}"
    elif mode == "📘 Concept Explainer":
        return f"Explain this {topic} concept clearly with a real-world analogy and an example:\n\n{user_input}"
    elif mode == "❓ Question Generator":
        return f"Generate {n} interview questions (mix of easy/medium/hard) on: {qtopic}"
    elif mode == "🎤 Mock Interview":
        if not current_chat["messages"]:
            return MOCK_INTERVIEW_PROMPT.format(role=role)
        return user_input
    else:
        return user_input

placeholder = "Ask Nexa..." if mode != "🎤 Mock Interview" else "Type your answer or 'start' to begin..."

if prompt := st.chat_input(placeholder):
    current_chat["messages"].append({"role": "user", "content": prompt})

    # auto-title the chat from the first message
    if current_chat["title"] == "New chat":
        current_chat["title"] = prompt[:30] + ("..." if len(prompt) > 30 else "")

    with st.chat_message("user", avatar="assets/user.png"):
        st.markdown(prompt)

    contextual_prompt = get_contextual_prompt(prompt)
    print(f"Contextual prompt: {contextual_prompt}")  # Debugging line

    history = [
        types.Content(role="user" if m["role"] == "user" else "model", parts=[types.Part(text=m["content"])])
        for m in current_chat["messages"][:-1]
    ]
    history.append(types.Content(role="user", parts=[types.Part(text=contextual_prompt)]))

    print(f"History for Gemini API: {[{'role': c.role, 'text': c.parts[0].text} for c in history]}")  # Debugging line
    with st.chat_message("assistant", avatar="assets/logo.png"):
        with st.spinner("Thinking..."):
            MAX_RETRIES = 3
            for attempt in range(MAX_RETRIES):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=history,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
                    )

                    print(f"Gemini API response: {response}")  # Debugging line
                    reply = response.text
                    break
                except Exception:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2)
                    else:
                        reply = "⚠️ Gemini API is currently busy (503 error).\n\nPlease try again in a few minutes."
            st.markdown(reply)

    current_chat["messages"].append({"role": "assistant", "content": reply})