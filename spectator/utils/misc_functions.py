import random


def get_random_item(items):
    return random.choice(items)


def sort_list(items, key, descending=True):
    return sorted(items, key=lambda x: x[key], reverse=descending)
