# Zeus289 tarafından geliştirilmiştir discord.gg/0289

import os
import sys
import time
import threading
import requests
import json
from colorama import init, Fore, Back, Style

init(autoreset=True)

API_URL = "https://discord.com/api/v9"

tokens = []
current_token_index = 0
active = False
channel_id = ""

os.system('clear' if os.name == 'posix' else 'cls')

print(Fore.GREEN + """
+--------------------------------------------------+
|                                                  |
|                  DISCORD TYPER                   |
|                  created by: Zeus289             |
|               iletişim: discord.gg/0289          |
|                                                  |
+--------------------------------------------------+
""" + Style.RESET_ALL)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.GREEN + """
+--------------------------------------------------+
|                  DISCORD TYPER                   |
|                  created by: Zeus289             |
|               iletişim: discord.gg/0289          |
+--------------------------------------------------+
""" + Style.RESET_ALL)

def get_token_headers(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def check_token(token):
    try:
        response = requests.get(f"{API_URL}/users/@me", headers=get_token_headers(token))
        return response.status_code == 200
    except:
        return False

def ask_tokens():
    global tokens
    
    while True:
        token = input(Fore.YELLOW + "token: " + Style.RESET_ALL).strip()
        if token:
            if check_token(token):
                tokens.append(token)
                print(Fore.GREEN + "✓ Token eklendi!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "✗ Token geçersiz! Yine de ekle? (e/h): " + Style.RESET_ALL, end="")
                if input().lower() == 'e':
                    tokens.append(token)
        
        print(Fore.YELLOW + "Başka token ekle? (y/n): " + Style.RESET_ALL, end="")
        if input().lower() != 'y':
            break

def send_message(token, channel_id, message):
    try:
        response = requests.post(
            f"{API_URL}/channels/{channel_id}/messages",
            headers=get_token_headers(token),
            json={"content": message}
        )
        return response.status_code == 200
    except:
        return False

def flood_mode():
    global active, current_token_index, channel_id
    
    clear_screen()
    print(Fore.CYAN + "=== FLOOD MODE ===" + Style.RESET_ALL)
    
    channel_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    
    if not os.path.exists('messages.txt'):
        with open('messages.txt', 'w') as f:
            f.write("test mesaji 1\ntest mesaji 2")
    
    with open('messages.txt', 'r') as f:
        messages = [line.strip() for line in f if line.strip()]
    
    print(Fore.GREEN + "Flood başlıyor... (Ctrl+C durdurur)")
    active = True
    msg_index = 0
    
    try:
        while active:
            token = tokens[current_token_index]
            msg = messages[msg_index]
            
            if send_message(token, channel_id, msg):
                print(Fore.GREEN + f"✓ {msg[:30]}")
            else:
                print(Fore.RED + "✗ Hata")
                current_token_index = (current_token_index + 1) % len(tokens)
            
            msg_index = (msg_index + 1) % len(messages)
            time.sleep(0.1)
    except KeyboardInterrupt:
        active = False
        main_menu()

def spam_mode():
    global active, current_token_index, channel_id
    
    clear_screen()
    print(Fore.CYAN + "=== SPAM MODE ===" + Style.RESET_ALL)
    
    msg = input(Fore.YELLOW + "Mesaj: " + Style.RESET_ALL).strip()
    count = int(input(Fore.YELLOW + "Adet: " + Style.RESET_ALL).strip())
    channel_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    
    active = True
    sent = 0
    
    try:
        while active and sent < count:
            token = tokens[current_token_index]
            
            if send_message(token, channel_id, msg):
                sent += 1
                print(Fore.GREEN + f"✓ {sent}/{count}")
            else:
                current_token_index = (current_token_index + 1) % len(tokens)
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    
    active = False
    main_menu()

def reaction_mode():
    global active, channel_id
    
    clear_screen()
    print(Fore.CYAN + "=== REACTION MODE ===" + Style.RESET_ALL)
    
    trigger = input(Fore.YELLOW + "Tetikleyici kelime: " + Style.RESET_ALL).strip()
    response = input(Fore.YELLOW + "Cevap: " + Style.RESET_ALL).strip()
    channel_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    
    print(Fore.GREEN + "Reaction mode aktif...")
    active = True
    last_id = None
    
    try:
        while active:
            token = tokens[current_token_index]
            
            try:
                r = requests.get(
                    f"{API_URL}/channels/{channel_id}/messages?limit=3",
                    headers=get_token_headers(token)
                )
                
                if r.status_code == 200:
                    for msg in r.json():
                        if trigger in msg['content'].lower() and msg['id'] != last_id:
                            send_message(token, channel_id, response)
                            print(Fore.GREEN + f"✓ Tepki verildi")
                            last_id = msg['id']
            except:
                pass
            
            time.sleep(1)
    except KeyboardInterrupt:
        active = False
        main_menu()

def show_tokens():
    clear_screen()
    print(Fore.CYAN + "=== TOKEN LISTESI ===" + Style.RESET_ALL)
    for i, t in enumerate(tokens):
        print(f"{i+1}. {t[:15]}...{t[-5:]}")
    input(Fore.YELLOW + "Devam etmek için Enter..." + Style.RESET_ALL)
    main_menu()

def main_menu():
    global active
    active = False
    time.sleep(0.5)
    
    clear_screen()
    print(Fore.BLUE + """
+--------------------------------------------------+
|                    ANA MENU                      |
+--------------------------------------------------+
|  1) Flood Mode (sonsuz txt)                      |
|  2) Spam Mode (tek mesaj)                        |
|  3) Reaction Mode (tepkiye cevap)                |
|  4) Token listesi                                 |
|  5) Yeni token ekle                               |
|  6) Cikis                                         |
+--------------------------------------------------+
    """ + Style.RESET_ALL)
    
    secim = input(Fore.YELLOW + "Secim: " + Style.RESET_ALL).strip()
    
    if secim == '1':
        flood_mode()
    elif secim == '2':
        spam_mode()
    elif secim == '3':
        reaction_mode()
    elif secim == '4':
        show_tokens()
    elif secim == '5':
        ask_tokens()
        main_menu()
    elif secim == '6':
        sys.exit(0)
    else:
        main_menu()

if __name__ == "__main__":
    try:
        ask_tokens()
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nCikiliyor...")
        sys.exit(0)