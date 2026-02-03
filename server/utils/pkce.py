import secrets
import string
import hashlib
import base64


"""
Based on the Spotify authentication flow with PKCE:
https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow

And the PKCE standard:
https://datatracker.ietf.org/doc/html/rfc7636#section-4.1
"""


# Creates a random 128 character sting to be the code verifier, including letters, digits, underscores, periods, hyphens, or tildes
def generate_code_verifier() -> str:
    allowed_chars = string.ascii_letters + string.digits + "-._~"
    verifier = "".join(secrets.choice(allowed_chars) for _ in range(128))
    return verifier


# Hashes the generated verifier using SHA-256 to be the code challenge
def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii")
    return challenge.rstrip("=")


# Wrapper to generate PKCE verifier and challenge pair
def get_pkce() -> tuple[str, str]:
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    return code_verifier, code_challenge
