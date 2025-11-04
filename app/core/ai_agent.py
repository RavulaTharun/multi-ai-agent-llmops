# app/core/ai_agent.py
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

def make_tools(allow_search: bool):
    if not allow_search:
        return []
    try:
        return [TavilySearch(
            max_results=3,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False
        )]
    except Exception as e:
        logger.error("Failed to init Tavily tool: %s", e)
        return []

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    # llm = ChatOpenAI(model=llm_id)
    llm = ChatGroq(model=llm_id)
    tools = make_tools(allow_search)

    # Build a prompt that injects your system prompt, then hands control to the agent messages
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}")  # create_react_agent will fill this with the running chat state
    ])

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,   # <-- use prompt instead of state_modifier
    )

    # Ensure messages are LangChain messages, not plain strings
    if isinstance(query, str):
        msgs = [HumanMessage(content=query)]
    else:
        msgs = [HumanMessage(content=m) for m in query]

    state = {"messages": msgs}
    response = agent.invoke(state)
    messages = response.get("messages", [])

    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1] if ai_messages else (messages[-1].content if messages else "")