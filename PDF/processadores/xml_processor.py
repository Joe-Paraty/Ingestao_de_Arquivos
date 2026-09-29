from pathlib import Path
import json
import xmltodict

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveJsonSplitter


def detect_xml_type(file: Path):

    # Converte o XML para uma estrutura Python
    with open(file, "r", encoding="utf-8") as f:
        data = xmltodict.parse(f.read())

    root_key = next(iter(data))
    root_data = data[root_key]

    # Procura uma lista de elementos repetitivos na raiz
    if isinstance(root_data, dict):

        for key, value in root_data.items():

            if isinstance(value, list):

                return {
                    "type": "linear",
                    "data": data,
                    "root_key": root_key,
                    "record_key": key
                }

    # XML aninhado/complexo
    return {
        "type": "nested",
        "data": data,
        "root_key": root_key,
        "record_key": None
    }


def process_linear_xml(
    file: Path,
    data,
    root_key,
    record_key,
    items_per_chunk: int = 50
):

    # Obtém a lista de registros
    items = data[root_key][record_key]

    docs = []

    # Divide a lista em blocos de 50 itens
    for start in range(0, len(items), items_per_chunk):

        end = min(
            start + items_per_chunk,
            len(items)
        )

        chunk = items[start:end]

        # Converte o bloco para texto estruturado
        content = json.dumps(
            chunk,
            ensure_ascii=False,
            indent=2
        )

        metadata = {
            "source": str(file),
            "type": ".xml",
            "structure": "linear",
            "root_key": root_key,
            "record_key": record_key,
            "start_item": start + 1,
            "end_item": end
        }

        docs.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return docs


def process_nested_xml(
    file: Path,
    data,
    root_key,
    max_chunk_size: int = 500
):

    # Divide a estrutura preservando a hierarquia
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
            "type": ".xml",
            "structure": "nested",
            "root_key": root_key
        })

    return docs


def process_xml(file: Path):

    # Identifica a estrutura do XML
    xml_info = detect_xml_type(file)

    print("XML TYPE:", xml_info["type"])
    print("ROOT KEY:", xml_info["root_key"])

    if xml_info["record_key"]:
        print("RECORD KEY:", xml_info["record_key"])

    # Processa XML linear
    if xml_info["type"] == "linear":

        return process_linear_xml(
            file=file,
            data=xml_info["data"],
            root_key=xml_info["root_key"],
            record_key=xml_info["record_key"]
        )

    # Processa XML aninhado
    if xml_info["type"] == "nested":

        return process_nested_xml(
            file=file,
            data=xml_info["data"],
            root_key=xml_info["root_key"]
        )

    return []