from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated

from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
import operator
from langgraph.checkpoint.sqlite import SqliteSaver



from langgraph.graph.message import add_messages
class ChatState(TypedDict):

    messages:Annotated[list[BaseMessage],add_messages]




from dotenv import load_dotenv
import sqlite3

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
   
)

model = ChatHuggingFace(llm=llm)


def chat_node(state:ChatState):


    #take user query from state
    messages = state["messages"]


    #send to llm
    response = model.invoke(messages)

    #response store state
    return {"messages":[response]}


conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

#add nodes
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot= graph.compile(checkpointer =checkpointer)

#test
def retrieve_all_threads():
  all_threads=set()
  for checkpoint in checkpointer.list(None):
    all_threads.add(checkpoint.config["configurable"]["thread_id"])

  return(list(all_threads))
