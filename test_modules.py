import sys
sys.path.insert(0, '.')

print('=== TEST 1: Document Loading ===')
from modules.document_loader import load_documents
docs = load_documents('documents')
print(f'Loaded {len(docs)} documents: {list(docs.keys())}')

print()
print('=== TEST 2: Tokenization ===')
from modules.tokenizer import tokenize
tokens = tokenize('Hello, World! Python is great.')
print(f'Tokens: {tokens}')

print()
print('=== TEST 3: Normalization ===')
from modules.normalizer import normalize, normalize_query_term
norm = normalize(['Hello', 'World!', 'Python123'])
print(f'Normalized: {norm}')
print(f'Query term py*: {normalize_query_term("py*")}')

print()
print('=== TEST 4: Inverted Index ===')
from modules.inverted_index import build_index, get_vocabulary
index = build_index(docs)
vocab = get_vocabulary(index)
print(f'Index size (unique terms): {len(vocab)}')
print(f'Sample - python: {index.get("python", [])}')
print(f'Sample - machine: {index.get("machine", [])}')
print(f'Sample - learning: {index.get("learning", [])}')
print(f'Sample - neural: {index.get("neural", [])}')

print()
print('=== TEST 5: Normal Queries ===')
from modules.query_processor import process_query
r = process_query('python', index, docs)
print(f'Query [python]: terms={r["query_terms"]}, docs={[x["doc_id"] for x in r["results"]]}')
r = process_query('machine learning', index, docs)
print(f'Query [machine learning]: terms={r["query_terms"]}, docs={[x["doc_id"] for x in r["results"]]}')
r = process_query('neural network', index, docs)
print(f'Query [neural network]: terms={r["query_terms"]}, docs={[x["doc_id"] for x in r["results"]]}')
r = process_query('xyznonexistent', index, docs)
print(f'Query [xyznonexistent]: docs={[x["doc_id"] for x in r["results"]]}, not_found={r["not_found_terms"]}')

print()
print('=== TEST 6: Wildcard Queries ===')
from modules.wildcard_processor import wildcard_search
r = wildcard_search('py*', index, vocab)
print(f'Wildcard [py*]: matched_terms={r["matched_terms"]}, docs={r["doc_ids"]}')
r = wildcard_search('comput*', index, vocab)
print(f'Wildcard [comput*]: matched_terms={r["matched_terms"]}, docs={r["doc_ids"]}')
r = wildcard_search('learn*', index, vocab)
print(f'Wildcard [learn*]: matched_terms={r["matched_terms"]}, docs={r["doc_ids"]}')
r = wildcard_search('*ing', index, vocab)
print(f'Wildcard [*ing]: sample_terms={r["matched_terms"][:6]}, docs={r["doc_ids"]}')
r = wildcard_search('xyz*', index, vocab)
print(f'Wildcard [xyz*]: matched_terms={r["matched_terms"]}, docs={r["doc_ids"]}')

print()
print('=== ALL TESTS PASSED ===')
