import requests
from langchain_community.embeddings import JinaEmbeddings
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
import json
from dotenv import load_dotenv
import os

load_dotenv()
jina_api_key = os.getenv("JINA_API_KEY")

text_embeddings = JinaEmbeddings(
    jina_api_key=jina_api_key, model_name="jina-embeddings-v2-base-en"
)

# Initialize Chroma for storing embeddings
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=text_embeddings,
    persist_directory="./chroma_langchain_db",  # Path where embeddings are saved
)

# Example documents to embed and store
# documents = [
#     "This is a test document.",
#     "LangChain is an amazing library for NLP tasks.",
#     "Embedding vectors and performing retrieval with Chroma is powerful."
# ]
def embedding_store():
    with open('fetched_articles.json', 'r') as file:
        fetched_data = json.load(file)
    
    # Step 2: Extract Title and Summary from each article
    documents = []
    for article in fetched_data:
        title = article.get('title', '')
        summary = article.get('summary', '')
        date = article.get('published', '')
        
        # Create a combined document from the title and summary
        combined_document = f"Title: {title}\nSummary: {summary}\nDate: {date}"
        documents.append(combined_document)
    
    # Embed documents and store them in the vector store
    doc_result = text_embeddings.embed_documents(documents)
    
    # Add embeddings to the Chroma vector store
    vector_store.add_texts(documents, embeddings=doc_result)
    print("Vector base updated")
# Query text
# query_text = "North of India plunged"

# # Embed query text
# query_result = text_embeddings.embed_query(query_text)

# # Retrieve the top-k similar documents
# top_k = 3  # Number of similar documents to retrieve
# retrieved_docs = vector_store.similarity_search(query_text, k=top_k)

# # Print out the retrieved documents
# for doc in retrieved_docs:
#     print(doc.page_content)
