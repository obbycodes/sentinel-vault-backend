# SentinelVault 🛡️

A hybrid cybersecurity and software engineering vault system designed for stateless, cryptographically signed token verification and secure data persistence using SQLAlchemy ORM.

## 📌 Architecture Overview
SentinelVault executes token generation, signing, and verification natively in Python. Secret keys are injected dynamically at runtime via environment variables—ensuring zero credential hardcoding—while SQLAlchemy ORM provides parameterized database interactions and strong type enforcement.

### Key Security & Engineering Features
* **Stateless Cryptographic Signing**: Native Python implementation for signing and verifying tokens without external cloud key management dependencies.
* **SQLAlchemy ORM Layer**: Safe data persistence utilizing parameterized queries to eliminate SQL injection attacks.
* **Strict Credential Hygiene**: Runtime configuration enforced via localized `.env` files excluded from version control.
* **Automated Testing Suite**: Full unit and integration coverage validating signing keys, token expirations, and database transactions.

---

## 🚀 Quick Start

### Prerequisites
* Python 3.11+

### Setup
1. **Clone Repository:**
   ```bash
   git clone [https://github.com/your-username/SentinelVault.git](https://github.com/your-username/SentinelVault.git)
   cd SentinelVault
