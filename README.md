# Gemini RAG System

A Retrieval Augmented Generation (RAG) system built with Google's Gemini API for document search and question answering.

## Features

- Upload and index multiple documents (TXT, PDF, MD, and 100+ formats)
- Semantic search through your documents
- Interactive question-answering interface
- Automatic document chunking and embedding
- Citation support for grounding responses
- Persistent storage of documents

## Setup

1. Install dependencies using uv:
```bash
uv sync
```

2. Make sure your `.env` file contains your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Quick Start

1. Place your documents in the `documents/` directory
2. Run the application:
```bash
uv run python main.py
```

3. The system will:
   - Create a file search store
   - Upload and index all documents from the `documents/` directory
   - Start an interactive Q&A session

4. Ask questions about your documents and get AI-powered answers with citations

### Programmatic Usage

You can also use the `GeminiRAG` class directly in your code:

```python
from main import GeminiRAG

# Initialize
rag = GeminiRAG()

# Create a store
rag.create_store("my-knowledge-base")

# Upload documents
rag.upload_file("path/to/document.pdf")
rag.upload_multiple_files(["doc1.txt", "doc2.pdf"])

# Query the system
response = rag.query("What are the main topics in the documents?")

# List all stores
stores = rag.list_stores()

# Clean up (optional)
rag.delete_store()
```

## Features Explained

### Document Upload
- Supports 100+ file formats including PDF, TXT, MD, DOCX, XLSX, and more
- Automatic chunking with configurable token limits
- Optional metadata for filtering and organization
- Persistent storage (documents remain until explicitly deleted)

### Semantic Search
- Uses advanced embeddings for understanding context
- Goes beyond keyword matching to find relevant content
- Configurable retrieval parameters

### Citations
- Responses include grounding metadata
- Trace answers back to source documents
- Verify information accuracy

## Configuration

You can customize the chunking behavior in `main.py`:

```python
config={
    'chunking_config': {
        'white_space_config': {
            'max_tokens_per_chunk': 500,  # Adjust chunk size
            'max_overlap_tokens': 50      # Adjust overlap
        }
    }
}
```

## Sample Documents

The repository includes three sample documents in the `documents/` directory:
- `python_basics.txt` - Python programming fundamentals
- `machine_learning.txt` - Machine learning concepts
- `web_development.md` - Web development guide

You can replace these with your own documents to create a custom knowledge base.

## API Costs

- Embeddings: $0.15 per 1M tokens (at indexing time)
- Storage: Free
- Query embeddings: Free
- Retrieved document tokens: Standard Gemini pricing

## Troubleshooting

**Issue**: `GEMINI_API_KEY not found`
- Solution: Ensure your `.env` file exists and contains the API key

**Issue**: No documents found
- Solution: Place your documents in the `documents/` directory

**Issue**: Upload fails
- Solution: Check file format is supported and file size is under 100 MB

## License

MIT License