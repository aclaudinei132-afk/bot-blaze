import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "✅ Bot MBDM v5 - API Alternativa Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)

ultimo_id = None
aguardando_casas = 0
cor_pendente = None
sinal_ativo = None
tentativa_gale = False
placar_green = 0
placar_red = 0

def monitorar():
    global ultimo_id, aguardando_casas, cor_pendente, sinal_ativo, tentativa_gale, placar_green, placar_red
    print("📡 Monitoramento v5 - API Alternativa...")
    
    # NOVA URL DE API (Mais estável para bots)
    URL_API = "https://api.tipmanager.net"

    while True:
        try:
            response = requests.get(URL_API, timeout=15)
            if response.status_code == 200:
                dados = response.json()
                if dados and len(dados) > 0:
                    # O formato dessa API é diferente
                    giro = dados[0] 
                    id_giro = giro['id']
                    num = int(giro['value']) # Nessa API o campo é 'value'
                    cor_res = int(giro['color_id']) # 1=V, 2=P, 0=B

                    if id_giro != ultimo_id:
                        ultimo_id = id_giro
                        print(f"🎰 Giro: {num} | Cor: {cor_res}")

                        # 1. VERIFICA GREEN/RED
                        if sinal_ativo:
                            if cor_res == sinal_ativo or cor_res == 0:
                                win_tipo = "DIRETO" if not tentativa_gale else "G1"
                                placar_green += 1
                                bot.send_message(CHAT_ID, f"✅ **GREEN {win_tipo}!**\n📊 {placar_green}W - {placar_red}L", parse_mode="Markdown")
                                sinal_ativo = None
                                tentativa_gale = False
                            elif not tentativa_gale:
                                tentativa_gale = True
                                bot.send_message(CHAT_ID, "🔄 **ENTRADA G1!**", parse_mode="Markdown")
                            else:
                                placar_red += 1
                                bot.send_message(CHAT_ID, f"❌ **RED!**\n📊 {placar_green}W - {placar_red}L", parse_mode="Markdown")
                                sinal_ativo = None
                                tentativa_gale = False

                        # 2. LOGICA DE ESPERA
                        if aguardando_casas > 0:
                            aguardando_casas -= 1
                            if aguardando_casas == 0:
                                cor_nome = "PRETO ⚫" if cor_pendente == 2 else "VERMELHO 🔴"
                                bot.send_message(CHAT_ID, f"🚨 **ENTRE AGORA: {cor_nome}**", parse_mode="Markdown")
                                sinal_ativo = cor_pendente
                                cor_pendente = None

                        # 3. NOVOS PADRÕES
                        if num in [10, 12]:
                            bot.send_message(CHAT_ID, f"🎰 {num}\n🚨 **ENTRADA: PRETO ⚫**", parse_mode="Markdown")
                            sinal_ativo = 2
                        elif num in [11, 8]:
                            bot.send_message(CHAT_ID, f"🎰 {num}\n⚠️ **AGUARDE 2 GIROS (P)...**", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 2
                        elif num == 1:
                            bot.send_message(CHAT_ID, f"🎰 {num}\n⚠️ **AGUARDE 2 GIROS (V)...**", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 1
            
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    try: bot.send_message(CHAT_ID, "🚀 **BOT V5 ATIVADO!**")
    except: pass
    monitorar()
