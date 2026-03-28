import telebot
import requests
import os
import time
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB ---
app = Flask('')
@app.route('/')
def home(): return "Bot Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)

def monitorar():
    print("🚀 MONITORAMENTO ATIVADO!")
    ultimo_id = None
    while True:
        try:
            # URL Direta da API
            r = requests.get("https://blaze.com", timeout=10)
            if r.status_code == 200:
                dados = r.json()
                if dados and dados[0]['id'] != ultimo_id:
                    num = int(dados[0]['value'])
                    ultimo_id = dados[0]['id']
                    cor = "🔴 VERMELHO" if num <= 7 else "⚫ PRETO"
                    if num == 0: cor = "⚪ BRANCO"
                    
                    bot.send_message(CHAT_ID, f"🎲 **Blaze Giro:** {num}\n🎯 Cor: {cor}")
            time.sleep(10)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(15)

if __name__ == "__main__":
    Thread(target=run).start()
    # MENSAGEM DE TESTE FORÇADA
    try:
        bot.send_message(CHAT_ID, "✅ **BOT CONECTADO COM SUCESSO!**")
    except Exception as e:
        print(f"ERRO TELEGRAM: {e}")
    monitorar()
