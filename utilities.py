import signal

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
    finally:
        signal.alarm(0)

def save_to_file(content, filename="loomfinder_samples.txt"):
    with open(filename, "a") as file:
        file.write(content + "\n\n")

def save_author(author, filename="Authors_list.txt"):
    with open(filename, "a") as file:
        file.write(author + "\n")

def get_random_saved_author(filename="Authors_list.txt"):
    try:
        with open(filename, "r") as file:
            authors = file.readlines()
        return random.choice(authors).strip() if authors else None
    except FileNotFoundError:
        return None
