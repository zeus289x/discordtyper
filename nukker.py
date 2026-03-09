#!/usr/bin/env python3
import os
import sys
import time
import threading
import requests
import json
import random
import webbrowser
import subprocess
import importlib.util
from datetime import datetime

def pip_kontrol_ve_kur():
    gerekli_paketler = ['requests', 'colorama']
    eksik_paketler = []
    
    for paket in gerekli_paketler:
        if importlib.util.find_spec(paket) is None:
            eksik_paketler.append(paket)
    
    if eksik_paketler:
        print(f"\nEksik paketler bulundu: {', '.join(eksik_paketler)}")
        print("Paketler yukleniyor...")
        for paket in eksik_paketler:
            subprocess.check_call([sys.executable, "-m", "pip", "install", paket])
        print("Tum paketler basariyla yüklendi!\n")
        time.sleep(2)
        os.execv(sys.executable, ['python'] + sys.argv)

pip_kontrol_ve_kur()

from colorama import init, Fore, Style
init(autoreset=True)

API_URL = "https://discord.com/api/v9"

tokenler = []
calisan_tokenler = []
aktif = False
kanal_id = ""
sunucu_id = ""
ses_kanal_id = ""
hedef_mesaj_id = ""

def temizle():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.RED + """
______ _____ _______ _______ _ _ ______ _______ ______  
(_____ (_____|_______) (_______) | | (_____ (_______|_____ 
  ____) )_____ _______ _ | |___| |_____) )____ _____) )
 / ____// ___ (_____ | | | |_____ | ____/ ___) | __ /
| (____( (___) ) | | | | _____| | | | |_____|  
|_______)_____/ |_| |_| (_______|_| |_______)_| |_|
                                                                 
    """ + Style.RESET_ALL)
    print(Fore.CYAN + "                    created by: Zeus289" + Style.RESET_ALL)
    print(Fore.YELLOW + "                    discord.gg/0289\n" + Style.RESET_ALL)

