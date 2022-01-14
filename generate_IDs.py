from random import randint


def generate_id():
    x = randint(1, 200000)
    with open('used_IDs.txt', 'r') as f:
        contents = f.readlines()

    while x in contents:
        x = randint(1, 200000)

    with open('used_IDs.txt', 'a') as f:
        f.write(str(x) + ' ')

    return str(x)


def remove_id(id_):
    with open("used_IDs.txt", "r") as f:
        lines = f.readlines()
    with open("used_IDs.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != id_:
                f.write(line)
