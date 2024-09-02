# Utility functions 
# utils/utils.py

import os
import logging
from datetime import datetime


def ensure_dir_exists(directory):
    """
    Ensure that a directory exists. If it doesn't, create it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")


def log_to_file(log_message, log_file='logs/general.log'):
    """
    Log a message to a specified file.
    """
    ensure_dir_exists(os.path.dirname(log_file))
    with open(log_file, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {log_message}\n")


def sanitize_filename(filename):
    """
    Sanitize a filename by removing or replacing characters that are not safe for file names.
    """
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


def calculate_similarity(str1, str2):
    """
    Calculate a simple similarity score between two strings.
    This could be expanded to use more complex algorithms like Levenshtein distance.
    """
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    return len(set1.intersection(set2)) / max(len(set1), len(set2))


def timestamped_filename(prefix, extension='txt'):
    """
    Generate a filename with a timestamp and a given prefix.
    Example: prefix_20210928_153045.txt
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{sanitize_filename(prefix)}_{timestamp}.{extension}"


def read_file_lines(file_path):
    """
    Read a file and return its lines as a list.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def write_list_to_file(file_path, data_list):
    """
    Write a list of strings to a file, each string on a new line.
    """
    ensure_dir_exists(os.path.dirname(file_path))
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write(f"{item}\n")
    logging.info(f"Data written to file: {file_path}")