def get_headers(token):
    return {
        'Authorization': token.strip(),
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def token_kontrol(token):
    token = token.strip()
    try:
        r = requests.get(f"{API_URL}/users/@me", headers=get_headers(token), timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                'valid': True,
                'username': f"{data.get('username', '')}#{data.get('discriminator', '0000')}",
                'id': data.get('id', ''),
                'email': data.get('email', 'Gizli'),
                'phone': data.get('phone', 'Yok'),
                'token': token
            }
        else:
            return {'valid': False, 'token': token}
    except:
        return {'valid': False, 'token': token}

def tokenleri_yukle_ve_kontrol_et():
    global tokenler, calisan_tokenler
    
    if not os.path.exists('token.txt'):
        with open('token.txt', 'w', encoding='utf-8') as f:
            f.write("# Tokenlerinizi satir satir yazin\n")
        print(Fore.YELLOW + "\ntoken.txt olusturuldu. Tokenleri ekleyip tekrar calistirin." + Style.RESET_ALL)
        input(Fore.YELLOW + "Devam icin Enter..." + Style.RESET_ALL)
        return False
    
    with open('token.txt', 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
    
    print(Fore.CYAN + "\nTokenler kontrol ediliyor..." + Style.RESET_ALL)
    
    gecici_tokenler = []
    gecici_calisan = []
    
    for satir in satirlar:
        token = satir.strip()
        if token and not token.startswith('#'):
            info = token_kontrol(token)
            if info['valid']:
                gecici_tokenler.append(info)
                gecici_calisan.append(info)
                print(Fore.GREEN + f"  {info['username']} - Gecerli" + Style.RESET_ALL)
            else:
                gecici_tokenler.append({'valid': False, 'token': token, 'username': 'GECERSIZ'})
                print(Fore.RED + f"  {token[:20]}... - Gecersiz" + Style.RESET_ALL)
    
    tokenler = gecici_tokenler
    calisan_tokenler = gecici_calisan
    
    print(Fore.YELLOW + f"\n{len(tokenler)} token, {len(calisan_tokenler)} gecerli" + Style.RESET_ALL)
    
    gecersiz_sayisi = len(tokenler) - len(calisan_tokenler)
    if gecersiz_sayisi > 0:
        cevap = input(Fore.MAGENTA + f"\n{gecersiz_sayisi} gecersiz token silinsin mi? (e/h): " + Style.RESET_ALL).lower()
        if cevap == 'e':
            with open('token.txt', 'w', encoding='utf-8') as f:
                for t in calisan_tokenler:
                    f.write(t['token'] + '\n')
            tokenler = calisan_tokenler.copy()
            print(Fore.GREEN + "Gecersiz tokenler silindi!" + Style.RESET_ALL)
    
    return len(calisan_tokenler) > 0

def mesaj_gonder(token, kanal_id, mesaj):
    try:
        r = requests.post(
            f"{API_URL}/channels/{kanal_id}/messages",
            headers=get_headers(token),
            json={"content": mesaj},
            timeout=10
        )
        return r.status_code == 200
    except:
        return False

def geri_sayim(saniye):
    for i in range(saniye, 0, -1):
        print(Fore.YELLOW + f"{i} saniye..." + Style.RESET_ALL, end='\r')
        time.sleep(1)
    print(Fore.GREEN + "BASLADI!        " + Style.RESET_ALL)

def spam_modu():
    global aktif, kanal_id
    
    temizle()
    print(Fore.MAGENTA + "=== SPAM MODU ===" + Style.RESET_ALL)
    print()
    
    if not calisan_tokenler:
        print(Fore.RED + "Hic gecerli token yok!" + Style.RESET_ALL)
        input()
        return
    
    kanal_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    mesaj = input(Fore.YELLOW + "Mesaj: " + Style.RESET_ALL).strip()
    
    try:
        tur = int(input(Fore.YELLOW + "Tur sayisi (0=sonsuz): " + Style.RESET_ALL).strip())
    except:
        tur = 0
    
    print(Fore.RED + "\n10 saniye icinde basliyor!" + Style.RESET_ALL)
    geri_sayim(10)
    
    aktif = True
    sayac = 0
    tur_sayac = 0
    
    print(Fore.GREEN + f"\n{len(calisan_tokenler)} token spam BASLADI!" + Style.RESET_ALL)
    print(Fore.YELLOW + "Durdurmak icin Ctrl+C" + Style.RESET_ALL)
    print("-" * 50)
    
    try:
        while aktif and (tur == 0 or tur_sayac < tur):
            threads = []
            for t in calisan_tokenler:
                thread = threading.Thread(
                    target=lambda: mesaj_gonder(t['token'], kanal_id, mesaj)
                )
                threads.append(thread)
                thread.start()
                sayac += 1
            
            for thread in threads:
                thread.join(timeout=0.1)
            
            tur_sayac += 1
            print(Fore.CYAN + f"Tur {tur_sayac} - {sayac} mesaj gonderildi" + Style.RESET_ALL)
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nSpam durduruldu!" + Style.RESET_ALL)
    
    print(Fore.GREEN + f"\nToplam {sayac} mesaj gonderildi" + Style.RESET_ALL)
    time.sleep(2)

def flood_modu():
    global aktif, kanal_id
    
    temizle()
    print(Fore.MAGENTA + "=== FLOOD MODU ===" + Style.RESET_ALL)
    print()
    
    if not calisan_tokenler:
        print(Fore.RED + "Hic gecerli token yok!" + Style.RESET_ALL)
        input()
        return
    
    kanal_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    
    if not os.path.exists('messages.txt'):
        with open('messages.txt', 'w', encoding='utf-8') as f:
            f.write("Selam\nNasilsin\nNe var ne yok")
    
    with open('messages.txt', 'r', encoding='utf-8') as f:
        mesajlar = [line.strip() for line in f if line.strip()]
    
    if not mesajlar:
        mesajlar = ["test"]
    
    try:
        hiz = float(input(Fore.YELLOW + "Hiz (saniye, 0.1=hizli): " + Style.RESET_ALL).strip() or "0.1")
    except:
        hiz = 0.1
    
    print(Fore.GREEN + f"\nFlood basliyor... ({hiz}s aralik)" + Style.RESET_ALL)
    print(Fore.YELLOW + "Durdurmak icin Ctrl+C" + Style.RESET_ALL)
    print("-" * 50)
    
    aktif = True
    msg_index = 0
    token_index = 0
    toplam = 0
    
    try:
        while aktif:
            token = calisan_tokenler[token_index]['token']
            msg = mesajlar[msg_index]
            
            if mesaj_gonder(token, kanal_id, msg):
                toplam += 1
                print(Fore.GREEN + f"  [{toplam}] {msg[:30]}" + Style.RESET_ALL)
                msg_index = (msg_index + 1) % len(mesajlar)
                token_index = (token_index + 1) % len(calisan_tokenler)
            else:
                print(Fore.RED + f"  Hata" + Style.RESET_ALL)
                token_index = (token_index + 1) % len(calisan_tokenler)
            
            time.sleep(hiz)
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nFlood durduruldu!" + Style.RESET_ALL)
    
    print(Fore.GREEN + f"\nToplam {toplam} mesaj gonderildi" + Style.RESET_ALL)
    time.sleep(2)

def tetik_modu():
    global aktif, kanal_id
    
    temizle()
    print(Fore.MAGENTA + "=== TETIK MODU ===" + Style.RESET_ALL)
    print()
    
    if not calisan_tokenler:
        print(Fore.RED + "Hic gecerli token yok!" + Style.RESET_ALL)
        input()
        return
    
    kanal_id = input(Fore.YELLOW + "Kanal ID: " + Style.RESET_ALL).strip()
    tetik_kelime = input(Fore.YELLOW + "Tetik kelime: " + Style.RESET_ALL).strip()
    cevap = input(Fore.YELLOW + "Cevap mesaji: " + Style.RESET_ALL).strip()
    
    print(Fore.GREEN + f"\n'{tetik_kelime}' araniyor..." + Style.RESET_ALL)
    print(Fore.YELLOW + "Durdurmak icin Ctrl+C" + Style.RESET_ALL)
    print("-" * 50)
    
    aktif = True
    token_index = 0
    son_mesaj_id = None
    
    try:
        while aktif:
            token = calisan_tokenler[token_index]['token']
            
            try:
                r = requests.get(
                    f"{API_URL}/channels/{kanal_id}/messages?limit=10",
                    headers=get_headers(token),
                    timeout=10
                )
                
                if r.status_code == 200:
                    for msg in r.json():
                        if (tetik_kelime.lower() in msg['content'].lower() and 
                            msg['id'] != son_mesaj_id and
                            msg['author']['id'] != calisan_tokenler[0]['id']):
                            
                            if mesaj_gonder(token, kanal_id, cevap):
                                print(Fore.GREEN + f"  {msg['author']['username']}: {msg['content'][:30]} -> cevap verildi" + Style.RESET_ALL)
                                son_mesaj_id = msg['id']
            except:
                pass
            
            token_index = (token_index + 1) % len(calisan_tokenler)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nTetik modu durduruldu!" + Style.RESET_ALL)
    
    time.sleep(2)

class SesBotu:
    def __init__(self, token, username, index):
        self.token = token.strip()
        self.username = username
        self.index = index
        self.baslik = f"Bot-{index}"
        self.aktif = True
    
    def calistir(self, sunucu_id, ses_kanal_id, kamera_acik, mikrofon_acik, oyun_durumu):
        while self.aktif:
            try:
                import websocket
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json", timeout=30)
                
                identify = {
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": "pc"
                        },
                        "presence": {
                            "status": "online",
                            "since": 0,
                            "activities": [],
                            "afk": False
                        }
                    }
                }
                
                if oyun_durumu:
                    identify["d"]["presence"]["activities"] = [{
                        "name": oyun_durumu,
                        "type": 0
                    }]
                
                ws.send(json.dumps(identify))
                
                result = ws.recv()
                hello_data = json.loads(result)
                heartbeat_interval = hello_data["d"]["heartbeat_interval"] / 1000
                
                time.sleep(2)
                
                voice_state = {
                    "op": 4,
                    "d": {
                        "guild_id": str(sunucu_id),
                        "channel_id": str(ses_kanal_id),
                        "self_mute": not mikrofon_acik,
                        "self_deaf": False,
                        "self_video": kamera_acik
                    }
                }
                ws.send(json.dumps(voice_state))
                
                durum = []
                if mikrofon_acik: durum.append("Mik Acik")
                else: durum.append("Mik Kapali")
                if kamera_acik: durum.append("Kamera Acik")
                if oyun_durumu: durum.append(oyun_durumu)
                
                print(Fore.GREEN + f"  {self.baslik} {self.username} ses kanalinda! {' | '.join(durum)}" + Style.RESET_ALL)
                
                last_heartbeat = time.time()
                
                while self.aktif:
                    try:
                        if time.time() - last_heartbeat > heartbeat_interval:
                            ws.send(json.dumps({"op": 1, "d": None}))
                            last_heartbeat = time.time()
                        
                        ws.settimeout(heartbeat_interval + 5)
                        try:
                            result = ws.recv()
                        except:
                            pass
                        
                        time.sleep(1)
                    except:
                        break
                
                ws.close()
                
            except Exception as e:
                print(Fore.YELLOW + f"  {self.baslik} yeniden baglaniyor..." + Style.RESET_ALL)
                time.sleep(5)
                continue

