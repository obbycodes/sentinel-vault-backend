# Architecture Decision Record [ADR-002]

> NOTE TO RECRUITERS: I have further amended my ADR structure to better simulate and reflect the collaborative governance of a collaborative environment, additionally, I have provided a retrospective ADR to compensate for production velocity while balancing documentation compliance. While this resulted in individual architectural decisions being bypassed during initial development phases, this allowed me to align my production velocity with my 60-day sprint without compromising system integrity.

#### Title: Retrospective Formalisation of Core Asynchronous Stack & DevSecOps Architecture
* **Status:** Approved (Post-Facto Baseline)
* **Date Requested:** 14 October 2026
* **Date Approved:** 14 October 2026
* **Amends:** None (Supersedes initial undocumented prototype phase)

## Context (Problem, Limitation or Goal)
During the initial high-velocity prototyping phase of the Asset Management & Telemetry System, the core software components and DevSecOps isolation boundaries were implemented rapidly to verify ingestion loops. Consequently, these architectural decisions were not formally catalogued, creating minor technical and documentation debt regarding system provenance and design justification.

## Decisions
We have retrospectively baselined and approved the following architectural snapshot as the production standard for the repository:
1. **API Ingestion Engine:** FastAPI paired with Uvicorn to guarantee non-blocking, asynchronous execution loops (`async/await`) for concurrent telemetry payloads.
2. **Persistence Abstraction:** SQLAlchemy ORM abstraction interacting with an underlying relational database engine.
3. **AppSec Verification Perimeter:** Binding runtime types via strict Pydantic contract validation schemas and hard-gating commits via Bandit SAST and Pytest pipelines.
4. **Docker Infrastructure:** The architecture mandates dropping host root privileges by pinning a dedicated system runtime account (USER appuser) within the build schema.


## Consequences (Pros and Cons)
* **Positive:** Eliminates 100% of historical architectural documentation debt. 
* **Positive:** Establishes an immutable, transparent design baseline that allows future engineering contributors to understand system trade-offs instantly.
* **Positive:** Establishes an airtight zero-trust sandbox boundary; if the application process is somehow compromised via a network vector, the attacker is trapped inside a low-privilege container with no path to elevate permissions on the host system.
* **Positive:** Drastically accelerates onboarding velocity, allowing developers or security assessors to spin up the entire multi-layered application environment via a single, unified orchestration block (`docker-compose up --build -d`) rather than manually tracking system dependencies.
* **Negative:** Requires a post-facto logging footprint, which temporarily impacted documentation velocity during the 60-day development sprint.
* **Negative:** Introduces a migration dependency; local database session managers must eventually be re-engineered and migrated out of localized instances onto clusterised container sessions (such as a multi-container PostgreSQL architecture).
* **Negative:** Heightens configurations risk; any minor mistake in the compose orchestration or port-forwarding blocks can introduce networking vulnerabilities or cause total application runtime failure.
