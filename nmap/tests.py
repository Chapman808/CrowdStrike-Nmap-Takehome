import pytest
from .util import formatNmapPorts, validateHostname
# Create your tests here.

class TestUtilFunctions():
    def test_emptyHostname(self):
        hostname = ""
        with pytest.raises(ValueError):
            validateHostname(hostname)

    def test_validIps(self):
        ips = ["10.15.100.1", "0.0.0.0", "192.168.1.1", "172.168.0.1", "127.0.0.1"]
        for ip in ips:
            assert ip == validateHostname(ip)

    def test_invalidIps(self):
        ips = ["asdf.00.0", "hello1.0.0.1", "notanip", "; whoami"]
        for ip in ips:
            with pytest.raises(ValueError):
                validateHostname(ip)

class TestFormatNmapPorts():
    def test_formatNmapPorts(self):
        nmapPorts = "Host: 45.33.32.156 (scanme.nmap.org)	Ports: 22/open/tcp//ssh///, 80/open/tcp//http///"
        intended = '["22", "80"]'
        assert intended == formatNmapPorts(nmapPorts)
        nmapPorts = ""
        intended = '[]'
        assert intended == formatNmapPorts(nmapPorts)