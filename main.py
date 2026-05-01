import psutil
import os

class HardCache:
    def __init__(self, max_size=45 * 1024 * 1024):
        self.max_size = max_size
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            self.prune()
        self.cache[key] = value

    def prune(self):
        # iOS uchun 45MB limitga qarshi, cache 45MBdan kam bo'lsa, hech narsa olib tashlamaymiz
        if len(self.cache) < self.max_size:
            return

        # Cache kattaligi 45MBdan katta bo'lsa, eng qadimgi elementlarni olib tashlaymiz
        sorted_keys = sorted(self.cache.keys())
        for key in sorted_keys[:-self.max_size]:
            del self.cache[key]

def check_memory():
    # iOS uchun 45MB limitga qarshi, agar memory 45MBdan katta bo'lsa, hard cache prun qilish uchun
    process = psutil.Process(os.getpid())
    if process.memory_info().rss > 45 * 1024 * 1024:
        return True
    else:
        return False

def main():
    cache = HardCache()
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')

    if check_memory():
        cache.prune()

    print(cache.get('key1'))  # value1
    print(cache.get('key2'))  # value2
    print(cache.get('key3'))  # None

if __name__ == "__main__":
    main()
