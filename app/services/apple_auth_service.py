from jose import jwt, jwk
from jose.utils import base64url_decode
import requests

class AppleJWTVerifier:
    APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"

    @staticmethod
    def verify_identity_token(identity_token: str, client_id: str) -> str:
        apple_keys = requests.get(AppleJWTVerifier.APPLE_KEYS_URL).json()["keys"]
        header = jwt.get_unverified_header(identity_token)
        key_data = next(k for k in apple_keys if k["kid"] == header["kid"])
        public_key = jwk.construct(key_data)

        message, encoded_signature = identity_token.rsplit(".", 1)
        decoded_signature = base64url_decode(encoded_signature.encode())

        if not public_key.verify(message.encode(), decoded_signature):
            raise ValueError("Invalid signature")

        payload = jwt.decode(identity_token, public_key, algorithms=[header["alg"]], audience=client_id)
        return payload["sub"]
