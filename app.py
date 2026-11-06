# app.py
# ---------------------------------------------------------
# MAIN APPLICATION FILE – Mini Information Retrieval System
# ---------------------------------------------------------
# This file is the entry point for the Streamlit web app.
# It ties together all modules:
#   document_loader  → loads .txt files from /documents
#   inverted_index   → builds the index from loaded docs
#   query_processor  → handles normal keyword queries (AND)
#   wildcard_processor → handles queries with '*' wildcard
#
# Run with:   streamlit run app.py
# ---------------------------------------------------------

import os
import streamlit as st

from modules.document_loader import load_documents
from modules.inverted_index import build_index, get_vocabulary
from modules.query_processor import process_query
from modules.wildcard_processor import wildcard_search
from modules.normalizer import normalize_query_term

# ── Path to the documents folder (relative to app.py) ─────────────────────────
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")


# ══════════════════════════════════════════════════════════════════════════════
#  CACHED RESOURCE: build index once per session, not on every interaction
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def initialize_system():
    """
    Loads documents and builds the inverted index exactly once.
    Streamlit's @st.cache_resource ensures this function is NOT
    re-executed on every user interaction (widget click / key press).

    Returns:
        tuple: (documents dict, inverted index dict, vocabulary list)
               OR raises an exception that the UI will display.
    """
    docs = load_documents(DOCUMENTS_DIR)
    idx = build_index(docs)
    vocab = get_vocabulary(idx)
    return docs, idx, vocab


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: detect if a query contains a wildcard
# ══════════════════════════════════════════════════════════════════════════════
def is_wildcard_query(query: str) -> bool:
    """Returns True if the query string contains the '*' wildcard character."""
    return '*' in query


# ══════════════════════════════════════════════════════════════════════════════
#  STREAMLIT PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Mini IR System",
    page_icon="🔍",
    layout="centered",
)


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.title("🔍 Mini Information Retrieval System")
st.markdown(
    "An inverted-index based search engine built with **Python** and **Streamlit**. "
    "Supports **normal keyword queries** (AND logic) and **wildcard queries** using `*`."
)
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
#  INITIALIZE SYSTEM (load docs + build index)
# ══════════════════════════════════════════════════════════════════════════════
try:
    documents, index, vocabulary = initialize_system()
    system_ready = True
except FileNotFoundError as e:
    st.error(f"📂 Directory Error: {e}")
    system_ready = False
except ValueError as e:
    st.error(f"📄 Document Error: {e}")
    system_ready = False
except Exception as e:
    st.error(f"⚠️ Unexpected error during initialization: {e}")
    system_ready = False


