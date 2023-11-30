import pandas as pd
import numpy as np
import gzip
import json
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

def is_normalized(vector):
    # Calculate the magnitude (length) of the vector
    magnitude = np.linalg.norm(vector)
    # Check if the magnitude is close to 1
    return np.isclose(magnitude, 1.0)

def load_embeddings(embeddings_path):
    print(f'Loading embeddings from {embeddings_path}')
    return np.load(embeddings_path)

def load_dataframe(dataframe_path):
    print(f'Loading dataframe from {dataframe_path}')
    with gzip.open(dataframe_path, 'rt', encoding='utf-8') as f:
        data = [json.loads(line.strip()) for line in f]
    paragraphs = [paragraph for item in data for paragraph in item['paragraphs']]
    return pd.DataFrame({'paragraphs': paragraphs})

def check_alignment(dataframe_path, embeddings_path):
    # Load your model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Load the dataframe and embeddings
    data = load_dataframe(dataframe_path)
    embeddings = load_embeddings(embeddings_path)

    # Pick a random row from the data
    random_index = np.random.randint(len(data))  # generate a random local index
    random_row = data.iloc[random_index]  # use iloc to select by local index

    # Print the randomly selected text
    print("Randomly selected text: ", random_row['paragraphs'])

    # Generate the embedding for this row using the SentenceTransformer model
    generated_embedding = model.encode([random_row['paragraphs']])[0]

    # Get the corresponding saved embedding
    saved_embedding = embeddings[random_index]  # use local index to access embeddings array

    # Compare the two embeddings by calculating their cosine similarity
    cosine_similarity = 1 - distance.cosine(generated_embedding, saved_embedding)

    # Set the threshold for misalignment detection
    similarity_threshold = 0.999

    # Stop the program and print an error message if misalignment is detected
    if cosine_similarity < similarity_threshold:
        raise ValueError(f"Embedding is not correctly aligned. Cosine similarity is {cosine_similarity}")

    print("Alignment check: Embedding is correctly aligned!")

# Call the function with paths to your data
check_alignment('/content/drive/MyDrive/datasets/simple_wiki/simplewiki-2020-11-01.jsonl.gz', '/content/drive/MyDrive/datasets/simple_wiki/simplewiki-2020-11-01.npy')