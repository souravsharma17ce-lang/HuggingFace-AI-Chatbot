from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


from langchain_core.tools import tool

import requests
import random


llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
   
)

model = ChatHuggingFace(llm=llm)


#tools
search_tools =DuckDuckGoSearchRun(region="us-en")


@tool
def  calculator(first_num:float,second_num:float,operation:str)->dict:
    """ Perform basic arithmetic operations.

    Args:
        first_num: First number.
        second_num: Second number.
        operation: Operation to perform. Must be add, sub, mul, or div.
    """

    try:
        if operation=="add":
            result = first_num+second_num
        elif operation=="sub":
            result = first_num-second_num
        elif operation =="mul":
            result =first_num*second_num
        elif operation=="div":
            if second_num==0:
                return{"eroor":"division by zero is not allowd"}
            result =first_num/second_num
        else:
            return{"error":f"unsupported opeation{operation}"}

        return{"first_num":first_num,"second_num":second_num,"operation":operation,"result":result}

    except Exception as e:
        return{"error":str(e)}


@tool
def get_stock_price(symbol:str)->dict:
    """
    fetch latest stock price for a given symbolusing alpha vantage with api key in 
    the url."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=2JX2O9O0VLXDDSCX"

    r = requests.get(url)
    return r.json()


#make tool list
tools = [get_stock_price,search_tools,calculator]

llm_with_tools = model.bind_tools(tools)


#state
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


#graph nodes
def chat_node(state:ChatState):
    """LLM NODE THAT MAY ANSEWER or request a tool call"""
    messages =state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages":[response]}

tool_node = ToolNode(tools) #executes tools calls



#checkpointer
conn =sqlite3.connect(database = "chatbot.db",check_same_thread =False)
checkpointer =SqliteSaver(conn =conn)
#graph structure
graph = StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node)


graph.add_edge(START,"chat_node")

graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")

chatbot = graph.compile(checkpointer =checkpointer)
print(chatbot)


# # #regular chat  
# config = {"configurable":{"thread_id":"1"}}
# out =chatbot.invoke({"messages":[HumanMessage(content="what is stock price of apple")]},config=config)
# print(out["messages"][-1].content)
# from IPython.display import Image, display

# display(Image(chatbot.get_graph().draw_mermaid_png()))


#helper function 
def retrieve_all_threads():
    all_threads =set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)