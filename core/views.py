
# Create your views here.
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Document
from .ai.document_loader import load_and_split
from .ai.embeddings import get_embeddings
from core.ai.vector_store import save_vectors
from .ai.rag_pipeline import ask

def upload_document(request):
    if request.method == 'POST':
        file = request.FILES['file']
        doc = Document.objects.create(file=file)

        docs = load_and_split(doc.file.path)
        embeddings = get_embeddings()
        save_vectors(docs, embeddings)

        return render(request, 'chat.html')

    return render(request, 'upload.html')

def chat_page(request):
    return render(request, 'chat.html')

def ask_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = ask(data["question"])

        return JsonResponse({
            "answer": result["result"]
        })
