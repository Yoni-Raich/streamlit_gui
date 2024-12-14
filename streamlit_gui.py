import streamlit as st
import os
import json
from datetime import datetime
from codeace import MappingAgent, CoreAgent, LLMManager
import git
from typing import Tuple

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
if 'extra_context' not in st.session_state:
    st.session_state.extra_context = None
if 'model_mode' not in st.session_state:
    st.session_state.model_mode = "agente"
if 'llm_model' not in st.session_state:
    st.session_state.llm_model = LLMManager().create_model_instance_by_name("azure")
if 'extra_context_select' not in st.session_state:
    st.session_state.extra_context_select = []
if 'improve_prompt' not in st.session_state:
    st.session_state.improve_prompt = False
def is_github_url(path: str) -> bool:
    """Check if the given path is a GitHub repository URL."""
    return path.startswith(("http://github.com/", "https://github.com/"))

def clone_github_repo(repo_url: str) -> Tuple[bool, str, str]:
    """
    Clone a GitHub repository to the repos directory.
    Returns: (success, message, repo_path)
    """
    try:
        repos_dir = os.path.join(os.path.dirname(__file__), "repos")
        os.makedirs(repos_dir, exist_ok=True)
        
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(repos_dir, repo_name)
        
        # Check if directory already exists and is not empty
        if os.path.exists(repo_path) and os.listdir(repo_path):
            # Directory exists and is not empty - return success since we already have it
            print(f"Repository already exists at {repo_path}")
            return True, f"Repository already exists at {repo_path}", repo_path
        
        git.Repo.clone_from(repo_url, repo_path)
        print(f"Repository cloned successfully to {repo_path}")
        return True, f"Repository cloned successfully to {repo_path}", repo_path
    except Exception as e:
        return False, f"Error cloning repository: {str(e)}", ""

def add_source_path(path: str) -> Tuple[bool, str]:
    """
    Add a new source path to saved paths.
    Returns: (success, message)
    """
    if path in st.session_state.saved_paths:
        return False, "Path already exists in saved sources"
    
    if is_github_url(path):
        with st.spinner('Cloning GitHub repository...'):
            success, message, repo_path = clone_github_repo(path)
            if success:
                st.session_state.saved_paths.append(repo_path)
                save_paths(st.session_state.saved_paths)
                return True, message
            return False, message
    
    if os.path.isdir(path):
        st.session_state.saved_paths.append(path)
        save_paths(st.session_state.saved_paths)
        return True, f"Added new source path: {path}"
    
    return False, "Invalid directory path"

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
    pre_response = ""
    with st.spinner('Finding relevant files...'):
        relevant_files = st.session_state.core_agent.find_relevant_files(user_input)
        st.markdown(f"📁 Found relevant files:\n\n{'\n'.join(relevant_files)}\n\n")

    if st.session_state.use_extra_source and st.session_state.extra_src_path:
        pre_agent = CoreAgent(model_name="azure", src_path=st.session_state.extra_src_path)
        with st.spinner('Finding relevant dependencies files...'):
            relevant_dependencies_files = pre_agent.find_relevant_files(user_input)
            st.markdown(f"📁 Found relevant dependencies files:\n\n {'\n'.join(relevant_dependencies_files)}\n\n")
        
        with st.spinner('Generating predictions from additional source...'):
            pre_response = pre_agent.process_dependencies_query(user_input, relevant_dependencies_files)
            st.write(f"🤖 Predictions from additional source:\n\n{pre_response}\n\n")
    
    with st.spinner('Generating response...'):
        if st.session_state.use_summery_contaxt:
            st.session_state.core_agent.add_extra_context_by_path(override=True)

        if st.session_state.use_extra_source and st.session_state.extra_src_path:
            st.session_state.core_agent.add_extra_context(pre_response)
            st.session_state.core_agent.add_extra_context(st.session_state.extra_context)
        
        if st.session_state.extra_context_select:
            for tag in st.session_state.extra_context_select:
                st.session_state.core_agent.add_extra_context_by_path(os.path.join("documentations", f"{tag}.md"))
                print(f"Added extra context from: {tag}")
        
        response = st.session_state.core_agent.process_code_query(user_input, relevant_files)
        return response

