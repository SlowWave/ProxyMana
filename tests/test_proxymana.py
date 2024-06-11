import unittest

from proxymana.proxymana import ProxyMana


class TestProxyMana(unittest.TestCase):

    def test_start_scheduler_thread(self):
        ProxyMana.start_scheduler_thread()
        self.assertEqual(ProxyMana._keep_running_scheduler, True)
        self.assertEqual(ProxyMana.proxy_timeout, 1)
        self.assertEqual(ProxyMana.proxy_search_freq, 1)
        self.assertEqual(ProxyMana.proxy_clear_freq, 120)
        self.assertEqual(ProxyMana.verbose, False)

    def test_start_scheduler_thread_custom_args(self):
        ProxyMana.start_scheduler_thread(
            proxy_timeout=3, proxy_search_freq=5, proxy_clear_freq=60, verbose=True
        )
        self.assertEqual(ProxyMana._keep_running_scheduler, True)
        self.assertEqual(ProxyMana.proxy_timeout, 3)
        self.assertEqual(ProxyMana.proxy_search_freq, 5)
        self.assertEqual(ProxyMana.proxy_clear_freq, 60)
        self.assertEqual(ProxyMana.verbose, True)

    def test_stop_scheduler_thread(self):
        ProxyMana.stop_scheduler_thread()
        self.assertEqual(ProxyMana._keep_running_scheduler, False)

    def test_get_new_proxy(self):
        ProxyMana.available_proxies = ["http://1.2.3.4:8080"]
        ProxyMana.invalid_proxies = []
        ProxyMana._available_proxies_busy = False
        ProxyMana._invlaid_proxies_busy = False
        ProxyMana._keep_running_scheduler = True
        new_proxy = ProxyMana.get_new_proxy()
        self.assertEqual("http://1.2.3.4:8080", new_proxy)

    def test_get_new_proxy_valid(self):
        ProxyMana.available_proxies = ["http://1.2.3.4:8080", "http://2.3.4.5:8080"]
        ProxyMana.invalid_proxies = ["http://1.2.3.4:8080"]
        ProxyMana._available_proxies_busy = False
        ProxyMana._invlaid_proxies_busy = False
        ProxyMana._keep_running_scheduler = True
        new_proxy = ProxyMana.get_new_proxy()
        self.assertEqual("http://2.3.4.5:8080", new_proxy)

    def test_get_new_proxy_while_scheduler_is_not_running(self):
        ProxyMana.available_proxies = ["http://1.2.3.4:8080"]
        ProxyMana.invalid_proxies = []
        ProxyMana._available_proxies_busy = False
        ProxyMana._invlaid_proxies_busy = False
        ProxyMana._keep_running_scheduler = False
        new_proxy = ProxyMana.get_new_proxy()
        self.assertIsNone(new_proxy)

    def test_remove_proxy(self):
        ProxyMana.remove_proxy("http://1.2.3.4:8080")
        self.assertIn("http://1.2.3.4:8080", ProxyMana.invalid_proxies)

    def test__clear_invalid_proxies(self):
        ProxyMana.invalid_proxies = ["http://1.2.3.4:8080"]
        ProxyMana._clear_invalid_proxies()
        self.assertEqual(ProxyMana.invalid_proxies, [])
