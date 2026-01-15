
# Create your views here.
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Document
from django.views.decorators.csrf import csrf_exempt
from .ai.document_loader import load_and_split
from .ai.embeddings import get_embeddings
from core.ai.vector_store import save_vectors
from .ai.rag_pipeline import ask
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
import tempfile

@csrf_exempt
def upload_document(request):
    if request.method == "POST":
        if "file" not in request.FILES:
            return HttpResponse("No file uploaded", status=400)

        file = request.FILES["file"]
        doc = Document.objects.create(file=file)

        file_path = doc.file.path

        docs = load_and_split(file_path)
        embeddings = get_embeddings()
        save_vectors(docs, embeddings)

        return render(request, "chat.html")

    return render(request, "upload.html")


def chat_page(request):
    return render(request, 'chat.html')

def ask_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = ask(data["question"])

        return JsonResponse({
            "answer": result["result"]
        })
