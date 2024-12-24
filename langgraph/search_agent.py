from langchain_community.tools import tavily_search

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


result = tool.invoke({"query": "What happened at the last wimbledon"})
answer = ''
for i in result:
    answer += i['url'] + '\n'
    answer += i['content'] + '\n'
    answer += '-'*50 + '\n\n\n'

return answer