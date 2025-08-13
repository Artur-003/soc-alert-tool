from ipaddress import ip_address, ip_network
from pathlib import Path

# ---------- утилиты ----------
def norm(s: str) -> str:
    return (s.strip().replace("\u200b", "").replace("\ufeff", "").lower())

def load_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = norm(raw)
        if s and not s.startswith("#"):
            lines.append(s)
    return lines

# ---------- загрузка списков ----------
ips_file   = Path("blacklist_ips.txt")
cidrs_file = Path("blacklist_cidrs.txt")
wl_file    = Path("whitelist_ips.txt")     # <— НОВОЕ

blocked_ips  = set(load_lines(ips_file))
blocked_nets = []
for cidr in load_lines(cidrs_file):
    try:
        blocked_nets.append(ip_network(cidr, strict=False))
    except ValueError:
        print(f"⚠️  пропустил некорректную подсеть: {cidr}")

whitelist_ips = set(load_lines(wl_file))    # <— НОВОЕ

print(f"Загружено: {len(blocked_ips)} IP, {len(blocked_nets)} подсетей; "
      f"whitelist {len(whitelist_ips)} IP")  # <— НОВОЕ

# ---------- проверка одного IP ----------
def check_ip(ip_str: str) -> tuple[bool, str]:
    ip_s = norm(ip_str)
    if not ip_s:
        return False, "пустой ввод"
    try:
        ip_obj = ip_address(ip_s)
    except ValueError:
        return False, f"некорректный IP: {ip_s}"

    # 1) приоритет — whitelist
    if ip_s in whitelist_ips:
        return False, "разрешён (whitelist)"

    # 2) точное совпадение в blacklist
    if ip_s in blocked_ips:
        return True, "совпадение по точному IP (blacklist)"

    # 3) попадание в подсеть blacklist
    for net in blocked_nets:
        if ip_obj in net:
            return True, f"совпадение по подсети {net} (blacklist)"

    return False, "не найден в списках"

# ---------- режимы запуска (как было) ----------
def check_interactive():
    target = input("Введите IP или путь к файлу со списком IP: ").strip()
    p = Path(target)
    if p.exists():
        print(f"Проверяю файл: {p}")
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            ok, reason = check_ip(line)
            mark = "⛔" if ok else "✅"
            print(f"{mark} {line.strip()} — {reason}")
    else:
        ok, reason = check_ip(target)
        mark = "⛔" if ok else "✅"
        print(f"{mark} {target} — {reason}")

if __name__ == "__main__":
    check_interactive()


print(f"Загружено: {len(blocked_ips)} IP и {len(blocked_nets)} подсетей; "
      f"whitelist {len(whitelist_ips)} IP")
