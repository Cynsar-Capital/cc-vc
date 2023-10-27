# models.py

from sqlalchemy import Column, Integer, String, create_engine, MetaData, ForeignKey, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///text_data.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True)
    chunks = relationship("TextChunk", back_populates="file")

class TextChunk(Base):
    __tablename__ = 'text_chunks'
    id = Column(Integer, primary_key=True)
    chunk_content = Column(Text)
    file_id = Column(Integer, ForeignKey('files.id'))
    file = relationship("File", back_populates="chunks")


class ProcessedText(Base):
    __tablename__ = 'processed_texts'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)  # Store the processed NLP content here
    file_id = Column(Integer, ForeignKey('files.id'))
    
    file = relationship("File", back_populates="processed_texts")

# Update the File model to establish the relationship
File.processed_texts = relationship("ProcessedText", back_populates="file")

class ExtractedTable(Base):
    __tablename__ = 'extracted_tables'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)  # Store the table content here
    file_id = Column(Integer, ForeignKey('files.id'))
    
    file = relationship("File", back_populates="extracted_tables")

# Update the File model to establish the relationship
File.extracted_tables = relationship("ExtractedTable", back_populates="file")



class Topics(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String, index=True)
    topic = Column(String)

# Embeddings Model
class Embeddings(Base):
    __tablename__ = 'embeddings'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String, index=True)
    chunk_id = Column(Integer, ForeignKey('processed_texts.id'))  # Assuming there's a chunks table with an id column
    embedding = Column(LargeBinary)  # Storing embeddings as binary data

# Clusters Model
class Clusters(Base):
    __tablename__ = 'clusters'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String, index=True)
    chunk_id = Column(Integer, ForeignKey('processed_texts.id'))
    cluster_label = Column(Integer)



class Entity(Base):
    __tablename__ = 'entities'
    
    id = Column(Integer, primary_key=True)
    entity_text = Column(Text)
    entity_label = Column(String)
    chunk_id = Column(Integer, ForeignKey('processed_texts.id'))

    # Establishing relationship with the TextChunk model
    processed_text = relationship("ProcessedText", back_populates="entities")

# Update the ProcessedText model to establish the relationship with entities
ProcessedText.entities = relationship("Entity", back_populates="processed_text")