def run_mapping_process(src_path):
    """Run the mapping process for the selected source"""
    
    with st.spinner('Running mapping process...'):
        status_placeholder = st.empty()
        mapping_agent = MappingAgent(model_name="azure", src_path=src_path)
        for status in mapping_agent.run_mapping_process(generate_summery = False):
            print(status)
            status_placeholder.text(status)
        status_placeholder.text("All files processed!")
        st.session_state.core_agent = CoreAgent(model_name="azure", src_path=src_path)
        st.session_state.mapping_done = True
        return True

def get_tags_from_documetations_folde():
    """Get tags from the documentations folder"""
    tags = []
    for root, dirs, files in os.walk("documentations"):
        for file in files:
            tags.append(file.split(".")[0])
    return tags
    
st.title("Code Ace™")
import codeace
st.write(f"version: {codeace.__version__}")


# New chat button
if st.button("New Chat"):
    st.session_state.messages = []
# Sidebar
with st.sidebar:
    # Logo and Image
    st.image('https://imgur.com/EQE1jjg.png', width=100)

    # General Settings
    with st.expander("General Settings", expanded=True):
        st.session_state.model_mode = st.toggle("Agente mode", value=True)
        st.write("Model mode: ", "Agente" if st.session_state.model_mode else "GPT-4o")
        st.session_state.use_summery_contaxt = st.checkbox(
            "Add Summary to Context", value=st.session_state.use_summery_contaxt
        )
        st.session_state.improve_prompt = st.checkbox("Improve prompt", value=st.session_state.improve_prompt)
           

    # Source Management
    with st.expander("Source Management", expanded=True):
        # Add new source path
        new_path = st.text_input("Add New Source Directory or GitHub repo URL")
        if new_path:
            success, message = add_source_path(new_path)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        
        # Primary source selection
        if st.session_state.saved_paths:
            src_path = st.selectbox(
                "Select Source Directory",
                st.session_state.saved_paths,
                index=0,
                placeholder="Choose a source directory...",
            )
            
            # Remove source button
            if src_path and st.button("Remove Selected Path"):
                st.session_state.saved_paths.remove(src_path)
                save_paths(st.session_state.saved_paths)
                st.session_state.current_source = None
                st.session_state.core_agent = None
                st.session_state.mapping_done = False
                st.rerun()
            
            # Update primary source
            if src_path:
                if src_path != st.session_state.current_source:
                    st.session_state.current_source = src_path
                    try:
                        st.session_state.core_agent = CoreAgent(
                            model_name="azure", src_path=src_path
                        )
                        st.info("CoreAgent initialized with new source path")
                        st.session_state.mapping_done = False
                    except Exception as e:
                        st.error(f"Error initializing CoreAgent: {str(e)}")
                
                # Run mapping process button
                if st.button("Run Mapping Process"):
                    if run_mapping_process(src_path):
                        st.success("Mapping completed!")
        else:
            st.info("No saved paths. Please add a source directory path.")

        # Additional source selection
        st.session_state.use_extra_source = st.checkbox(
            "Use Additional Source", value=st.session_state.use_extra_source
        )
        
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

    # Add Extra Context
    with st.expander("Extra Context", expanded=False):
        tags_list = get_tags_from_documetations_folde()
        st.session_state.extra_context_select = st.multiselect("Select Extra Context",tags_list)
        
        st.text_area("Add extra context text", key="extra_context_input")
        if st.button("Apply"):
            st.session_state.extra_context = st.session_state.extra_context_input
            st.success("Extra context added successfully!")

    # Conversation Management
    with st.expander("Conversation Management", expanded=False):
    
        
        # Save conversation button
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
    if st.session_state.improve_prompt:
        with st.spinner('Improving prompt...'):
            st.session_state.core_agent.add_extra_context_by_path(r'C:\streamlit_gui\LineTools_documentation.md')
            prompt = st.session_state.core_agent.improve_user_prompt(prompt)
        
    # Display user message
    st.chat_message("user", avatar=USER_AVATAR_PATH).markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if st.session_state.model_mode:
        response = process_user_query(st.session_state.messages)
    else:
        response = st.session_state.llm_model.invoke(st.session_state.messages).content
    
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR_PATH):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    # = None

