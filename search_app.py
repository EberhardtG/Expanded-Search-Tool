import streamlit as st
import chromadb
import os

st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")

# --- ChromaDB Setup ---
@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path="./search_db")
    return client.get_or_create_collection(
        name="course_docs",
        configuration={"hnsw": {"space": "cosine"}}
    )

collection = get_collection()

# --- Document Loading & Chunking ---
def load_and_chunk(directory, chunk_size=400, overlap=50):
    chunks = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(('.txt', '.md')):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        for i, para in enumerate(paragraphs):
            chunks.append({
                "text": para,
                "source": filename,
                "chunk_id": f"{filename}_{i}",
                "chunk_index": i,
            })
    return chunks

# --- Sidebar: Ingestion Controls ---
with st.sidebar:
    st.title("📁 Document Manager")

    if st.button("🔄 Re-index Documents"):
        docs_path = "docs/docs/docs"  # YOUR ACTUAL PATH
        chunks = load_and_chunk(docs_path)
        if chunks:
            collection.upsert(
                documents=[c["text"] for c in chunks],
                metadatas=[{
                    "source": c["source"],
                    "chunk_index": str(c["chunk_index"])
                } for c in chunks],
                ids=[c["chunk_id"] for c in chunks],
            )
            st.success(f"Indexed {len(chunks)} chunks from {len(set(c['source'] for c in chunks))} files")
        else:
            st.warning("No .txt or .md files found in docs/ folder")

    st.metric("Documents in DB", collection.count())

    st.divider()
    n_results = st.slider("Results to show", 1, 10, 5)

    st.divider()

# --- Sidebar: Source Filter ---
all_metas = collection.get(include=["metadatas"])["metadatas"]
unique_sources = sorted({m["source"] for m in all_metas})

st.sidebar.header("Source Filter")

selected_sources = st.sidebar.multiselect(
    "Search only within these files:",
    options=unique_sources,
    default=unique_sources
)

st.sidebar.write(f"Total sources available: **{len(unique_sources)}**")

# --- Main Search Interface ---
st.title("🔍 Semantic Search")
st.write("Search your course documents by meaning, not just keywords.")

query = st.text_input("Enter your search query", placeholder="How does authentication work?")

if query and collection.count() > 0:

    # --- APPLY FILTER LOGIC ---
    if len(selected_sources) == len(unique_sources):
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, collection.count())
        )
    else:
        results = collection.query(
            query_texts=[query],
            where={"source": {"$in": selected_sources}},
            n_results=min(n_results, collection.count())
        )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    ids = results["ids"][0]  # <-- FIX: use ids list

    st.subheader(f"Showing {len(docs)} of {collection.count()} total documents")

    # --- Display Results ---
    for doc, metadata, distance, chunk_id in zip(docs, metas, dists, ids):

        # Relevance badge
        if distance < 0.5:
            relevance = "🟢 High"
        elif distance < 1.0:
            relevance = "🟡 Medium"
        else:
            relevance = "🔴 Low"

        with st.container():
            col_meta, col_score = st.columns([3, 1])
            with col_meta:
                st.write(f"**{metadata['source']}** — chunk {metadata['chunk_index']}")
            with col_score:
                st.write(f"{relevance} (dist: {distance:.3f})")

            # Expandable preview
            preview = doc[:150] + "..."
            with st.expander(preview):
                st.write(doc)

            # Similar-to-this button (now FIXED)
            if st.button("Similar to this →", key=f"similar_{chunk_id}"):
                similar = collection.query(
                    query_texts=[doc],
                    n_results=5
                )
                st.subheader("Similar Results")
                for sdoc, smeta, sdist in zip(
                    similar["documents"][0],
                    similar["metadatas"][0],
                    similar["distances"][0]
                ):
                    st.write(f"**{smeta['source']}** — dist {sdist:.3f}")
                    st.write(sdoc)
                    st.write("---")

            st.divider()

elif collection.count() == 0:
    st.info("👈 Click 'Re-index Documents' in the sidebar to load your documents first.")
