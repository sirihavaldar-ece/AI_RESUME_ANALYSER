"""Small text-cleaning helpers used before skill matching."""

import re


def clean_text(text: str) -> str:
    """Lowercase text, keep useful programming symbols, and tidy whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
