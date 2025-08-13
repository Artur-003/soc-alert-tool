blacklist = [
    "192.168.1.10",
    "203.0.113.5",
    "10.0.0.15"
]
whitelist = [
    "133.0.0.13",
    "100.10.10.0",
    "011.2.2.10"
]
ip = input("Введите IP для проверки: ").strip()

if ip in blacklist:
    print("Доступ запрещен: ", ip)
if ip in whitelist:
    print("Доступ разрешен: ", ip)
else:
    print("Уходи: ", ip)
