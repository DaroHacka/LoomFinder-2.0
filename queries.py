import time
import random
import requests

from random_selection import get_weighted_random_choice

valid_subjects = ["literature", "history", "science", "religion", "philosophy", "art", "education", "politics", "technology", "medicine", "social science", "music", "economics"]

def get_page_number(query_type, date_range=None):
    if query_type in valid_subjects:
        return random.randint(1, 10)
    elif query_type == "date":
        if date_range and " - " in date_range:
            start_date, end_date = map(int, date_range.split(" - "))
            if (end_date - start_date) >= 5:
                return random.randint(1, 10)
    return 1

def build_query_string(title=None, genre=None, anything=None, author=None, subject=None, start_date=None, end_date=None):
    query = ['mediatype:texts', 'language:(english)']
    
    query_type = None
    date_range = None
    if not any([title, genre, anything, author, subject, start_date, end_date]):
        subject = get_weighted_random_choice()
        query_type = subject.lower()
        query.append(f'subject:({subject})')
    else:
        if title:
            query.append(f'title:({title})')
            query_type = "title"
        if genre:
            query.append(f'genre:({genre})')
            query_type = genre.lower()
        if anything:
            query.append(f'({anything})')
            query_type = "anything"
        if author:
            query.append(f'creator:({author})')
            query_type = "author"
        if subject:
            query.append(f'subject:({subject})')
            query_type = subject.lower()
        if start_date and end_date:
            date_range = f"{start_date} - {end_date}"
            query.append(f'date:[{start_date}-01-01 TO {end_date}-12-31]')
            query_type = "date"
    
    page_number = get_page_number(query_type, date_range)
    page_number = max(page_number, 1)
    query_string = " AND ".join(query)
    query_url = f"https://archive.org/advancedsearch.php?q={query_string}&fl[]=identifier&fl[]=title&fl[]=creator&rows=1000&page={page_number}&output=json"
    #print(f"Query URL: {query_url}")  # Debugging print statement

    return query_url

def get_random_book(query_url, retry_limit=5):
    attempt = 0
    while attempt < retry_limit:
        try:
            response = requests.get(query_url)
            if response.status_code == 200:
                books = response.json().get("response", {}).get("docs", [])
                if books:
                    return random.choice(books)
            elif response.status_code == 403:
                print("403 Forbidden. Retrying...")
        except Exception as e:
            print(f"Error: {e}. Retrying...")

        attempt += 1
        time.sleep(1)
    raise Exception("Failed to fetch data after multiple attempts.")
