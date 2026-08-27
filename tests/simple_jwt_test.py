from src.security import create_access_token, decode_access_token

token = create_access_token({"username": "alex", "role": "admin"})
print(f"Generated: {token}")

valid_data = decode_access_token(token)
print(f"\nDecoded Data: {valid_data}")

tampered_token = token[:-5]
invalid_data = decode_access_token(tampered_token)
print(f"\nTampered token result (must Fail): {invalid_data}")




