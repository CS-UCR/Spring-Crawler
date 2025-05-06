from simhash import Simhash
from bs4 import BeautifulSoup

seen_hashes = []

SIMHASH_THRESHOLD = 3

def get_text_from_html(content: bytes) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def comput_simhash(text: str) -> Simhash:
    return Simhash(text.split())

def is_duplicate(content: bytes) -> bool:
    text = get_text_from_html(content)
    new_hash = comput_simhash(text)

    for existing_hash in seen_hashes:
        if new_hash.distance(existing_hash) <= SIMHASH_THRESHOLD:
            return True
    
    seen_hashes.append(new_hash)
    return False