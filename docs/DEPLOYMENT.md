# Deployment Guide — Oracle Cloud Free Tier

Complete step-by-step deployment of the AI-Driven Cloud Honeypot on a permanently free Oracle Cloud VM.

---

## Step 1 — Create Oracle Cloud Account

1. Go to `cloud.oracle.com` → **Start for free**
2. Select home region: **India South (Hyderabad)** or **India West (Mumbai)**
3. Verify with credit card (₹1 charge — refunded, Always Free resources only)

---

## Step 2 — Create the VM

**Compute → Instances → Create Instance**

| Setting | Value |
|---|---|
| Name | `honeypot-vm` |
| Image | Ubuntu 22.04 LTS |
| Shape | `VM.Standard.E2.1.Micro` (AMD, 1 OCPU, 1GB RAM — Always Free) |
| Network | Assign public IPv4 ✅ |
| SSH Key | Paste your `~/.ssh/id_rsa.pub` |

---

## Step 3 — Open Firewall Ports

### Oracle Security List
Networking → VCN → Default Security List → Add Ingress Rules:

| Source CIDR | Protocol | Destination Port |
|---|---|---|
| 0.0.0.0/0 | TCP | 80 |
| 0.0.0.0/0 | TCP | 443 |
| 0.0.0.0/0 | TCP | 2222 |
| 0.0.0.0/0 | TCP | 5000 |

### Ubuntu OS Firewall
```bash
bash scripts/open_ports.sh
```

---

## Step 4 — Deploy

```bash
# SSH into VM
ssh ubuntu@<your-oracle-ip>

# Clone repository
git clone https://github.com/VS-cyber-sec/ai-cloud-honeypot.git
cd ai-cloud-honeypot

# Install dependencies
pip3 install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env   # fill in Supabase, Telegram credentials

# Install systemd services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable honeypot honeypot-dashboard honeypot-sync
sudo systemctl start  honeypot honeypot-dashboard honeypot-sync

# Verify all running
sudo systemctl status honeypot honeypot-dashboard honeypot-sync
```

---

## Step 5 — Verify

```bash
# Watch live attack logs
sudo journalctl -u honeypot -f

# Check dashboard
curl http://localhost:5000/api/stats

# Open in browser
http://<your-oracle-ip>:5000
```

Within minutes of deployment you will see real internet scan traffic appearing in the logs.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Port shows filtered in nmap | Check Oracle Security List AND Ubuntu iptables |
| SSH access denied | Use `ubuntu@<ip>` not `root@<ip>`; check key permissions `chmod 600 ~/.ssh/key` |
| GeoIP says lookup failed | Private IP (normal in local lab); check internet connectivity with `curl ip-api.com/json/8.8.8.8` |
| Dashboard shows no events | Confirm `packet_logger.jsonl` exists and honeypot service is running |
| Supabase insert fails | Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env` match your project |
