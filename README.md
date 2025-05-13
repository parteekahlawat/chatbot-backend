# RAG Pipeline and Chat API

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline, a **Flask-based back-end API**, and integrates **Redis** for session management. The goal is to ingest news articles, process them with embeddings, store the embeddings in a vector database, and allow for interactive chat with history retrieval.

## Features

### 1. RAG Pipeline:
- **Ingest News Articles**: 
  - The pipeline ingests approximately **50 news articles** through an RSS feed.
  
- **Jina Embeddings**: 
  - The articles are embedded using **Jina Embeddings** to convert the text into numerical vectors.
  
- **Chroma Vector Store**: 
  - The embeddings are stored in **Chroma**, a vector database for fast retrieval of semantically similar documents.

- **Retrieve Top-K Passages**: 
  - For each query, the top-k most relevant passages are retrieved from the vector store.

- **Gemini API for Final Answer**: 
  - The top-k passages are sent to the **Gemini API** to generate the final response.

### 2. Back-End:
- **REST API**:
  - A **Flask**-based REST API is developed to handle communication with the front-end and provide endpoints for chat and data retrieval.

- **Socket-Based Chat**:
  - A **SocketIO** connection is established to enable real-time, two-way communication for interactive chat.

- **Session History**:
  - The API allows fetching a session's message history and clearing the session's data.

### 3. Storage:
- **Redis**:
  - **Redis** is used as an **in-memory data store** for chat history management.
  - Each session's chat history is stored as a list in Redis, which can be accessed, updated, or cleared dynamically.

## Technologies Used
- **Jina Embeddings**: Used for generating embeddings for text documents.
- **Chroma**: A vector database used to store and retrieve embedded documents.
- **Flask**: A lightweight Python web framework used to build the REST API.
- **SocketIO**: Used to enable real-time chat communication.
- **Redis**: An in-memory data store used to manage chat session history.
- **Gemini API**: Used to generate final answers based on the top-k retrieved passages.

## Setup

### Requirements
- Python 3.7+
- Installed docker for redis
- Install required Python libraries:
  ```bash
  git clone <repo-link>
  cd ./backend
  pip install -r requirements.txt

  Add .env file, details mentioned below
  ```

### Environment Variables
- Ensure the following environment variables are set up in a .env file:
```bash
JINA_API_KEY: Your API key for Jina embeddings.

REDIS_HOST: Host address for Redis (default localhost).

REDIS_PORT: Port for Redis (default 6379).

GOOGLE_API_KEY: API key for the Gemini API.
```

- Run redis on docker
  ```bash
  docker run --name redis -p 6379:6379 -d redis
  ```

- Run main file
```bash
python main.py
```
## Your Server is running now on port 5000
