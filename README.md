# Mentor Bahasa Inggris Virtual (AI Agent) 🎓

Asisten & Mentor belajar Bahasa Inggris virtual berbasis AI yang ditenagai oleh **Google Gemini 2.5/3.5 Flash**, **Supabase**, dan **Python Telegram Bot**.

---

## 📱 Panduan Penggunaan Bot di Telegram

Bot ini dapat langsung diakses oleh siapa saja di aplikasi Telegram tanpa perlu instalasi apapun di HP/Laptop mereka.

### 1. Cara Menemukan Bot
1. Buka aplikasi **Telegram** (di HP / Web / Desktop).
2. Di kolom pencarian (*Search*), ketik username bot:
   👉 [**@AiMentorInggrisBot**](https://t.me/AiMentorInggrisBot)
3. Klik tombol **`START`** (atau kirim pesan `/start`) untuk mendaftarkan akun.

---

### 2. Panduan Fitur & Contoh Pesan

| Fitur | Cara Pakai / Contoh Pesan | Yang Akan Diterima Pengguna |
|---|---|---|
| **Pendaftaran / Menu** | `/start` | Sambutan ramah & panduan cara menggunakan bot. |
| **Latihan Reading** | `buatkan soal reading tentang liburan` | Teks bacaan pendek dalam Bahasa Inggris + 3 pertanyaan pemahaman. |
| **Cek Grammar (Writing)** | `periksa: I goes to school yesterday` | Analisis kesalahan tata bahasa, kalimat yang benar, dan penjelasan ramah. |
| **Latihan Listening** | `buatkan latihan listening tentang memesan kopi` | **File Audio (Text-to-Speech)** percakapan 2 orang (*Puck* & *Kore*) + daftar pertanyaan kuis. |
| **Latihan Speaking** | `buatkan tugas speaking` | Instruksi tema berbicara, panduan durasi (~1 menit), dan contoh kalimat pembuka. |
| **Evaluasi Suara (Speaking)** | Kirim **Voice Note (VN)** berbicara bahasa Inggris | Skor pelafalan (*pronunciation*), feedback sandwich, dan tips perbaikan cara membaca kata. |
| **Tips Belajar Harian** | `kasih tips belajar` | Tips dan motivasi praktis belajar Bahasa Inggris harian. |
| **Laporan Belajar (PDF)** | `/report` | **File Dokumen PDF** berisi rangkuman aktivitas belajar dan penilaian selama 7 hari terakhir. |

---

### 3. Notifikasi Pengingat Otomatis ⏰
Bot secara otomatis akan mengirimkan pesan motivasi dan pengingat latihan setiap hari pada pukul **06:00 WIB** kepada semua pengguna yang sudah terdaftar.


---

## 🛠️ Panduan Developer: Menjalankan Bot Sendiri

### 1. Kebutuhan Sistem (*Prerequisites*)
- Python `>= 3.12`
- Package manager [`uv`](https://docs.astral.sh/uv/)
- Akun Google AI Studio (Gemini API Key)
- Akun Supabase (Database URL & Anon Key)
- Akun Telegram BotFather (Bot Token)

### 2. Konfigurasi Lingkungan (`.env`)
Buat file `.env` di root direktori dengan isi:
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL="gemini-3.5-flash"
GEMINI_MODEL_TTS="gemini-2.5-flash-preview-tts"

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Menjalankan Aplikasi

```bash
# Menjalankan Telegram Bot
uv run main.py

# Menjalankan Mode Terminal CLI (tanpa Telegram)
uv run main.py --cli
```

---

## ☁️ Deployment Cloud (24/7 Nonstop)

Proyek ini telah dikonfigurasi dan siap untuk di-deploy ke **Railway**, **Render**, **Koyeb**, atau **VPS**:
- `railway.toml`: Konfigurasi worker & restart policy.
- `Procfile`: Definisi proses `worker: uv run main.py`.
- `Dockerfile`: Multi-stage build menggunakan `python:3.12-slim` + `uv`.
- `.dockerignore` & `.gitignore`: Pengamanan kredensial dan cache media.
