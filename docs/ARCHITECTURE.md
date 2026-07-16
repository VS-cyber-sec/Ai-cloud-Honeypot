# System Architecture

## Three-Layer Deception Architecture

### Layer 1 — Passive Reconnaissance (ports 22, 443)
Raw socket (`AF_INET, SOCK_RAW, IPPROTO_TCP`) at the OS kernel level.
- Does not bind to or occupy port 22 or 443
- Intercepts every SYN packet silently
- Extracts source IP, TTL, TCP flags, window size
- The real SSH daemon on port 22 is completely untouched

### Layer 2 — Active SSH Deception (port 2222)
Paramiko library in server mode.
- Completes full SSH cryptographic handshake (MSG_KEXINIT → DH key exchange → session keys)
- `check_auth_password()` captures every credential submitted
- Always returns `AUTH_FAILED` — no attacker ever gets shell access
- Logs SSH client banner to fingerprint attack tool (Hydra, Medusa, paramiko, libssh)

### Layer 3 — HTTP Deception (port 80)
Plain TCP socket serving fake HTTP responses.

| Route | Response | Label |
|---|---|---|
| `/wp-admin`, `/wp-login.php` | Fake WordPress login | `exploit_attempt` |
| `/phpmyadmin` | Fake phpMyAdmin panel | `exploit_attempt` |
| `/.env` | Fake Laravel secrets | `exploit_attempt` |
| `/xmlrpc.php` | WordPress XML-RPC | `exploit_attempt` |
| `/shell.php`, `/cmd.php`, `/c99.php` | Fake shell output | `web_shell_probe` |
| `/latest/meta-data/` | Fake AWS credentials | `cloud_metadata_probe` |
| `/.kube/config` | Fake Kubernetes config | `cloud_metadata_probe` |
| `/actuator/env` | Fake Spring Boot | `cloud_metadata_probe` |

## Data Flow

```
Raw TCP packet
      │
      ▼
Protocol parser (TCP/SSH/HTTP)
      │
      ▼
GeoIP enrichment (ip-api.com, cached per IP)
      │
      ▼
Scanner detection (3+ ports / 10s sliding window)
      │
      ▼
ML Feature extraction (12 features)
      │
      ▼
Random Forest predict_proba() → label + confidence
      │
      ├──► packet_logger.log  (human-readable text)
      ├──► packet_logger.jsonl (structured JSON Lines)
      ├──► Supabase PostgreSQL (cloud persistence)
      └──► Telegram Bot (if high-value label)
```

## Module Dependencies

```
packet_logger.py
    ├── imports geoip.py
    ├── imports alerts.py
    ├── imports cloud_logger.py
    └── imports ml/honeypot_model_v2.py (predict_event)

sync/sync_sender.py
    └── watches packet_logger.log + .jsonl
    └── ships delta to sync/sync_receiver.py via HTTP

sync/sync_receiver.py
    └── receives logs
    └── runs ML classification on new events
    └── pushes results to Supabase
```
