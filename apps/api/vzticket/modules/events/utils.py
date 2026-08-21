import re
import unicodedata


def slugify_city(value: str) -> str:
    value = value.strip().lower()
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r'[^a-z0-9]+', '-', value)

    return value.strip('-')
