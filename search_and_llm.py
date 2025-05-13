from langchain_community.embeddings import JinaEmbeddings
from langchain_chroma import Chroma
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
jina_api_key = os.getenv("JINA_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # google_api_key=google_api_key
    # other params...
)
# Initialize the Jina embeddings (same as in the first script)
text_embeddings = JinaEmbeddings(
    jina_api_key=jina_api_key, model_name="jina-embeddings-v2-base-en"
)
# Load the Chroma vector store from the persist directory
vector_store = Chroma(
    collection_name="example_collection",  # Use the same collection name
    embedding_function=text_embeddings,
    persist_directory="./chroma_langchain_db",  # Same path where embeddings are stored
)

def llmAnswer(query, k, answers):
    messages = [
        {
            "type": "system",
            "content": f"You are a helpful assistant which will summarize the top {k} similar answers for the query given. Just give me one relevant answer by summarising it. Strictly don't use any single or double quotes in the response"
        },
        {
            "type": "user",
            "content": f"Query: {query}\nAnswers: {answers}"
        }
    ]
    ai_msg = llm.invoke(messages)
    # print(ai_msg.content)
    return ai_msg.content

def searchQuery(query):
    # query_text = "who made this application"
    query_text = query

    # Embed the query text
    # query_result = text_embeddings.embed_query(query_text)
    top_k=3
    retrieved_docs = vector_store.similarity_search(query_text, k=top_k)

    # Print out the retrieved documents
    answers = """
    """
    for doc in retrieved_docs:
        # print(f"Document Content: {doc.page_content}")
        answers+=doc.page_content
    responseFromLLM = llmAnswer(query_text, top_k, answers)
    # print(responseFromLLM)
    return str(responseFromLLM)
    # return "hey"
# val = searchQuery("who made this application")
# print(val)