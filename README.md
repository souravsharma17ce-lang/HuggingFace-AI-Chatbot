# 🤖 AI Chatbot using Hugging Face, LangGraph & SQLite

An AI-powered conversational chatbot built using **Python, Hugging Face, LangGraph, Streamlit, and SQLite**.

The chatbot supports **conversation memory and persistent chat history** using LangGraph's checkpointing system with SQLite. Users can create multiple conversations and switch between previous chat threads from the Streamlit sidebar.

## 🚀 Features

* 🤖 AI-powered conversational chatbot
* 🤗 Uses a Hugging Face Transformer model
* 🧠 Natural Language Processing (NLP)
* 🔄 LangGraph-based chatbot workflow
* 💾 Persistent conversation history using SQLite
* 🧵 Multiple conversation threads using `thread_id`
* 🔁 Resume previous conversations
* 🖥️ Interactive Streamlit interface
* ⚡ Streaming AI responses
* 🔌 Easy to integrate with APIs and web applications

## 🛠️ Technologies Used

* Python
* Hugging Face Transformers
* LangChain
* LangGraph
* PyTorch
* Streamlit
* SQLite
* NLP
* Hugging Face Model Hub

## 📂 Project Structure

```text
Chatbot/
│
├── langgraph_database.py
├── streaming_frontend_resume.py
├── streamlit_frontend_database.py
├── requirements.txt
├── README.md
└── .gitignore
```

> SQLite database and checkpoint files are generated locally and are excluded from Git using `.gitignore`.

## ⚙️ How It Works

The chatbot uses **LangGraph** to manage the conversation workflow and **SQLite** to persist conversation checkpoints.

### 1. User sends a message

The user enters a message through the Streamlit chat interface.

### 2. Thread ID identifies the conversation

Each conversation is assigned a unique `thread_id`.

```python
CONFIG = {
    "configurable": {
        "thread_id": thread_id
    }
}
```

The `thread_id` allows the chatbot to identify and continue a specific conversation.

### 3. LangGraph processes the message

The message is passed to the LangGraph chatbot along with the conversation configuration.

```python
chatbot.stream(
    {"messages": [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode="messages"
)
```

### 4. Conversation state is saved

LangGraph uses a **checkpointer** to save the chatbot state.

SQLite is used as the persistent storage for these checkpoints.

### 5. Previous conversations can be restored

Saved `thread_id`s are retrieved from the checkpoint database and displayed in the Streamlit sidebar.

Users can select an old conversation and continue chatting from where they left off.

## 💾 SQLite & Checkpointing

SQLite is a lightweight, file-based relational database.

In this project, SQLite is used to persist **LangGraph checkpoints and conversation state**.

The database allows the chatbot to maintain conversation history even after restarting the Streamlit application.

Example:

```python
sqlite3.connect(
    database="chatbot.db",
    check_same_thread=False
)
```

The database file is generated locally and should not be committed to GitHub.

## 🧵 Conversation Threads

Each conversation has a unique `thread_id`.

For example:

```text
Thread 1 → User's first conversation

Thread 2 → User's second conversation

Thread 3 → User's third conversation
```

The application stores these thread IDs and allows the user to switch between conversations.

This makes it possible to maintain **multiple independent chat sessions**.

## 🔄 Loading Previous Conversations

Previous conversations are retrieved from the LangGraph checkpointer.

```python
def retrieve_all_threads():
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(
            checkpoint.config["configurable"]["thread_id"]
        )

    return list(all_threads)
```

The retrieved thread IDs are displayed in the Streamlit sidebar.

When a user selects a thread, its saved messages are loaded using the corresponding `thread_id`.

## 🖥️ Streamlit Interface

The chatbot provides an interactive Streamlit interface with:

* New Chat button
* Conversation sidebar
* Chat history
* User messages
* Assistant responses
* Streaming responses
* Conversation switching

Example workflow:

```text
User
 ↓
Streamlit
 ↓
LangGraph
 ↓
Hugging Face Model
 ↓
AI Response
 ↓
SQLite Checkpointer
 ↓
Persistent Chat History
```

## 📦 Installation

Clone the repository:

```bash
git clone <your-github-repository-url>

cd Chatbot
```

Create and activate your virtual environment:

```bash
python -m venv chat
```

Windows PowerShell:

```powershell
.\chat\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

If your Hugging Face model requires an API token, create a `.env` file:

```text
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Make sure `.env` is included in `.gitignore` so that your API key is never pushed to GitHub.

## ▶️ Run the Application

Run the Streamlit application:

```bash
streamlit run streaming_frontend_resume.py
```

The application will open in your browser.

## 🤗 Hugging Face Model

The chatbot uses a **Hugging Face Transformer model** for generating responses.

The model can be loaded using the Hugging Face `transformers` library.

Example:

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained(
    "<your-model-name>"
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "<your-model-name>"
)
```

## 📌 Example

**User:**

```text
Hello, how are you?
```

**Chatbot:**

```text
Hello! I'm doing well. How can I help you?
```

The conversation can then be continued while maintaining the selected conversation thread.

## 🔮 Future Improvements

* 🔐 User authentication
* 🗄️ PostgreSQL database support
* 🧠 Advanced long-term memory
* 📄 RAG-based document question answering
* 🎙️ Voice input/output
* 🌐 Online deployment
* 🌍 Multi-language support
* 🤖 Agentic AI capabilities
* 🛠️ Tool calling
* 📊 Conversation analytics

## 👨‍💻 Author

**Sourav Sharma**

AI/ML Engineer | Python Developer

---

⭐ If you found this project useful, consider giving it a star!
