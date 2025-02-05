import signal
import random

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout):
    def handler(signum, frame):
        raise TimeoutExpired

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        return input(prompt)
    except TimeoutExpired:
        print("\nNo response received. Program will end now.")
        raise TimeoutExpired
    finally:
        signal.alarm(0)

def save_to_file(content, filename="loomfinder_samples.txt"):
    with open(filename, "a") as file:
        file.write(content + "\n\n")

def save_author(author, filename="/home/dan/myscripts/loomfinder_section_code/Authors_list.txt"): # Add your path to LoomFinder to save from anywhere in the terminal
    try:
        with open(filename, "r") as file:
            authors = file.readlines()
        # Check if author is already in the list
        author_names = {name.strip().lower() for name in authors}
        variations = {' '.join(author.split()[::-1]).lower() for author in author_names}
        if author.lower() not in author_names and author.lower() not in variations:
            with open(filename, "a") as file:
                file.write(author + "\n")
    except FileNotFoundError:
        with open(filename, "w") as file:
            file.write(author + "\n")

def get_random_saved_author(filename="Authors_list.txt"):
    try:
        with open(filename, "r") as file:
            authors = file.readlines()
        return random.choice(authors).strip() if authors else None
    except FileNotFoundError:
        return None
