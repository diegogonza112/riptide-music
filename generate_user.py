import requests
import random
import generate_IDs


def generate_user():
    with open("words", "r") as words:
        WORDS = list(set(words.read().split()))

    joiners = ['.', '_', '-', '']

    return WORDS[random.randint(0, len(WORDS))] + \
           joiners[random.randint(0, 3)] + \
           WORDS[random.randint(0, len(WORDS))] + \
           generate_IDs.generate_id()
