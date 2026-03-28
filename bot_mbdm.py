import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA O RAILWAY (MANTER ONLINE) ---
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot MBDM Online e Monitorando a Blaze!"

def run():
    # O Railway fornece a porta automaticamente
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
    
    # Headers para evitar o bloqueio da Blaze e simular um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://blaze.com"
    }
    
    # URL da API estável (Funciona para quem usa .com ou .bet.br)
    URL_API = "https://blaze.com"

    while True:
        try:
            # Timeout de 20 segundos para evitar que a conexão caia no Railway
            response = requests.get(URL_API, headers=headers, timeout=20)
            
            if response.status_code == 200:
                dados = response.json()
                
                # Verifica se a API retornou a lista de números corretamente
                if isinstance(dados, list) and len(dados) > 0:
                    giro_atual = dados[0] # Pega o número mais recente (topo da lista)
                    id_giro = giro_atual['id']
                    
                    # Só processa se for um ID NOVO (para não repetir o sinal)
                    if id_giro != ultimo_id_processado:
                        num = int(giro_atual['value'])
                        ultimo_id_processado = id_giro
                        print(f"🎰 Novo número detectado: {num}")

                        # --- LÓGICA DOS SEUS PADRÕES ---

                        # PADRÃO 1: Se cair 10 ou 12 (ENTRADA PRETO)
                        if num == 10 or num == 12:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"🚨 *PADRÃO DETECTADO (10/12)!*\n\n"
                                   f"🎯 Entrada: *PRETO ⚫*\n"
                                   f"⚪ Proteção no Branco\n"
                                   f"🔄 Até G1")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                        # PADRÃO 2: Se cair 11 ou 8 (ATENÇÃO PARA PRETO)
                        elif num == 11 or num == 8:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (11/8)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *PRETO ⚫* + ⚪ Branco")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

                        # PADRÃO 3: Se cair o número 1 (ATENÇÃO PARA VERMELHO)
                        elif num == 1:
                            msg = (f"🎰 Número: *{num}*\n"
                                   f"⚠️ *ATENÇÃO (NÚMERO 1)!*\n\n"
                                   f"⏳ Aguarde 2 casas...\n"
                                   f"🎯 Depois entre no *VERMELHO 🔴* + ⚪ Branco")
                            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
            
            # Checa a cada 5 segundos para ser o mais rápido possível
            time.sleep(5)

        except Exception as e:
            # Se houver erro de conexão, ele avisa no Log e tenta de novo
            print(f"⚠️ Aguardando estabilidade da rede... (Erro: {e})")
            time.sleep(10)

if __name__ == "__main__":
    # Inicia o servidor web em uma thread separada
    t = Thread(target=run)
    t.start()
    
    # Mensagem de teste inicial
    try:
        bot.send_message(CHAT_ID, "✅ **BOT MBDM CONECTADO E CORRIGIDO!**\nMonitorando números: 10, 12, 11, 8 e 1.")
    except Exception as e:
        print(f"Erro ao enviar mensagem inicial: {e}")
        
    # Inicia o loop de monitoramento
    monitorar()
