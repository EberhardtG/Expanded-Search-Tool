

# 🔍 Semantic Search Engine (ChromaDB + Streamlit)

A semantic search tool that lets you explore course documents by **meaning**, not keywords.  
Built with **ChromaDB**, **SentenceTransformer embeddings**, and an interactive **Streamlit UI**.

This project is part of the *Applied AI: Embeddings & Retrieval* module and implements all required features from the Expanded Search Tool assignment.

---

## 🚀 Features

### ✅ Core Features
- **Semantic search** using vector embeddings  
- **Persistent ChromaDB database** (`search_db/`)  
- **Automatic document ingestion & chunking**  
- **Source filtering** via sidebar multiselect  
- **Result count display**  
  - Example: *“Showing 5 of 23 total documents”*  
- **Expandable previews**  
  - First 150 characters shown  
  - Full text available inside an expander  
- **Relevance scoring badges**  
  - 🟢 High  
  - 🟡 Medium  
  - 🔴 Low  

### ⭐ Bonus Features
- **“Similar to this” button**  
  - Runs a new semantic query using the selected result  
- **Unique source count** displayed in sidebar  

---

## 📂 Project Structure

```
project/
│
├── search_app.py          # Streamlit application
├── search_db/             # ChromaDB persistent storage
└── docs/                  # Your text files (nested path supported)
    └── docs/docs/         # Actual document location
```

Your `.txt` and `.md` files live inside:

```
docs/docs/docs/
```

The app automatically loads and chunks them.

---

## 🧠 How It Works

### 1. Document Ingestion
- Loads `.txt` and `.md` files  
- Splits them into paragraph-based chunks  
- Stores each chunk with metadata:
  - `source` (filename)
  - `chunk_index`
  - `id` (unique chunk identifier)

### 2. Embedding & Storage
- Each chunk is embedded using a SentenceTransformer model  
- Stored in ChromaDB with cosine similarity search  

### 3. Semantic Querying
- User enters a natural-language query  
- ChromaDB returns the most semantically similar chunks  
- Results are filtered by selected source files if desired  

---

## 🖥️ UI Overview

### Sidebar
- **Re-index Documents** button  
- **Document count**  
- **Result count slider**  
- **Source filter multiselect**  
- **Unique source count**

### Main Panel
- Search input  
- Result count  
- Expandable result previews  
- Relevance badges  
- “Similar to this” buttons  

---

## 🔧 Running the App

Install dependencies:

```bash
pip install streamlit chromadb sentence-transformers
```

Run the app:

```bash
streamlit run search_app.py
```

Make sure your document files are located inside:

```
docs/docs/docs/
```

---

## 📈 Future Enhancements

- Add embedding model selection  
- Add chunk highlighting for matched terms  
- Add fuzzy keyword fallback search  
- Add document upload UI  
- Add vector visualization (UMAP/PCA)

---

## 🎓 Educational Purpose

This project builds the foundation for your **Module 7 Semantic Search Engine**, teaching:

- Embedding-based retrieval  
- Chunking strategies  
- Metadata filtering  
- Interactive search UI design  
- Persistent vector database usage  

Each feature here reduces the work needed for the final module project.

---
