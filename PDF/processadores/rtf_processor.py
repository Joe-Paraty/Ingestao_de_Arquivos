from pathlib import Path

from striprtf.striprtf import rtf_to_text
from langchain_core.documents import Document


def process_rtf(file: Path):

    # Lê o arquivo RTF
    with open(file, "r", encoding="utf-8") as f:
        rtf_content = f.read()

    # Extrai o texto limpo
    text = rtf_to_text(rtf_content)

    # Cria o Document
    docs = [
        Document(
            page_content=text,
            metadata={
                "source": str(file),
                "type": ".rtf"
            }
        )
    ]

    return docs