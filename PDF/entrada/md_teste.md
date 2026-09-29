# DOCUMENTO DE TESTE --- MARKDOWN

> Arquivo criado para testar a ingestão de `.md` no pipeline Python.

## 1. Objetivo

Este documento serve para verificar se o pipeline consegue reconhecer e
preservar a estrutura de um arquivo **Markdown nativo**, sem necessidade
de OCR ou conversão documental.

## 2. Elementos presentes

-   Títulos e subtítulos
-   Parágrafos
-   **Texto em negrito**
-   *Texto em itálico*
-   `código inline`
-   Lista com marcadores
-   Lista numerada
-   Tabela Markdown
-   Link
-   Bloco de código
-   Citação

## 3. Tabela de teste

  Formato      Categoria           Tratamento          Saída
  ------------ ------------------- ------------------- -------------
  PDF          Documento           Docling / OCR       Markdown
  DOCX         Documento           Docling             Markdown
  PNG / JPG    Imagem              OCR / Docling       Markdown
  CSV / XLSX   Tabular             Pandas / OpenPyXL   Estruturado
  JSON / XML   Estruturado         Parser específico   Estruturado
  MD           Texto estruturado   Leitura direta      Markdown

## 4. Fluxo de processamento

1.  Detectar a extensão `.md`.
2.  Ler o arquivo diretamente como texto UTF-8.
3.  Preservar a sintaxe Markdown.
4.  Extrair metadados, se necessário.
5.  Aplicar chunking.
6.  Gerar embeddings.
7.  Enviar os chunks para o armazenamento vetorial.
8.  Utilizar o conteúdo no processo de **RAG**.

## 5. Exemplo de código

``` python
from pathlib import Path

arquivo = Path("documento.md")
conteudo = arquivo.read_text(encoding="utf-8")

print(conteudo)
```

## 6. Exemplo de RAG

O fluxo conceitual pode ser representado assim:

`Arquivo → Extração → Markdown → Chunking → Embeddings → Vector Store → Retriever → LLM`

## 7. Link de teste

[Projeto Docling no GitHub](https://github.com/docling-project/docling)

## 8. Citação

> Um arquivo Markdown já possui uma estrutura textual adequada para
> processamento, portanto normalmente não precisa ser convertido
> novamente para Markdown.

------------------------------------------------------------------------

**Fim do documento de teste.**
