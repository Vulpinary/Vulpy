import secrets

secret_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY={secret_key}")