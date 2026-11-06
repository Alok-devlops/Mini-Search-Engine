# Mini Information Retrieval System

A college-level **Web Search Mining / Information Retrieval** project built with **Python** and **Streamlit**.  
It demonstrates core IR concepts: document loading, tokenization, text normalization, inverted index construction, keyword search with AND logic, and wildcard search.

---

## Project Structure

```
WSM_Search_Engine/
├── app.py                      # Streamlit entry point – ties all modules together
├── requirements.txt            # Python dependencies (streamlit only)
├── README.md                   # This file
├── modules/
│   ├── __init__.py             # Marks modules/ as a Python package
│   ├── document_loader.py      # Reads .txt files from the documents/ directory
│   ├── tokenizer.py            # Splits raw text into word tokens using regex
│   ├── normalizer.py           # Lowercases tokens and strips non-alpha characters
│   ├── inverted_index.py       # Builds the inverted index dictionary
│   ├── query_processor.py      # Handles normal multi-word AND queries
│   └── wildcard_processor.py   # Handles wildcard queries using * pattern matching
└── documents/
    ├── doc1.txt                # Artificial Intelligence overview
    ├── doc2.txt                # Machine Learning fundamentals
    ├── doc3.txt                # Python for Data Science
    ├── doc4.txt                # Deep Learning and Neural Networks
    └── doc5.txt                # Data Science and Big Data Technologies
```

---

## Module Descriptions

### `document_loader.py`
Reads every `.txt` file from the `documents/` directory and returns a dictionary:
```python
{ "doc1": "Introduction to Artificial Intelligence ...", ... }
```
Raises `FileNotFoundError` if the directory is missing and `ValueError` if no `.txt` files exist.

### `tokenizer.py`
Uses Python's `re` module to extract alphabetic word tokens from raw text:
```
"Hello, World!" → ["Hello", "World"]
```

### `normalizer.py`
Converts tokens to lowercase and removes non-alphabetic characters for consistent index keys:
```
["Hello", "World!"] → ["hello", "world"]
```
Also provides `normalize_query_term()` which preserves the `*` wildcard character.

### `inverted_index.py`
Builds the core inverted index data structure:
```python
{
  "python":  ["doc1", "doc3"],
  "machine": ["doc2", "doc3", "doc4"],
  ...
}
```
Each term maps to a **sorted list of doc IDs** that contain it. Duplicate entries per document are avoided using Python sets.

### `query_processor.py`
Handles normal keyword queries:
- Tokenizes and normalizes the query.
- Looks up each term in the index.
- Applies **AND logic** via Python set intersection.
- Returns matching document IDs with contextual snippets.

### `wildcard_processor.py`
Handles wildcard queries containing `*`:
- Converts `*` to the regex equivalent `.*`.
- Matches the pattern against all indexed vocabulary terms.
- Returns all documents that contain any matching term.

**Examples:**
| Query    | Matches               |
|----------|-----------------------|
| `py*`    | python, pytorch       |
| `comput*`| computer, computing   |
| `*ing`   | learning, computing   |
| `learn*` | learning, learned     |

### `app.py`
The Streamlit frontend that:
- Initializes the system once using `@st.cache_resource`.
- Shows index statistics in the sidebar.
- Accepts queries and routes to either the normal or wildcard processor.
- Displays results with document previews and snippets.

---

## Installation

> **Prerequisite:** Python 3.8 or higher installed.

```bash
# 1. Navigate to the project directory
cd WSM_Search_Engine

# 2. (Recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## How to Use

1. **Normal Search:** Type one or more keywords (e.g., `machine learning`) and click **Search**.  
   Only documents containing **all** terms (AND logic) are returned.

2. **Wildcard Search:** Use `*` in your query (e.g., `py*` or `comput*`).  
   The system matches the pattern against the full vocabulary and returns relevant documents.

3. **No Results:** A friendly message is shown with suggestions to refine the query.

---

## Test Queries

| Query Type  | Example Query       | Expected Behaviour                              |
|-------------|---------------------|-------------------------------------------------|
| Single word | `python`            | Returns doc3                                    |
| AND query   | `machine learning`  | Returns docs containing both terms              |
| AND query   | `neural network`    | Returns doc2, doc4                              |
| Wildcard    | `py*`               | Matches python; returns doc3                    |
| Wildcard    | `comput*`           | Matches computer, computing; returns relevant docs |
| Wildcard    | `learn*`            | Matches learning; returns multiple docs         |
| No result   | `xyzabc`            | Displays "no documents matched" message         |

---

## Core Concepts Demonstrated

| Concept               | Location                      |
|-----------------------|-------------------------------|
| Tokenization          | `modules/tokenizer.py`        |
| Text Normalization    | `modules/normalizer.py`       |
| Inverted Index        | `modules/inverted_index.py`   |
| Boolean (AND) Retrieval | `modules/query_processor.py` |
| Wildcard Expansion    | `modules/wildcard_processor.py` |
| Modular Architecture  | Separate files per concern    |
| Caching / Performance | `@st.cache_resource` in app.py |

---

## Technology Stack

- **Python 3.8+** – Core language
- **Streamlit** – Web-based GUI framework
- **re** – Regular expressions for tokenization and wildcard matching
- **os** – Directory and file I/O
- **collections** – (available, not explicitly needed after using dicts + sets)

No external search APIs, AI APIs, or databases are used. All retrieval is done from local `.txt` files using the in-memory inverted index.
