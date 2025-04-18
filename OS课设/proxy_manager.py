import random
import requests

class ProxyManager:
    def __init__(self, proxy_file="proxy_list.txt", validate=False):
        self.proxy_file = proxy_file
        self.proxy_list = self.load_proxy_list()
        if validate:
            self.proxy_list = self.validate_all()
        print(f"✅ 已载入代理 {len(self.proxy_list)} 条")

    def load_proxy_list(self):
        try:
            with open(self.proxy_file, "r", encoding="utf-8") as f:
                proxies = list(set(line.strip() for line in f if line.strip()))
                return proxies
        except Exception as e:
            print(f"❌ 无法读取代理文件: {e}")
            return []

    def get_random_proxy(self):
        if not self.proxy_list:
            return None
        return random.choice(self.proxy_list)

    def validate_proxy(self, proxy, timeout=5):
        """测试代理是否可用"""
        try:
            res = requests.get("https://httpbin.org/ip", proxies={
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }, timeout=timeout)
            return res.status_code == 200
        except Exception:
            return False

    def validate_all(self):
        """验证所有代理的可用性（耗时）"""
        valid_proxies = []
        print("🔍 正在验证代理可用性...")
        for proxy in self.proxy_list:
            if self.validate_proxy(proxy):
                valid_proxies.append(proxy)
                print(f"✅ 可用代理: {proxy}")
            else:
                print(f"❌ 无效代理: {proxy}")
        print(f"🎯 验证完成，有效代理共 {len(valid_proxies)} 条")
        return valid_proxies
