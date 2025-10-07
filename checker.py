import random
import time
import requests
import sys
import os
import json
from colorama import Fore, Style, init
import shutil

init(autoreset=True)


def load_config():
    try:
        with open("config.json", "r") as cfg:
            return json.load(cfg)
    except:
        sys.exit()


config = load_config()
webhook_url = config.get("webhookUrl")


def set_console_title(title):
    if sys.platform.startswith("win"):
        import ctypes

        ctypes.windll.kernel32.SetConsoleTitleW(title)


def set_console_size(width, height):
    if sys.platform.startswith("win"):
        os.system(f"mode con: cols={width} lines={height}")


def generate_username(length):
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    first_char = random.choice("abcdefghijklmnopqrstuvwxyz")
    return first_char + "".join(random.choice(chars) for _ in range(length - 1))


def send_to_webhook(username, length):
    if not webhook_url:
        return
    payload = {
        "username": "daN",  # nome da webhook
        "avatar_url": "https://i.pinimg.com/736x/08/e9/bc/08e9bcd17b82ca6bdd51e90cbec90c19.jpg",  # ícone da webhook
        "embeds": [
            {
                "title": "New Gamertag Available!",
                "description": f"`{username}` is **available**",
                "color": 0x2ECC71,
                "thumbnail": {
                    "url": "https://i.pinimg.com/736x/d2/89/55/d28955c587d108a153a9be85e4918163.jpg"
                },
                "fields": [
                    {"name": "type", "value": f"{length} characters", "inline": True}
                ],
            }
        ],
    }
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except:
        pass


def create_file_with_ascii():
    ascii_art = r"""
   ██████╗  █████╗ ███╗   ███╗███████╗████████╗ █████╗  ██████╗ 
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ 
  ██║  ███╗███████║██╔████╔██║█████╗     ██║   ███████║██║  ███╗
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝
           https://github.com/6hax | https://github.com/Dansvn
"""
    with open("Gamertags_Available.txt", "w", encoding="utf-8") as file:
        file.write(ascii_art + "\n")


def center_text(text):
    columns = shutil.get_terminal_size((120, 20)).columns
    centered = ""
    for line in text.splitlines():
        spaces = (columns - len(line)) // 2
        centered += " " * max(spaces, 0) + line + "\n"
    return centered


def animate_banner(text, delay=0.005):
    columns = shutil.get_terminal_size((120, 20)).columns
    lines = text.splitlines()
    for line in lines:
        spaces = (columns - len(line)) // 2
        padded_line = " " * max(spaces, 0) + line
        for char in padded_line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")


def check_gamertags():
    total_checked, available_count, taken_count = 0, 0, 0
    length = int(input(Fore.CYAN + "\n[?] Enter desired username length: "))

    if not os.path.isfile("Gamertags_Available.txt"):
        create_file_with_ascii()

    with open("Gamertags_Available.txt", "a", encoding="utf-8") as file:
        while True:
            username = generate_username(length)
            try:
                response = requests.get(
                    f"https://xboxgamertag.com/search/{username}",
                    headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
                    timeout=10,
                )
                if "Gamertag doesn't exist" in response.text:
                    print(Fore.GREEN + f"[AVAILABLE] {username}")
                    available_count += 1
                    file.write(f"{username}\n")
                    file.flush()
                    send_to_webhook(username, length)
                else:
                    print(Fore.RED + f"[TAKEN] {username}")
                    taken_count += 1
                total_checked += 1
                if total_checked % 40 == 0:
                    print(
                        Fore.YELLOW
                        + f"\n[INFO] Pausing for 1 minute after {total_checked} checks..."
                    )
                    time.sleep(60)
            except:
                time.sleep(2)


def print_banner():
    banner = r"""
    
██╗  ██╗██████╗  ██████╗ ██╗  ██╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
╚██╗██╔╝██╔══██╗██╔═══██╗╚██╗██╔╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
 ╚███╔╝ ██████╔╝██║   ██║ ╚███╔╝     █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
 ██╔██╗ ██╔══██╗██║   ██║ ██╔██╗     ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██╔╝ ██╗██████╔╝╚██████╔╝██╔╝ ██╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                  
made by hax & dan | github.com/6hax
"""
    animate_banner(banner, delay=0.01)


if __name__ == "__main__":
    set_console_title("Gamertag Checker - V1")
    set_console_size(122, 49)
    print_banner()
    check_gamertags()
