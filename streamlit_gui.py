import streamlit as st
import os
import json
from datetime import datetime
from codeace import MappingAgent, CoreAgent

# Constants
ASSISTANT_AVATAR_PATH = 'https://imgur.com/FgmmmH7.png'
USER_AVATAR_PATH = 'https://ps.w.org/user-avatar-reloaded/assets/icon-128x128.png'

# Page config
st.set_page_config(layout="wide", page_title="Code Ace™", page_icon="🤖")

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        max-width: 80%;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_source' not in st.session_state:
    st.session_state.current_source = None
if 'mapping_done' not in st.session_state:
    st.session_state.mapping_done = False
if 'core_agent' not in st.session_state:
    st.session_state.core_agent = None
if 'use_extra_source' not in st.session_state:
    st.session_state.use_extra_source = False
if 'extra_src_path' not in st.session_state:
    st.session_state.extra_src_path = None
if 'use_summery_contaxt' not in st.session_state:
    st.session_state.use_summery_contaxt = True
def load_paths():
    """Load saved paths from JSON file"""
    try:
        with open("saved_paths.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_paths(paths):
    """Save paths to JSON file"""
    with open("saved_paths.json", "w") as f:
        json.dump(paths, f)

def load_last_source():
    """Load the last used source path"""
    try:
        with open("last_source.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_last_source(source):
    """Save the last used source path"""
    with open("last_source.json", "w") as f:
        json.dump(source, f)

# Initialize session state for paths
if 'saved_paths' not in st.session_state:
    st.session_state.saved_paths = load_paths()
    last_source = load_last_source()
    if last_source:
        st.session_state.current_source = last_source

def save_conversation(messages, filename):
    """Save conversation history to a file"""
    history_folder = os.path.join(os.path.dirname(__file__), "history")
    os.makedirs(history_folder, exist_ok=True)
    file_path = os.path.join(history_folder, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)
    return file_path

def load_conversation(file_path):
    """Load conversation history from a file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def process_user_query(messages):
    """Process the latest user query"""
    if not st.session_state.core_agent:
        return "Please select a source directory and run the mapping process first."
    
    user_input = messages[-1]["content"]
    
    with st.spinner('Finding relevant files...'):
        relevant_files = st.session_state.core_agent.find_relevant_files(user_input)
        st.write(f"📁 Found relevant files:\n\n {'\n'.join(relevant_files)}\n\n")
    
    if st.session_state.use_extra_source and st.session_state.extra_src_path:
        with st.spinner('Generating predictions from additional source...'):
            pre_agent = CoreAgent(model_name="azure", src_path=st.session_state.extra_src_path)
            pre_response = extra_agent.process_code_query(user_input, relevant_files)
        
    with st.spinner('Generating response...'):
        if st.session_state.use_summery_contaxt:
            st.session_state.core_agent.add_extra_context_by_path()
        response = st.session_state.core_agent.process_code_query(user_input, relevant_files)
        return response

def run_mapping_process(src_path):
    """Run the mapping process for the selected source"""
    with st.spinner('Running mapping process...'):
        mapping_agent = MappingAgent(model_name="azure", src_path=src_path)
        mapping_agent.run_mapping_process(generate_summery = False)
        st.session_state.core_agent = CoreAgent(model_name="azure", src_path=src_path)
        st.session_state.mapping_done = True
        return True

st.title("Code Ace™")

# Sidebar
with st.sidebar:
    st.image('https://imgur.com/EQE1jjg.png', width=100)
    
    st.session_state.use_summery_contaxt = st.checkbox("Add Summery to contaxt", value=st.session_state.use_summery_contaxt)
    # Add new path input
    new_path = st.text_input("Add New Source Directory Path")
    
    # Source selection dropdown
    if st.session_state.saved_paths:
        src_path = st.selectbox(
            "Select Source Directory",
            st.session_state.saved_paths,
            index=None,
            placeholder="Choose a source directory..."
        )
        
        # Remove path button
        if src_path and st.button("Remove Selected Path"):
            st.session_state.saved_paths.remove(src_path)
            save_paths(st.session_state.saved_paths)
            st.session_state.current_source = None
            st.session_state.core_agent = None
            st.session_state.mapping_done = False
            st.rerun()
        
        if src_path:
            if src_path != st.session_state.current_source:
                st.session_state.current_source = src_path
                try:
                    st.session_state.core_agent = CoreAgent(model_name="azure", src_path=src_path)
                    st.info("CoreAgent initialized with new source path")
                    st.session_state.mapping_done = False
                except Exception as e:
                    st.error(f"Error initializing CoreAgent: {str(e)}")
            
            if st.button("Run Mapping Process"):
                if run_mapping_process(src_path):
                    st.success("Mapping completed!")
    else:
        st.info("No saved paths. Please add a source directory path.")
    
    # Add checkbox and extra source selection after the main source selection
    st.session_state.use_extra_source = st.checkbox("Use Additional Source", value=st.session_state.use_extra_source)
    
    if st.session_state.use_extra_source:
        if st.session_state.saved_paths:
            extra_src_path = st.selectbox(
                "Select Additional Source Directory",
                [path for path in st.session_state.saved_paths if path != src_path],
                index=None,
                placeholder="Choose additional source directory...",
                key="extra_source_select"
            )
            
            if extra_src_path:
                st.session_state.extra_src_path = extra_src_path
                st.info(f"Additional source selected: {extra_src_path}")
        else:
            st.info("No saved paths available for additional source.")
    else:
        st.session_state.extra_src_path = None
    
    # New chat button
    if st.button("New Chat"):
        st.session_state.messages = []
    
    # Save conversation
    if st.button("Save Conversation"):
        if st.session_state.messages:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_history_{timestamp}.json"
            saved_path = save_conversation(st.session_state.messages, filename)
            st.success(f"Conversation saved to {saved_path}")
        else:
            st.warning("No conversation to save.")
    
    # Load conversation
    uploaded_file = st.file_uploader("Load Conversation", type="json")
    if uploaded_file is not None:
        loaded_messages = json.loads(uploaded_file.getvalue())
        st.session_state.messages = loaded_messages
        st.success("Conversation loaded successfully!")
    
 

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=ASSISTANT_AVATAR_PATH if message["role"] == "assistant" else USER_AVATAR_PATH):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know about the code?"):
    # Display user message
    st.chat_message("user", avatar=USER_AVATAR_PATH).markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get and display assistant response
    response = process_user_query(st.session_state.messages)
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR_PATH):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})