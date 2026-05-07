import streamlit as st
from api_client import checkauth_user , fetch_ai_response
# 1. Page Configuration (Overrides/Adds to TOML)
st.set_page_config(
    page_title="Multi-Agent Security Auditor",
    page_icon="🛡️",
    layout="wide"
)
# Checking if user not logged in then swtich to login page
if "user" not in st.session_state:
    st.toast("Please Login before accessing Vantaguard",icon='☠️')
    st.switch_page('pages/login.py')

# 2. Sidebar - Status & Project Info
with st.sidebar:
    st.title("🛡️ Auditor Settings")
    st.info("System: Gemini 2.0 + Groq Llama 3.3")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. Main Header
st.title("Vantaguard - Architectural Intelligence. Autonomous Assurance.")
st.markdown("---")

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input Logic
if prompt := st.chat_input("Enter GitHub URL or security query..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message (Calling FastAPI)
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents are auditing the codebase...",show_time=True):
            response = fetch_ai_response(prompt)
            # Retrieving response
            body = response.json()
            # Getting client response
            if response.status_code==200:
                result = body.get('message','No response received')
                st.balloons()            
                if result:
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
            else:
                result = body.get('error')
                st.error('Error while generating client response')
                st.toast(body.get('error'),icon='☠️',duration='long')