# ══════════════════════════════════════════════════════════════════════════════
#  SYSTEM STATS SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
if system_ready:
    with st.sidebar:
        st.header("📊 Index Statistics")
        st.metric("Documents Indexed", len(documents))
        st.metric("Vocabulary Size", len(vocabulary))

        st.markdown("---")
        st.subheader("📄 Indexed Documents")
        for doc_id in sorted(documents.keys()):
            st.markdown(f"- `{doc_id}.txt`")

        st.markdown("---")
        st.subheader("💡 Query Examples")
        st.markdown(
            "**Normal:**\n"
            "- `machine learning`\n"
            "- `neural network`\n"
            "- `python data`\n\n"
            "**Wildcard:**\n"
            "- `py*`\n"
            "- `comput*`\n"
            "- `learn*`\n"
            "- `*ing`\n"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SEARCH INTERFACE
# ══════════════════════════════════════════════════════════════════════════════
if system_ready:

    # ── Search input ──────────────────────────────────────────────────────────
    query_input = st.text_input(
        label="🔎 Enter your search query:",
        placeholder="e.g.  machine learning   OR   py*   OR   comput*",
        help="For AND search type multiple words. Use * for wildcard: py* → python, pytorch",
    )

    # ── Search button ─────────────────────────────────────────────────────────
    search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

    st.divider()

    # ── Process the query only when the button is pressed ─────────────────────
    if search_clicked:

        # --- Guard: empty query ---
        if not query_input.strip():
            st.warning("⚠️ Please enter a search query before clicking Search.")

        # ─────────────────────────────────────────────────────────────────────
        #  BRANCH A: WILDCARD QUERY
        # ─────────────────────────────────────────────────────────────────────
        elif is_wildcard_query(query_input):

            # Normalize the wildcard pattern (lowercase, keep '*')
            pattern = normalize_query_term(query_input.strip())

            st.subheader(f"🃏 Wildcard Search — `{pattern}`")

            wc_result = wildcard_search(pattern, index, vocabulary)

            matched_terms = wc_result["matched_terms"]
            matched_docs  = wc_result["doc_ids"]

            if not matched_terms:
                # No vocabulary term matched the pattern
                st.info(
                    f"🔍 No vocabulary terms matched the pattern **`{pattern}`**.\n\n"
                    "Try a broader pattern, e.g. `py*` or `learn*`."
                )
            else:
                # Show which vocabulary terms were matched
                st.success(
                    f"✅ Pattern **`{pattern}`** matched **{len(matched_terms)}** "
                    f"vocabulary term(s): `{'`, `'.join(matched_terms)}`"
                )

                if not matched_docs:
                    st.info("No documents found containing any of the matched terms.")
                else:
                    st.markdown(
                        f"**{len(matched_docs)} document(s) found:**"
                    )

                    for doc_id in matched_docs:
                        with st.expander(f"📄 {doc_id}.txt", expanded=True):
                            # Display a small preview of the document
                            preview = documents[doc_id][:400].strip()
                            st.text_area(
                                label="Document Preview",
                                value=preview + ("..." if len(documents[doc_id]) > 400 else ""),
                                height=120,
                                disabled=True,
                                key=f"wc_{doc_id}",
                            )

        # ─────────────────────────────────────────────────────────────────────
        #  BRANCH B: NORMAL KEYWORD QUERY (AND logic)
        # ─────────────────────────────────────────────────────────────────────
        else:
            result = process_query(query_input.strip(), index, documents)

            query_terms   = result["query_terms"]
            results       = result["results"]
            not_found     = result["not_found_terms"]

            st.subheader(f"📋 Search Results — `{query_input.strip()}`")

            # Show which terms were searched
            if query_terms:
                st.markdown(
                    f"**Query terms (AND):** `{'`, `'.join(query_terms)}`"
                )

            # Warn about terms not in the vocabulary
            if not_found:
                st.warning(
                    f"⚠️ The following term(s) were **not found** in the index "
                    f"and reduced results to zero: `{'`, `'.join(not_found)}`"
                )

            if not results:
                st.info(
                    "🔍 No documents matched your query.\n\n"
                    "**Tips:**\n"
                    "- Check your spelling.\n"
                    "- Try fewer or simpler keywords.\n"
                    "- Use a wildcard, e.g. `py*` instead of `python`."
                )
            else:
                st.success(f"✅ **{len(results)} document(s) found.**")

                for item in results:
                    doc_id  = item["doc_id"]
                    snippet = item["snippet"]

                    with st.expander(f"📄 {doc_id}.txt", expanded=True):
                        st.text_area(
                            label="Relevant Snippet",
                            value=snippet,
                            height=100,
                            disabled=True,
                            key=f"norm_{doc_id}",
                        )

    # ── Idle state message ────────────────────────────────────────────────────
    elif not search_clicked:
        st.markdown(
            "👆 **Enter a query above and click Search** to retrieve documents.\n\n"
            "- **Normal query:** type one or more keywords → AND retrieval\n"
            "- **Wildcard query:** use `*` as a wildcard, e.g. `py*`, `comput*`"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.divider()
st.caption(
    "Mini Information Retrieval System · "
    "Built with Python & Streamlit · "
    "Inverted Index + Wildcard Search"
)
