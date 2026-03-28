import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask('')
@app.route('/')
def home(): return "Bot MBDM Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None 

def pegar_giro():
    try:
          url = "https://blaze.com"
          headers = {"User-Agent": "Mozilla/5.0"}
          r = requests.get(url, headers=headers, timeout=15)
          if r.status_code == 200: return r.json()
          return None
    except: return None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO MBDM ATIVADO!")
    while True:
        try:
            giro = pegar_giro()
            if giro and giro.get('id') != ultimo_id_processado:
                num = int(giro['value'])
                ultimo_id_processado = giro['id']
                print(f"Novo número: {num}")
                if num in [10, 12]: bot.send_message(CHAT_ID, "🚨 **SINAL: PRETO ⚫**")
                elif num == 0: bot.send_message(CHAT_ID, "💎 **BRANCO (0)!**")
            time.sleep(8)
        except: time.sleep(10)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.send_message(CHAT_ID, "✅ **Bot MBDM Iniciado com Sucesso!**")
    monitorar()
