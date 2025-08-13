from collections import defaultdict
from pathlib import Path

# Путь к лог-файлу
log_file = Path("access.log")

# Словарь для подсчёта ошибок по IP
failed_attempts = defaultdict(int)

# Читаем файл
with log_file.open(encoding="utf-8") as f:
    for line in f:
        if "FAILED" in line:
            # Находим IP
            parts = line.split()
            for part in parts:
                if part.startswith("IP="):
                    ip = part.split("=")[1]
                    failed_attempts[ip] += 1

# Вывод IP, у которых 3 и более неудачных попыток
print("🔍 Подозрительные IP:")
for ip, count in failed_attempts.items():
    if count >= 3:
        print(f"⛔ {ip} — {count} неудачных попыток")


print("DEBUG: все IP с ошибками:")
for ip, count in failed_attempts.items():
    print(f"{ip}: {count}")




import csv

with open("suspicious_ips.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["IP", "Количество ошибок"])
    for ip, count in failed_attempts.items():
        if count >= 3:
            writer.writerow([ip, count])

print("✅ Отчёт сохранён в suspicious_ips.csv")







import requests

# --- Настройки Telegram ---
BOT_TOKEN = "8248764947:AAE5HWQjFFdDGXSdqDAGIQlFce1tGhG5IT4"
CHAT_ID = "5717271579"

def send_alert_to_telegram(ip, count):
    text = f"⚠ Обнаружено подозрительное поведение!\nIP: {ip}\nПопыток входа с ошибкой: {count}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            print("❌ Ошибка отправки в Telegram:", r.text)
    except Exception as e:
        print("❌ Ошибка при подключении к Telegram:", e)




# Отправка алертов по IP с 3+ ошибками
for ip, count in failed_attempts.items():
    if count >= 3:
        print(f"⛔ {ip} — {count} неудачных попыток")
        send_alert_to_telegram(ip, count)
