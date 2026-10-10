# Architecture Decision Record [ADR-0001]
### Title: Application & Database Infrastructure
#### Date Requested: 05/09/2026
#### Date Approved: 05/09/2026
#### Status: Approved

<hr color="gray">
<!-- A clear and concise description of what the problem or limitation is. (e.g., "Performance bottlenecks, security concern, vulnerability...") -->

## Problem, limitation or goal
The asset and telemetry system needed a network to establish connections between endpoints, API and the server without performance bottlenecks and low processing speeds, while establishing a database that automatically sanitises SQL inputs to mitigate SQLi attacks. For our API, each endpoint must be able to communicate to the server through a secure HTTP/HTTPS connection to prevent MiTM (Man-In-The-Middle) attacks, data theft and confidentiality breaches.

<!-- A clear and concise description of what you want to happen as a result of this implementation. -->
## Decision (FastAPI)
I decided to implement a RESTful API infrastructure using FastAPI, which is a highly performing, lightweight API built around the Python framework, which processes data payloads in sub-second speeds, often on par with Node.js and Go, additionally, its stateless nature, client-server seperation, cache management and layered systems allows for both client-sided (front-end) and server-sided code (back-end) to be scaled seperately from each other while being able to communicate seamlessly with each other, additionally, its cache management (determining which data is cacheable or not), allows for efficient memory namagement and minimal processing overhead. 

## Decision (SQLalchemy)
I decided to implement an Object Relational Mapper, `SQLalchemyORM`, with an `SQLite` database. This is because SQLalchemy automatically sanitises inputs without having to manually sanitise them, easily mitigating against SQLi attacks, this is done using OOP (Object Oriented Programming), representing tables as classes, inheriting from a Base class template, mitigating the use of raw SQL queries and strings. It also abstracts many database dialects such as `PostgreSQL`, `MySQL`, `SQLite` and `SQL Server` without rewriting queries.

<!-- Any alternative solutions or features you've thought about, and why this is the ultimate choice. -->
## Pros & Cons
### Pros (FastAPI)
* FastAPI has speeds that nearly matches Node.js and Go, ultimately serving as the best option for our Python framework.
* Layered systems allow for client-server interaction seamlessly while evolving on its own.
* Efficient memory management by only cacheing specific data, rather than all data.
* Includes self-documenting capabilities from type hints in order for developers or testers to understand our software's behaviour.
* Includes built-in data validation using `Pydantic` which allows for security at the network layer.
* FastAPI can handle concurrency with minimal processing overhead while achieving sub-second performance speeds due to its asynchronous architecture.
* FastAPI can inject various dependency functions, allowing for efficient database management and authentication methods such as JWT tokenisation, RBAC (Role Based Access Control) and user registration/login.

### Pros (SQLalchemyORM)
* `sqlalchemy.orm` allows flexibility by tightening Python classes to database tables, columns and values. This allows for tables and relationships to be mapped seamlessly using classes, objects, inheritance, primary and foreign keys.
* `sqlalchemy.orm` abstracts database dialects such as `PostgreSQL`, `MySQL`, `SQLite` and `SQL Server`, removing the requirement to overwrite queries if you change database dialects, giving flexbility.
* It actively protects against SQLi (SQL injection attacks) by automatically sanitising outputs when using ORMs as they treat query **parameters** as safe variables rather than string concatenations used from raw SQL (string concatenation is bad practise in raw SQL if done improperly, you would have to manually parameterise data such as `"SELECT * FROM users WHERE email = %s"`.)
* It maps schemas into clean Python data structures, which allows complex data validation builds before data hits the database. This is a great advantage since FastAPI utilises a built-in data validation package `Pydantic`, which means we can implement data validation schemas seamlessly.

### Cons (FastAPI)
* `async/await` event handlers can freeze FastAPI's event loop under improperly implemented asynchronous events, which can lead to massive performance bottlenecks.
* FastAPI has no standardised structure for for databases or authentication, production-level softwares must work around this by implementing their own self-configured structure which can cause "sphagetti code" if we are not careful. (Involves manually configuring database connection thread management, stateless authentication etc.)
* Despite FastAPI's powerful dependency injections, on a large-scale, thousands of dependency functions causes debugging, testing and maintainability bottlenecks, which increases code complexity and makes sufficient code coverage less achievable. 

### Cons (SQLalchemyORM)
* Because `sqlalchemy.orm` automatically turns SQL database rows/tables into heavy Python objects, the processing overhead required to do so ends up becoming an "**abstraction penalty"**. This becomes a notable issue as the project scales, for example 10,000 queries would end up taking a significant amount of processing overhead.
* `sqlalchemy.orm` relies heavily on explicit primary keys and relational constraints to track an object's state. ORMs can return inconsistent results if we decided to hook it to a previous legacy system we developed months ago, as our new system would have different primary keys (IDs unique to each column) and their own respective relational constraints, leading to heavy incompatibility.
* If not managed properly, qeuries will be fetched sequentially one-by-one as `sqlalchemy.orm`, this can have severe performance bottlenecks on large-scale production software, as more queries pile up.
* While it does create validation schemas as a Python object, more modern ORMs such as `SQLModel` is more compatible with Pydantic than `sqlalchemy`. It requires explicit configurations to achieve the same result.

<!-- Add any other context, mockup designs, architecture diagrams or user flows here. -->
![Architecture diagram](.github/assets/ADR0001.png)


