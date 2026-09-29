from pathlib import Path

import pandas as pd
from langchain_core.documents import Document


def process_tabular(file: Path, rows_per_chunk: int = 50):

    extension = file.suffix.lower()

    # CSV
    if extension == ".csv":
        tables = {
            "CSV": pd.read_csv(file)
        }

    # XLSX
    elif extension == ".xlsx":
        tables = pd.read_excel(
            file,
            sheet_name=None
        )

    else:
        raise ValueError(f"Unsupported format: {extension}")

    docs = []

    # Iterate through each table/sheet
    for sheet_name, df in tables.items():

        # Split the DataFrame into chunks of 50 rows
        for start in range(0, len(df), rows_per_chunk):

            end = min(
                start + rows_per_chunk,
                len(df)
            )

            chunk = df.iloc[start:end]

            # Convert the chunk to text
            content = chunk.to_csv(
                index=False
            )

            metadata = {
                "source": str(file),
                "type": extension,
                "start_row": start + 2,
                "end_row": end + 1
            }

            # XLSX files may contain multiple sheets
            if extension == ".xlsx":
                metadata["sheet"] = sheet_name

            docs.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

    return docs