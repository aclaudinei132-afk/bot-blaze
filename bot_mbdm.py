import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB (PARA O RAILWAY NÃO DESLIGAR) ---
app = Flask('')
@app.route('/')
def home(): return "Bot MBDM Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES DO SEU ROBÔ (TOKEN E ID) ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None 

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO AUTOMÁTICO ATIVADO!")
    
    while True:
        try:
            # Lendo a API da Blaze (O SEGREDO DO SINAL)
            url = "https://blaze.com"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                dados = r.json()
                # O [0] garante que pegamos o giro MAIS RECENTE da lista
                giro_atual = dados[0]
                
                if giro_atual['id'] != ultimo_id_processado:
                    num = int(giro_atual['value'])
                    ultimo_id_processado = giro_atual['id']
                    print(f"Número na Blaze: {num}")

                    # --- SEUS PADRÕES AUTOMATIZADOS ---

                    # Padrão para Preto (Se cair 10 ou 12)
                    if num == 10 or num == 12:
                        msg = f"🎰 Número: **{num}**\n🚨 **PADRÃO (10/12)!**\n\n🎯 Entrada: **PRETO ⚫**\n⚪ Proteção no Branco\n🔄 Até G1"
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                    # Alerta para Preto (Se cair 11 ou 8)
                    elif num == 11 or num == 8:
                        msg = f"🎰 Número: **{num}**\n⚠️ **ATENÇÃO (11/8)!**\n\n⏳ Aguarde 2 casas...\n🎯 Depois entre no **PRETO ⚫** + ⚪ Branco"
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                    # Alerta para Vermelho (Se cair o número 1)
                    elif num == 1:
                        msg = f"🎰 Número: **{num}**\n⚠️ **ATENÇÃO (NÚMERO 1)!**\n\n⏳ Aguarde 2 casas...\n🎯 Depois entre no **VERMELHO 🔴** + ⚪ Branco"
                        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            
            time.sleep(8) # Verifica a cada 8 segundos
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Inicia o servidor e o bot
    Thread(target=run).start()
    try:
        bot.send_message(CHAT_ID, "✅ **BOT MBDM AUTOMÁTICO ATIVADO!**\nMonitorando números: 10, 12, 11, 8 e 1.")
    except:
        pass
    monitorar()
