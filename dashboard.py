import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from style import STYLE

if "page" not in st.session_state:
    st.session_state.page = "chatbot"  
    
if "show_analysis_table" not in st.session_state:
    st.session_state.show_analysis_table = False


from chatbot import render_chatbot_page

st.markdown(STYLE, unsafe_allow_html=True)

ST_LOGIN_USER = os.getenv("ST_USERNAME")
ST_LOGIN_PASS = os.getenv("ST_PASSWORD")


def login():
    with st.form("login_form"):
        st.markdown("### Login to MeinHaus AI Services Dashboard")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)

        if submit:
            if username == ST_LOGIN_USER and password == ST_LOGIN_PASS:
                st.session_state.authenticated = True
                st.success("Login successful! Reloading...")
                st.rerun()
            else:
                st.error("Invalid username or password")

# if "authenticated" not in st.session_state or not st.session_state.authenticated:
#     login()
#     st.stop()


with st.sidebar:
    st.subheader("MeinHaus AI Dashboard")
    if st.button("Chatbot Integration", type="primary", use_container_width=True):
        st.session_state.page = "chatbot"
    # if st.button("Autofill Feature", type="primary", use_container_width=True):
    #     st.session_state.page = "autofill"
    # if st.button("RingCentral Integration", type="primary", use_container_width=True):
    #     st.session_state.page = "ringcentral"

if st.session_state.page == "chatbot":
    render_chatbot_page()
