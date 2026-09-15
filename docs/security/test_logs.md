<style>
    .non-threat {
        color: grey
    }

    .low {
    color: green
    }

    .medium {
    color: orange
    }

    .high {
    color: red
    }

    .critical {
    color: rgb(163, 0, 0)
    }
</style>

# Testing Logs

| Test # 	| Date 	| Description / Module 	| Expected Result 	| Actual Result 	| Outcome 	| Test File (if applicable) 	| Commit link 	| Bug/fix reference 	|
|---	|---	|---	|---	|---	|---	|---	|---	|---	|
| 1 	|  	| FastAPI setup with root app information and health check endpoint (main) 	| Both endpoints return `200 OK` and response body. 	| Both endpoints return 200 OK and response body. 	| Pass 	|  	|  	|  	|
| 2 	|  	| SQLalchemyORM database setup (database) 	| Executing health check's route logic must return `200 OK` and `sentinel-vault.db` must be created. 	| Error while creating database (500 Internal Server Error), the database was configured and created properly, but was not connected to FastAPI. 	| Fail 	|  	|  	|  	|
| 3 	|  	| SQLalchemyORM database setup (database) 	| Executing health check's route logic must return `200 OK` and `sentinel-vault.db` must be created. 	| Executing health check's route logic returned 200 OK and sentinel-vault.db was created. 	| Pass 	|  	|  	|  	|
| 4 	|  	| Virtual environment setup for passwordlib and dependency isolation (security) 	| Git bash CLI must return (venv) indicating the virtual enviroment is created 	| Git bash CLI returned (venv) indicating the virtual enviroment is created 	| Pass 	|  	|  	|  	|
| 5 	|  	| Password hashing helper module (security) 	| Entering a plaintext password through the module must hash including the salt $argon2id$. 	| Entering a plaintext password through the module heshes including the salt $argon2id$. 	| Pass 	| simple_hashing_test.py 	|  	|  	|
| 6 	|  	| Password verification function (security) 	| Entering the same plaintext password through verification must return True, and incorrect/mistmatching return False. 	| Entering the same plaintext password through verification  returns True, and incorrect/mistmatching returns False. 	| Pass 	| simple_hashing_test.py 	|  	|  	|
| 7 	|  	| Stateless authentication & JWT signing - creating a token (security) 	| Created and signed token must be returned in a token format hiding containing claims, secret key and algorithm using the test file: `simple_jwt_test.py` 	| Created and signed token returned a token format hiding containing claims, secret key and algorithm using the test file: simple_jwt_test.py 	| Pass 	| simple_jwt_test.py 	|  	|  	|
| 8 	|  	| Stateless authentication & JWT signing - decoding a token (security) 	| Decoded token must return a JSON response body containing user claims and expiry using the secret key and algorithm. 	| Decoded token did not return a JSON response body containing user claims and expiry using the secret key and algorithm, returned None. 	| Fail 	| simple_jwt_test.py 	|  	|  	|
| 9 	|  	| Stateless authentication & JWT signing - decoding a token (security) 	| Decoded token must return a JSON response body containing user claims and expiry using the secret key and algorithm. 	| Decoded token did return a JSON response body containing user claims and expiry using the secret key and algorithm. 	| Pass 	| simple_jwt_test.py 	|  	|  	|
| 10 	|  	| Stateless authentication & JWT signing - handling a tampered token (security) 	| Decoded tampered token must return None and error `401 Unauthorised`. 	| Decoded tampered token did return None and error 401 unauthorised. 	| Pass 	| simple_jwt_test.py  	|  	|  	|
| 11 	|  	| Registration endpoint setup - Creating user's record (main) 	| Must return `201 Created` with a new record containing the `values, id, username, email, hashed_password` and `role` where role's default value is `"Viewer"`, and their values matched entered information. 	| Returned 201 Created with a new record containing the values, id, username, email, hashed_password and role where role's default value is "Viewer", and their values matched entered information. 	| Pass 	|  	|  	|  	|
| 12 	|  	| Login endpoint setup (main) 	| Must return `401 Unauthorised` if username or password is incorrect, and `200 OK` if both is a database match. 	| Returned 401 Unauthorised if username or password is incorrect, and 200 OK if both is a database match. 	| Pass 	|  	|  	|  	|
| 13 	|  	| Registration endpoint setup - Password hashing verification (main) 	| Upon registration, must return `201 Created`, with their hashed_password in a hashed format and salt `$argon2id$` 	| Upon registration, returned 201 Created, with their hashed_password in a hashed format and salt $argon2id$ 	| Pass 	|  	|  	|  	|
| 14 	|  	| Login endpoint setup - Token signing & attachment (main) 	| User must be granted a token that lasts 30 minutes (expiry), with their tokenised string. 	| User is granted a token that lasts 30 minutes (expiry), with their tokenised string. 	| Pass 	|  	|  	|  	|
| 15 	|  	| Login endpoint setup - Token expiry test (main) 	| `401 Unauthorised` must be returned if their token has been active for more than 30 minutes. 	| 401 Unauthorised was returned if their token has been active for more than 30 minutes. 	| Pass 	|  	|  	|  	|
| 16 	|  	| Login endpoint setup - Mismatched or tampered token (main) 	| `401 Unauthorised` if their token has been tampered with or mismatched. 	| 401 Unauthorised was returned as expected. 	| Pass 	|  	|  	|  	|
| 17 	|  	| Login & Session cookie creation (main) 	| Created cookie shows on the network tab named `"access_token"` and JWT token. Must be HTTP only and `same_site="lax"` 	| Created cookie shows on the network tab named "access_token" and JWT token. Is HTTP only and same_site="lax" as expected. 	| Pass 	|  	|  	|  	|
| 18 	|  	| Login & Session cookie authentication module (security) 	| Returns error 401 Unauthorised if cookie is not valid, or user is not authenticated. (no cookie present) 	| Returned error 401 Unauthorised if cookie is not valid, or user is not authenticated as expected. (no cookie present) 	| Pass 	|  	|  	|  	|
| 19 	|  	| Create protected endpoint placeholders - System Reset (main) 	| Returns JSON response body `{"message": "System reset successful"}` if logged in user has allowed role: `"Admin"`. 	| Returned JSON response body {"message": "System reset successful"} if logged in user has allowed role: "Admin". 	| Pass 	|  	|  	|  	|
| 20 	|  	| Create protected endpoint placeholders - System Reset RBAC Test (main) 	| Returns `403 Forbidden` if user does not have allowed role: `"Admin"`. 	| Returned JSON response body {"message": "System reset successful"}. 	| Fail 	|  	|  	|  	|
| 21 	|  	| Create protected endpoint placeholders - System Reset RBAC Test (main) 	| Returns `403 Forbidden` if user does not have allowed role: `"Admin"`. 	| Returned 403 Forbidden if user does not have allowed role: "Admin". 	| Pass 	|  	|  	|  	|
| 22 	|  	| Verify that the refactored security module retains functional parity with legacy security module (security) 	| Executing endpoints (register, login) with functions from the refactored security module will function as normal.  	| Executed endpoints (register, login) with functions and encountered 500 Internal Server Error due to incorrect arguments using the joserfc encoding and decoding function. 	| Fail 	|  	|  	|  	|
| 23 	|  	| Verify that the refactored security module retains functional parity with legacy security module (security) 	| Executing endpoints (register, login) with functions from the refactored security module will function as normal.  	| Executed endpoints (register, login) with functions from the refactored security module functions as normal.  	| Pass 	|  	|  	|  	|
| 24 	|  	| Audit logging system setup & api/telemetry/logs endpoint (security) 	| Upon running `api/telemetry/logs` endpoint, it must return an empty JSON response body. 	| Upon running api/telemetry/logs endpoint, it returned an empty JSON response body. 	| Pass 	|  	|  	|  	|
| 25 	|  	| Audit logging system setup - protecting endpoint using RBAC (security) 	| Protected endpoint must only allow users with roles Analyst and Admin with `200 OK` 	| Protected endpoint only allows users with roles Analyst and Admin with 200 OK 	| Pass 	|  	|  	|  	|
| 26 	|  	| Audit logging system setup - restricting unauthorised users (security) 	| Protected endpoint must return `403 Forbidden` if a Viewer attempts to view them. 	| Protected endpoint returned 403 Forbidden if a Viewer attempts to view them. 	| Pass 	|  	|  	|  	|
| 27 	|  	| Rate limiting system setup - Protecting endpoints from brute-force (main) 	| Rate limited endpoints return `200 OK`/`201 Created` if less than 5 requests were made in a minute. 	| Rate limited endpoints returns 200 OK/201 Created if less than 5 requests were made in a minute as expected. 	| Pass 	|  	|  	|  	|
| 28 	|  	| Rate limiting system setup - Limit testing (main) 	| Rate limited endpoints return `429 Too Many Requests` and blocks the user's connection if exceeds 5 requests per minute. 	| Rate limited endpoints returned 429 Too Many Requests and blocks the user's connection if exceeds 5 requests per minute as expected. 	| Pass 	|  	|  	|  	|
| 29 	|  	| HTTP security headers middleware setup - (main) 	| Specified headers must display in every response header of each endpoint. 	| Specified headers display in every response header of each endpoint. 	| Pass 	|  	|  	|  	|
| 30 	|  	| Telemetry log submission module (main) 	| Entry must be saved in the database with specified `values, device_id, cpu_usage, memory_usage` and status default to `"NORMAL"`. 	| Entry was saved in the database with specified values, device_id, cpu_usage, memory_usage and status default to "NORMAL" as expected 	| Pass 	|  	|  	|  	|
| 31 	|  	| Data validation sub-module: Valid data (main) 	| Each data validation constraint must be passed and run the route logic. 	| Each data validation constraint has passed route logic has been ran. 	| Pass 	|  	|  	|  	|
| 32 	|  	| Data validation sub-module: Extreme data (main) 	| Each data validation constraint must be passed and run the route logic. 	| Each data validation constraint has passed route logic has been ran. 	| Pass 	|  	|  	|  	|
| 33 	|  	| Data validation sub-module: Invalid data (main) 	| The server must return `422 Unprocessable Entity` due to a data validation rule violation. 	| The server returns 422 Unprocessable Entity due to a data validation rule violation. 	| Pass 	|  	|  	|  	|
| 34 	|  	| Telemetry pagination module setup (main) 	| Server returns a filtered JSON response body from the database with a limit of 10 logs in one response (example) and an offset of 2 (starts 2 logs later) 	| Server returned a filtered JSON response body from the database with a limit of 10 logs in one response (example) and an offset of 2 (starts 2 logs later) 	| Pass 	|  	|  	|  	|
| 35 	|  	| Anomaly detection module setup (main) 	| Extreme data values when submitting a log must trigger logging system with the alert `"CRITICAL_ANOMALY"` 	| Extreme data values when submitting a log triggered logging system with the alert "CRITICAL_ANOMALY" 	| Pass 	|  	|  	|  	|
| 36 	| 14/09/2026 21:43	| Telemetry aggregation & analytics dashboard module (main) 	| Route must return number of devices and anomalies, including average CPU and RAM usage in a JSON response body.	| Route returned number of devices and anomalies, including average CPU and RAM usage in a JSON response body as expected. 	| Pass 	|  	|  	|  	|
| 37 	| 14/09/2026 22:26 	| Pytest Execution Pipeline module (test_auth) 	| Pytest CLI should return 2 passed tests within the `test_auth` module. 	| Error: `httpx2` must be installed to run pytest on `test_auth.py` 	| Fail 	|  	|  	|  	|
| 38 	| 14/09/2026 22:33 	| Pytest Execution Pipeline module (test_auth) 	| Pytest CLI should return 2 passed tests within the `test_auth` module. 	| Error: `ModuleNotFoundError`, database could not be imported. 	| Fail 	|  	|  	|  	|
| 39 	| 14/09/2026 22:51 	| Pytest Execution Pipeline module (test_auth) 	| Pytest CLI should return 2 passed tests within the `test_auth` module. 	| Error: `OperationalError`, `sqlalchemy` could not find table `users`. (x2)	| Fail 	|  	|  	|  	|
| 40 	| 14/09/2026 23:27 	| Pytest Execution Pipeline module (test_auth) 	| Pytest CLI should return 2 passed tests within the `test_auth` module. 	| Pytest CLI returned 2 passed tests within the `test_auth` module as expected. 	| Pass 	|  	|  	|  	|  	|
| 41 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 42 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 43 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 44 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 45 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 46 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 47 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 48 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 49 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 50 	|  	|  	|  	|  	|  	|  	|  	|  	|
| 51 	|  	|  	|  	|  	|  	|  	|  	|  	|