def ses_modu():
    temizle()
    print(Fore.MAGENTA + "=== SES MODU ===" + Style.RESET_ALL)
    print()
    
    if not calisan_tokenler:
        print(Fore.RED + "Hic gecerli token yok!" + Style.RESET_ALL)
        input()
        return
    
    sunucu_id = input(Fore.YELLOW + "Sunucu ID: " + Style.RESET_ALL).strip()
    ses_kanal_id = input(Fore.YELLOW + "Ses Kanali ID: " + Style.RESET_ALL).strip()
    
    kamera = input(Fore.YELLOW + "Kamera acilsin mi? (e/h): " + Style.RESET_ALL).lower() == 'e'
    mikrofon = input(Fore.YELLOW + "Mikrofon acilsin mi? (e/h): " + Style.RESET_ALL).lower() == 'e'
    
    oyun_durumu = None
    if input(Fore.YELLOW + "Oyun durumu gozuksun mu? (e/h): " + Style.RESET_ALL).lower() == 'e':
        oyun_durumu = input(Fore.YELLOW + "Oyun adi: " + Style.RESET_ALL).strip()
    
    print(Fore.GREEN + f"\n{len(calisan_tokenler)} token ses kanalina ekleniyor..." + Style.RESET_ALL)
    print(Fore.RED + "Durdurmak icin Ctrl+C\n" + Style.RESET_ALL)
    
    botlar = []
    for i, t in enumerate(calisan_tokenler, 1):
        bot = SesBotu(t['token'], t['username'], i)
        thread = threading.Thread(target=bot.calistir, args=(sunucu_id, ses_kanal_id, kamera, mikrofon, oyun_durumu))
        thread.daemon = True
        thread.start()
        botlar.append(bot)
        time.sleep(random.uniform(2, 4))
    
    print(Fore.GREEN + f"\n{len(calisan_tokenler)} ses botu baslatildi!" + Style.RESET_ALL)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nSes botlari durduruluyor..." + Style.RESET_ALL)
        for bot in botlar:
            bot.aktif = False
        time.sleep(3)

