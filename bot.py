import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# Menyimpan tiket yang sedang dikerjakan
tiket_aktif = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Friday aktif ✅")


async def mulai_inc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah nomor INC diberikan
    if not context.args:
        await update.message.reply_text(
            "Format:\n/inc INC53749470"
        )
        return

    incident = context.args[0].upper()

    # Buat data tiket dengan nilai default
    tiket_aktif[incident] = {
        "incident": incident,
        "close": "",
        "dropcore": "",
        "patchcord": "0",
        "soc": "",
        "pslave": "0",
        "passive18": "0",
        "passive14": "",
        "pigtail": "",
        "adaptor": "0",
        "roset": "0",
        "rj45": "",
        "lan": "0",
    }

    await update.message.reply_text(
        f"✅ Ticket {incident} dibuat.\n\n"
        "Sekarang masukkan data pekerjaan.\n"
        "Contoh:\n"
        "/close ganti dc\n"
        "/dropcore 20M\n"
        "/pslave 2"
    )


async def isi_close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "close",
        "CLOSE"
    )


async def isi_dropcore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "dropcore",
        "DROPCORE"
    )


async def isi_patchcord(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "patchcord",
        "PATCHCORD"
    )


async def isi_soc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "soc",
        "SOC"
    )


async def isi_pslave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "pslave",
        "PSLAVE"
    )


async def isi_passive18(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "passive18",
        "PASSIVE 1|8"
    )


async def isi_passive14(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "passive14",
        "PASSIVE 1|4"
    )


async def isi_pigtail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "pigtail",
        "PIGTAIL"
    )


async def isi_adaptor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "adaptor",
        "ADAPTOR"
    )


async def isi_roset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "roset",
        "ROSET"
    )


async def isi_rj45(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "rj45",
        "RJ 45"
    )


async def isi_lan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await simpan_data(
        update,
        context,
        "lan",
        "LAN"
    )


async def simpan_data(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    nama_data: str,
    nama_tampilan: str,
):
    # Belum ada tiket
    if not tiket_aktif:
        await update.message.reply_text(
            "❌ Belum ada ticket.\n"
            "Gunakan /inc terlebih dahulu."
        )
        return

    # Ambil tiket yang sedang aktif
    incident = list(tiket_aktif.keys())[-1]

    # Cek nilai yang dikirim
    if not context.args:
        await update.message.reply_text(
            f"Format:\n/{update.message.text.split()[0][1:]} nilai"
        )
        return

    # Gabungkan semua argumen menjadi satu teks
    nilai = " ".join(context.args)

    tiket_aktif[incident][nama_data] = nilai

    await update.message.reply_text(
        f"✅ {nama_tampilan}: {nilai}"
    )

async def lihat_tiket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tiket_aktif:
        await update.message.reply_text(
            "❌ Belum ada ticket aktif."
        )
        return

    incident = list(tiket_aktif.keys())[-1]
    tiket = tiket_aktif[incident]

    laporan = f"""/INPUT: {tiket["incident"]}

CLOSE : {tiket["close"]}

DROPCORE: {tiket["dropcore"]}
PATCHCORD: {tiket["patchcord"]}
SOC: {tiket["soc"]}
PSLAVE: {tiket["pslave"]}
PASSIVE 1|8: {tiket["passive18"]}
PASSIVE 1|4: {tiket["passive14"]}
PIGTAIL: {tiket["pigtail"]}
ADAPTOR: {tiket["adaptor"]}
ROSET: {tiket["roset"]}
RJ 45: {tiket["rj45"]}
LAN: {tiket["lan"]}
===================="""

    await update.message.reply_text(laporan)
application = Application.builder().token(TOKEN).build()

application.add_handler(
    CommandHandler("lihat", lihat_tiket)
)
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("inc", mulai_inc))

application.add_handler(CommandHandler("c", isi_close))
application.add_handler(CommandHandler("dc", isi_dropcore))
application.add_handler(CommandHandler("pc", isi_patchcord))
application.add_handler(CommandHandler("soc", isi_soc))
application.add_handler(CommandHandler("pslave", isi_pslave))
application.add_handler(CommandHandler("passive18", isi_passive18))
application.add_handler(CommandHandler("passive14", isi_passive14))
application.add_handler(CommandHandler("pigtail", isi_pigtail))
application.add_handler(CommandHandler("adaptor", isi_adaptor))
application.add_handler(CommandHandler("roset", isi_roset))
application.add_handler(CommandHandler("rj45", isi_rj45))
application.add_handler(CommandHandler("lan", isi_lan))


application.run_polling()