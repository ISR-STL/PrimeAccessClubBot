import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Configurações do BOT ---
BOT_TOKEN = "8046727069:AAF6wzLZycKZSYOCkx-TJLSkIjRzq7M0a9I"
GROUP_ID = -4823572709
INTERVALO_ENVIO = 3600  # intervalo em segundos (1 hora)

# --- Funções do Bot ---
async def gerar_mensagem_en():
    return "✅ Mensagem automática do bot!"

async def envio_automatico(context: ContextTypes.DEFAULT_TYPE):
    msg = await gerar_mensagem_en()
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=msg,
        disable_web_page_preview=True
    )

async def start_auto_posting(application):
    job_queue = application.job_queue
    job_queue.run_repeating(envio_automatico, interval=INTERVALO_ENVIO, first=5)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot de envio automático ativado para o grupo!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    # Iniciar envio automático
    app.post_init(lambda _: asyncio.create_task(start_auto_posting(app)))

    print("✅ BOT ONLINE com envio automático em grupo!")
    app.run_polling()

# --- Servidor Flask para manter Railway ativo ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot está rodando no Railway!"

if __name__ == "__main__":
    # Executa Flask em paralelo para manter o Railway ativo
    import threading
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=5000)).start()

    # Executa o bot
    main()
