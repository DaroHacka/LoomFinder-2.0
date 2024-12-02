#!/usr/bin/env python3

import argparse
from queries import build_query_string, get_random_book
from parsing import parse_parameters
from random_selection import get_random_text_segment
from utilities import save_to_file, save_author, input_with_timeout, TimeoutExpired, get_random_saved_author
from categories import literature_genres, other_subjects
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoomFinder: A versatile text searching tool for Archive.org. Imagine entering a library containing over 28 million documents, you can see books everywhere around you, however you feel that the most inspiring books are in that particular direction, so you pick one up and read a random chapter. This is how LoomFinder works. Have a nice journey!")
    parser.add_argument('params', nargs='*', help='Search parameters: [t:title] [g:genre] [x:anything] [a:author] [s:subject] [d:date]')
    parser.add_argument('--save', action='store_true', help='Save the output to a file')
    parser.add_argument('--list-genres', action='store_true', help='List available genres')
    parser.add_argument('--list-subjects', action='store_true', help='List available subjects')
    args = parser.parse_args()

    # Check for the prose positional argument
    prose_mode = False
    if 'prose' in args.params:
        prose_mode = True
        args.params.remove('prose')

    # List genres or subjects if requested
    if args.list_genres:
        print("Available genres:")
        for genre in literature_genres:
            print(f"- {genre}")
        sys.exit(0)

    if args.list_subjects:
        print("Available subjects:")
        for subject in other_subjects:
            print(f"- {subject}")
        sys.exit(0)

    params = args.params

    # Handling prose mode
    if prose_mode:
        author = get_random_saved_author()
        if not author:
            print("No authors available in the saved list.")
            sys.exit(0)
        params = [f"a:{author}"]

    title, genre, anything, author, subject, date = parse_parameters(params)
    start_date, end_date = None, None
    if date and '-' in date:
        start_date, end_date = date.split('-')

    query_url = build_query_string(title=title, genre=genre, anything=anything, author=author, subject=subject, start_date=start_date, end_date=end_date)

    # Ensure the query URL is printed
    print(f"Query URL: {query_url}")

    try:
        book = get_random_book(query_url)
        title, author, text_segment = get_random_text_segment(book)
        output = f"Book Title: {title}\nAuthor: {author}\nRandom Text Segment: {text_segment}"
        print(output)

        if args.save:
            save_to_file(output)
            print("Output saved to file.")

        # Only save the author's name if not already in the list and not in prose mode
        if not prose_mode and author.lower() != "unknown author":
            try:
                save_author_choice = input_with_timeout("Do you want to save the author's name? (yes/y/no/n): ", 10) # Increase the time, e.g., from 10 seconds to 60 seconds, if you need more time to read the extract and decide whether to save the author.
                if save_author_choice and save_author_choice.lower() in ["yes", "y"]:
                    save_author(author)
                    print("Author's name saved.")
                elif save_author_choice and save_author_choice.lower() in ["no", "n"]:
                    print("Author's name not saved.")
            except TimeoutExpired:
                print("Bye")

    except Exception as e:
        print(e)
