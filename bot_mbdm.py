import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread
from datetime import datetime

# --- SERVIDOR WEB ---
app = Flask('')
@app.route('/')
def home(): return "Bot MBDM Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"

bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None 

def pegar_giro():
    try:
        url = "https://blaze.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            dados = r.json()
            return dados[0]
        return None
    except:
        return None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO MBDM ATIVADO!")
    while True:
        try:
            giro = pegar_giro()
            if giro and giro.get('id') != ultimo_id_processado:
                num = int(giro['value'])
                ultimo_id_processado = giro['id']
                hora = datetime.now().strftime('%H:%M:%S')
                print(f"[{hora}] Novo número: {num}")

                if num == 10 or num == 12:
                    bot.send_message(CHAT_ID, f"🚨 **SINAL: PRETO ⚫**\n🔄 G1", parse_mode="Markdown")
                elif num == 11 or num == 8:
                    bot.send_message(CHAT_ID, f"⚠️ **ALERTA: {num}**\n🎯 Foco: **PRETO ⚫**", parse_mode="Markdown")
                elif num == 1:
                    bot.send_message(CHAT_ID, f"⚠️ **ALERTA: {num}**\n🎯 Foco: **VERMELHO 🔴**", parse_mode="Markdown")
                elif num == 0:
                    bot.send_message(CHAT_ID, "💎 **BRANCO (0) NA TELA!**", parse_mode="Markdown")
            time.sleep(8)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)
if __name__ == "__main__":
    # Abre a porta correta para o Render não desligar o bot
    import os
    port = int(os.environ.get("PORT", 8080))
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=port))
    t.daemon = True
    t.start()
    
    # Envia a mensagem e inicia o monitoramento
    bot.send_message(CHAT_ID, "✅ **Bot MBDM Iniciado com Sucesso!**")
    monitorar()
