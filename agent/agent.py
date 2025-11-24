import os
from tools.web_search_tool import web_search
from tools.llm_tool import llm_answer
from tools.database_tool import save_chat_tool

def agent(query: str) -> str:

    # Step 1: Web search
    web_output = web_search.invoke(query)

    # Step 2: LLM final answer
    final_answer = llm_answer.invoke({
    "query": query,
    "web_results": web_output
    })
    
    # 3. save chat using LangChain tool
    save_chat_tool.invoke({
        "user_query": query,
        "agent_answer": final_answer
    })

    return final_answer
