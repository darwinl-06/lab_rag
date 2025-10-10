# rag/ingest.py
import json
from pathlib import Path
from langchain_community.document_loaders import TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

PERSIST_DIR = Path("./chroma")

def load_documents():
    docs = []

    # returns_policy.md
    if Path("returns_policy.md").exists():
        md_loader = TextLoader("returns_policy.md", encoding="utf-8")
        docs += md_loader.load()

    # products.json -> a texto legible por chunk
    if Path("products.json").exists():
        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        for p in products:
            content = (
                f"SKU: {p.get('sku')}\n"
                f"Nombre: {p.get('name')}\n"
                f"Categoría: {p.get('category')}\n"
                f"Precio: {p.get('price')}\n"
                f"Descripción: {p.get('description')}\n"
            )
            docs.append(Document(page_content=content, metadata={"source": "products.json"}))

    return docs

def build_index():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR)
    )
    
    print(f"[OK] Index construido en {PERSIST_DIR.resolve()} con {len(chunks)} chunks.")

if __name__ == "__main__":
    build_index()
