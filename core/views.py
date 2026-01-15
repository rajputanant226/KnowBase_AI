
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
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return render(request, "upload.html", {"error": "No file uploaded"})

        if not uploaded_file.name.endswith(".pdf"):
            return render(request, "upload.html", {"error": "Only PDF allowed"})

        # ✅ save to /tmp (Render-safe)
        temp_path = f"/tmp/{uuid.uuid4()}.pdf"
        with open(temp_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # ✅ load + split
        docs = load_and_split(temp_path)

        embeddings = get_embeddings()
        save_vectors(docs, embeddings)

        # optional cleanup
        os.remove(temp_path)

        return render(request, "chat.html", {
            "message": "Document indexed successfully"
        })

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
