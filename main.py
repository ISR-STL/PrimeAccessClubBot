import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8046727069:AAF6wzLZycKZSYOCkx-TJLSkIjRzq7M0a9I"

# ✅ CONFIGURAÇÕES
GROUP_ID = -1001234567890  # <-- depois vamos colocar o ID do seu grupo
INTERVALO_ENVIO = 900  # 900s = 15min

MAX_VAGAS = 500
vagas_atual = 327  # Exemplo inicial, depois conectaremos com Google Forms

forms_link = "https://forms.gle/5sJNUBMTusfRfxqSA"

# ✅ MENSAGENS PT/EN COM CONTADOR
def gerar_mensagem_pt():
    if vagas_atual < MAX_VAGAS:
        return f"""
🚨 **PRÉ-VENDA EXPRESS – SOMENTE 48 HORAS!** 🚨

🔥 **SoByen (SBN)** – Token do agronegócio digital com escassez programada  

✅ **Preço pré-venda:** US$ 0,01  
✅ **Listagem:** US$ 0,02 (lucro imediato 100%)  
✅ **Compra mínima:** US$ 5 | **Máxima:** US$ 1.000  
✅ **Pagamento:** BNB (Rede BSC)

📊 **{vagas_atual}/{MAX_VAGAS} vagas já preenchidas! Restam {MAX_VAGAS - vagas_atual} vagas!**

👉 **Whitelist (limitada aos 500 primeiros):**  
{forms_link}
"""
    else:
        return f"""
✅ **Whitelist ENCERRADA!**
Todas as **{MAX_VAGAS} vagas foram preenchidas.**

⚠️ **Abrimos lista de espera para a próxima rodada!**
👉 Cadastre-se aqui: {forms_link}
"""

def gerar_mensagem_en():
    if vagas_atual < MAX_VAGAS:
        return f"""
🚨 **FLASH PRE-SALE – ONLY 48 HOURS!** 🚨

🔥 **SoByen (SBN)** – The digital agribusiness token with programmed scarcity  

✅ **Pre-sale price:** US$ 0.01  
✅ **Listing price:** US$ 0.02 (instant 100% profit)  
✅ **Min:** US$ 5 | **Max:** US$ 1,000  
✅ **Payment:** BNB (BSC Network)

📊 **{vagas_atual}/{MAX_VAGAS} spots already taken! Only {MAX_VAGAS - vagas_atual} left!**

👉 **Whitelist (limited to first 500 users):**  
{forms_link}
"""
    else:
        return f"""
✅ **Whitelist CLOSED!**
All **{MAX_VAGAS} spots are filled.**

⚠️ **Waiting list is now OPEN for the next round!**
👉 Sign up here: {forms_link}
"""

# ✅ Função de envio automático alternando PT/EN
async def envio_automatico(context: ContextTypes.DEFAULT_TYPE):
    global vagas_atual
    # Alternar mensagem PT/EN a cada envio
    if vagas_atual % 2 == 0:
        msg = gerar_mensagem_pt()
    else:
        msg = gerar_mensagem_en()

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

if __name__ == "__main__":
    main()