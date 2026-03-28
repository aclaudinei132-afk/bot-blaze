import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO SERVIDOR PARA O RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Bot MBDM Online"

def run():
    # Isso resolve o erro de "No open ports"
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES DO BOT ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None 

def pegar_giro():
    try:
        # URL da API da Blaze corrigida
        url = "https://blaze.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO ATIVADO!")
    while True:
        try:
            dados = pegar_giro()
            # Pega o primeiro item da lista de resultados
            if dados and len(dados) > 0:
                giro = dados[0]
                if giro.get('id') != ultimo_id_processado:
                    num = int(giro['value'])
                    ultimo_id_processado = giro['id']
                    
                    # Envia sinal simples para teste
                    if num == 0:
                        bot.send_message(CHAT_ID, "💎 **BRANCO (0)!**", parse_mode="Markdown")
                    elif num <= 7:
                        bot.send_message(CHAT_ID, f"🚨 **SINAL: VERMELHO 🔴** ({num})", parse_mode="Markdown")
                    else:
                        bot.send_message(CHAT_ID, f"🚨 **SINAL: PRETO ⚫** ({num})", parse_mode="Markdown")
            
            time.sleep(8)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Inicia o servidor e o bot
    Thread(target=run).start()
    try:
        bot.send_message(CHAT_ID, "✅ **Bot MBDM Iniciado com Sucesso!**")
    except:
        pass
    monitorar()
