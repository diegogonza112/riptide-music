import requests
import random
import generate_IDs


def generate_user():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

    response = requests.get(word_site)
    WORDS = response.content.splitlines()

    return WORDS[random.randint(0, len(WORDS))].decode("utf-8") + '_' + \
           WORDS[random.randint(0, len(WORDS))].decode("utf-8") + \
           generate_IDs.generate_id()
