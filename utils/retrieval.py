from models.embeddings import load_embeddings

def retrieve_relevant_docs(query, top_k=3):
    vector_store = load_embeddings()
    results = vector_store.similarity_search(query, k=top_k)
    return [doc.page_content for doc in results]
