# import os
# from langchain_community.vectorstores import FAISS

# def save_vectors(docs, embeddings):
#     os.makedirs("data/vector_store", exist_ok=True)
#     db = FAISS.from_documents(docs, embeddings)
#     db.save_local("data/vector_store")
#     return db





# from qdrant_client import QdrantClient
# from qdrant_client.models import VectorParams, Distance
# from langchain_community.vectorstores import Qdrant

# COLLECTION_NAME = "knowbase_docs"
# QDRANT_URL = "http://localhost:6333"
# VECTOR_SIZE = 1536  # OpenAI embeddings size

# def save_vectors(docs, embeddings):
#     client = QdrantClient(url=QDRANT_URL)

#     # 1️⃣ Create collection ONLY if it does not exist
#     collections = [c.name for c in client.get_collections().collections]

#     if COLLECTION_NAME not in collections:
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=VECTOR_SIZE,
#                 distance=Distance.COSINE,
#             ),
#         )

#     # 2️⃣ Add documents (NO recreate, NO init_from)
#     qdrant = Qdrant(
#         client=client,
#         collection_name=COLLECTION_NAME,
#         embeddings=embeddings,
#     )

#     qdrant.add_documents(docs)

import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_community.vectorstores import Qdrant

COLLECTION_NAME = "knowbase_docs"
VECTOR_SIZE = 1536  # OpenAI embeddings

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

def save_vectors(docs, embeddings):
    client = get_qdrant_client()

    # ✅ safe create (idempotent)
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
    except Exception:
        # collection already exists → ignore
        pass

    # ✅ recommended LangChain method
    Qdrant.from_documents(
        docs,
        embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION_NAME,
    )

# COLLECTION_NAME = "knowbase_docs"
# VECTOR_SIZE = 1536  # OpenAI embedding size

# def get_qdrant_client():
#     return QdrantClient(
#         url=os.getenv("QDRANT_URL"),
#         api_key=os.getenv("QDRANT_API_KEY"),  # None for local
#     )

# def save_vectors(docs, embeddings):
#     client = get_qdrant_client()

#     # 1️⃣ Create collection if not exists
#     collections = [c.name for c in client.get_collections().collections]

#     if COLLECTION_NAME not in collections:
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(
#                 size=VECTOR_SIZE,
#                 distance=Distance.COSINE,
#             ),
#         )

#     # 2️⃣ Add documents safely
#     qdrant = Qdrant(
#         client=client,
#         collection_name=COLLECTION_NAME,
#         embeddings=embeddings,
#     )

#     qdrant.add_documents(docs)



