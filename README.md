# Gemini File Search Tool: Production-Ready RAG System

A comprehensive Retrieval Augmented Generation (RAG) implementation using Google's **File Search Tool in Gemini API**. This system combines semantic search with grounded AI responses to deliver verifiable, citation-backed answers from your document repositories.

## 🚀 Overview

This implementation leverages Google's File Search Tool to provide enterprise-grade semantic search without the operational overhead of maintaining vector databases, embedding pipelines, or custom retrieval systems. Built on the `gemini-embedding-001` model and Gemini 2.5 Flash for generation.

## ✨ Key Features

### Document Management
- **100+ File Format Support**: PDF, TXT, MD, DOCX, XLSX, and more
- **Intelligent Indexing**: Automatic document chunking and embedding generation
- **Persistent Storage**: File search stores with managed infrastructure
- **Metadata Support**: Organize and filter documents with custom metadata

### Semantic Search & Retrieval
- **Advanced Embeddings**: Uses `gemini-embedding-001` with 128-3072 dimensional flexibility
- **Task-Optimized**: 8 specialized embedding types (RETRIEVAL, SEMANTIC_SIMILARITY, QA, etc.)
- **Matryoshka Representation Learning (MRL)**: Efficient dimension scaling without quality loss
- **Context-Aware**: Understands semantic meaning beyond keyword matching

### Response Generation
- **Grounded Answers**: AI responses with automatic source attribution
- **Citation Support**: Transparent grounding metadata showing exact sources
- **Interactive Q&A**: Built-in command-line interface for queries
- **Configurable**: Adjustable chunking strategies and retrieval parameters

## 🛠️ Setup

### Prerequisites
- Python 3.11+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Install dependencies using uv**:
```bash
uv sync
```

2. **Configure your API key**:
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

