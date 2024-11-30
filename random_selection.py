import time
import random
import re
import time
import requests
from categories import literature_genres, default_genres_subjects

def get_random_text_segment(book, retry_limit=5):
    attempt = 0
    while attempt < retry_limit:
        metadata_url = f"https://archive.org/metadata/{book['identifier']}"
        response = requests.get(metadata_url)
        if response.status_code != 200:
            print(f"Failed to fetch metadata: {response.status_code}. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        metadata = response.json()
        files = metadata.get("files", [])
        txt_files = [file for file in files if file.get("name", "").endswith(".txt")]

        if not txt_files:
            print("No text file available for this book. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        text_url = f"https://archive.org/download/{book['identifier']}/{txt_files[0]['name']}"
        response = requests.get(text_url)
        if response.status_code != 200:
            print(f"Failed to fetch book content: {response.status_code}. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        text = response.text
        words = re.findall(r'\S+', text)
        num_words = 200
        if len(words) < num_words:
            print("The book doesn't contain enough words. Retrying...")
            attempt += 1
            time.sleep(1)
            continue

        start = random.randint(0, len(words) - num_words)
        segment = words[start:start + num_words]

        end_index = start + num_words
        while end_index < len(words) and not words[end_index].endswith('.'):
            segment.append(words[end_index])
            end_index += 1

        author = book.get('creator', 'Unknown Author')
        return book['title'], author, ' '.join(segment)
    raise Exception("Failed to fetch valid text segment after multiple attempts.")

def get_weighted_random_choice():
    weights = [0.8 if genre in literature_genres else 0.2 for genre in default_genres_subjects]
    return random.choices(default_genres_subjects, weights=weights, k=1)[0]
