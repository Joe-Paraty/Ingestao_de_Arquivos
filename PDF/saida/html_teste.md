# Teste Docling - HTML

# Documento HTML de Teste - Docling

**Objetivo:** testar a ingestão de HTML e sua transformação em conteúdo estruturado.

## 1. Conteúdo textual

Este arquivo contém elementos típicos de uma página HTML: títulos, parágrafos, **texto em negrito** , *texto em itálico* , listas, tabela, link e bloco de código.

## 2. Elementos para reconhecimento

- Títulos H1, H2 e H3
- Parágrafos
- Lista não ordenada
- Lista numerada
- Tabela HTML nativa
- Hiperlink
- Bloco de código

## 3. Tabela de teste

| Formato   | Categoria     | Tratamento       | Saída esperada   |
|-----------|---------------|------------------|------------------|
| PDF       | Documento     | Parse / OCR      | Markdown         |
| DOCX      | Documento     | Estrutura nativa | Markdown         |
| PNG / JPG | Imagem        | OCR              | Markdown         |
| HTML      | Documento Web | DOM / estrutura  | Markdown         |

## 4. Exemplo de pipeline

1. Identificar a extensão do arquivo.
2. Encaminhar o arquivo para o processador apropriado.
3. Extrair texto e estrutura.
4. Converter o resultado para Markdown.
5. Preparar chunks para embeddings e RAG.

### RAG + Docling

O Markdown pode funcionar como uma representação intermediária entre a extração documental e as etapas de **chunking, embeddings, armazenamento vetorial e recuperação semântica** .

## 5. Código de exemplo

```
arquivo = "documento.html"
extensao = ".html"

if extensao == ".html":
    print("Processar documento HTML")
```

## 6. Link de teste

Este é um [link para o projeto Docling](https://github.com/DS4SD/docling) incluído para verificar como hyperlinks são representados após a conversão.

Fim do documento HTML de teste.