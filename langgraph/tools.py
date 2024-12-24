from langchain_core.tools import tool
from codeace import CoreAgent, MappingAgent, LLMManager
from langchain_community.tools import tavily_search
from intel_wiki_lib.intel_wiki_api import IntelWikiAPI
@tool
def get_relevant_files(user_query: str, src_path: str) -> list:
    """
    Get the relevant files based on the user query to get more information and context about the query.

    Args:
        user_query (str): The user query keyword or phrase to use for searching the files.
        src_path (str): The source path where the files are located.
    """
    print(f"\n@call get_relevant_files({user_query}, {src_path}):\n\n")
    # Initialize the CoreAgent
    core_agent = CoreAgent(model_name="azure", src_path=src_path)

    # Get the relevant files
    relevant_files = core_agent.find_relevant_files(user_query)
    return relevant_files

@tool
def find_definitions(tags_to_find, tags_file_path):
    """
    Finds the files where the given tags are defined based on a ctags file.
    This version is adapted for the specific ctags format where the kind
    is indicated by a single letter at the end of the line.

    Args:
        tags_to_find (list): A list of tag names (strings) to search for.
        tags_file_path (str): The path to the ctags file.

    Returns:
        dict: A dictionary where keys are the tag names and values are the file paths
              where the tag is defined. If a tag is not found, it will not be
              present in the dictionary.
    """
    print(f"\n@call find_definitions({tags_to_find}, {tags_file_path}):\n\n")
    definitions = {}
    try:
        with open(tags_file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 4:  # Expecting at least 4 parts now
                    tag_name = parts[0]
                    file_path = parts[1]
                    kind = parts[3]  # The kind is the 4th part

                    # Define which kinds represent definitions
                    definition_kinds = ['c', 'f', 'v']  # Class, function, variable

                    if tag_name in tags_to_find and kind in definition_kinds:
                        definitions[tag_name] = file_path
    except FileNotFoundError:
        print(f"Error: ctags file not found at {tags_file_path}")
    return definitions

@tool
def find_implementations(tags_to_find, tags_file_path):
    """
    Finds the files where the given tags are likely implemented based on a ctags file.
    Note: ctags doesn't explicitly mark "implementation". This function identifies
    references to the tag which could indicate implementation.

    Args:
        tags_to_find (list): A list of tag names (strings) to search for.
        tags_file_path (str): The path to the ctags file.

    Returns:
        dict: A dictionary where keys are the tag names and values are the file paths
              where the tag is likely implemented (referenced). If a tag is not found,
              it will not be present in the dictionary.
    """
    implementations = {}
    try:
        with open(tags_file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    tag_name = parts[0]
                    file_path = parts[1]
                    if tag_name in tags_to_find:
                        implementations[tag_name] = file_path
    except FileNotFoundError:
        print(f"Error: ctags file not found at {tags_file_path}")
    return implementations

@tool
def web_search(query: str) -> str:
    """
    Perform a web search using the given query.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    tool = tavily_search.TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)


    result = tool.invoke({"query": query})
    answer = ''
    for i in result:
        answer += i['url'] + '\n'
        answer += i['content'] + '\n'
        answer += '-'*50 + '\n\n\n'
    print(f'@call web_search({query}):\n\n{answer}')
    return answer

@tool
def intel_wiki_search(key_word: str) -> str:
    """
    Perform a search on IntelWiki using the given keyword.
    
    Args:
        key_word (str): The keyword to search for.
    
    Returns:
        str: The search results.
    """
    wiki_app = IntelWikiAPI()
    results = wiki_app.search_by_keyword(key_word, result_limit=5)
    answer = ''
     
    for idx, result in enumerate(results):
        answer += f"Result:\n {idx + 1}\n"
        answer += f"Title:\n {result.title}\n"
        answer += f"URL:\n {result.url_link}\n\n"
        answer += '-'*50 + '\n\n\n'

    print(f'@call intel_wiki_search({key_word}):\n\n{answer}')
    return answer  
    
available_functions = {
   "web_search": web_search,
    "intel_wiki_search": intel_wiki_search,
}

if __name__ == "__main__":
    # Initialize the LLMManager
    print(intel_wiki_search("tsn"))