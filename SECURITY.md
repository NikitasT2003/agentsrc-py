# Security Policy

## Supported Versions

| Version | Supported          |
| :------ | :----------------- |
| 0.1.x   | ✅ Current release |

## Reporting a Vulnerability

If you discover a security vulnerability in `agentsrc-py`, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email: **[tsoumasnikitas@gmail.com](mailto:tsoumasnikitas@gmail.com)**

Include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within **48 hours** and aim to release a fix within **7 days** for critical issues.

## Scope

`agentsrc-py` operates locally and fetches package artifacts from PyPI. Security considerations include:

- **Archive extraction**: The tool unpacks `tar.gz` and `.whl` files. We use Python's standard `tarfile` and `zipfile` modules.
- **Network requests**: HTTP requests are made to `pypi.org` only. No user data is transmitted.
- **Local file writes**: Output is written exclusively to `.agentsrc/` within the project directory.
- **No telemetry**: The tool does not collect or send any usage data.
