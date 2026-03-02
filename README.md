# discordtyper

DISCORD TYPER - TOOL'UN TAM ANLATIMI

BU TOOL NE İŞE YARAR?

Discord'da otomatik mesaj göndermek için yapılmış bir araç. 3 farklı modu var:

· Flood Mode (sonsuz mesaj döngüsü)
· Spam Mode (tek mesajı belirli sayıda gönderme)
· Reaction Mode (kelimeye otomatik cevap verme)

KURULUM ADIMLARI

1. Termux'u Güncelle

```bash
pkg update && pkg upgrade -y
```

2. Python ve Git Kur

```bash
pkg install python -y
pkg install git -y
```

3. Gerekli Kütüphaneleri Kur

```bash
pip install requests
pip install colorama
```

4. Tool'u İndir

```bash
git clone https://github.com/zeus289x/discordtyper.git
```

5. Klasöre Gir

```bash
cd discordtyper
```

6. Çalıştır

```bash
python typer.py
```

TOKEN ALMA (EN ÖNEMLİ KISIM)

Token olmadan bu tool çalışmaz. Token almak için 2 yöntem var:

Yöntem 1: Bluecord ile (Telefon için en kolayı)

1. Telefona Bluecord indir (Discord'un modlu hali)
2. Hesabınla giriş yap
3. Sağ üstte profil resmine tıkla
4. Account Switcher'ı bul
5. Hesabının yanındaki üç noktaya tıkla
6. "Copy Token" de, token kopyalanır
7. Termux'a yapıştır

ÖNEMLİ: Token aldıktan sonra Bluecord'dan çıkış yapma! Çıkış yaparsan token sıfırlanır, aldığın token geçersiz olur.

Yöntem 2: Bilgisayardan

1. Discord'u tarayıcıda aç (chrome, opera)
2. F12'ye bas (geliştirici araçları açılır)
3. Network sekmesine tıkla
4. Herhangi bir kanala mesaj yaz
5. "messages" yazan şeye tıkla
6. Sağ tarafta "Authorization" yazan yerdeki uzun kod token'dır

TOKEN GİRME

Tool'u çalıştırınca ilk olarak token sorar:

```
token: 
```

Token'ini yapıştır. Geçerliyse yeşil tik atar.

Sonra sorar: "Ek token eklemek ister misin? (y/n):"

· y yazarsan yeni token girersin
· n yazarsan menüye geçersin

Neden çok token? Bir token hata verirse diğerine geçsin diye.

ANA MENÜ

Tokenleri girdikten sonra ana menü gelir:

```
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
```

MODLARIN DETAYLI ANLATIMI

1. FLOOD MODE (Sonsuz Mesaj Döngüsü)

Bu modda messages.txt dosyasındaki mesajlar sırayla gönderilir, sonsuza kadar devam eder.

Nasıl kullanılır:

· Menüde 1 yaz
· Kanal ID gir
· Program messages.txt'deki mesajları okur
· 0.1 saniye aralıkla gönderir
· Ctrl+C ile durdurursun

messages.txt dosyası:
Tool ilk çalıştığında messages.txt yoksa otomatik oluşturur. İçinde örnek mesajlar olur.

Kendi mesajlarını yazmak için:

```bash
nano messages.txt
```

Dosyayı aç, içindekileri sil, kendi mesajlarını alt alta yaz. Örnek:

```
discord.gg/0289'a bekleriz
Zeus289 yaptı bu tool'u
flood baslıyor
herkese selam
deneme mesajı
```

Kaydet: Ctrl+X, Y, Enter

Sonra tool'u tekrar çalıştır, flood mode'u seç. Mesajlar sırayla gider.

2. SPAM MODE (Tek Mesaj Belirli Sayıda)

Bu modda tek bir mesajı kaç kere yazacağını belirlersin, o kadar gönderir sonra durur.

Nasıl kullanılır:

· Menüde 2 yaz
· Spamlanacak mesajı yaz (örnek: discord.gg/0289)
· Kaç kere gönderileceğini yaz (örnek: 50)
· Kanal ID gir
· Mesajlar gönderilmeye başlar
· Sayı tamamlanınca durur veya Ctrl+C ile durdurabilirsin

3. REACTION MODE (Kelimeye Otomatik Cevap)

Bu modda kanalı izler, birisi belirli bir kelimeyi yazarsa otomatik cevap verir.

Nasıl kullanılır:

· Menüde 3 yaz
· Tepki verilecek kelimeyi yaz (örnek: merhaba)
· Verilecek cevabı yaz (örnek: merhaba kardeş naber)
· Kanal ID gir
· Program kanalı izlemeye başlar (1 saniye aralıkla kontrol eder)
· Birisi "merhaba" yazarsa otomatik "merhaba kardeş naber" yazar
· Kendi mesajlarına tepki vermez
· Ctrl+C ile durdurursun

4. TOKEN LİSTESİ

Menüde 4 yazarsan eklediğin tokenleri gösterir:

· Yeşil tik: geçerli token
· Kırmızı çarpı: geçersiz token

5. YENİ TOKEN EKLE

Menüde 5 yazarsan yeni token ekleyebilirsin.

6. ÇIKIŞ

Menüde 6 yazarsan program kapanır.

KANAL ID NEREDEN BULUNUR?

Discord'da:

1. Ayarlara gir
2. Geliştirici Modu'nu aç (Developer Mode)
3. Kanala sağ tıkla (telefonda basılı tut)
4. "ID'yi Kopyala" (Copy ID) de

Bu ID'yi kanal sorduğunda yapıştır.

ÖNEMLİ BİLGİLER

Hız Sınırı

Program 0.1 saniye bekleme ile çalışır. Çünkü Discord çok hızlı mesaj atarsan seni banlar veya rate-limit yer. Bu hız güvenli sayılır.

Token Patlarsa

Eğer token hata verirse (401, 403 gibi), program otomatik olarak diğer tokena geçer. Bu yüzden birden fazla token eklemek iyidir.

Durdurma

Her modda Ctrl+C basarsan program durur ve ana menüye döner.

Riskler

Bu tool'u kullanırken Discord hesabının banlanma riski vardır. Özellikle çok hızlı ve çok fazla mesaj atarsan ban yersin. Sorumluluk tamamen sende.

SIK KARŞILAŞILAN SORUNLAR

S: Token geçersiz diyor, ne yapmalıyım?
C: Token'i yanlış kopyalamış olabilirsin. Tekrar almayı dene. Bluecord'dan aldıysan çıkış yapmadığından emin ol.

S: messages.txt nerede?
C: Tool'un olduğu klasörde. ls yazarsan görürsün. Yoksa tool çalışınca otomatik oluşur.

S: Kanal ID nereden alınır?
C: Discord'da geliştirici modunu aç, kanala sağ tıkla, ID'yi kopyala.

S: Çok hızlı mesaj atıyor, sorun olur mu?
C: 0.1 saniye ayarlı, bu genelde sorun çıkarmaz. Ama yine de çok abartma.

S: Reaction mode çalışmıyor?
C: Trigger kelimeyi doğru yazdığından emin ol. Büyük-küçük harf duyarlı değil ama yine de kontrol et.

S: Token'ım çalınır mı?
C: Token sadece senin telefonunda durur. Kimse görmez. Ama token'ı kimseyle paylaşma.

DOSYA YAPISI

```
discord-typer/
├── typer.py           (ana program)
├── messages.txt       (flood mesajları)
└── README.md          (bu dosya)
```

İLETİŞİM

Bir sorun olursa veya geliştirme önerin varsa:

Discord: discord.gg/0289
Yapımcı: Zeus289

SON SÖZ

Tool'u kullanırken dikkatli ol. Discord kurallarına aykırı işler yaparsan hesabın gider. Bu tool eğitim amaçlıdır, sorumluluk kullanıcıya aittir.

Kolay gelsin, iyi eğlenceler.
