import bleach

def sanitize_and_validate_text(text):
    return bleach.clean(text, strip=True)