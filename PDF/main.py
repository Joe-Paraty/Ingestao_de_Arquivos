from pathlib import Path

from processadores.docling_processor import process_docling
from processadores.tabular_processor import process_tabular
from processadores.json_processor import process_json
from processadores.xml_processor import process_xml
from processadores.rtf_processor import process_rtf
from processadores.markdown_processor import process_markdown

file = Path("entrada/md_teste.md")
extension = file.suffix.lower()


if extension in [".pdf", ".docx", ".html", ".pptx", ".png", ".jpg", ".jpeg"]:

    docs = process_docling(file)

    print("DOC_CHUNKS:")
    print(docs)


elif extension in [".csv", ".xlsx"]:

    docs = process_tabular(file)

    print("DOC_CHUNKS:")
    print(docs)


elif extension == ".rtf":

    docs = process_rtf(file)

    print("DOC_CHUNKS:")
    print(docs)


elif extension in [".json", ".jsonl", ".ndjson"]:

    docs = process_json(file)

    print("DOC_CHUNKS:")
    print(docs)


elif extension == ".xml":
    
    docs = process_xml(file)

    print("DOC_CHUNKS:")
    print(docs)

elif extension == ".md":
    
    docs = process_markdown(file)

    print("DOC_CHUNKS:")
    print(docs)



else:
    print("Unsupported format")