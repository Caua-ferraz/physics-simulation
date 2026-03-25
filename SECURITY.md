# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (`main`) | Yes |
| older commits | No |

Only the latest code on `main` receives security attention. If you are running an older version, please update before reporting.

## Scope

This is a local desktop physics simulation with no network access, no server, no authentication, and no user data storage. The attack surface is minimal, but the following are still in scope:

- **Dependency vulnerabilities** — issues in `matplotlib` or `numpy` that could affect users running the app.
- **Malicious input handling** — if crafted user input (e.g. in parameter fields) causes unexpected code execution or crashes outside normal error handling.
- **Unsafe file operations** — if a future feature reads/writes files and does so insecurely.

The following are **out of scope**: social engineering, physical access attacks, issues in the Python interpreter itself.

## Reporting a Vulnerability

Please **do not** open a public issue for security vulnerabilities.

Instead, report privately via GitHub's built-in private disclosure:
1. Go to the repository on GitHub.
2. Click **Security** → **Report a vulnerability**.
3. Fill in the details: affected version, description, reproduction steps, and potential impact.

You will receive an acknowledgment within **72 hours**. If the issue is confirmed, a fix will be released as soon as possible and you will be credited in the release notes (unless you prefer to remain anonymous).
