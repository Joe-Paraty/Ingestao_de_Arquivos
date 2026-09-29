from pathlib import Path
import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveJsonSplitter


def is_json_lines(file: Path) -> bool:

    # Verifica se cada linha não vazia é um JSON independente
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        return len(lines) > 1 and all(
            json.loads(line) is not None for line in lines
        )

    except json.JSONDecodeError:
        return False


def detect_json_type(file: Path):

    # Tenta carregar como JSON tradicional
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError:

        if is_json_lines(file):
            return {
                "type": "json_lines",
                "data": None,
                "root_key": None
            }

        raise ValueError(
            f"Invalid JSON or JSON Lines file: {file}"
        )

    # Lista direta
    if isinstance(data, list):
        return {
            "type": "linear",
            "data": data,
            "root_key": None
        }

    # Dicionário com uma única lista principal
    if isinstance(data, dict) and len(data) == 1:

        root_key = next(iter(data))

        if isinstance(data[root_key], list):
            return {
                "type": "linear",
                "data": data,
                "root_key": root_key
            }

    # JSON aninhado
    if isinstance(data, dict):
        return {
            "type": "nested",
            "data": data,
            "root_key": None
        }

    # Valor JSON simples
    return {
        "type": "value",
        "data": data,
        "root_key": None
    }


def process_linear_json(
    file: Path,
    data,
    root_key=None,
    items_per_chunk: int = 50
):

    # Obtém a lista de registros
    items = data[root_key] if root_key else data

    docs = []

    # Divide a lista em blocos de 50 itens
    for start in range(0, len(items), items_per_chunk):

        end = min(
            start + items_per_chunk,
            len(items)
        )

        chunk = items[start:end]

        # Converte o chunk para texto JSON
        content = json.dumps(
            chunk,
            ensure_ascii=False,
            indent=2
        )

        metadata = {
            "source": str(file),
            "type": ".json",
            "structure": "linear",
            "start_item": start + 1,
            "end_item": end
        }

        # Adiciona a chave-raiz quando existir
        if root_key:
            metadata["root_key"] = root_key

        docs.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return docs


def process_nested_json(
    file: Path,
    data,
    max_chunk_size: int = 500
):

    # Divide o JSON aninhado preservando sua estrutura
    splitter = RecursiveJsonSplitter(
        max_chunk_size=max_chunk_size
    )

    docs = splitter.create_documents(
        texts=[data]
    )

    # Adiciona metadados aos Documents
    for doc in docs:

        doc.metadata.update({
            "source": str(file),
            "type": ".json",
            "structure": "nested"
        })

    return docs


def process_json_lines(
    file: Path,
    lines_per_chunk: int = 50
):

    # Lê cada linha como um objeto JSON independente
    with open(file, "r", encoding="utf-8") as f:
        items = [
            json.loads(line)
            for line in f
            if line.strip()
        ]

    docs = []

    # Divide os registros em blocos de 50 linhas
    for start in range(0, len(items), lines_per_chunk):

        end = min(
            start + lines_per_chunk,
            len(items)
        )

        chunk = items[start:end]

        # Converte o bloco para texto JSON
        content = json.dumps(
            chunk,
            ensure_ascii=False,
            indent=2
        )

        metadata = {
            "source": str(file),
            "type": ".json",
            "structure": "json_lines",
            "start_line": start + 1,
            "end_line": end
        }

        docs.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return docs


def process_json(file: Path):

    # Identifica a estrutura do JSON
    json_info = detect_json_type(file)

    print("JSON TYPE:", json_info["type"])

    if json_info["root_key"]:
        print("ROOT KEY:", json_info["root_key"])

    # Processa JSON linear
    if json_info["type"] == "linear":

        return process_linear_json(
            file=file,
            data=json_info["data"],
            root_key=json_info["root_key"]
        )

    # Processa JSON aninhado
    if json_info["type"] == "nested":

        return process_nested_json(
            file=file,
            data=json_info["data"]
        )

    # Processa JSON Lines
    if json_info["type"] == "json_lines":

        return process_json_lines(
            file=file
        )

    # Outros valores JSON
    return []