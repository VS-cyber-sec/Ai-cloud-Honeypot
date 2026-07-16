#!/bin/bash
# test_labels.sh — Simulate all 8 ML label classes
# Run from Kali Linux attacker VM against your honeypot
# Usage: bash test_labels.sh <honeypot-ip>

TARGET=${1:-"<your-honeypot-ip>"}

if [ "$TARGET" = "<your-honeypot-ip>" ]; then
    echo "[!] Usage: bash test_labels.sh <honeypot-ip>"
    exit 1
fi

echo "=================================================="
echo "  Honeypot ML Label Test Suite"
echo "  Target: $TARGET"
echo "=================================================="

echo ""
echo "[1/8] brute_force — SSH credential stuffing"
hydra -l root -P /usr/share/wordlists/rockyou.txt \
      ssh://$TARGET -s 2222 -t 4 -I &
HYDRA_PID=$!
sleep 2

echo ""
echo "[2/8] ssh_probe — SSH banner grab"
nc -w 3 $TARGET 2222
sleep 1

echo ""
echo "[3/8] web_shell_probe — RCE path probing"
for p in /shell.php /cmd.php /c99.php; do
    curl -s -o /dev/null -w "  $p → %{http_code}\n" http://$TARGET$p
    sleep 0.5
done

echo ""
echo "[4/8] exploit_attempt — CMS/CVE path probing"
for p in /wp-login.php /xmlrpc.php /.env /phpmyadmin /wp-admin; do
    curl -s -o /dev/null -w "  $p → %{http_code}\n" http://$TARGET$p
    sleep 0.5
done

echo ""
echo "[5/8] cloud_metadata_probe — cloud credential theft"
for p in /latest/meta-data/ /.kube/config /actuator/env; do
    curl -s -o /dev/null -w "  $p → %{http_code}\n" http://$TARGET$p
    sleep 0.5
done

echo ""
echo "[6/8] web_recon — scanner User-Agent fingerprinting"
curl -s -o /dev/null -A "masscan/1.0"        http://$TARGET/ && echo "  masscan UA sent"
curl -s -o /dev/null -A "zgrab/0.x"          http://$TARGET/ && echo "  zgrab UA sent"
curl -s -o /dev/null -A "python-requests/2.x" http://$TARGET/ && echo "  python-requests UA sent"

echo ""
echo "[7/8] automated_scan — Nmap fast multi-port"
nmap -sS -T4 -p 22,80,443,2222 $TARGET

echo ""
echo "[8/8] port_scan — Nmap slow single-port"
nmap -sS -T1 -p 22,80 $TARGET

echo ""
echo "Letting Hydra run for 30 more seconds..."
sleep 30
kill $HYDRA_PID 2>/dev/null

echo ""
echo "=================================================="
echo "  Test complete."
echo "  Check: tail -f packet_logger.jsonl"
echo "  Dashboard: http://$TARGET:5000"
echo "=================================================="
