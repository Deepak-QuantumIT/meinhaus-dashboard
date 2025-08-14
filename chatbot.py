import os
import requests
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Load envs
ST_LOGIN_USER = os.getenv("ST_USERNAME")
ST_LOGIN_PASS = os.getenv("ST_PASSWORD")

def ask_to_assistant(query: str | None, files: list | None):
    with st.chat_message("assistant"):
        with st.spinner("wait..."):
            user_id = None
            thread_id = st.session_state.thread_id or None

            if st.session_state.user_state == "Logged In":
                user_id = str(st.session_state.user_id)

            form_data = {
                "user_id": user_id,
                "chat_id": thread_id,
                "query": query
            }

            files_data = []
            if files:
                for i, file in enumerate(files[:2]):
                    files_data.append(("imgs", (file.name, file, file.type or "image/jpeg")))

            response = requests.post(
                url=f"{os.getenv('MEINHAUS_AI_BACKEND_HOST')}/api/chat-with-assistant",
                data=form_data,
                files=files_data if files_data else None,
                headers={"X-API-Key": os.getenv("APP_API_KEY")},
                timeout=120
            )

            status_code = response.status_code
            try:
                response = response.json()
                if status_code == 200:
                    agent = response["details"]["agent"]
                    content = response["details"]["response"]
                    assistant_reply = f"{content}\n\n**Replyed by:** `{agent}`"
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    st.markdown(assistant_reply)
                    return response["details"].get("event")
                else:
                    st.markdown(f"**Error**: `{status_code}` | {response['msg']}")
            except Exception:
                st.markdown(f"**Error**: `{status_code}` | {response.text}", unsafe_allow_html=True)

def render_chatbot_page():
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = uuid4().hex
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 3
        
    st.subheader("Meinhaus Chatbot")

    with st.sidebar:
        st.markdown("### ⚙️ Chatbot Settings")
        
        st.session_state.user_state = st.radio(
            "Change Chatbot Behaviour",
            ("Logged Out", "Logged In"),
            help="Switch between chatbot states for testing."
        )
        
        st.info(
            "💡 This is a dummy UI for testing purposes only. "
            "It will not work for other preregistered users."
            "It will work for new users also.",
            icon="ℹ️"
        )
        
        if st.session_state.user_state == "Logged In":
            st.markdown(f"**🧑 Test User ID:** `{st.session_state.user_id}`")

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 **Welcome to MeinHaus!** How can I assist you today?"
        }]
        st.session_state.show_initial_options = True

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            for img in msg.get("imgs", []):
                st.image(img)
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your question...", file_type=["jpg", "jpeg", "png"], accept_file=True):
        query = prompt.text
        files = prompt.files
        st.session_state.messages.append({"role": "user", "content": query, "imgs": files})

        with st.chat_message("user"):
            for file in files:
                st.image(file)
            st.markdown(query)

        ask_to_assistant(query, files)
