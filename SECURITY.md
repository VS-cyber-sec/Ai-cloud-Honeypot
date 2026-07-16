# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| main branch | ✅ |
| Tagged releases | ✅ |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please:

1. **Do not** open a public GitHub issue
2. Email the team directly with details
3. Include: description, reproduction steps, potential impact

We will respond within 48 hours and work to patch any confirmed vulnerabilities promptly.

## Security Design Principles

This project follows these security principles:

- **Never grant access**: The Paramiko SSH server always returns `AUTH_FAILED` — no code path can be manipulated to grant shell access
- **Input sanitisation**: All attacker-supplied data is sanitised before logging — control characters stripped, length bounded
- **Minimal privilege**: Run as non-root user; only `CAP_NET_RAW` granted to Python for raw socket
- **Outbound blocking**: iptables blocks all unnecessary egress to prevent the honeypot being used as an attack launchpad
- **Credential isolation**: `.env` secrets stored separately, never committed to version control
- **Data integrity**: MD5 checksums on all sync payloads; shared-secret authentication on sync API

## Responsible Disclosure

This tool is designed for defensive research. Any use of techniques demonstrated here against systems you do not own is illegal and unethical. The authors are not responsible for misuse.
