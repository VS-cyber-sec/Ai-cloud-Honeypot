"""
tests/test_http_lures.py — Integration tests for HTTP lure routes
Tests the lure route dictionary and response logic without starting the server.
Run: python3 -m pytest tests/test_http_lures.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'honeypot'))


class TestLureRoutes:
    """Verify all expected lure routes are defined."""

    REQUIRED_ROUTES = [
        "/admin", "/wp-admin", "/phpmyadmin", "/.env",
        "/wp-login.php", "/xmlrpc.php", "/shell.php",
        "/cmd.php", "/c99.php", "/latest/meta-data/",
        "/.kube/config", "/actuator/env", "/.git",
        "/config.php", "/backup.zip", "/shell", "/robots.txt"
    ]

    def test_all_required_routes_defined(self):
        from packet_logger import LURE_ROUTES
        for route in self.REQUIRED_ROUTES:
            assert route in LURE_ROUTES, f"Missing lure route: {route}"

    def test_routes_have_responses(self):
        from packet_logger import LURE_ROUTES
        for route, value in LURE_ROUTES.items():
            assert len(value) >= 2, f"Route {route} missing response tuple"
            get_resp, _, label = value
            assert get_resp is not None, f"Route {route} has no GET response"
            assert isinstance(label, str), f"Route {route} has no label"

    def test_shell_routes_labelled_correctly(self):
        from packet_logger import LURE_ROUTES
        shell_routes = ["/shell.php", "/cmd.php", "/c99.php"]
        for route in shell_routes:
            if route in LURE_ROUTES:
                _, _, label = LURE_ROUTES[route]
                assert "SHELL" in label.upper(), \
                    f"{route} should have SHELL label, got: {label}"

    def test_cloud_routes_labelled_correctly(self):
        from packet_logger import LURE_ROUTES
        cloud_routes = ["/latest/meta-data/", "/.kube/config"]
        for route in cloud_routes:
            if route in LURE_ROUTES:
                _, _, label = LURE_ROUTES[route]
                assert any(k in label.upper() for k in ["CLOUD","KUBE","META","AWS"]), \
                    f"{route} should have cloud label, got: {label}"


class TestHTTPParser:
    """Test HTTP request parsing."""

    def test_parse_valid_get_request(self):
        from packet_logger import parse_http_request
        raw = b"GET /wp-admin HTTP/1.1\r\nHost: example.com\r\nUser-Agent: masscan\r\n\r\n"
        result = parse_http_request(raw)
        assert result is not None
        assert result["method"] == "GET"
        assert result["path"] == "/wp-admin"
        assert result["headers"].get("User-Agent") == "masscan"

    def test_parse_post_with_body(self):
        from packet_logger import parse_http_request
        body = b"username=admin&password=password123"
        raw = (b"POST /wp-admin HTTP/1.1\r\nContent-Length: " +
               str(len(body)).encode() + b"\r\n\r\n" + body)
        result = parse_http_request(raw)
        assert result is not None
        assert result["method"] == "POST"
        assert "admin" in result["body_preview"]

    def test_parse_invalid_returns_none(self):
        from packet_logger import parse_http_request
        raw = b"not a valid http request at all"
        result = parse_http_request(raw)
        assert result is None

    def test_parse_form_body_credentials(self):
        from packet_logger import parse_form_body
        body = "username=root&password=toor123"
        result = parse_form_body(body)
        assert result.get("username") == "root"
        assert result.get("password") == "toor123"