def tepkileri_al(token, kanal_id, mesaj_id):
    try:
        r = requests.get(
            f"{API_URL}/channels/{kanal_id}/messages/{mesaj_id}",
            headers=get_headers(token),
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if 'reactions' in data:
                return [r['emoji']['name'] for r in data['reactions']]
        return []
    except:
        return []

def tepki_ekle(token, kanal_id, mesaj_id, emoji):
    try:
        r = requests.put(
            f"{API_URL}/channels/{kanal_id}/messages/{mesaj_id}/reactions/{emoji}/@me",
            headers=get_headers(token),
            timeout=10
        )
        return r.status_code == 204
    except:
        return False

def haha_modu():
    global sunucu_id
    
    temizle()
    print(Fore.MAGENTA + "=== HAHA MODU ===" + Style.RESET_ALL)
    print()
    
    if not calisan_tokenler:
        print(Fore.RED + "Hic gecerli token yok!" + Style.RESET_ALL)
        input()
        return
    
    sunucu_id = input(Fore.YELLOW + "Sunucu ID: " + Style.RESET_ALL).strip()
    
    print(Fore.GREEN + f"\n{len(calisan_tokenler)} token ile haha modu baslatiliyor..." + Style.RESET_ALL)
    print(Fore.YELLOW + "Her 30 saniyede bir sunucudaki son mesajlar kontrol edilecek" + Style.RESET_ALL)
    print(Fore.RED + "Durdurmak icin Ctrl+C\n" + Style.RESET_ALL)
    
    token_index = 0
    islenen_mesajlar = set()
    
    try:
        while True:
            token = calisan_tokenler[token_index]['token']
            
            try:
                r = requests.get(
                    f"{API_URL}/guilds/{sunucu_id}/channels",
                    headers=get_headers(token),
                    timeout=10
                )
                
                if r.status_code == 200:
                    kanallar = r.json()
                    metin_kanallari = [k for k in kanallar if k['type'] == 0]
                    
                    for kanal in metin_kanallari[:5]:
                        try:
                            r2 = requests.get(
                                f"{API_URL}/channels/{kanal['id']}/messages?limit=10",
                                headers=get_headers(token),
                                timeout=10
                            )
                            
                            if r2.status_code == 200:
                                for msg in r2.json():
                                    if msg['id'] in islenen_mesajlar:
                                        continue
                                    
                                    tepkiler = tepkileri_al(token, kanal['id'], msg['id'])
                                    
                                    if tepkiler:
                                        emoji = random.choice(tepkiler)
                                        if tepki_ekle(token, kanal['id'], msg['id'], emoji):
                                            print(Fore.GREEN + f"  #{kanal['name']} - {msg['author']['username']}: {msg['content'][:20]} -> +{emoji}" + Style.RESET_ALL)
                                            islenen_mesajlar.add(msg['id'])
                                        
                                        time.sleep(random.uniform(1, 3))
                        except:
                            continue
                
            except Exception as e:
                print(Fore.RED + f"  Hata: {e}" + Style.RESET_ALL)
            
            token_index = (token_index + 1) % len(calisan_tokenler)
            
            for i in range(30):
                time.sleep(1)
                print(Fore.CYAN + f"Sonraki tarama: {30-i} saniye" + Style.RESET_ALL, end='\r')
            print()
            
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nHaha modu durduruldu!" + Style.RESET_ALL)
        time.sleep(2)

def zeus289_panel():
    temizle()
    print(Fore.CYAN + """
══════════════════════════════════════════════
         ZEUS289 COMMUNITY PANEL              
══════════════════════════════════════════════
  Web sitemize yonlendiriliyorsunuz...        
                                              
  https://289community.xyz/zeus289            
                                              
  Telegram: @zeus289                          
  Discord: discord.gg/0289                    
══════════════════════════════════════════════
""" + Style.RESET_ALL)
    
    webbrowser.open("https://289community.xyz/zeus289")
    input(Fore.YELLOW + "\nDevam etmek icin Enter..." + Style.RESET_ALL)

def ana_menu():
    while True:
        temizle()
        print(Fore.WHITE + """
┌──────────────────────────────────────────────┐
│            ANA MENU                           │
├──────────────────────────────────────────────┤
│  1. Spam Modu (Coklu Token Ayni Anda)        │
│  2. Flood Modu (messages.txt Dongusu)        │
│  3. Tetik Modu (Kelimaye Tepki)              │
│  4. Token Check & Add                         │
│  5. Ses Modu (Kanal + Kamera + Mik + Oyun)   │
│  6. Haha Modu (Tum Mesajlarin Tepkileri)     │
│  7. Zeus289 Panel                             │
│  8. Cikis                                      │
└──────────────────────────────────────────────┘
        """ + Style.RESET_ALL)
        
        print(Fore.YELLOW + f"{len(calisan_tokenler)} gecerli token" + Style.RESET_ALL)
        secim = input(Fore.CYAN + "\nSeciminiz: " + Style.RESET_ALL).strip()
        
        if secim == "1":
            spam_modu()
        elif secim == "2":
            flood_modu()
        elif secim == "3":
            tetik_modu()
        elif secim == "4":
            tokenleri_yukle_ve_kontrol_et()
        elif secim == "5":
            ses_modu()
        elif secim == "6":
            haha_modu()
        elif secim == "7":
            zeus289_panel()
        elif secim == "8":
            print(Fore.RED + "\nCikiliyor... created by: Zeus289" + Style.RESET_ALL)
            sys.exit(0)

if __name__ == "__main__":
    try:
        tokenleri_yukle_ve_kontrol_et()
        ana_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nCikiliyor... created by: Zeus289" + Style.RESET_ALL)
        sys.exit(0)