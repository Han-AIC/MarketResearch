import streamlit as st
import json
from datetime import datetime

# Function to display messages with custom styles
def display_messages(messages):
    for message in messages:
        if message['role'] == 'User':
            st.markdown(f"<div style='background-color: #d1e7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>{message['role']}:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #d4edda; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>{message['role']}:</strong> {message['content']}</div>", unsafe_allow_html=True)

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Filename to save the configuration
CONFIG_FILE = "config.json"

# Function to save configuration to a file
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Function to load configuration from a file
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to initialize Elasticsearch connection
def initialize_elasticsearch(endpoint, username):
    try:
        print(endpoint, username)
        st.sidebar.success("Elasticsearch initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing Elasticsearch: {e}")

def initialize_llm(endpoint, api_key):
    try:
        print(endpoint, api_key)
        st.sidebar.success("LLM initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing LLM: {e}")
# Load the saved configuration
saved_config = load_config()

# Elasticsearch parameters input
st.sidebar.header("Elasticsearch Configuration")
es_endpoint = st.sidebar.text_input("Endpoint", value=saved_config.get("es_endpoint", ""), key="es_endpoint")
es_username = st.sidebar.text_input("Username", value=saved_config.get("es_username", ""), key="es_username")
# Button to initialize Elasticsearch
if st.sidebar.button("Initialize Elastic"):
    initialize_elasticsearch(es_endpoint, es_username)

# Additional configuration sections
st.sidebar.header("LLM Configuration")
llm_endpoint = st.sidebar.text_input("Endpoint", value=saved_config.get("llm_endpoint", ""), key="llm_endpoint")
llm_username = st.sidebar.text_input("API Key", value=saved_config.get("llm_api_key", ""), key="llm_api_key")
# Button to initialize LLM
if st.sidebar.button("Initialize LLM"):
    initialize_llm(llm_endpoint, llm_username)

# Save configuration button
if st.sidebar.button("Save Configuration"):
    config = {
        "es_endpoint": st.session_state.es_endpoint,
        "es_username": st.session_state.es_username,
        "llm_endpoint": st.session_state.llm_endpoint,
        "llm_api_key": st.session_state.llm_api_key,
    }
    save_config(config)
    st.sidebar.success("Configuration saved!")


# Function to handle user input
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.messages.append({"role": "User", "content": user_input})
        st.session_state.messages.append({"role": "Bot", "content": f"Echo: {user_input}"})
        st.session_state.user_input = ""  # Clear the input field

# Chat input
st.text_input("You:", key="user_input", on_change=handle_input)

# Display chat messages
display_messages(st.session_state.messages)

# File upload
uploaded_file = st.file_uploader("Choose a file")

# Handle file upload
if uploaded_file:
    st.write(f"Uploaded file: {uploaded_file.name}")
    # You can process the file here