#!/bin/bash
# open_ports.sh — Opens all honeypot ports in Ubuntu iptables
# Run on Oracle Cloud VM after first SSH login

echo "[*] Opening honeypot ports in iptables..."

sudo iptables -I INPUT 1 -p tcp --dport 80   -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 443  -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 2222 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 5000 -j ACCEPT

sudo apt install -y iptables-persistent
sudo netfilter-persistent save

echo "[✓] Ports 80, 443, 2222, 5000 are now open"
echo "[*] Verify with: sudo ss -tlnp"
