import re
from unicodedata import normalize


def bleach(given_text: str) -> str:
    extra_space = normalize('NFKD', given_text)
    return extra_space.replace('\n', '')


def fix_last_dharko(given_text: str) -> str:
    dharko = '।'
    matches = re.finditer(dharko, given_text)
    all_dharkos = [match.start() for match in matches]
    index_of_last_dharko = max(all_dharkos)
    # also include the dharko after slicing the given text
    fixed_text = given_text[:index_of_last_dharko+1]
    return fixed_text
