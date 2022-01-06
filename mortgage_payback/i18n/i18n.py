import functools
import os
import yaml

LOCALE = "en"


@functools.lru_cache
def get_dictionary(locale: str):
    with open(os.path.join(os.path.dirname(__file__), f"{locale}.yaml"), "r") as stream:
        return yaml.safe_load(stream)


def get_text(name: str):
    dictionary = get_dictionary(LOCALE)
    return dictionary[name]


def set_locale(locale: str):
    global LOCALE
    LOCALE = locale
