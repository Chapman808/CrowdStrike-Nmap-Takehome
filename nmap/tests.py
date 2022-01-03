from django.test import TestCase
import unittest
from .util import validateHostname
# Create your tests here.

class TestHostnameValidation(unittest.TestCase):
    def test_emptyHostname(self):
        hostname = ""
        with self.assertRaises(ValueError):
            validateHostname(hostname)

    def test_validIps(self):
        ips = ["10.15.100.1", "0.0.0.0", "192.168.1.1", "172.168.0.1", "127.0.0.1"]
        for ip in ips:
            self.assertEqual(ip, validateHostname(ip))

    def test_invalidIps(self):
        ips = ["asdf.00.0", "hello1.0.0.1", "notanip", "; whoami"]
        for ip in ips:
            with self.assertRaises(ValueError):
                validateHostname(ip)

if __name__ == '__main__':
    unittest.main()