## Fix Logs
**All failures go here.**
### Key<br>
**Catastrophic Failure**: Multiple bugs within the program causes it to fail.<br>**Failure**: A bug within the program causes it to fail.<br>**Threat**: A block of code, package used or module poses a serious security risk.<br>**Vulnerability**: A block of code, package used or module poses a medium or lower security risk.<br>**Risk**: Any other non-security risk that involves bad practise or impacts software quality negatively.<br>

| Problem | Date & Time | Description | Fix | 
| :---: | :--- | :--- | :--- |
| **1** | 20/08/26<br>18:33 | **Failure (Human Error):** Attempted to run the server using `uvicorn main:app` –reload returns a command not found error as it was not in the correct directory to find the package and command `uvicorn`. | Added `python -m` in the beginning in order to locate the module and execute it as a main code.<br><br>**Later fix (29/08):**<br>*cd src -> uvicorn main:app --reload* |
| **2** | 21/08/26<br>17:02 | **Failure (Hallucination/Human Error):** Attempted to import base class and session maker functionality from a deprecated module `sqlalchemy.ext.declarative`. This took place because I accidentally accepted an auto-suggesstion from Cursor's built-in agent. | Feature was deprecated, replaced imported module with new module, `sqlalchemy.orm`. |
| **3** | 23/08/26 –<br>25/08/26<br>22:42 | **Risk (Scope creep):** Attempted to implement JWT stateless authentication with AWS KMS, which is an enterprise-level scope, and is outside my current ability. | Manually programmed locally handled JWT token management and locking it into a HTTP-only cookie. |
| **4** | 28/08/26<br>14:01 | **Risk (Human Error):** Coded endpoints such as the login and register endpoint without documenting potential errors inside the endpoint metadata (`api/login`, `api/register`)<br><br>*Issue raised by SonarQube Cloud – AI agent code verifier*<br><br>This is a high risk, as any consumers or developers using the API will find it unreliable due to undocumented errors. | Manually programmed both endpoints to have errors documented, including the error description and expected content (response body). |
| **5** | 29/08/26<br>12:35 | **Threat (Miss):** Only implemented rate limiting to the login endpoint, which allows attackers to target unprotected endpoints to carry out DDoS and DoS attacks. Rate-limits should be applied to all endpoints, but not the exact same rate limit. | Applied different rate limits to endpoints<br>Dashboard + Profile: 10/min<br>Metrics: 7/min<br>Logs: 5/min<br>**Later fix (31/08)**: Added a global rate-limit to all endpoints and specified tighter rate-limits to security-sensitive and resource heavy endpoints. |
| **6** | <span style="color:red">Unresolved<span> | **Threat (Miss):** Did not account for HTTPS when assigning HTTP-only cookies, it must have “secure=True” to only allow cookies through a secure TLS connection. | No fix yet. |
| **7** | 01/09/2026 22:25 | **Failure (Human Error)**: Attempted to use a class “Field” for telemetry pagination function from a package that was not imported. | Imported the class `Field` from Pydantic. |
| **8** | 09/09/2026 18:18 | **Failure (Human Error):** Did not setup the connection thread between FastAPI and the configured database. | Correctly configured the connection thread between FastAPI and the configured database, binding it to the session engine. |
| **9** | 09/09/2026 22:34 | **Failure (Human Error):** Used incorrect paramaters/arguements for `josertc` encoding and decoding function while trying to refactor JWT signing module and replacing deprecated package, `python-jose`. | `josertc` has paramaters `(claims, secret key, algorithm)` with the additional claims validation instead of `python-jose`'s `(payload, key, algorithm)` without claims validation. |
| **10** | 10/09/2026 22:34 | **Failure (Human Error):** Dependency function `RoleChecker` (now known as `allow_roles`) iterated indefinitely due to FastAPI's handling of dependency functions from classes. This was due to an improperly refactored `RoleChecker` dependency function, where there was another dependency `get_current_user`. | Changed `RoleChecker` to `allow_roles` and changed it from an object to a function so that FastAPI doesn't indefinitely iterate through the objects. |
| **11** | 01/09/2026 22:34 | **Failure (Human Error):** Attempted to use Pydantic’s `Field()` for validation types and field arguments rather than FastAPI’s `Query()`. | Used `Annotated[]` and `Query()` for FastAPI to understand validation types and field arguments. |
| **12** | 14/09/2026 22:26 | **Failure (Human Error):** `httpx2` must be installed to run pytest on `test_auth`. Attempted to run `pytest` without it. | Installed required package `httpx2`. |
| **13** | 14/09/2026 22:33 | **Failure (Human Error):** `ModuleNotFoundError`, database could not be found because the test database setup was configured incorrectly. |  Imported `Base` from `sqlalchemy` and adjusted code syntax to properly configure the database. |
| **14** | 14/09/2026 22:51 | **Failure (Human Error):** `OperationalError`, `sqlalchemy` could not find table `users`. |  The wrong `Base` class was imported, since it was imported from `sqlalchemy` instead of `database` module, it created a clean, new database template, imported `Base` from `database` module instead, additionally, imported `models` module so that `sqlalchemy` could potentially detect it. |
| **15** | 14/09/2026 22:52 | **Failure (Human Error):** `OperationalError`, `sqlalchemy` could not find table `users`. (**x2**) | `sqlalchemy` by default setup a new connection thread to a new and refreshed database that was later created. Fixed this by forcing `sqlalchemy` to connect all threads to the same database using `StaticPool`. |

