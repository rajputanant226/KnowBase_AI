# import os
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS


# def ask(question):
#     embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small",
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

#     db = FAISS.load_local(
#         "data/vector_store",
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     retriever = db.as_retriever(search_kwargs={"k": 3})

#     # ✅ FIXED LINE
#     docs = retriever.invoke(question)

#     context = "\n\n".join(doc.page_content for doc in docs)

#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0,
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

#     prompt = f"""
# Answer the question using ONLY the context below.

# Context:
# {context}

# Question:
# {question}
# """

#     response = llm.invoke(prompt)

#     return {
#         "answer": response.content,
#         "sources": [doc.metadata for doc in docs]
#     }







from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

COLLECTION_NAME = "knowbase_docs"
QDRANT_URL = "http://localhost:6333"

def ask(question):
    embeddings = OpenAIEmbeddings()
    client = QdrantClient(url=QDRANT_URL)

    db = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )

    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )

    return qa.invoke({"query": question})

