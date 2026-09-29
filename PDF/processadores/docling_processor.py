from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
import json


def process_docling(file):

    # Output in chunks for future RAG
    loader_chunks = DoclingLoader(
        file_path=str(file),
        export_type=ExportType.DOC_CHUNKS
    )

    docs = loader_chunks.load()

    # Markdown output
    loader_markdown = DoclingLoader(
        file_path=str(file),
        export_type=ExportType.MARKDOWN
    )

    docs_markdown = loader_markdown.load()

    # Save Markdown content
    name = file.stem
    markdown_path = f"saida/{name}.md"

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(docs_markdown[0].page_content)

    # Save DOC_CHUNKS as JSON
    chunks_data = []

    for doc in docs:
        chunks_data.append({
            "page_content": doc.page_content,
            "metadata": doc.metadata
        })

    chunks_path = f"saida/{name}_chunks.json"

    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(
            chunks_data,
            f,
            ensure_ascii=False,
            indent=4
        )

    return docs