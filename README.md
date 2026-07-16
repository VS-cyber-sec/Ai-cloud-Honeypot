<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Oracle_Cloud-Free_Tier-F80000?style=for-the-badge&logo=oracle&logoColor=white"/>
<img src="https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-Random_Forest-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

<br/><br/>

```
 ██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ████████╗
 ██║  ██║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
 ███████║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ ██████╔╝██║   ██║   ██║
 ██╔══██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██╔═══╝ ██║   ██║   ██║
 ██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║   ██║     ╚██████╔╝   ██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝      ╚═════╝    ╚═╝
```

# AI-Driven Cloud Honeypot for Attack Detection

### A permanently internet-facing, ML-classified, cloud-native honeypot — deployed on Oracle Cloud Free Tier at **₹0/month**

<br/>

> Captures real SSH brute-force credentials, HTTP attack payloads, and port scan metadata from live internet traffic.  
> Classifies every event in real time using a Random Forest model.  
> Stores everything in Supabase. Alerts you via Telegram. Shows it live on a Flask dashboard.

<br/>

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue)](https://python.org)
[![Oracle Cloud](https://img.shields.io/badge/Deployed%20on-Oracle%20Cloud-red)](https://cloud.oracle.com)
[![Zero Cost](https://img.shields.io/badge/Infrastructure%20Cost-₹0%2Fmonth-brightgreen)](https://cloud.oracle.com/free)
[![ICSAIEM 2026](https://img.shields.io/badge/Published-ICSAIEM%202026-blueviolet)](https://dypcoei.edu.in)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [ML Attack Classification](#-ml-attack-classification)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Services](#-services)
- [Testing](#-testing)
- [Results](#-results)
- [Team](#-team)
- [Publication](#-publication)
- [License](#-license)

---

## 🔍 Overview

Traditional firewalls block attacks silently — revealing nothing about who attacked, what tools they used, what credentials they tried, or where they came from. This project fills that intelligence gap.

**AI-Driven Cloud Honeypot** is a multi-port deception system that:

| Feature | Detail |
|---|---|
| 🎯 **Deep SSH Capture** | Paramiko server completes full SSH handshake, captures every brute-force credential |
| 🌐 **HTTP Lure Layer** | 17 fake routes attract CMS scanners, web shell probers, cloud metadata harvesters |
| 🗺️ **GeoIP Enrichment** | Every attacker IP resolved to country, city, ISP, ASN |
| 🤖 **ML Classification** | Random Forest classifies events into 8 attack label classes in real time |
| ☁️ **Cloud Storage** | All events persisted to Supabase PostgreSQL automatically |
| 📱 **Telegram Alerts** | Instant mobile notifications for high-value attack events |
| 📊 **Live Dashboard** | Flask web dashboard with auto-refresh, top attacker IPs, port status |
| 🔄 **ML Sync Service** | Automatic log shipping to separate ML machine for safe data backup |
| 💰 **Zero Cost** | Entirely free-tier infrastructure — Oracle Cloud, Supabase, Telegram |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INTERNET ATTACK TRAFFIC                           │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Oracle Cloud VM — Ubuntu 22.04 (Always Free)           │
│                                                                     │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────────┐ │
│  │  Port 22/443  │  │   Port 2222   │  │        Port 80           │ │
│  │  Raw Socket   │  │  Paramiko SSH │  │   Fake Apache HTTP       │ │
│  │  (Passive)    │  │  Deep Server  │  │   17 Lure Routes         │ │
│  └──────┬───────┘  └──────┬────────┘  └────────────┬─────────────┘ │
│         │                 │                         │               │
│         └─────────────────┼─────────────────────────┘               │
│                           ▼                                         │
│              ┌─────────────────────────┐                            │
│              │   GeoIP Enrichment      │  ← ip-api.com (cached)    │
│              │   Scanner Detection     │  ← 3+ ports / 10s         │
│              │   ML Classification     │  ← Random Forest (8 labels)│
│              └───────────┬─────────────┘                            │
│                          ▼                                          │
│         ┌─────────────────────────────────────┐                     │
│         │  Dual Log  (.log text + .jsonl)      │                     │
│         └──────┬──────────────────────┬────────┘                    │
│                │                      │                             │
│                ▼                      ▼                             │
│         Flask Dashboard         Sync Sender ──► ML Machine          │
│         (Port 5000)             (Delta sync)                        │
└─────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
   Supabase DB          Telegram Bot         GeoIP API
   (PostgreSQL)         (Alerts)             (ip-api.com)
```

---

## 🤖 ML Attack Classification

The Random Forest classifier assigns one of **8 attack labels** to every captured event:

| Label | Description | Example Trigger |
|---|---|---|
| `brute_force` | SSH credential stuffing at high rate | Hydra / Medusa against port 2222 |
| `ssh_probe` | Single SSH banner grab | `nc -w 3 <ip> 2222` |
| `exploit_attempt` | Known CVE / CMS path probe | `/xmlrpc.php`, `/.env`, `/wp-login.php` |
| `web_shell_probe` | RCE shell upload / access attempt | `/shell.php`, `/cmd.php`, `/c99.php` |
| `cloud_metadata_probe` | Cloud credential theft attempt | `/latest/meta-data/`, `/.kube/config` |
| `web_recon` | General HTTP scanning | Masscan, ZGrab, Nikto User-Agent |
| `automated_scan` | High-rate multi-port scan | Nmap `-T4` hitting 3+ ports in 10s |
| `port_scan` | Low-rate TCP SYN probe | Nmap `-T1` single port |

**Model performance:** F1-weighted = **0.87** (5-fold Stratified K-Fold CV)

---

## 📁 Repository Structure

```
ai-cloud-honeypot/
│
├── honeypot/                    # Core honeypot engine
│   ├── packet_logger.py         # Main script — all 4 port listeners
│   ├── geoip.py                 # GeoIP enrichment module (cached)
│   ├── alerts.py                # Telegram Bot notification service
│   └── cloud_logger.py          # Supabase event persistence
│
├── ml/                          # Machine learning pipeline
│   ├── honeypot_model_v2.py     # Random Forest training + evaluation
│   ├── predict.py               # Live single-event classification
│   └── retrain.py               # Incremental model update script
│
├── dashboard/                   # Flask web dashboard
│   └── app.py                   # Dashboard API + embedded HTML frontend
│
├── sync/                        # ML machine data sync service
│   ├── sync_sender.py           # Runs on Oracle VM — ships logs to ML machine
│   └── sync_receiver.py         # Runs on ML machine — receives + classifies
│
├── scripts/                     # Setup and utility scripts
│   ├── setup_honeypot.sh        # One-shot Oracle VM setup
│   ├── setup_ml.sh              # One-shot ML machine setup
│   ├── test_labels.sh           # Attack simulation — all 8 ML labels
│   └── open_ports.sh            # iptables port opening utility
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Detailed system architecture
│   ├── DEPLOYMENT.md            # Step-by-step Oracle Cloud deployment
│   ├── ML_GUIDE.md              # Model training and evaluation guide
│   └── API.md                   # Dashboard and sync API reference
│
├── tests/                       # Test suite
│   ├── test_geoip.py            # GeoIP module unit tests
│   ├── test_http_lures.py       # HTTP lure route integration tests
│   └── test_ml_pipeline.py      # ML pipeline unit tests
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
│
├── .env.example                 # Environment variable template
├── requirements.txt             # Python dependencies
├── systemd/                     # systemd service files
│   ├── honeypot.service
│   ├── honeypot-dashboard.service
│   └── honeypot-sync.service
├── LICENSE
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites

- Oracle Cloud Free Tier account ([cloud.oracle.com](https://cloud.oracle.com))
- Ubuntu 22.04 VM (AMD `VM.Standard.E2.1.Micro` — always free)
- Python 3.10+
- Supabase account ([supabase.com](https://supabase.com))
- Telegram Bot token (from [@BotFather](https://t.me/botfather))

### 1. Clone the Repository

```bash
git clone https://github.com/VS-cyber-sec/ai-cloud-honeypot.git
cd ai-cloud-honeypot
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

Fill in your credentials:

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-anon-key
TELEGRAM_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
ML_HOST=http://your-ml-machine-ip:8765
SYNC_SECRET=your-shared-secret
```

### 4. Set Up Oracle Cloud Firewall

```bash
# Open all honeypot ports in Ubuntu iptables
bash scripts/open_ports.sh
```

### 5. Run the Honeypot

```bash
# Run interactively (testing)
sudo python3 honeypot/packet_logger.py --verbose

# Run as permanent systemd service (production)
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable honeypot honeypot-dashboard honeypot-sync
sudo systemctl start  honeypot honeypot-dashboard honeypot-sync
```

### 6. Open Dashboard

```
http://<your-oracle-ip>:5000
Login: admin / admin
```

---

## ⚙️ Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | ✅ | Supabase project URL |
| `SUPABASE_KEY` | ✅ | Supabase anon public key |
| `TELEGRAM_TOKEN` | ✅ | Telegram Bot API token |
| `TELEGRAM_CHAT_ID` | ✅ | Your Telegram chat ID |
| `ML_HOST` | Optional | ML machine receiver URL |
| `SYNC_SECRET` | Optional | Shared secret for sync auth |
| `LOG_PATH` | Optional | Log file path (default: `packet_logger.log`) |

---

## 🛠️ Services

The system runs three independent systemd services:

| Service | Port | Description |
|---|---|---|
| `honeypot.service` | 22, 80, 443, 2222 | Core packet logger + SSH/HTTP servers |
| `honeypot-dashboard.service` | 5000 | Flask web dashboard |
| `honeypot-sync.service` | — | Log sync sender to ML machine |

```bash
# Check all services
sudo systemctl status honeypot honeypot-dashboard honeypot-sync

# Watch live logs
sudo journalctl -u honeypot -f

# Restart everything
sudo systemctl restart honeypot honeypot-dashboard honeypot-sync
```

---

## 🧪 Testing

### Simulate All 8 ML Label Classes (from Kali VM)

```bash
# Edit target IP first
nano scripts/test_labels.sh

# Run all 8 attack types
bash scripts/test_labels.sh
```

### Individual Tests

```bash
# Label 1 — brute_force
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://<ip> -s 2222 -t 4

# Label 2 — ssh_probe
nc -w 3 <ip> 2222

# Label 3 — web_shell_probe
curl http://<ip>/shell.php
curl http://<ip>/cmd.php

# Label 4 — exploit_attempt
curl http://<ip>/wp-login.php
curl http://<ip>/xmlrpc.php

# Label 5 — cloud_metadata_probe
curl http://<ip>/latest/meta-data/
curl http://<ip>/.kube/config

# Label 6 — web_recon
curl -A "masscan/1.0" http://<ip>/

# Label 7 — automated_scan
nmap -sS -T4 -p 22,80,443,2222 <ip>

# Label 8 — port_scan
nmap -sS -T1 -p 22,80 <ip>
```

### Unit Tests

```bash
python3 -m pytest tests/ -v
```

---

## 📊 Results

| Metric | Value |
|---|---|
| SSH Credential Capture Rate | **100%** (Hydra brute-force testing) |
| HTTP Lure Routes | **17/17** operational |
| GeoIP Resolution Rate | **100%** (public IPs) |
| ML F1-Weighted Score | **0.87** (5-fold CV) |
| Average Confidence Score | **0.91** |
| Telegram Alert Delivery | **100%** |
| Service Uptime | **99.9%** (auto-restart via systemd) |
| Monthly Infrastructure Cost | **₹0** |

### Attack Distribution (first 24h of deployment)

```
brute_force         ████████████████████  47%
automated_scan      ████████████          28%
web_recon           ████████              18%
exploit_attempt     ███                    4%
port_scan           ██                     2%
web_shell_probe     █                      1%
```

---

## 👥 Team

| Name | Role | GitHub |
|---|---|---|
| **Vaishnavi Chavan** | Team Lead / ML Engineer | [@VS-cyber-sec](https://github.com/VS-cyber-sec) |
| **Yuvraj Dudhal** | Network / Backend Engineer | — |
| **Aniket Patil** | Cloud / DevOps Engineer | — |
| **Akash Wavhal** | Frontend / Testing Engineer | — |

**Guide:** Prof. Shilpa Vishwabrahma  
**Institution:** Dr. D. Y. Patil College of Engineering & Innovation, Talegaon, Pune

---

## 📄 Publication

This project was accepted for presentation at:

> **ICSAIEM 2026** — International Conference on Sustainable Advancements in Intelligent Engineering and Management  
> Dr. D. Y. Patil College of Engineering & Innovation, Varale, Talegaon, Pune

---

## 🔒 Ethical Use

This system is designed exclusively for **defensive security research** on infrastructure you own and control.

- The honeypot never initiates any outbound attack
- It never grants access to any attacker regardless of submitted credentials
- All captured data is used solely for academic research and threat intelligence
- Running this system against infrastructure you do not own is illegal

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this repository if it helped your research ⭐**

Made with 🔐 for cybersecurity research by Team VS-cyber-sec

</div>
