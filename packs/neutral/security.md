# Security and data protection

The checklist is the [OWASP Top 10](https://owasp.org/Top10/) and [ASVS](https://owasp.org/www-project-application-security-verification-standard/), plus the [OWASP Top 10 for LLM applications](https://genai.owasp.org/) where the product uses models or agents.

## Every change
- **Access control (A01).** Authorisation on every handler; no IDOR; the acting user from validated credentials, never the request.
- **Crypto (A02).** TLS 1.2 minimum, 1.3 where supported; vetted libraries only; password hashing with Argon2id, scrypt or bcrypt.
- **Injection (A03).** Parameterised queries; output encoding; no shell or query built from strings.
- **Insecure design (A04).** Concurrency control on read-modify-write; idempotency on money and webhooks; rate limits on anonymous and expensive endpoints.
- **Misconfiguration (A05).** No debug endpoints or verbose errors outside development; secure headers.
- **Vulnerable components (A06).** Dependencies pinned and patched.
- **Authentication (A07).** Lockout or throttling; no account-enumeration oracle.
- **Integrity (A08).** No unsafe deserialisation; signed artifacts where it matters.
- **Logging (A09).** Security events logged; **no personal data, secrets or tokens in logs**, telemetry, URLs or error bodies.
- **SSRF (A10).** Outbound URLs allowlisted.

## Secrets and identifiers
No secrets in code, config or history. Before every push, the outgoing commits' content and messages are grepped for keys, tokens, e-mail addresses and identifiers. A hit is removed by rewriting the branch before the push, never by a follow-up commit: a secret added and then removed still ships in history.

## Data protection
- Collect the minimum, for a stated purpose.
- Consent before any non-essential tracking or embed.
- Erasure and retention as the project's policy states.
- An audit trail on changes to personal data.
- Data residency as the law and the product require.

## A finding
The security champion gives a **strategy**: the control, the failing test that pins it, and the developer path. The owning agent implements it. The finding closes when the pinning test is in the diff and fails without the control.
