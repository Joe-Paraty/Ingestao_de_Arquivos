from pathlib import Path

from langchain_core.documents import Document


def process_markdown(file: Path):

    # Lê o conteúdo Markdown
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Cria o Document
    docs = [
        Document(
            page_content=content,
            metadata={
                "source": str(file),
                "type": ".md"
            }
        )
    ]

    return docs