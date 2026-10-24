# 11. Security and Multi-Tenancy

Security is an architectural requirement, not a final checklist. A system must verify identity, enforce what that identity may do, protect sensitive data, and prevent one tenant from affecting or accessing another tenant's resources.

## 11.1 Authentication versus authorization

- **Authentication:** Establishes who or what is making a request.
- **Authorization:** Determines whether that identity may perform the requested action on the target resource.

A valid login or token does not mean the caller can access every resource. Authorization should consider the user, action, resource, tenant, and relevant policy.

## 11.2 Apply least privilege and trust boundaries

Grant each service, user, and workload only the permissions it needs. Identify trust boundaries between clients, gateways, services, workers, databases, and external providers.

Important practices include:
- Validate input at system boundaries.
- Enforce authorization on the server, not only in the UI.
- Use TLS for data in transit and suitable encryption for sensitive data at rest.
- Store secrets in a managed secret system and rotate them safely.
- Avoid logging credentials, tokens, or unnecessary personal data.
- Use secure defaults and keep dependencies patched.

A gateway can authenticate requests, but services must not blindly trust headers or identity claims unless the path and token validation make that trust explicit.

## 11.3 Multi-tenant isolation

Tenants may share infrastructure while requiring logical or physical separation. Common models include:
- **Shared tables with tenant ID:** Efficient, but every query and write must enforce tenant scoping.
- **Separate schema/database per tenant:** Stronger separation options and customization, with more operational overhead.
- **Dedicated infrastructure per tenant:** Useful for strict isolation or special requirements, but typically more expensive.

Isolation includes more than database rows: caches, object storage paths, search indexes, queues, logs, metrics, exports, and background jobs must also preserve tenant boundaries.

Use defense in depth: authorization checks, tenant-scoped data access, constraints where possible, and tests designed to detect cross-tenant access.

## 11.4 Abuse controls and sensitive operations

Rate limits and quotas can protect against accidental or malicious resource exhaustion. Apply them at appropriate scopes: user, tenant, API key, IP, or expensive resource. IP-only limits can be unfair behind shared networks; identity-only limits may not stop distributed abuse.

For high-impact operations, consider stronger authorization, audit logs, idempotency, and explicit confirmation where appropriate. Security logging should be useful without collecting secrets or excessive sensitive data.

## 11.5 Common interview questions

### What is the difference between authentication and authorization?

Authentication establishes identity; authorization checks whether that identity may perform an action on a resource. Authorization must be enforced for each protected operation, even after a successful login.

### How do you prevent cross-tenant data leaks?

Make tenant identity part of the authorization and data-access model. Enforce scoping on reads, writes, background jobs, caches, and exports; use database constraints or isolation where available; and test attempts to access another tenant's identifiers. Hiding a tenant ID in the UI is not security.

### Should every service trust the API gateway?

No. Trust should be explicit and limited. Services may validate tokens or accept authenticated identity from a protected internal path, but they need controls against direct access, spoofed headers, and misconfigured network boundaries.

### How do you design for security without overcomplicating the system?

Start with assets, threats, trust boundaries, and required controls. Use standard, well-maintained authentication and encryption mechanisms, least privilege, centralized secret management, and auditable authorization. Add specialized controls when the threat model or compliance needs justify them.

## Quick revision

- Authentication answers who; authorization answers what they may do.
- Treat every service boundary as a place to validate trust.
- Tenant isolation must cover all data paths, not only primary database queries.
- Use least privilege, secret management, encryption, and privacy-aware logging.
- Apply quotas and rate limits to protect shared resources.
