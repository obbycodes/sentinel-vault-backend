# Threat Model

### This project uses a competent-based STRIDE Mitigation strategy, which means the system is analysed based on the attacker's competency. This model analyses threats considering the attacker has moderate competency.

• **Spoofing: (Unmitigated)** Due to the HTTPS flag being disabled (False), an attacker can perform a Man-in-the-Middle (MiTM) attack to capture unencrypted authentication tokens in transit. They can then use these stolen credentials to impersonate legitimate devices or users when communicating with the FastAPI backend.

• **Tampering: (Unmitigated)** Attackers can exploit logical vulnerabilities within third-party FastAPI routers or flawed validation logic to manipulate structural API payloads, tamper with database records, or alter JWT claims.

• **Repudiation: (Unmitigated)** Attackers may attempt to delete or alter telemetry ingestion logs (removing infection anomalies, login failures, or system events) to hide their tracks. This can be mitigated by streaming logs in real-time to an immutable, centralized logging platform that the FastAPI container cannot alter or delete.

• **Information Disclosure: (Mitigated)** Attackers can map out system architecture, backend dependencies, and database schemas by forcing unhandled exceptions that return verbose 500 Internal Server Error stack traces or specific try/except messages. This is mitigated by disabling FastAPI debug mode and returning unified, generic errors to the user.

• **Denial of Service: (Unmitigated)** Attackers can target the resource-heavy /api/telemetry/submit endpoint, rapidly sending telemetry logs to exhaust Uvicorn/Python worker processes and crash the server application.

• **Elevation of Privilege: (Unmitigated)** If the application container runs with root privileges or misconfigured Linux capabilities, an attacker who successfully achieves Remote Code Execution (RCE) via a framework flaw will automatically inherit root-level control over the environment.

#### Why not analyse high-level attackers?
Even if our product is pushed to production, it does **not** mean our system will be targeted by state-sponsored attackers. Our system will be attacked depending on its profile, and how large its infrastructure is and what it solves.

For example, if our asset and telemetry system tracks devices across the the world internationally or regionally across a country, **then** there is a necessity to do so. Because our threat profile is so high, we must account for those potential security risks and vulnerabilities.

**BUT.** If our system only tracks about 10,000 devices in a specific area, or sparsed out, then its profile is smaller, and only would be a target for smaller and medium-level attackers.




