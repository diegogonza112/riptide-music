from random import randint


def generate_id():
    x = randint(1, 200000)
    return str(x)
