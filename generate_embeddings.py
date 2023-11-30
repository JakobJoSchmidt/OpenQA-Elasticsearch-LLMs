import os
import json
import gzip
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Mount Google Drive
drive.mount('/content/drive')

# Model name
model_name = 'sentence-transformers/all-mpnet-base-v2'

# Wikipedia dataset file path
wikipedia_filepath = '/content/drive/MyDrive/datasets/simple_wiki/simplewiki-2020-11-01.jsonl.gz'

# Base path to store the embeddings
embeddings_dir = '/content/drive/MyDrive/embeddings/simple_wiki/'

def generate_embeddings(model, data):
    print('Generating embeddings...')
    embeddings = model.encode(data)
    return embeddings

def save_embeddings(embeddings, idx):
    embedding_file = os.path.join(embeddings_dir, f'embeddings-{idx:02}.npy')
    print(f'Saving embeddings to {embedding_file}')
    np.save(embedding_file, embeddings)

def main():
    model = SentenceTransformer(model_name)

    with gzip.open(wikipedia_filepath, 'rt', encoding='utf8') as fIn:
        paragraphs = []
        embeddings = []

        for line in tqdm(fIn, desc="Reading file"):
            data = json.loads(line.strip())
            for paragraph in data['paragraphs']:
                paragraphs.append(paragraph)
                embeddings.append(model.encode(paragraph))

                if len(paragraphs) % 1000 == 0:  # Save embeddings every 1000 paragraphs to reduce memory usage
                    save_embeddings(np.array(embeddings), len(paragraphs) // 1000)
                    embeddings = []

        # Save embeddings for the last batch of paragraphs
        if embeddings:
            save_embeddings(np.array(embeddings), len(paragraphs) // 1000 + 1)

    print('Done!')

    # Load all embeddings and concatenate them
    embeddings_all = []
    for i in range(1, len(paragraphs) // 1000 + 2):  # Plus 2 to account for the last batch
        embeddings_i = np.load(os.path.join(embeddings_dir, f'embeddings-{i:02}.npy'))
        embeddings_all.append(embeddings_i)

    embeddings_all = np.concatenate(embeddings_all, axis=0)
    np.save(os.path.join(embeddings_dir, 'embeddings-all.npy'), embeddings_all)

    print('All embeddings saved to a single file.')

main()