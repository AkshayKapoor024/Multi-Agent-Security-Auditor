import streamlit as st
from api_client import fetch_audit_response

# 1. Page Configuration (Overrides/Adds to TOML)
st.set_page_config(
    page_title="Multi-Agent Security Auditor",
    page_icon="🛡️",
    layout="wide"
)

bt = st.button('Click to navigate to login-page')
if bt:
    st.switch_page('pages/login.py')

# 2. Sidebar - Status & Project Info
with st.sidebar:
    st.title("🛡️ Auditor Settings")
    st.info("System: Gemini 2.0 + Groq Llama 3.3")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. Main Header
st.title("Automated Security Auditor")
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
        with st.spinner("🤖 Agents are auditing the codebase..."):
            result = fetch_audit_response(prompt)
            st.balloons('Success')
            if result:
                response_text = result.get("app_response", "No response received.")
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})