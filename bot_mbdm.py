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
    return "✅ Bot MBDM Online e Sincronizado!"

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
    print("🚀 MONITORAMENTO EM TEMPO REAL ATIVADO!")
    
    # Headers para simular navegador e evitar o erro de bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://blaze.com"
    }
    
    # URL da API oficial (funciona para todos os domínios da Blaze)
    URL_API = "https://blaze.com"

    while True:
        try:
            # Faz a chamada para a API com timeout de 20 segundos
            response = requests.get(URL_API, headers=headers, timeout=20)
            
            if response.status_code == 200:
                dados = response.json()
                
                # Verifica se recebemos a lista de giros
                if isinstance(dados, list) and len(dados) > 0:
                    giro_atual = dados[0] # Pega o giro mais recente no topo da lista
                    id_giro = giro_atual['id']
                    
                    # Só processa se for um ID novo (giro inédito)
                    if id_giro != ultimo_id_processado:
                        num = int(giro_atual['value'])
                        ultimo_id_processado = id_giro
                        print(f"🎰 Novo número detectado: {num}")

                        # --- LÓGICA DE PADRÕES ---

                        # PADRÃO 1: Se cair 10 ou 12 (PRETO)
                        if num == 10 or num == 12:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"🚨 *PADRÃO DETECTADO (10/12)!*\n\n"
                                   f"🎯 Entrada: *PRETO ⚫*\n"
                                   f"⚪ Proteção no Branco\n"
                                   f"🔄 Até G1")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                        # PADRÃO 2: Se cair 11 ou 8 (ATENÇÃO PRETO)
                        elif num == 11 or num == 8:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (11/8)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *PRETO ⚫* + ⚪ Branco")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                        # PADRÃO 3: Se cair o número 1 (ATENÇÃO VERMELHO)
                        elif num == 1:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (NÚMERO 1)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *VERMELHO 🔴* + ⚪ Branco")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            
            # Checa a cada 5 segundos
            time.sleep(5)

        except Exception as e:
            print(f"⚠️ Erro de conexão, tentando novamente... ({e})")
            time.sleep(10)

if __name__ == "__main__":
    # Roda o servidor web (flask) em paralelo
    t = Thread(target=run)
    t.start()
    
    # Mensagem de ativação no Telegram
    try:
        bot.send_message(CHAT_ID, "✅ **BOT MBDM CONECTADO E CORRIGIDO!**\nMonitorando números: 10, 12, 11, 8 e 1.")
    except Exception as e:
        print(f"Erro ao enviar mensagem inicial: {e}")
        
    # Inicia o loop de monitoramento
    monitorar()
