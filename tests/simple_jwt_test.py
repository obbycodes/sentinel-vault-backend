from security import create_access_token, decode_access_token


def test_encoding_and_decoding_token():
    token = create_access_token({"username": "alex", "role": "admin"})
    assert token is not None

    valid_data = decode_access_token(token)
    assert valid_data is not None
    assert valid_data["username"] == "alex"
    assert valid_data["role"] == "admin"


def test_tampered_token_returns_none():
    token = create_access_token({"username": "alex", "role": "admin"})
    assert token is not None

    tampered_token = token[:-5]

    invalid_data = decode_access_token(tampered_token)
    assert invalid_data is None
