import streamlit as st
from datetime import datetime , UTC
import pytz

from api_client import (
    checkauth_user,
    fetch_ai_response,
    logout_user,
    get_full_chat_history,
    get_chat_history
)

st.set_page_config(
    page_title="Multi-Agent Security Auditor",
    page_icon="🛡️",
    layout="wide",
)

# Current UTC time
india_time = datetime.now(pytz.timezone("Asia/Kolkata"))
current_hour = india_time.hour

# Greeting logic
if 5 <= current_hour < 12:
    greeting = "Good Morning"

elif 12 <= current_hour < 17:
    greeting = "Good Afternoon"

elif 17 <= current_hour < 21:
    greeting = "Good Evening"

else:
    greeting = "Good Night"

st.markdown(
    """
    <style>
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    .user-pill {
        border-radius: 14px;
        padding: 0.6rem 0.8rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .chat-item {
        padding: 0.4rem 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state:
    st.toast("Please Login before accessing Vantaguard", icon="☠️")
    st.switch_page("pages/login.py")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = []

if "show_user_panel" not in st.session_state:
    st.session_state.show_user_panel = False

def refresh_chat_histories():
    response = get_full_chat_history()
    if response and response.status_code == 200:
        body = response.json()
        st.session_state.chat_histories = body.get("chat_histories", [])
    else:
        st.session_state.chat_histories = []

def load_chat(chat_id: str):
    response = get_chat_history(chat_id)
    if not response:
        st.toast("Failed to load chat history", icon="☠️")
        return

    if response.status_code != 200:
        body = response.json()
        st.toast(body.get("error", "Failed to load chat history"), icon="☠️")
        return

    body = response.json()
    chat = body.get("chat_history", {})
    messages = chat.get("messages", [])

    loaded_messages = []
    for msg in messages:
        role = "user" if msg.get("role") == "human" else "assistant"
        loaded_messages.append(
            {
                "role": role,
                "content": msg.get("content", ""),
            }
        )

    st.session_state.messages = loaded_messages
    st.session_state.current_chat_id = chat_id
    st.rerun()

if not st.session_state.chat_histories:
    refresh_chat_histories()

with st.sidebar:
    user = st.session_state.user

    if st.button(f"👤 {user.get('name', 'User')}", key="profile_toggle", use_container_width=True):
        st.session_state.show_user_panel = not st.session_state.show_user_panel

    if st.session_state.show_user_panel:
        with st.container(border=True):
            st.markdown(f"**Name:** {user.get('name', '')}")
            st.markdown(f"**Username:** {user.get('username', '')}")
            st.markdown(f"**Email:** {user.get('email', '')}")

            if st.button("Logout", key="logout_btn", use_container_width=True):
                response = logout_user()
                if response and response.status_code == 200:
                    st.session_state.clear()
                    st.rerun()
                else:
                    st.toast("Logout failed", icon="☠️")

    st.markdown("---")
    st.title("🛡️ Auditor Settings")
    st.info("System: Gemini 2.0 + Groq Llama 3.3")

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()

    st.markdown("---")
    st.subheader("Chat Histories")

    if st.session_state.chat_histories:
        for chat in st.session_state.chat_histories:
            chat_id = str(chat.get("chat_id", ""))
            title = chat.get("title", "Untitled Chat")

            with st.container(border=True):
                st.markdown(f"**{title[:32].strip()}**")
                st.caption(chat_id)

                if st.button(
                    "Open",
                    key=f"open_{chat_id}",
                    use_container_width=True,
                ):
                    load_chat(chat_id)
    else:
        st.caption("No chat histories found.")

st.title("Vantaguard - Architectural Intelligence. Autonomous Assurance.")

st.markdown(f"<h3 style='font-weight:500'> {greeting} , {st.session_state.user['name'].split(' ')[0]} 🙂‍↕️",unsafe_allow_html=True)

st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter GitHub URL or security query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents are auditing the codebase...", show_time=True):
            response = fetch_ai_response(prompt, st.session_state.current_chat_id)

            if not response:
                st.error("Connection failed")
            else:
                body = response.json()

                if response.status_code == 200:
                    result = body.get("message", "No response received")
                    returned_chat_id = body.get("conversational_id")

                    if not st.session_state.current_chat_id and returned_chat_id:
                        st.session_state.current_chat_id = returned_chat_id

                    st.balloons()

                    if result:
                        st.markdown(result)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": result}
                        )

                    if not st.session_state.chat_histories:
                        refresh_chat_histories()

                    if returned_chat_id and returned_chat_id not in [
                        str(chat.get("chat_id", "")) for chat in st.session_state.chat_histories
                    ]:
                        refresh_chat_histories()

                else:
                    st.error("Error while generating client response")
                    st.toast(body.get("error", "Unknown error"), icon="☠️")