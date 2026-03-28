import telebot
import requests
import time
from flask import Flask
from threading import Thread
from datetime import datetime

# --- SERVIDOR WEB (OBRIGATÓRIO PARA A RENDER MANTER O BOT VIVO) ---
app = Flask('')
@app.route('/')
def home(): return "Bot MBDM Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- CONFIGURAÇÕES DO SEU BOT ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"

bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None 

def pegar_giro():
    try:
        # API oficial da Blaze para o Double
        url = "https://blaze.com"
    
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            dados = r.json()
            return dados[0] # Pega o giro mais recente da lista
        return None
    except:
        return None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO MBDM ATIVADO!")
    
    while True:
        try:
            giro = pegar_giro()
            
            # Verifica se o ID do giro é novo para não repetir sinal
            if giro and giro.get('id') != ultimo_id_processado:
                num = int(giro['value'])
                id_atual = giro['id']
                ultimo_id_processado = id_atual
                
                hora = datetime.now().strftime('%H:%M:%S')
                print(f"[{hora}] Novo número: {num}")

                # --- SEUS NÚMEROS MÁGICOS ---
                
                # 1. Gatilho para Preto (10 ou 12)
                if num == 10 or num == 12:
                    bot.send_message(CHAT_ID, f"🚨 **SINAL: PRETO ⚫**\nNúmero base: {num}\n⚪ Branco (Proteção)\n🔄 G1", parse_mode="Markdown")

                # 2. Alerta de Espera (11 ou 8)
                elif num == 11 or num == 8:
                    bot.send_message(CHAT_ID, f"⚠️ **ALERTA: {num}**\nAguarde...\n🎯 Foco: **PRETO ⚫**", parse_mode="Markdown")

                # 3. Alerta para Vermelho (1)
                elif num == 1:
                    bot.send_message(CHAT_ID, f"⚠️ **ALERTA: {num}**\nAguarde...\n🎯 Foco: **VERMELHO 🔴**", parse_mode="Markdown")
                
                # 4. Branco (0)
                elif num == 0:
                    bot.send_message(CHAT_ID, "💎 **BRANCO (0) NA TELA!**", parse_mode="Markdown")

            time.sleep(8) # Intervalo de checagem
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Inicia o servidor web em segundo plano
    t = Thread(target=run)
    t.start()
    # Envia mensagem inicial no Telegram
    bot.send_message(CHAT_ID, "✅ **Bot MBDM Iniciado com Sucesso na Render!**")
    # Inicia o monitoramento da Blaze
    monitorar()
