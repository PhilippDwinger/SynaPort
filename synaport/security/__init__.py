import secrets

def get_key():
    return secrets.token_urlsafe(32)