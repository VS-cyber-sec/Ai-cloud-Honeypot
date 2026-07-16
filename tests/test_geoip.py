"""
tests/test_geoip.py — Unit tests for GeoIP enrichment module
Run: python3 -m pytest tests/test_geoip.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'honeypot'))

from geoip import geoip_lookup, format_geoip_section, _is_private

class TestPrivateIPDetection:
    def test_rfc1918_10_range(self):
        assert _is_private("10.0.0.1") == True

    def test_rfc1918_192168_range(self):
        assert _is_private("192.168.1.100") == True

    def test_rfc1918_172_range(self):
        assert _is_private("172.16.0.1") == True

    def test_loopback(self):
        assert _is_private("127.0.0.1") == True

    def test_public_ip(self):
        assert _is_private("8.8.8.8") == False

    def test_public_ip_china(self):
        assert _is_private("112.122.0.1") == False

class TestGeoIPLookup:
    def test_private_ip_returns_stub(self):
        result = geoip_lookup("192.168.1.1")
        assert result["country"] == "Private/LAN"
        assert result["city"] == "-"

    def test_loopback_returns_stub(self):
        result = geoip_lookup("127.0.0.1")
        assert result["country"] == "Private/LAN"

    def test_returns_dict(self):
        result = geoip_lookup("192.168.0.1")
        assert isinstance(result, dict)

class TestFormatGeoIPSection:
    def test_private_ip_format(self):
        geo = {"country": "Private/LAN", "country_code": "--",
               "region": "-", "city": "-", "isp": "-", "as": "-"}
        output = format_geoip_section(geo)
        assert "Private/LAN" in output

    def test_empty_geo_fallback(self):
        output = format_geoip_section({})
        assert "failed" in output.lower() or "private" in output.lower()

    def test_normal_geo_format(self):
        geo = {"country": "China", "country_code": "CN",
               "region": "Guangdong", "city": "Shenzhen",
               "isp": "China Telecom", "as": "AS4134"}
        output = format_geoip_section(geo)
        assert "China" in output
        assert "Shenzhen" in output
        assert "China Telecom" in output
