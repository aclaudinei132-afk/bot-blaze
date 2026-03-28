import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO SERVIDOR WEB (OBRIGATÓRIO PARA RAILWAY) ---
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot MBDM Online e Monitorando!"

def run():
    # O Railway usa a variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES DO BOT ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"

bot = telebot.TeleBot(TOKEN)
ultimo_id_processado = None

def monitorar():
    global ultimo_id_processado
    print("🚀 MONITORAMENTO BLAZE ATIVADO!")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    # API de resultados reais (Double)
    URL_API = "https://blaze1.space"

    while True:
        try:
            # Puxa os dados da API
            response = requests.get(URL_API, headers=headers, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                
                if dados and len(dados) > 0:
                    # Pega o giro mais recente (índice 0)
                    giro_atual = dados[0] 
                    id_giro = giro_atual['id']
                    
                    # Só processa se for um giro NOVO
                    if id_giro != ultimo_id_processado:
                        num = int(giro_atual['roll']) # Campo 'roll' é o número sorteado
                        ultimo_id_processado = id_giro
                        print(f"🎰 Novo número: {num}")

                        msg = ""

                        # --- LÓGICA DE PADRÕES ---
                        
                        # PADRÃO 10 ou 12 (Entrada Imediata)
                        if num == 10 or num == 12:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"🚨 *PADRÃO DETECTADO (10/12)!*\n\n"
                                   f"🎯 Entrada: *PRETO ⚫*\n"
                                   f"⚪ Proteção no Branco\n"
                                   f"🔄 Até G1")

                        # PADRÃO 11 ou 8 (Atenção)
                        elif num == 11 or num == 8:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (11/8)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *PRETO ⚫* + ⚪ Branco")

                        # PADRÃO 1 (Atenção Vermelho)
                        elif num == 1:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (NÚMERO 1)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *VERMELHO 🔴* + ⚪ Branco")

                        if msg:
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            
            # Checa a cada 3 segundos
            time.sleep(3)

        except Exception as e:
            print(f"⚠️ Erro na conexão: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Inicia o servidor Flask em paralelo
    t = Thread(target=run)
    t.daemon = True
    t.start()
    
    # Mensagem de ativação no Telegram
    try:
        bot.send_message(CHAT_ID, "✅ **BOT MBDM CONECTADO!**\nMonitorando números: 10, 12, 11, 8 e 1.")
    except Exception as e:
        print(f"Erro ao enviar sinal inicial: {e}")
        
    monitorar()
