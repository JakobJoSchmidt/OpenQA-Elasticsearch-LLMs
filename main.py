!pip install sentence-transformers elasticsearch

from sentence_transformers import SentenceTransformer, CrossEncoder, util
import numpy as np
from sklearn.preprocessing import normalize
from transformers import RobertaTokenizer, RobertaForQuestionAnswering
from google.colab import drive
drive.mount('/content/drive')

# Assuming Elasticsearch is properly set up
# Index name
index_name = "simple_wiki_ex"

# Model name
model_name = "all-mpnet-base-v2"

# Name of Cross Encoder
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


def generate_embedding(query_text):
    # todo remove normalize
    model = SentenceTransformer(model_name)
    embedding = model.encode([query_text])
    normalized_embedding = normalize(embedding).tolist()[0]
    return normalized_embedding


def bm25_search(query_text, result_size=10):
    bm25_query = {
        "match": {
            "text": query_text
        }
    }

    try:
        response = es.search(index=index_name, query=bm25_query, size=result_size)
        hits = response['hits']['hits']
        return hits
    except Exception as e:
        print(f"Error executing BM25 search query: {e}")


def semantic_search(query_text, result_size=10):
    # Generate the query vector
    query_vector = generate_embedding(query_text)
    # Define the body of the search query
    knn_query = {
            "field": "text_embedding",
            "query_vector": query_vector,
            "k": result_size,  # Number of nearest neighbors to return
            "num_candidates": 100
    }

    # Execute the search query
    try:
        response = es.search(index=index_name, knn=knn_query)
        hits = response['hits']['hits']
        return hits
    except Exception as e:
        print(f"Error executing the semantic search query: {e}")


def rerank_passages(results, query_text):
    cross_input_pairs = []
    passages = []

    for result in results:
        for hit in result:
            passage = hit['_source']['text']
            input_pair = [query_text, passage]
            cross_input_pairs.append(input_pair)
            passages.append({'text': passage, 'cross_score': None})

    cross_scores = cross_encoder.predict(cross_input_pairs)

    for idx in range(len(cross_scores)):
        passages[idx]['cross_score'] = cross_scores[idx]

    passages = sorted(passages, key=lambda x: x['cross_score'], reverse=True)
    passages = passages[:10]  # Limit results to 10
    return passages


def qa_model(query_text, context):
    # Load the tokenizer and model
    model = RobertaForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
    tokenizer = RobertaTokenizer.from_pretrained("deepset/roberta-base-squad2")

    # Tokenize the inputs
    inputs = tokenizer(query_text, context, return_tensors="pt")

    # Forward pass through the model
    outputs = model(**inputs)

    # Get the predicted start and end positions of the answer
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Find the most probable answer span
    start_index = start_logits.argmax()
    end_index = end_logits.argmax() + 1  # Add 1 to include the end token

    # Convert token indices to actual tokens
    tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
    answer = tokenizer.convert_tokens_to_string(tokens[start_index:end_index])

    if answer.strip() in ["", "<s>"]:
      message = "Sorry, I couldn't find an answer to your question in the provided context."
      answer = ""

    return answer

def print_results(results, section_title, search_result_size=10):
    print(f"\n-------------------------")
    print(section_title)
    print("-------------------------\n")
    for result in results[:search_result_size]:
        print(f"{result['_score']} {result['_source']['text']}")

def print_reranked_results(passages, section_title="Top Re-Ranked Results", display_size=10):
    print("\n-------------------------")
    print(section_title)
    print("-------------------------\n")
    for passage in passages[:display_size]:  # Only print the first display_size results
        print(f"{passage['cross_score']} {passage['text']}\n")

def print_final_answer(query_text, answer, context):
    print("\n-------------------------")
    print("Final Answer")
    print("-------------------------\n")
    print(f"Query: {query_text}\n")
    print("Answer Span:\n\n", context, width=120)
    print("\nAnswer:", answer, "\n")
    print("-------------------------\n")

def get_answer(query_text, return_context=False, search_result_size=10, rerank_result_size=10, verbose=False, print_bm25=False, print_semantic=False, print_rerank=False, print_final=False):
    # Perform BM25 search and semantic search
    results = []
    search_result = bm25_search(query_text, search_result_size)
    results.append(search_result)
    search_result = semantic_search(query_text, search_result_size)
    results.append(search_result)

    # Re-rank passages using the cross encoder
    passages = rerank_passages(results, query_text)

    if verbose or print_bm25:
        print_results(results[0], "Top BM25 Search Results", search_result_size)

    if verbose or print_semantic:
        print_results(results[1], "Top Semantic Search Results", search_result_size)

    if verbose or print_rerank:
        print_reranked_results(passages, display_size=rerank_result_size)

    # Use the QA model to get the final answer
    context = passages[0]['text']
    answer  = qa_model(query_text, context)

    if verbose or print_final:
      print_final_answer(query_text, answer, context)

    if return_context:
        return answer, context
    else:
        return answer