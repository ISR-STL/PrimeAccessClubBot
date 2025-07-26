if __name__ == "__main__":
    import threading
    import os

    # Porta dinâmica do Railway
    port = int(os.environ.get("PORT", 5000))

    # Thread para rodar o BOT
    def run_bot():
        print("🚀 Iniciando BOT do Telegram...")
        main()  # chama a função principal do bot

    # Thread para rodar o Flask (keep-alive)
    def run_flask():
        print("🌐 Iniciando Flask para manter ativo no Railway...")
        flask_app.run(host="0.0.0.0", port=port)

    # Inicia ambos em paralelo
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_flask).start()
