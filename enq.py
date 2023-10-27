import argparse
import logging
import queue
import threading

# Local module imports
from get_data import extract_pdf_content_and_store, retrieve_chunks_and_apply_nlp
from database.db_utils import initialize_database
from logging_util import logger

from topic import generate_topic

# Create a global task queue
task_queue = queue.Queue()

def worker():
    """Worker function to process tasks."""
    while True:
        task, arg = task_queue.get()
        if task == "process_pdf":
            process_pdf(arg)
        elif task == "apply_nlp_on_file":
            apply_nlp_on_file(arg)
        elif task == "generate_topic_from_data":
            generate_topic_from_data(arg)
        elif task == "initialize_db":
            initialize_db()
        task_queue.task_done()

def process_pdf(pdf_path):
    """Process a given PDF by extracting its content and storing it."""
    logger.info(f'Processing PDF: {pdf_path}')
    pdf_text = extract_pdf_content_and_store(pdf_path)
    return pdf_text

def apply_nlp_on_file(file_name):
    """Retrieve chunks of text from a file and apply NLP processing."""
    logger.info(f"Processing PDF for NLP: {file_name}")
    retrieve_chunks_and_apply_nlp(file_name)

def generate_topic_from_data(file_name):
    """Retrieve processed NLP data and generate out of the box topic."""
    logger.info(f"Processing content from NLP(DB) for Generating Topic: {file_name}")
    generate_topic(file_name)

def initialize_db():
    """Initialize the database."""
    initialize_database()
    logger.info("Database initialized successfully!")

def main():
    """Main function to manage command-line interface."""
    parser = argparse.ArgumentParser(description="Operations on PDF and Database.")
    
    # Argument to specify the PDF path for extraction
    parser.add_argument("-e", "--extract", help="Path to the PDF file for extraction.", default=None)
    
    # Argument to specify the PDF file name for NLP processing
    parser.add_argument("-n", "--nlp", help="File name of the PDF for NLP processing.", default=None)

    parser.add_argument("-t", "--topic", help="Generate topic out of the processed NLP data.", default=None)
    
    # Argument to manage the database
    parser.add_argument("-c", "--command", choices=["initDB"], help="Database operation command.", default=None)
    
    args = parser.parse_args()
    
    # Start worker threads
    for _ in range(2):  # Starting 2 worker threads, adjust as needed
        threading.Thread(target=worker, daemon=True).start()

    # Add tasks to the queue based on command-line arguments
    if args.extract:
        task_queue.put(("process_pdf", args.extract))
    
    if args.nlp:
        task_queue.put(("apply_nlp_on_file", args.nlp))

    if args.topic:
        task_queue.put(("generate_topic_from_data", args.topic))
    
    if args.command == "initDB":
        task_queue.put(("initialize_db", None))

    # Block until all tasks are done
    task_queue.join()

if __name__ == "__main__":
    main()
