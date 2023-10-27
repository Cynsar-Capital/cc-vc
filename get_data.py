import PyPDF2
import spacy
import pdfplumber
from spacy.lang.en.stop_words import STOP_WORDS
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
import pandas as pd
from logging_util import logger
from database.db_utils import store_file_with_chunks, store_processed_text, get_chunks_for_file, store_extracted_tables
nlp = spacy.load("en_core_web_sm")

from utility import reduce_duplicates, remove_consecutive_duplicates


def determine_chunk_size(file_path):
    """Determine chunk size based on file size."""
    file_size = os.path.getsize(file_path)  # File size in bytes
    logger.info('Determining chunk size')
    if file_size < 10e6:  # up to 10MB
        return 200000
    elif file_size < 50e6:  # 10MB to 50MB
        return 500000
    elif file_size < 100e6:  # 50MB to 100MB
        return 1000000
    else:  # greater than 100MB
        return 2000000



def process_extracted_text(text):
    words = text.split()
    processed_words = []

    for i, word in enumerate(words):
        if len(word) == 1 and processed_words:
            processed_words[-1] += word  # append the character to the last word
        else:
            processed_words.append(word)

    return ' '.join(processed_words)


def extract_layout_from_pdf_in_batches(pdf_path, batch_size=10):
    """
    Extracts content (text and tables) from a PDF in batches of pages.

    Parameters:
    - pdf_path (str): Path to the PDF file.
    - batch_size (int, optional): Number of pages to process in each batch. Default is 10.

    Yields:
    - dict: Dictionary containing both text content and tables of each page in the current batch.
    """
    
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        
        # Determine the total number of pages in the PDF
        num_pages = len(pdf.pages)
        
        # Iterate over the pages in batches
        for i in range(0, num_pages, batch_size):
            
            # Initialize an empty list to store the content of the current batch of pages
            batch_content = []
            
            # Iterate over each page in the current batch
            for j in range(i, min(i + batch_size, num_pages)):
                page = pdf.pages[j]
                
                # Extract the text and tables from the page
                extracted_text = page.dedupe_chars().extract_text()
                ## For now we stick to the text
                
                # Construct the page content as a dictionary
                page_content = {
                    "text": extracted_text if extracted_text else ""
                }
                
                batch_content.append(page_content)
            
            # Yield the batch content
            yield batch_content





def extract_tables_from_pdf(pdf_path, batch_size=10):
    """
    Extracts tables from a PDF in batches.

    Args:
    - pdf_path (str): Path to the PDF file.
    - batch_size (int): Number of pages to process in a single batch.

    Yields:
    - List of tables extracted from batch of pages.
    """
    logger.info('Starting table extraction...')
    
    tables_batch = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            tables_batch.extend(page.extract_tables())
            # If batch size is reached or it's the last page, yield the tables
            if i % batch_size == 0 or i == total_pages:
                logger.info(f'Extracted tables from page {i-batch_size+1} to {i}')
                yield tables_batch
                tables_batch = []
                
    logger.info('Table extraction finished.')

def extract_text_from_pdf(pdf_path):
    logger.info('Extracting Text From PDF')
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)  # Use PdfReader instead of PdfFileReader
        pdf_text = []
        for page_num in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page_num].extract_text()
            pdf_text.append(text)
    raw_text = "\n".join(pdf_text)
    logger.info('Extracting Text From PDF finished', {len(raw_text)})
    return raw_text


def enhanced_preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Using spaCy NLP pipeline for tokenization and lemmatization
    doc = nlp(text)
    
    # Lemmatization, removing punctuation and stop words
    tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    
    # Joining tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text


# 3. Information Extraction using pre-trained NER model
def extract_pdf_in_chunks_and_store(pdf_path, chunk_size=500000):
    """Extracts text from a PDF, splits it into chunks, and stores the chunks in the database."""
    logger.info('Extracting PDF and Store in Chunks From PDF')
    text = extract_text_from_pdf(pdf_path)
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Store the chunks in the database
    store_file_with_chunks(pdf_path, chunks)
    logger.info('Extracting PDF and Storing in Chunks From PDF finished')


def retrieve_chunks_and_apply_nlp(file_name):
    """Retrieves chunks associated with a file from the database and applies NLP processing."""
    logger.info('Retrieve Chunks and Apply NLP in Chunks From DB')
    chunks = get_chunks_for_file(file_name)
    
    processed_chunks = []
    for chunk in chunks:
        preprocessed_chunk = enhanced_preprocess_text(chunk)
        logger.info(f'Processing chunk: {preprocessed_chunk[:50]}...')  # Log the start of the chunk for reference
        doc = nlp(preprocessed_chunk)
        processed_chunks.append(doc.text)  # Assuming you want to store the processed text; modify as needed
    
    # Store the processed NLP data in the database
    store_processed_text(file_name, processed_chunks)
    logger.info(f'Retrieved {processed_chunks} , Chunks and Applied NLP in Chunks From DB')
    
    return processed_chunks


def extract_pdf_content_and_store(pdf_path):
    """Extracts text and tables from a PDF, then stores the chunks and tables in the database."""
    
    # Log start of PDF extraction
    logger.info(f"Starting extraction of {pdf_path} content and storing in DB.")
    
    # Determine the chunk size for the specific PDF
    chunk_size = determine_chunk_size(pdf_path)
    logger.info(f"Determined chunk size: {chunk_size} characters.")
    
    # Extract content from PDF page by page
    batched_content = extract_layout_from_pdf_in_batches(pdf_path)
    
    page_count = 0  # Keep track of processed pages
    
    for batch in batched_content:
        for content in batch:
            page_count += 1
            text = content.get("text", "").replace('\n', ' ')
            # Store each chunk in the database
            store_file_with_chunks(pdf_path, text)
            logger.info(f"Stored content from page {page_count} of {pdf_path}.")            
            logger.info(f"Processed page {page_count} of text from {pdf_path}.")

    # Log completion of PDF extraction
    logger.info(f"Finished extracting content from {pdf_path} and storing in DB.")





def extract_pdf_tables_and_store(pdf_path):
    """Extracts  tables from a PDF, then stores  and tables in the database."""
    logger.info('Extracting tables {pdf_path} , Content and Storing in DB')

    for batch_index, table_batch in enumerate(extract_tables_from_pdf(pdf_path)):
        for table_index, table in enumerate(table_batch):
        # Convert each table to a DataFrame
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_csv(f"batch_{batch_index}_table_{table_index}.csv", index=False)
            store_extracted_tables(pdf_path, table_batch)
            logger.info(f"Stored tables from batch {batch_index}")

        logger.info(f"Processed batch {batch_index}")




