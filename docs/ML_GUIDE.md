# ML Classification Guide

## 8 Attack Label Classes

| Label | Trigger Condition |
|---|---|
| `brute_force` | SSH with high attempt rate (ip_request_rate > 10 or ts_count > 5) |
| `ssh_probe` | SSH single connection, banner grab only |
| `exploit_attempt` | HTTP to known CVE/CMS paths |
| `web_shell_probe` | HTTP to shell/RCE paths |
| `cloud_metadata_probe` | HTTP to cloud/k8s metadata paths |
| `web_recon` | HTTP with known scanner User-Agent |
| `automated_scan` | Same IP hits 3+ ports in 10 seconds |
| `port_scan` | Low-rate TCP SYN probes |

## Feature Vector (12 features)

| Feature | Type | Description |
|---|---|---|
| `first_octet` | Numerical | First octet of source IP (range hint) |
| `is_private` | Binary | 1 if RFC-1918 private IP |
| `hour` | Numerical | Hour of attack (0-23) |
| `minute` | Numerical | Minute of attack (0-59) |
| `day_of_week` | Numerical | Day (0=Monday, 6=Sunday) |
| `src_port` | Numerical | Source port of attacker |
| `dst_port` | Numerical | Destination port targeted |
| `ttl` | Numerical | IP Time-To-Live (OS fingerprint) |
| `window_size` | Numerical | TCP window size |
| `ip_request_rate` | Numerical | Total connections from this IP |
| `is_exploit_path` | Binary | 1 if HTTP path matches exploit list |
| `is_known_scanner` | Binary | 1 if User-Agent matches scanner list |

## Training

```bash
# Train on collected log data
python3 ml/honeypot_model_v2.py

# Outputs:
#   honeypot_rf_pipeline_v2.pkl  — trained model
#   label_encoder_v2.pkl         — label encoder
#   reports/confusion_matrix.png
#   reports/feature_importance.png
#   reports/training_report.json
```

## Live Classification

```python
from ml.honeypot_model_v2 import predict_event

result = predict_event({
    "src_ip": "1.2.3.4",
    "dst_port": "80",
    "protocol": "HTTP",
    "http_path": "/wp-admin",
    "user_agent": "masscan/1.0"
})

print(result["label"])       # "exploit_attempt"
print(result["confidence"])  # 0.91
```

## Incremental Retraining

```bash
# Retrain with new data collected since last training
python3 ml/retrain.py --new-log /path/to/new_data.log
```

Run this weekly as new attack data accumulates to keep the model current.

## Evaluation Metrics

- **Primary:** F1-weighted (handles class imbalance)
- **Secondary:** F1-macro (equal weight per class)
- **Validation:** 5-fold Stratified K-Fold CV
- **Tuning:** RandomizedSearchCV (20 iterations, 3-fold inner CV)
- **Current F1-weighted:** 0.87
