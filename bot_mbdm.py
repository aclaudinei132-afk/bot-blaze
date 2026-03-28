import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA O RAILWAY ---
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot MBDM Online e Monitorando!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES DO SEU ROBÔ ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"

bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO EM TEMPO REAL ATIVADO!")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": "https://blaze.com"
    }
    
    # --- LINHA 39 CORRIGIDA ABAIXO (O SEGREDO DOS NÚMEROS) ---
    URL_API = "https://blaze.com"

    while True:
        try:
            response = requests.get(URL_API, headers=headers, timeout=15)
            
            if response.status_code == 200:
                dados = response.json()
                
                # Pegamos o primeiro item da lista (giro mais recente)
                giro_atual = dados[0]
                id_giro = giro_atual['id']
                
                if id_giro != ultimo_id_processado:
                    num = int(giro_atual['value'])
                    ultimo_id_processado = id_giro
                    print(f"🎰 Novo número na mesa: {num}")

                    # --- SEUS PADRÕES ---

                    # Padrão 10 ou 12 -> PRETO
                    if num == 10 or num == 12:
                        msg = (f"🎰 Número: *{num}*\n"
                               f"🚨 *PADRÃO DETECTADO (10/12)!*\n\n"
                               f"🎯 Entrada: *PRETO ⚫*\n"
                               f"⚪ Proteção no Branco\n"
                               f"🔄 Até G1")
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                    # Padrão 11 ou 8 -> ATENÇÃO PRETO
                    elif num == 11 or num == 8:
                        msg = (f"🎰 Número: *{num}*\n"
                               f"⚠️ *ATENÇÃO (11/8)!*\n\n"
                               f"⏳ Aguarde 2 casas...\n"
                               f"🎯 Depois entre no *PRETO ⚫* + ⚪ Branco")
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                    # Padrão 1 -> ATENÇÃO VERMELHO
                    elif num == 1:
                        msg = (f"🎰 Número: *{num}*\n"
                               f"⚠️ *ATENÇÃO (NÚMERO 1)!*\n\n"
                               f"⏳ Aguarde 2 casas...\n"
                               f"🎯 Depois entre no *VERMELHO 🔴* + ⚪ Branco")
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            
            time.sleep(5) # Verifica a cada 5 segundos

        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            time.sleep(10)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    
    try:
        bot.send_message(CHAT_ID, "✅ **BOT MBDM ATIVADO COM SUCESSO!**\nMonitorando números: 10, 12, 11, 8 e 1.")
        print("Bot iniciado e mensagem de boas-vindas enviada!")
    except Exception as e:
        print(f"Erro Telegram: {e}")
        
    monitorar()
