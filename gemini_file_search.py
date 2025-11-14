import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

class GeminiRAG:
    """RAG system using Gemini File Search API"""

    def __init__(self, api_key: str = None):
        """Initialize the RAG system with Gemini API"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Set API key in environment for the client
        os.environ['GOOGLE_API_KEY'] = self.api_key
        self.client = genai.Client(api_key=self.api_key)

        self.uploaded_files = []
        self.file_search_store = None
        self.model_name = "gemini-2.5-pro"
        print(f"Initialized with model: {self.model_name}")

    def create_store(self, store_name: str = "gemini-rag-store"):
        """Create a File Search store"""
        print(f"Creating file search store: {store_name}")

        # Create the File Search store with display name
        self.file_search_store = self.client.file_search_stores.create(
            config={'display_name': store_name}
        )

        print(f"File search store created: {self.file_search_store.name}")
        return self.file_search_store

    def upload_file(self, file_path: str, metadata: dict = None):
        """Upload a file to Gemini and import it into the file search store"""
        if not self.file_search_store:
            raise ValueError("No file search store created. Call create_store() first.")

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Uploading file: {file_path.name}")

        # Upload file using the Files API
        # display_name is used for the human-readable filename (no format restrictions)
        uploaded_file = self.client.files.upload(
            file=str(file_path),
            config={'display_name': file_path.name}
        )

        print(f"File uploaded: {uploaded_file.name}")

        # Import the file into the File Search store
        print("Importing file into search store...")
        operation = self.client.file_search_stores.import_file(
            file_search_store_name=self.file_search_store.name,
            file_name=uploaded_file.name
        )

        # Wait until import is complete
        while not operation.done:
            time.sleep(2)
            operation = self.client.operations.get(operation)

        print(f"File imported successfully: {file_path.name}")
        self.uploaded_files.append(uploaded_file)
        return uploaded_file

    def upload_multiple_files(self, file_paths: list):
        """Upload multiple files"""
        results = []
        for file_path in file_paths:
            try:
                result = self.upload_file(file_path)
                results.append((file_path, result))
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")
                results.append((file_path, None))
        return results

    def query(self, question: str, metadata_filter: str = None):
        """Query the RAG system using file search"""
        if not self.file_search_store:
            raise ValueError("No file search store created. Call create_store() first.")

        if not self.uploaded_files:
            raise ValueError("No files uploaded. Call upload_file() first.")

        print(f"\nQuery: {question}")
        print("-" * 50)

        # Use the file search store as a tool in the generation call
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=question,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[self.file_search_store.name]
                        )
                    )
                ]
            )
        )

        # Extract and print answer
        answer = response.text
        print(f"\nAnswer:\n{answer}\n")

        # Extract and display grounding sources
        if response.candidates and len(response.candidates) > 0:
            grounding = response.candidates[0].grounding_metadata

            if not grounding or not grounding.grounding_chunks:
                print("No grounding sources found")
            else:
                # Extract unique sources from grounding chunks
                sources = set()
                for chunk in grounding.grounding_chunks:
                    if hasattr(chunk, 'retrieved_context') and hasattr(chunk.retrieved_context, 'title'):
                        sources.add(chunk.retrieved_context.title)

                if sources:
                    print("\nSources:")
                    for i, source in enumerate(sorted(sources), 1):
                        print(f"{i}. {source}")
        else:
            print("No candidate responses found")

        return response

    def list_files(self):
        """List all uploaded files"""
        try:
            all_files = self.client.files.list()
            return list(all_files)
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def delete_files(self):
        """Delete all uploaded files"""
        print(f"Deleting {len(self.uploaded_files)} uploaded files...")
        for file in self.uploaded_files:
            try:
                self.client.files.delete(name=file.name)
                print(f"Deleted: {file.name}")
            except Exception as e:
                print(f"Error deleting {file.name}: {e}")
        self.uploaded_files = []
        print("All files deleted")

    def list_stores(self):
        """List all file search stores"""
        try:
            stores = self.client.file_search_stores.list()
            return list(stores)
        except Exception as e:
            print(f"Error listing stores: {e}")
            return []

    def delete_store(self, store_name: str = None):
        """Delete the file search store"""
        if self.file_search_store:
            try:
                self.client.file_search_stores.delete(name=self.file_search_store.name)
                print(f"Deleted file search store: {self.file_search_store.name}")
                self.file_search_store = None
            except Exception as e:
                print(f"Error deleting store: {e}")
        else:
            print("No file search store to delete")


def main():
    """Example usage of the Gemini RAG system"""

    # Initialize RAG system
    rag = GeminiRAG()

    # Create a file search store
    rag.create_store("my-knowledge-base")

    # Example: Upload files from a directory
    # You can modify this to point to your documents
    docs_dir = Path("documents")

    if docs_dir.exists() and docs_dir.is_dir():
        print(f"\nFound documents directory. Uploading files...")
        files = list(docs_dir.glob("*.txt")) + list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.md"))
        if files:
            rag.upload_multiple_files([str(f) for f in files])
        else:
            print("No supported files found in documents directory")
    else:
        print("\nNo 'documents' directory found.")
        print("Please create a 'documents' directory and add your files there.")
        print("Supported formats: .txt, .pdf, .md, and many more")
        return

    # Interactive query loop
    print("\n" + "=" * 50)
    print("RAG System Ready!")
    print("=" * 50)
    print("Type your questions (or 'quit' to exit):\n")

    while True:
        try:
            question = input("Question: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                break
            if question:
                rag.query(question)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()