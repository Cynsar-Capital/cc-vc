Global North vs. Global South Venture Financial Model Visualization Tool

## Overview

This project aims to provide visualization and inferences towards the Global North Venture Financial Model versus the Global South Venture Financial Model. By distilling data from various reliable sources, the tool uncovers insights into industry practices, focusing on early-stage ventures.

## Why?
Our objective is to validate hypotheses regarding industry practices and understand the disparities in early-stage venture attraction between the Global North and Global South.

## Features

1. Data Extraction: Extract data from various file formats, with a particular focus on PDF files.
2. Topic Generation: Utilize advanced algorithms to generate topics from the extracted data.
3. Data Visualization: Visual representations of data for better clarity and understanding.
4. Inferences: Draw conclusions using various statistical tools to determine current industry trends.

## Project Structure

- enq.py: Handles task queuing and threading operations.
- get_data.py: Responsible for extracting data from files, especially PDFs, and storing them in a database.
- logging_util.py: Centralized logging configuration for the project.
- topic.py: Manages topic generation, embedding extraction, and clustering of data.
- utility.py: Houses utility functions, including data extraction from CSV or Excel files.
- db_utils.py: Contains database utility functions, such as initialization and data storage.
- models.py: Defines the database structure using SQLAlchemy, listing all the table models.


## Usage

1. Begin by initializing the database using initialize_database() from the db_utils.py file.
2. Extract data from your desired file format. For PDFs, utilize functions within the get_data.py file.
3. Use the topic generation functionalities in the topic.py file to derive topics from the extracted data.
4. For additional utility functions, refer to utility.py.
5. All tasks can be queued using the functionalities provided in the enq.py file.

## Dependencies

```
PyPDF2
spaCy
pdfplumber
gensim
TensorFlow
SQLAlchemy

```
... and more.
Ensure all dependencies are installed before running any scripts. like `pip install -r requirements.txt`


## Conclusion

By leveraging this tool, stakeholders can gain insights into the financial models of ventures in both the Global North and Global South, enabling informed decision-making. We encourage feedback and contributions to make this tool even more effective in the future.