3. **Add your documents**:
Place your documents in the `documents/` directory (created automatically if it doesn't exist)

## 📖 Usage

### Quick Start (Interactive Mode)

1. Run the application:
```bash
uv run python gemini_file_search.py
```

2. The system will:
   - Create a file search store named "my-knowledge-base"
   - Upload and index all documents from the `documents/` directory
   - Start an interactive Q&A session

3. Ask questions and receive AI-powered answers with source citations:
```
Question: What are the key concepts in machine learning?
--------------------------------------------------

Answer:
Machine learning focuses on three main paradigms: supervised learning,
unsupervised learning, and reinforcement learning...

Sources:
1. machine_learning.txt
```

### Programmatic Usage

Use the `GeminiRAG` class directly in your Python code:

```python
from gemini_file_search import GeminiRAG

# Initialize the RAG system
rag = GeminiRAG()

# Create a file search store
rag.create_store("my-knowledge-base")

# Upload single file
rag.upload_file("path/to/document.pdf")

# Upload multiple files
rag.upload_multiple_files([
    "docs/report.pdf",
    "docs/analysis.txt",
    "docs/research.md"
])

# Query the system
response = rag.query("What are the main findings?")
print(response.text)

# Access grounding metadata
if response.candidates:
    grounding = response.candidates[0].grounding_metadata
    if grounding and grounding.grounding_chunks:
        for chunk in grounding.grounding_chunks:
            print(f"Source: {chunk.retrieved_context.title}")

# List all file search stores
stores = rag.list_stores()
for store in stores:
    print(f"Store: {store.name}")

# Clean up resources (optional)
rag.delete_files()  # Delete uploaded files
rag.delete_store()  # Delete the file search store
```

## 🧠 Technical Deep Dive

### Embedding Architecture

The File Search Tool uses Google's **`gemini-embedding-001`** model with the following capabilities:

#### Flexible Dimensionality
- **Range**: 128 to 3,072 dimensions
- **Recommended**: 768, 1,536, or 3,072 dimensions
- **Default**: 3,072-dimensional embeddings
- **Technology**: Matryoshka Representation Learning (MRL) enables efficient truncation without significant quality loss

#### Task-Optimized Embeddings (8 Types)

The model supports specialized embedding types for different use cases:

| Task Type | Description | Use Case |
|-----------|-------------|----------|
| `RETRIEVAL_DOCUMENT` | Document indexing | Building searchable document stores |
| `RETRIEVAL_QUERY` | Search queries | General search and retrieval |
| `SEMANTIC_SIMILARITY` | Text comparison | Finding similar content |
| `CLASSIFICATION` | Categorization | Organizing content by labels |
| `CLUSTERING` | Grouping | Discovering content patterns |
| `QUESTION_ANSWERING` | QA optimization | Building Q&A systems |
| `CODE_RETRIEVAL_QUERY` | Code search | Natural language code search |
| `FACT_VERIFICATION` | Evidence retrieval | Fact-checking systems |

#### Performance Features
- **Input Capacity**: Up to 2,048 tokens per request
- **Batch Processing**: 50% cost reduction for batch operations
- **Pre-normalized Outputs**: 3,072-dim embeddings ready for similarity computation
- **Vector DB Compatible**: Works with BigQuery, AlloyDB, ChromaDB, Pinecone, Qdrant, Weaviate

### File Search Store Management

File Search Stores provide managed infrastructure for document indexing:

- **Automatic Chunking**: Intelligent document splitting for optimal retrieval
- **Embedding Generation**: Automatic vectorization of document chunks
- **Metadata Support**: Custom metadata for filtering and organization
- **Persistent Storage**: Documents remain indexed until explicitly deleted
- **Grounding Metadata**: Automatic source tracking for citations

### How RAG Works in This System

1. **Document Upload**: Files uploaded via `client.files.upload()`
2. **Import to Store**: Files imported into search store with `import_file()`
3. **Automatic Processing**: Documents chunked and embedded automatically
4. **Query Time**: User question sent to Gemini with File Search Tool
5. **Retrieval**: Relevant chunks retrieved based on semantic similarity
6. **Generation**: Gemini generates response using retrieved context
7. **Grounding**: Response includes citations linking back to source documents

## 🎯 Use Cases

This RAG system is ideal for:

### Enterprise Applications
- **Internal Knowledge Bases**: Centralize company documentation, policies, and procedures
- **Customer Support**: Automated responses based on product documentation and FAQs
- **Research & Development**: Quick access to research papers, technical reports, and patents

### Developer Tools
- **Code Documentation**: Search through codebase documentation and API references
- **Technical Q&A**: Answer technical questions from engineering wikis and guides
- **Onboarding**: Help new team members find relevant information quickly

### Academic & Research
- **Literature Review**: Search and synthesize information from research papers
- **Study Assistance**: Answer questions from textbooks and course materials
- **Reference Management**: Quick retrieval of citations and source materials

## 📊 Pricing & Costs

| Operation | Cost | Notes |
|-----------|------|-------|
| **Embedding Generation** | $0.15 per 1M tokens | One-time cost at indexing |
| **Storage** | FREE | No ongoing storage costs |
| **Query Embeddings** | FREE | No cost for search queries |
| **Retrieved Content** | Standard Gemini pricing | Pay only for tokens in LLM context |
| **Batch Processing** | 50% discount | Use batch API for cost savings |

**Example**: Indexing 1,000 pages (~500K tokens) costs approximately **$0.075**

## 📁 Sample Documents

The repository includes sample documents in the `documents/` directory:

| File | Content | Purpose |
|------|---------|---------|
| `python_basics.txt` | Python programming fundamentals | Demonstrate text file indexing |
| `machine_learning.txt` | ML concepts and algorithms | Show technical content retrieval |
| `web_development.md` | Web development guide | Test markdown parsing |
| `attention.pdf` | "Attention is All You Need" paper | Verify PDF processing |

Replace these with your own documents to create a custom knowledge base.

## 🔧 Troubleshooting

### Common Issues

**`GEMINI_API_KEY not found`**
- **Cause**: Missing or incorrect `.env` file
- **Solution**: Create `.env` file with `GEMINI_API_KEY=your_key_here`

**`No documents found in directory`**
- **Cause**: Empty `documents/` directory
- **Solution**: Add supported files (PDF, TXT, MD, DOCX, etc.) to `documents/`

**`400 INVALID_ARGUMENT` error during upload**
- **Cause**: Invalid file name format
- **Solution**: The code automatically handles this by using `display_name` instead of `name`

**`No file search store created`**
- **Cause**: Calling `upload_file()` before `create_store()`
- **Solution**: Always call `create_store()` first, then upload files

**File processing takes too long**
- **Cause**: Large files or slow network
- **Solution**: The system automatically polls operation status; be patient with large files

**No grounding sources in response**
- **Cause**: Question not related to uploaded documents
- **Solution**: Ensure your query is relevant to the indexed content

## 📚 Additional Resources

### Official Documentation
- [Gemini API Overview](https://ai.google.dev/gemini-api/docs)
- [Embeddings in Gemini API](https://ai.google.dev/gemini-api/docs/embeddings)
- [File Search Tool Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [Grounding with Google Search](https://ai.google.dev/gemini-api/docs/grounding)

### Related Technologies
- [Matryoshka Representation Learning (MRL)](https://arxiv.org/abs/2205.13147)
- [Retrieval Augmented Generation (RAG) Paper](https://arxiv.org/abs/2005.11401)
- [Vector Databases Comparison](https://benchmark.vectorview.ai/)

### Python SDK
- [Google GenAI Python SDK](https://github.com/googleapis/python-genai)
- [API Reference](https://googleapis.github.io/python-genai/)

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with Google's Gemini API and File Search Tool. Special thanks to the Google AI team for providing powerful, accessible AI infrastructure.

---

**Questions?** Open an issue or check the [official documentation](https://ai.google.dev/gemini-api/docs/file-search)