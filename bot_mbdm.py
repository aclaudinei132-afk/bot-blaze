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
            # URL DA API CORRIGIDA (O SEGREDO)
            url = "https://blaze.com"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                dados = r.json()
                # O [0] garante que pegamos o giro mais atual da lista
                giro_atual = dados[0]
                
                if giro_atual['id'] != ultimo_id:
                    num = int(giro_atual['value'])
                    ultimo_id = giro_atual['id']
                    
                    # Define a cor do sinal
                    cor_emoji = "🔴 VERMELHO" if num <= 7 else "⚫ PRETO"
                    if num == 0: cor_emoji = "⚪ BRANCO"
                    
                    # Envia a mensagem para o Telegram
                    msg = f"🎲 **Novo Giro Blaze!**\n\n🎯 Número: **{num}**\n🎨 Cor: **{cor_emoji}**"
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                    print(f"Sinal enviado: {num} - {cor_emoji}")

            time.sleep(10)
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
            time.sleep(15)

if __name__ == "__main__":
    Thread(target=run).start()
    # MENSAGEM DE TESTE
    try:
        bot.send_message(CHAT_ID, "✅ **BOT CONECTADO E MONITORANDO A BLAZE!**")
    except:
        pass
    monitorar()
