# ===============================
# 📱 Chatbot Administrasi Kepegawaian Puskesmas Sungai 9
# Versi Siap Deploy Render ✅
# ===============================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    CallbackQueryHandler, ContextTypes
)
import json, os

# ========== KONFIGURASI ==========
BOT_TOKEN = "8203384752:AAEiGSxEPYoaG7pl5_42s7qZJBoURdcgBxw"
ADMIN_ID = 1293418119
DATA_FILE = "data_statistik.json"

# ========== INISIALISASI FILE DATA ==========
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": [], "interactions": 0, "feedback": []}, f)

def update_statistics(user_id):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if user_id not in data["users"]:
        data["users"].append(user_id)
    data["interactions"] += 1
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ========== MENU UTAMA ==========
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📈 Kenaikan Pangkat", callback_data="pangkat")],
        [InlineKeyboardButton("🏖️ Cuti", callback_data="cuti")],
        [InlineKeyboardButton("📘 Panduan Penggunaan Chatbot", callback_data="panduan")],
        [InlineKeyboardButton("☎️ Hubungi Admin", callback_data="admin")],
    ]
    await query.edit_message_text(
        "🏠 *Menu Utama*\n\nSilakan pilih layanan administrasi yang ingin kamu urus 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== PESAN PEMBUKA ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    update_statistics(user.id)
    await update.message.reply_text(
        "😄 Hai! Sebelum mulai, ucapkan salam atau selamat pagi dulu dong, "
        "dan jangan lupa sebutin nama kamu siapa?"
    )

# ========== RESPON UCAPAN SALAM ==========
async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    update_statistics(user.id)
    name = text.split()[-1].capitalize() if len(text.split()) > 1 else user.first_name
    context.user_data["name"] = name
    context.user_data["greeting"] = text.split()[0].capitalize()
    await update.message.reply_text(
        f"☀️ {context.user_data['greeting']} juga, {name}!\n"
        "Aku asisten virtual administrasi kepegawaian Puskesmas Sungai 9.\n\n"
        "Mau urus administrasi apa hari ini?\n"
        "Aku bisa bantuin kamu dengan cepat dan tepat 💪"
    )
    await show_main_menu(update, context)

# ========== MENU UTAMA (TAMPIL DARI SALAM) ==========
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Kenaikan Pangkat", callback_data="pangkat")],
        [InlineKeyboardButton("🏖️ Cuti", callback_data="cuti")],
        [InlineKeyboardButton("📘 Panduan Penggunaan Chatbot", callback_data="panduan")],
        [InlineKeyboardButton("☎️ Hubungi Admin", callback_data="admin")],
    ]
    await update.message.reply_text(
        "Pilih jenis layanan administrasi yang ingin kamu urus 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== SUBMENU PANGKAT ==========
async def pangkat_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🪶 Reguler", callback_data="pangkat_reguler")],
        [InlineKeyboardButton("🧾 Fungsional", callback_data="pangkat_fungsional")],
        [InlineKeyboardButton("🏛️ Struktural", callback_data="pangkat_struktural")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        "📈 Jenis Kenaikan Pangkat yang tersedia:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== DETAIL PANGKAT ==========
async def pangkat_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    jenis = query.data.split("_")[1]
    update_statistics(query.from_user.id)
    data = {
        "reguler": (
            "📋 *Kenaikan Pangkat Reguler*\n\n"
            "📌 *Syarat:*\n"
            "- Sudah 4 Tahun dalam pangkat terakhir\n"
            "- Fotocopy SK terakhir (legalisir)\n"
            "- SKP 2 tahun terakhir bernilai baik\n\n"
            "🗂️ *Berkas:*\n"
            "- Nota Usul\n- Surat Pengantar\n- SK Pangkat terakhir\n"
            "- SK CPNS & PNS (untuk KP pertama)"
        ),
        "fungsional": (
            "📋 *Kenaikan Pangkat Fungsional*\n\n"
            "📌 *Syarat:*\n"
            "- Fotocopy SK terakhir (legalisir)\n"
            "- SK Jabatan Fungsional (legalisir)\n"
            "- SKP 2 tahun terakhir bernilai baik\n"
            "- Penilaian Angka Kredit (PAK)\n\n"
            "🗂️ *Berkas:*\n"
            "- Nota Usul\n- Surat Pengantar\n- SK Pangkat terakhir\n"
            "- SK Jabatan terakhir\n- SKP & PPK 2 tahun terakhir\n- Asli PAK"
        ),
        "struktural": (
            "📋 *Kenaikan Pangkat Struktural*\n\n"
            "📌 *Syarat:*\n"
            "- Sudah 4 Tahun dalam pangkat terakhir\n"
            "- Fotocopy SK terakhir (legalisir)\n"
            "- SK Jabatan & SK Pelantikan\n"
            "- SPMT & SKP 2 tahun terakhir bernilai baik"
        ),
    }
    keyboard = [
        [InlineKeyboardButton("📋 Langkah Pengajuan", callback_data=f"langkah_{jenis}")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="pangkat")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        text=data[jenis],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== CUTI ==========
async def cuti_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🌴 Tahunan", callback_data="cuti_tahunan")],
        [InlineKeyboardButton("🤒 Sakit", callback_data="cuti_sakit")],
        [InlineKeyboardButton("🚨 Alasan Penting", callback_data="cuti_penting")],
        [InlineKeyboardButton("🤰 Melahirkan", callback_data="cuti_melahirkan")],
        [InlineKeyboardButton("🧳 Besar", callback_data="cuti_besar")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Bersama", callback_data="cuti_bersama")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        "🏖️ Jenis Cuti yang tersedia:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== DETAIL CUTI ==========
async def cuti_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    jenis = query.data.split("_")[1]
    update_statistics(query.from_user.id)
    deskripsi = {
        "tahunan": "• Diberikan setelah 1 tahun bekerja\n• Maksimal 12 hari kerja per tahun.",
        "sakit": "• 1–14 hari wajib surat dokter\n• >14 hari wajib surat dokter pemerintah\n• Maksimal 1 tahun (bisa diperpanjang).",
        "penting": "• Keluarga inti meninggal/sakit keras\n• Perkawinan, istri melahirkan, musibah\n• Maksimal 1 bulan.",
        "melahirkan": "• Untuk anak ke-1 sampai ke-3 (maks. 3 bulan)\n• Anak ke-4 dst: diberikan cuti besar.",
        "besar": "• Masa kerja ≥5 tahun berturut-turut\n• Maksimal 3 bulan.",
        "bersama": "• Mengacu pada Keputusan Presiden\n• Tidak memotong cuti tahunan.",
    }
    keyboard = [
        [InlineKeyboardButton("📋 Langkah Pengajuan", callback_data=f"langkah_{jenis}")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="cuti")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        f"📋 *Cuti {jenis.capitalize()}*\n\n{deskripsi[jenis]}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== LANGKAH PENGAJUAN ==========
async def langkah_pengajuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    jenis = query.data.split("_")[1]
    if jenis in ["tahunan", "sakit", "penting", "melahirkan", "besar", "bersama"]:
        back_callback = "cuti"
        title = f"Cuti {jenis.capitalize()}"
    else:
        back_callback = "pangkat"
        title = f"Kenaikan Pangkat {jenis.capitalize()}"
    keyboard = [
        [InlineKeyboardButton("⬅️ Kembali", callback_data=back_callback)],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        f"🪜 *Langkah Pengajuan {title}*\n"
        "1️⃣ Siapkan berkas yang dibutuhkan\n"
        "2️⃣ Serahkan ke bagian kepegawaian\n"
        "3️⃣ Tunggu proses verifikasi dan penerbitan SK ✅",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ========== PANDUAN & ADMIN ==========
async def panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📘 *Panduan Penggunaan Chatbot:*\n\n"
        "1️⃣ Ketik /start untuk memulai\n"
        "2️⃣ Pilih layanan yang ingin kamu urus\n"
        "3️⃣ Ikuti langkah-langkah yang tersedia\n"
        "4️⃣ Gunakan tombol kembali untuk navigasi ⬅️",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]]),
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "☎️ *Hubungi Admin TU:*\nKlik tautan berikut untuk menghubungi admin:\n"
        "[t.me/minsei9](https://t.me/minsei9)",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]]),
    )

# ========== STATISTIK ==========
async def statistik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 Hanya admin yang bisa melihat statistik.")
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    total_users = len(data["users"])
    total_interactions = data["interactions"]
    await update.message.reply_text(
        f"📊 *Laporan Penggunaan Chatbot*\n\n"
        f"👥 Total Pengguna Unik: {total_users}\n"
        f"💬 Total Interaksi: {total_interactions}\n",
        parse_mode="Markdown"
    )

# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("statistik", statistik))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greeting))
    app.add_handler(CallbackQueryHandler(pangkat_menu, pattern="^pangkat$"))
    app.add_handler(CallbackQueryHandler(cuti_menu, pattern="^cuti$"))
    app.add_handler(CallbackQueryHandler(pangkat_detail, pattern="^pangkat_"))
    app.add_handler(CallbackQueryHandler(cuti_detail, pattern="^cuti_"))
    app.add_handler(CallbackQueryHandler(langkah_pengajuan, pattern="^langkah_"))
    app.add_handler(CallbackQueryHandler(panduan, pattern="^panduan$"))
    app.add_handler(CallbackQueryHandler(admin, pattern="^admin$"))
    app.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    print("🚀 Bot aktif di Render...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
