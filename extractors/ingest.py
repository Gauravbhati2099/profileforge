import os

from extractors.loader import load_file
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


DOCUMENTS_DIR = "documents"

all_docs = []

for file in os.listdir(DOCUMENTS_DIR):

    path = os.path.join(DOCUMENTS_DIR, file)

    text = load_file(path)

    if not text or not text.strip():
        print(f"[EMPTY SKIP] {file}")
        continue

    all_docs.append(
        Document(
            page_content=text,
            metadata={
                "source_file": file,
                "file_path": path
            }
        )
    )

print("Loaded docs:", len(all_docs))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)

chunks = splitter.split_documents(all_docs)

for idx, chunk in enumerate(chunks, start=1):

    chunk.metadata["chunk_id"] = idx
    chunk.metadata["chunk_length"] = len(chunk.page_content)

print("Chunks:", len(chunks))


# Save readable chunks

with open(
    "chunks_debug.txt",
    "w",
    encoding="utf-8"
) as f:

    for chunk in chunks:

        f.write("=" * 100 + "\n")
        f.write(f"CHUNK ID     : {chunk.metadata['chunk_id']}\n")
        f.write(f"SOURCE FILE  : {chunk.metadata['source_file']}\n")
        f.write(f"FILE PATH    : {chunk.metadata['file_path']}\n")
        f.write(f"CHUNK LENGTH : {chunk.metadata['chunk_length']}\n")
        f.write("=" * 100 + "\n\n")

        f.write(chunk.page_content)
        f.write("\n\n\n")


# Save metadata CSV

with open(
    "chunk_metadata.csv",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "chunk_id,source_file,chunk_length\n"
    )

    for chunk in chunks:

        f.write(
            f"{chunk.metadata['chunk_id']},"
            f"\"{chunk.metadata['source_file']}\","
            f"{chunk.metadata['chunk_length']}\n"
        )


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = FAISS.from_documents(
    chunks,
    embeddings
)

db.save_local("vectorstore")

print("Vector DB created successfully")
print("Chunk file: chunks_debug.txt")
print("Chunk metadata: chunk_metadata.csv")