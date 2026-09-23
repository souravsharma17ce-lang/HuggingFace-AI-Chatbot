# 🤖 AI Chatbot using Hugging Face, LangGraph, Tools & SQLite

An AI-powered conversational chatbot built using **Python, Hugging Face, LangGraph, LangChain, Streamlit, and SQLite**.

The chatbot supports **conversation memory, persistent chat history, multiple conversation threads, tool calling, and streaming AI responses**.

It can use external tools such as **web search, calculator, and stock price lookup** based on the user's query.

## 🚀 Features

* 🤖 AI-powered conversational chatbot
* 🤗 Hugging Face Transformer model
* 🔄 LangGraph-based chatbot workflow
* 🧠 Conversation memory
* 💾 Persistent chat history using SQLite
* 🧵 Multiple conversation threads using `thread_id`
* 🔁 Resume previous conversations
* 🖥️ Interactive Streamlit interface
* ⚡ Streaming AI responses
* 🔧 Tool calling using LangGraph
* 🔍 Web search using DuckDuckGo
* 🧮 Calculator tool for arithmetic operations
* 📈 Stock price lookup using Alpha Vantage API
* 🔌 Easy integration with APIs and external tools

## 🛠️ Technologies Used

* Python
* Hugging Face
* LangChain
* LangGraph
* Streamlit
* SQLite
* PyTorch
* DuckDuckGo Search
* Alpha Vantage API
* NLP
* Hugging Face Model Hub

## 📂 Project Structure

```text
Chatbot/
│
├── langgraph_tools.py
├── frontend_tools.py
├── requirements.txt
├── README.md
└── .gitignore
```

> SQLite database files and environment files are generated locally and should not be committed to GitHub.

## ⚙️ How It Works

The application uses **LangGraph** to manage the chatbot workflow and **SQLite** to persist conversation checkpoints.

### 1. User sends a message

The user enters a message through the Streamlit interface.

```text
User
 ↓
Streamlit Frontend
 ↓
LangGraph
```

### 2. LangGraph processes the message

The user message is passed to the LangGraph chatbot.

```python
chatbot.stream(
    {"messages": [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode="messages"
)
```

### 3. LLM decides whether a tool is required

The Hugging Face model is connected with multiple tools.

```python
tools = [
    get_stock_price,
    search_tools,
    calculator
]

llm_with_tools = model.bind_tools(tools)
```

Depending on the user's question, the model can either:

* Answer directly
* Call the calculator
* Search the web
* Fetch stock information

### 4. Tool execution

LangGraph's `ToolNode` executes the requested tool.

```python
tool_node = ToolNode(tools)
```

The workflow is:

```text
START
  ↓
chat_node
  ↓
Tool required?
  ├── No → END
  │
  └── Yes
       ↓
     tools
       ↓
   chat_node
       ↓
      END
```

## 🔧 Available Tools

### 🧮 Calculator

The calculator performs basic arithmetic operations:

* Addition
* Subtraction
* Multiplication
* Division

Example:

```text
User:
What is 25 multiplied by 10?

Chatbot:
250
```

The tool accepts:

```python
calculator(
    first_num,
    second_num,
    operation
)
```

Supported operations:

```text
add
sub
mul
div
```

### 🔍 DuckDuckGo Web Search

The chatbot can search the web when the user asks for current or external information.

Example:

```text
User:
Search for the latest AI news.

Chatbot:
[AI-generated response based on search results]
```

The search tool is integrated using:

```python
DuckDuckGoSearchRun()
```

### 📈 Stock Price Tool

The chatbot can fetch stock market information using the **Alpha Vantage API**.

Example:

```text
User:
What is the stock price of Microsoft?

Chatbot:
[Latest available stock information]
```

The tool accepts a stock symbol:

```python
get_stock_price("MSFT")
```

## 🧠 LangGraph State

The chatbot maintains conversation messages using a typed state.

```python
class ChatState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]
```

The `add_messages` reducer allows new messages to be added to the existing conversation history.

## 💾 SQLite & Checkpointing

SQLite is used as a persistent storage layer for LangGraph checkpoints.

```python
conn = sqlite3.connect(
    database="chatbot.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn=conn)
```

The checkpointer stores conversation state so that previous conversations can be restored.

The database is created locally:

```text
chatbot.db
```

It should not be committed to GitHub.

## 🧵 Conversation Threads

Each conversation is identified using a unique `thread_id`.

Example:

```text
Thread 1 → First conversation
Thread 2 → Second conversation
Thread 3 → Third conversation
```

The configuration is passed to LangGraph:

```python
CONFIG = {
    "configurable": {
        "thread_id": thread_id
    }
}
```

This allows multiple independent conversations to be maintained.

## 🔄 Resume Previous Conversations

The application retrieves existing thread IDs from the SQLite checkpointer.

```python
def retrieve_all_threads():
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(
            checkpoint.config["configurable"]["thread_id"]
        )

    return list(all_threads)
```

Users can select an existing conversation from the Streamlit sidebar and continue chatting from the saved state.

## 🖥️ Streamlit Interface

The frontend provides:

* New Chat button
* Conversation sidebar
* Multiple chat threads
* Previous conversation loading
* Chat history
* User messages
* AI responses
* Streaming responses
* Thread switching

Example:

```text
┌──────────────────────────────┐
│        Streamlit UI          │
│                              │
│  Sidebar                     │
│  ├── New Chat                │
│  ├── Thread 1                │
│  ├── Thread 2                │
│  └── Thread 3                │
│                              │
│  Chat                         │
│  User: Hello                  │
│  AI: Hello! How can I help?  │
│                              │
└──────────────────────────────┘
```

## 🔄 Complete Workflow

```text
                    User
                     ↓
              Streamlit Frontend
                     ↓
                LangGraph
                     ↓
                Chat Node
                     ↓
             Hugging Face LLM
                     ↓
            ┌────────┴────────┐
            ↓                 ↓
       Direct
```
