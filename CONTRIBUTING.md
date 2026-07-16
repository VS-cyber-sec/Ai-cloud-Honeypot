# Contributing

Thank you for your interest in contributing to the AI-Driven Cloud Honeypot project.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest features
- Include your Python version, OS, and error message
- For security vulnerabilities, email the team directly

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Write tests for any new functionality in `tests/`
4. Ensure all tests pass: `python3 -m pytest tests/ -v`
5. Submit a pull request with a clear description

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Keep functions focused — one responsibility per function
- Use type hints where possible

### Adding New Lure Routes
To add a new HTTP lure route:
1. Define the fake response HTML/text in `honeypot/packet_logger.py`
2. Add the route to `LURE_ROUTES` dictionary with `(get_response, post_response, label)` tuple
3. Add a test case in `tests/test_http_lures.py`
4. Update `docs/ARCHITECTURE.md` with the new route

### Adding New ML Labels
To add a new attack label class:
1. Add the label to `assign_label()` in `ml/honeypot_model_v2.py`
2. Collect training data for the new class
3. Retrain the model and verify F1-weighted score
4. Add test cases in `tests/test_ml_pipeline.py`
5. Update `README.md` ML labels table

## Ethical Guidelines

All contributions must maintain the system's purely defensive and observational nature:
- No code that facilitates active attacks
- No code that retaliates against attackers
- No code that exfiltrates data to unauthorised parties
- All captured data handling must comply with applicable privacy laws
