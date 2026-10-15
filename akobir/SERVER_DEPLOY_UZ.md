# 🚀 Telegram Musiqa Botini Serverga Joylash Qo'llanmasi

Ushbu qo'llanmada botingizni istalgan serverga (**Railway, Render, VPS/Ubuntu/Debian, Docker**) 24/7 rejimida xatosiz ishlaydigan qilib joylash bosqichma-bosqich tushuntirilgan.

---

## 🛠 Loyihada Qilingan Barcha Tuzatishlar va Yangilanishlar:

1. **✅ Majburiy obunadagi («Obunani tekshirish») tugmasi tuzatildi:**
   - Oldin foydalanuvchi obuna bo'lib «Obunani tekshirish» (`check_sub`) tugmasini bossa, hech narsa bo'lmay qotib turardi. Endi obunani qayta tekshirib, xush kelibsiz xabari va asosiy menyuni chiqaradi.
2. **✅ HTML Entity va `<>` belgilari sababli yuzaga keladigan xatolar bartaraf etildi:**
   - Musiqa nomi, ijrochi, video tavsifi yoki qo'shiq matnida `<`, `>`, `&` belgilari bo'lsa Telegram `can't parse entities` xatosini berib qo'shiqni yubormasdi. Barcha matnlarga xavfsiz `html.escape` filtri o'rnatildi.
3. **✅ Server xotirasi (RAM) to'lib ketishi (Memory Leak) tuzatildi:**
   - Qidiruv sessiyalari (`SEARCH_CACHE`) va musiqalar keshiga avtomatik chegara (bounded cache) o'rnatildi. Server RAM xotirasi endi cheksiz ko'payib ketmaydi.
4. **✅ Server diski (Disk Space) to'lib qolishidan himoya qilindi:**
   - Har 20 daqiqada `downloads/` papkasidagi eski yuklab olingan fayllarni avtomatik tozalab turuvchi orqa fon jarayoni (`cleanup_temp_files_loop`) qo'shildi.
5. **✅ SQLite "Database is locked" muammosi yo'qotildi:**
   - Ma'lumotlar bazasi yuqori yuklamalarga moslashtirildi: `WAL (Write-Ahead Logging)` rejimi va `15 soniyalik busy timeout` yoqildi. Bir vaqtning o'zida yuzlab foydalanuvchi kirganda ham baza qotmaydi.
6. **✅ Cloud Web Health-Check (`PORT`) qo'shildi:**
   - Render, Railway Web Service yoki Koyeb da `PORT` orqali tekshirish talab qilinadi. Bot endi server portiga javob bera oladi va "Port bind timed out" xatosi bilan to'xtab qolmaydi.
7. **✅ Bot ma'lumotlarini (Username va Ism) avtomatik aniqlash:**
   - Bot ishga tushganda o'zining `@username` ini Telegram API dan avtomatik oladi. `.env` dagi eskirgan usernameni qo'lda almashtirib yurish shart emas.
8. **✅ YouTube Datacenter IP blokirovkasiga qarshi himoya:**
   - yt-dlp uchun `mweb`, `android`, `ios`, `web` mijozlari integratsiya qilindi hamda `cookies.txt` yoki `YOUTUBE_COOKIES` muhit o'zgaruvchisidan foydalanish imkoniyati yaratildi.

---

## 🌐 1-USUL: Railway orqali joylash (Eng oson va tezkor)

1. Loyihani o'z **GitHub** hisobingizga yuklang (push qiling).
   *(Diqqat: `.gitignore` avtomatik ravishda `.env` va `bot.db` ni yashiradi, xavfsiz)*
2. [Railway.app](https://railway.app) saytiga kiring va GitHub orqali kiring (Sign in with GitHub).
3. **New Project** -> **Deploy from GitHub repo** ni bosing va botingiz repozitoriyasini tanlang.
4. Loyiha sozlamalari (**Variables**) bo'limiga o'ting va quyidagi o'zgaruvchilarni qo'shing:
   - `BOT_TOKEN` = `botingiz_tokeni`
   - `ADMINS` = `telegram_id_raqamingiz` (masalan: `8453269531`)
   - `BOT_NAME` = `HitMusic Bot`
   - `GEMINI_API_KEY` = `sizning_gemini_kalitingiz` (ixtiyoriy)
5. **Deploy** tugmasini bosing. Railway `Dockerfile` orqali hamma narsani (Python, FFmpeg) avtomatik o'rnatib, botni ishga tushiradi!

---

## 🌐 2-USUL: Render.com orqali joylash

1. [Render.com](https://render.com) ga kiring.
2. **New +** -> **Background Worker** (yoki **Web Service**) ni tanlang.
3. GitHub repozitoriyangizni ulang.
4. Muhit sifatida **Docker** ni tanlang (loyiha ichidagi `Dockerfile` avtomatik olinadi).
5. **Environment Variables** ga `BOT_TOKEN`, `ADMINS`, `GEMINI_API_KEY` ni kiriting.
6. **Create Service** ni bosing.

---

## 🖥 3-USUL: Shaxsiy Linux VPS Serverda (Ubuntu / Debian) joylash

VPS serveringizga SSH orqali kiring:
```bash
ssh root@serveringiz_ip
```

### Variant A: Docker Compose orqali (Tavsiya etiladi)

1. Serverga Docker va Docker Compose o'rnatilgan bo'lsin:
   ```bash
   apt update && apt install -y docker.io docker-compose-plugin
   ```
2. Loyihani serverga ko'chiring:
   ```bash
   git clone <repozitoriya_manzili> /root/musicbot
   cd /root/musicbot
   ```
3. `.env` faylini yarating va ma'lumotlaringizni kiriting:
   ```bash
   nano .env
   ```
4. Botni orqa fonda ishga tushiring:
   ```bash
   docker compose up -d --build
   ```
5. Loglarni ko'rish:
   ```bash
   docker compose logs -f
   ```

---

### Variant B: Systemd xizmati orqali (Docker siz)

1. Serverda FFmpeg va Python 3 ni o'rnating:
   ```bash
   apt update && apt install -y python3 python3-pip python3-venv ffmpeg
   ```
2. Loyihani sozlang:
   ```bash
   cd /root/akobir
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Tizim xizmatiga qo'shish:
   ```bash
   cp bot.service /etc/systemd/system/bot.service
   systemctl daemon-reload
   systemctl enable bot.service
   systemctl start bot.service
   ```
4. Xizmat holatini tekshirish:
   ```bash
   systemctl status bot.service
   ```

---

## 🍪 Serverda YouTube cheklovlarini (Sign in / 429) aylanib o'tish

Ayrim xorijiy datacenter IP manzillaridan (Hetzner, DigitalOcean va h.k.) YouTube qo'shiq yuklashni cheklashi mumkin.
Buning oldini olish juda oddiy:
1. Kompyuteringizdagi Chrome brauzeriga **Get cookies.txt LOCALLY** kengaytmasini o'rnating.
2. [youtube.com](https://youtube.com) ga kiring va kengaytma orqali `cookies.txt` faylini yuklab oling.
3. Ushbu `cookies.txt` faylini loyihaning bosh papkasiga joylashtiring:
   - Agar Railway/Render ishlatsangiz: fayl ichidagi barcha matnni nusxalab, `YOUTUBE_COOKIES` nomli Environment Variable ga joylashtirib qo'ying.
   - Bot avtomatik ravishda cookies dan foydalanadi va YouTube bloklaridan chetlab o'tadi!
