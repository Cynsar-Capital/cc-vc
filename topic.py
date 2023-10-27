import gensim
from gensim import corpora
from database.db_utils import get_processed_texts, store_topics, store_clusters, store_embeddings, get_embeddings_by_file
from logging_util import logger
import tensorflow_hub as hub
import tensorflow as tf
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')

# Load the BERT model
bert_embed = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3", trainable=False)


# Function to generate topics
def generate_topic(file_name):
    logger.info(f'Working out the topic for {file_name}')
    processed_chunks = get_processed_texts(file_name)

    # Prepare the corpus and dictionary
    texts = [chunk.split() for chunk in processed_chunks]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Apply LDA with hyperparameter tuning
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, random_state=42, 
                                                alpha='auto', eta='auto', iterations=400)
    topics = lda_model.print_topics(num_words=100)

    # Store topics in the database
    topics_to_store = [{"file_name": file_name, "topic": topic[1]} for topic in topics]
    store_topics(topics_to_store)


# Function to get BERT embeddings
def get_bert_embeddings(file_name):
    """Convert texts into BERT embeddings."""
    embeddings = []

    processed_chunks = get_processed_texts(file_name)
    
    # Tokenize texts using BERT tokenizer
    for text in processed_chunks:
        tokenized_text = model.tokenize(text)  # We're now consistently using SentenceTransformer's tokenization
        input_mask = [1] * len(tokenized_text)
        segment_ids = [0] * len(tokenized_text)
        bert_inputs = [tokenized_text, input_mask, segment_ids]
        
        # Get embeddings using the provided BERT model
        embedding = bert_embed(bert_inputs)
        embeddings.append(embedding)

    embeddings_to_store = [{"file_name": file_name, "embedding": embedding} for embedding in embeddings]
    store_embeddings(embeddings_to_store)
    return embeddings

# Function to cluster embeddings
def cluster_embeddings(file_name,n_clusters=100):
    """Cluster embeddings using KMeans."""
    embeddings = get_embeddings_by_file(file_name)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(embeddings)
    labels = kmeans.labels_

    # Store clusters in the database
    if file_name:
        clusters_to_store = [{"file_name": file_name, "chunk_id": idx, "cluster_label": label} for idx, label in enumerate(labels)]
        store_clusters(clusters_to_store)

    return labels

