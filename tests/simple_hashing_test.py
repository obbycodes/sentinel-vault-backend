from security import hash_password, verify_password


def test_hashing():
    RAW_PASSWORD = "TEST_PASSWORD!"
    hashed_password = hash_password(RAW_PASSWORD)

    assert verify_password(RAW_PASSWORD, hashed_password) is True


def test_wrong_hashing():
    RAW_PASSWORD = "TEST_PASSWORD!"
    WRONG_PASSWORD = "FAKE_PASSWORD!"

    hashed_password = hash_password(RAW_PASSWORD)

    assert verify_password(WRONG_PASSWORD, hashed_password) is False
