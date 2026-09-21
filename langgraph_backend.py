from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated

from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
import operator
from langgraph.checkpoint.memory import InMemorySaver



from langgraph.graph.message import add_messages
class ChatState(TypedDict):

    messages:Annotated[list[BaseMessage],add_messages]




from dotenv import load_dotenv

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



checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

#add nodes
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


chatbot= graph.compile(checkpointer =checkpointer)



