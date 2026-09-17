import sys

from security import hash_password, verify_password

RAW_PASSWORD = str(input("Enter a password: "))
hashed_password = hash_password(RAW_PASSWORD)

print(f"Hashed password: {hashed_password}")
print(f"Verifying password: {verify_password(RAW_PASSWORD, hashed_password)}")

wrong_password = str(input("Now enter a wrong password: "))
print(f"Verifying wrong password: {verify_password(wrong_password, hashed_password)}")
print("[TEST ENDED] Exiting terminal.")
print("-" * 20)

sys.exit()
