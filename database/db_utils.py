from sqlalchemy.orm import sessionmaker
from database.models import engine, TextChunk, File, ProcessedText, ExtractedTable, Entity, Topics, Embeddings, Clusters
from logging_util import logger
from utility import table_to_string

Session = sessionmaker(bind=engine)

def initialize_database():
    # This will create all tables that don't exist yet, based on your models
    File.metadata.create_all(engine)

def store_file_with_chunks(file_name, text_chunks):
    session = Session()
    
    # Query the database to check if a file with the given file_name already exists
    file_entry = session.query(File).filter_by(file_name=file_name).first()

    # If the file does not exist, create a new file entry
    if not file_entry:
        file_entry = File(file_name=file_name)
        session.add(file_entry)
        session.flush()  # This will ensure that file_entry gets an ID even if not committed yet

    # For each chunk in text_chunks, create a TextChunk entry associated with the file
    
    chunk_entry = TextChunk(chunk_content=text_chunks, file=file_entry)
    session.add(chunk_entry)

    session.commit()
    session.close()


def store_chunk(text_chunk):
    session = Session()
    chunk = TextChunk(chunk_content=text_chunk)
    session.add(chunk)
    session.commit()
    session.close()

# In db_utils.py or equivalent

def get_chunks_for_file(file_name):
    """Retrieve chunks associated with a file from the database."""
    session = Session()
    file_entry = session.query(File).filter_by(file_name=file_name).first()
    if not file_entry:
        logger.error(f"No file found with name: {file_name}")
        session.close()
        return []
    
    chunks = [chunk.chunk_content for chunk in file_entry.chunks]
    session.close()
    return chunks

def store_processed_text(file_name, processed_data):
    """Store the processed NLP data in the database."""
    session = Session()
    file_entry = session.query(File).filter_by(file_name=file_name).first()
    if not file_entry:
        logger.error(f"No file found with name: {file_name}")
        session.close()
        return
    
    for data in processed_data:
        processed_text_entry = ProcessedText(content=data, file=file_entry)
        session.add(processed_text_entry)
    
    session.commit()
    session.close()

def get_processed_texts(file_name):
    session = Session()
    # This query will retrieve the File record and its related ProcessedText records
    file_with_texts = session.query(File).filter(File.file_name == file_name).first()

    if file_with_texts is not None:
        processed_texts = [text.content for text in file_with_texts.processed_texts]
        return processed_texts
    else:
        logger.warn(f"No file found with ID: {file_name}")
        return []



# In db_utils.py or equivalent

def store_extracted_tables(file_name, tables_batch):
    """Store a batch of extracted tables in the database."""
    session = Session()
    
    # Check if the file entry exists in the database
    file_entry = session.query(File).filter_by(file_name=file_name).first()
    if not file_entry:
        file_entry = File(file_name=file_name)
        session.add(file_entry)
        session.flush()  # To ensure ID is generated if this is a new entry

    # For each table in tables_batch, create an ExtractedTable entry associated with the file
    for table in tables_batch:
        table_string = table_to_string(table)
        table_entry = ExtractedTable(content=table_string, file=file_entry)
        session.add(table_entry)

    session.commit()
    session.close()


def get_tables_for_file(file_name):
    """Retrieve tables associated with a file from the database."""
    session = Session()
    file_entry = session.query(File).filter_by(file_name=file_name).first()
    if not file_entry:
        logger.error(f"No file found with name: {file_name}")
        session.close()
        return []
    
    tables = [table.content for table in file_entry.extracted_tables]
    session.close()
    return tables


def get_entities_by_file(file_name):
    db_session = Session()
    entities = db_session.query(Entity).join(Entity.chunk).join(TextChunk.file).filter(File.file_name == file_name).all()
    
    # Convert entities to a list of dictionaries
    entity_list = []
    for entity in entities:
        entity_dict = {
            "entity_text": entity.entity_text,
            "entity_label": entity.entity_label,
            "chunk_id": entity.chunk_id
        }
        entity_list.append(entity_dict)
    
    return entity_list

# Function to store entities in the database
def store_entities(entities, chunk_id):
    db_session = Session()
    for entity in entities:
        new_entity = Entity(
            entity_text=entity["entity_text"],
            entity_label=entity["entity_label"],
            chunk_id=chunk_id
        )
        db_session.add(new_entity)
    
    # Commit the changes to the database
    db_session.commit()



# Function to fetch topics by file name
def get_topics_by_file(file_name):
    db_session = Session()
    topics = db_session.query(Topics).filter(Topics.file_name == file_name).all()
    
    # Convert topics to a list of dictionaries
    topic_list = []
    for topic in topics:
        topic_dict = {
            "file_name": topic.file_name,
            "topic": topic.topic
        }
        topic_list.append(topic_dict)
    
    return topic_list


def get_embeddings_by_file(file_name):
    db_session = Session()
    embeddings = db_session.query(Embeddings).join(Embeddings.chunk).join(ProcessedText.file).filter(File.file_name == file_name).all()
    
    # Convert embeddings to a list of dictionaries
    embedding_list = []
    for embedding in embeddings:
        embedding_dict = {
            "file_name": embedding.file_name,
            "chunk_id": embedding.chunk_id,
            "embedding": embedding.embedding  # Assuming you want to retrieve embeddings as binary data
        }
        embedding_list.append(embedding_dict)
    
    return embedding_list


def get_clusters_by_file(file_name):
    db_session = Session()
    clusters = db_session.query(Clusters).join(Clusters.chunk).join(ProcessedText.file).filter(File.file_name == file_name).all()
    
    # Convert clusters to a list of dictionaries
    cluster_list = []
    for cluster in clusters:
        cluster_dict = {
            "file_name": cluster.file_name,
            "chunk_id": cluster.chunk_id,
            "cluster_label": cluster.cluster_label
        }
        cluster_list.append(cluster_dict)
    
    return cluster_list


def store_topics(topics):
    db_session = Session()
    for topic in topics:
        new_topic = Topics(
            file_name=topic["file_name"],
            topic=topic["topic"]
        )
        db_session.add(new_topic)
    
    # Commit the changes to the database
    db_session.commit()

# Function to store embeddings in the database
def store_embeddings(embeddings):
    db_session = Session()
    for embedding in embeddings:
        new_embedding = Embeddings(
            file_name=embedding["file_name"],
            chunk_id=embedding["chunk_id"],
            embedding=embedding["embedding"]
        )
        db_session.add(new_embedding)
    
    # Commit the changes to the database
    db_session.commit()

# Function to store clusters in the database
def store_clusters(clusters):
    db_session = Session()
    for cluster in clusters:
        new_cluster = Clusters(
            file_name=cluster["file_name"],
            chunk_id=cluster["chunk_id"],
            cluster_label=cluster["cluster_label"]
        )
        db_session.add(new_cluster)
    
    # Commit the changes to the database
    db_session.commit()