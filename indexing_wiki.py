import os
import json
import gzip
import time
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout  
from elasticsearch.helpers import bulk
from scipy.spatial import distance
from tqdm import tqdm

model = SentenceTransformer('all-mpnet-base-v2')
# Path to the Simple Wikipedia dataset and embeddings
dataset_filepath = '/Users/jakob/Dev/Masterarbeit/datasets/simple_wiki/simplewiki-2020-11-01.jsonl.gz'
embeddings_filepath = '/Users/jakob/Dev/Masterarbeit/datasets/simple_wiki/simplewiki-2020-11-01.npy'
last_index_file = '/Users/jakob/Dev/Masterarbeit/datasets/simple_wiki/last_index.txt'
index_name= "simple_wiki_ex"

def create_es_index(es, index_name):
    print('Creating Elasticsearch index...')

    mapping = {
        "properties": {
            "text": {"type": "text"},
            "text_embedding": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "dot_product"
            }
        }
    }       

    es.indices.create(
        index=index_name,
        body={
            "mappings": {
                "_source": {
                    "excludes": ["text_embedding"]
                },
                "properties": mapping["properties"]
            }
        },  
        ignore=400  # Ignore 400 already_exists_exception
    )

def check_alignment(passages_chunk, embeddings):
    similarity_threshold = 0.999  # Set the threshold for misalignment detection

    # Get the first doc in the chunk
    first_global_index, first_docid, first_paragraph = passages_chunk[0]

    # Get the corresponding embedding
    first_embedding = embeddings[first_global_index].tolist()  # Convert numpy array to list for serialization

    # Generate an embedding for the paragraph
    generated_embedding = model.encode(first_paragraph)

    # Compare the two embeddings by calculating their cosine similarity
    cosine_similarity = 1 - distance.cosine(generated_embedding, first_embedding)

    # Raise an error if misalignment is detected
    if cosine_similarity < similarity_threshold:
        raise ValueError(f"Embedding is not correctly aligned for docid {first_docid}. Cosine similarity is {cosine_similarity}")

    print(f"Alignment checked for doc with global id: {first_global_index}")

def generate_data_for_indexing(passages_chunk, embeddings):
    print("Generating data for bulk indexing ....")
    for global_index, docid, paragraph in passages_chunk:
        embedding = embeddings[global_index].tolist()  # Convert numpy array to list for serialization
        yield {
            "_index": index_name,
            "_id": docid,
            "_source": {
                "text": paragraph,  # Paragraph text
                "text_embedding": embedding  # Corresponding embedding
            }
        }



def bulk_index_passages(es_client, passages_chunk, embeddings):
    # Set the maximum number of retries
    max_retries = 10
    retries = 0

    while retries < max_retries:
        try:
            print("Starting to bulk index...")
            # Bulk index the data
            bulk(es_client, generate_data_for_indexing(passages_chunk, embeddings))
            # If bulk indexing is successful, break out of the loop
            break
        except ConnectionTimeout as e:
            # Handle the connection timeout exception
            print(f"Connection timeout error occurred: {e}")
            print(f"Retrying chunk starting with docid {passages_chunk[0][0]} - Attempt {retries + 1}/{max_retries}")
            time.sleep(5 + retries*3)  # Wait for a few seconds before retrying
            retries += 1

    # If bulk indexing still fails after max_retries, raise the last exception
    if retries == max_retries:
        raise ConnectionTimeout(f"Failed to index chunk starting with docid {passages_chunk[0][1]} after {max_retries} retries")

def load_passages(dataset_filepath):
    """
    Load passages from a gzipped JSONL file.

    :param dataset_filepath: Path to the gzipped JSONL file.
    :return: List of passages. Each passage is a tuple of the form (global_index, docid, paragraph).
    """
    passages = []

    with gzip.open(dataset_filepath, 'rt', encoding='utf8') as fIn:
        global_index = 0  
        for idx_article, line in enumerate(fIn):
            data = json.loads(line.strip())
            for idx_paragraph, paragraph in enumerate(data['paragraphs']):
                docid = f"{idx_article}#{idx_paragraph}"  # Create a document ID from the article and paragraph indices
                passages.append((global_index, docid, paragraph))
                global_index += 1  # Increment the global index

    return passages

def main():

    chunk_size = 1000  # Define the size of your chunks
    
    # Load the last processed global index
    with open(last_index_file, 'r') as f:
        start_index = int(f.read().strip())
    
    # Load the passages (replace with your actual code for loading passages)
    passages = load_passages(dataset_filepath)

    # Create an Elasticsearch client 
    es = Elasticsearch("http://localhost:9200")
    create_es_index(es, index_name)

    # Load embedding file
    embeddings = np.load(embeddings_filepath)

    total_chunks = len(passages) // chunk_size
    start_chunk = start_index // chunk_size
    progress_bar = tqdm(total=total_chunks, desc="Indexing progress", initial=start_chunk)  
    print("\n")


    # Process and index the passages in chunks
    for i in range(start_index, len(passages), chunk_size):  

        end_index = min(i + chunk_size, len(passages))  # Ensure the end index doesn't exceed the number of passages
        chunk = passages[i:end_index]
        print(f"starting with chunk {i} - {end_index}")

        # Check alignment for the first doc
        check_alignment(chunk, embeddings)  

        bulk_index_passages(es, chunk, embeddings)
        
        # Save the last processed global index
        with open(last_index_file, 'w') as f:
            f.write(str(i + chunk_size))  # Write the index of the last processed chunk plus the chunk size
        print(f"saved {i + chunk_size} to last_indexed.txt")
        progress_bar.update(1)  # update the progress bar by 1 step
        print("\n")
    
    progress_bar.close()  # close the progress bar after finishing

main()
