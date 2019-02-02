def search_for_vowels(word: str) -> set:
    """Zwraca zbior samoglosek w danym slowie"""
    vowels = set('aeiou')
    return vowels.intersection(set(word))


def search_for_letters(phrase: str, letters: str = 'aeiou') -> set:
    """Zwraca wspolne litery obu zbiorow"""
    return set(phrase).intersection(set(letters))