import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB ---
app = Flask('')
@app.route('/')
def home(): return "✅ Bot MBDM com Espera Automática Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)

# --- VARIÁVEIS DE CONTROLE ---
ultimo_id = None
aguardando_casas = 0  # Contador de pulos
cor_pendente = None   # Qual cor entrar após a espera
sinal_ativo = None    # Cor que estamos monitorando o Green
tentativa_gale = False
placar_green = 0
placar_red = 0

def monitorar():
    global ultimo_id, aguardando_casas, cor_pendente, sinal_ativo, tentativa_gale, placar_green, placar_red
    print("📡 Monitoramento Inteligente Iniciado...")
    
    URL_API = "https://blaze.com"

    while True:
        try:
            response = requests.get(URL_API, timeout=10)
            if response.status_code == 200:
                dados = response.json()
                if dados and len(dados) > 0:
                    giro = dados[0]
                    id_giro = giro['id']
                    num = int(giro['roll'])
                    cor_res = int(giro['color']) # 1=Verm, 2=Preto, 0=Branco

                    if id_giro != ultimo_id:
                        ultimo_id = id_giro
                        print(f"🎰 Giro: {num} | Cor: {cor_res}")

                        # 1. VERIFICA GREEN/RED DO SINAL ATIVO
                        if sinal_ativo:
                            if cor_res == sinal_ativo or cor_res == 0:
                                win_tipo = "DIRETO" if not tentativa_gale else "G1"
                                placar_green += 1
                                bot.send_message(CHAT_ID, f"✅ **GREEN {win_tipo}!**\n📊 Placar: {placar_green}W - {placar_red}L", parse_mode="Markdown")
                                sinal_ativo = None
                                tentativa_gale = False
                            elif not tentativa_gale:
                                tentativa_gale = True
                                bot.send_message(CHAT_ID, "🔄 **ENTRADA G1!**\nRepetir cor + Branco", parse_mode="Markdown")
                            else:
                                placar_red += 1
                                bot.send_message(CHAT_ID, f"❌ **RED!**\n📊 Placar: {placar_green}W - {placar_red}L", parse_mode="Markdown")
                                sinal_ativo = None
                                tentativa_gale = False

                        # 2. LOGICA DE ESPERA (PARA 11, 8 E 1)
                        if aguardando_casas > 0:
                            aguardando_casas -= 1
                            if aguardando_casas == 0:
                                cor_nome = "PRETO ⚫" if cor_pendente == 2 else "VERMELHO 🔴"
                                bot.send_message(CHAT_ID, f"🚨 **ENTRE AGORA: {cor_nome}**\n⚪ Proteção no Branco\n🔄 Até G1", parse_mode="Markdown")
                                sinal_ativo = cor_pendente
                                cor_pendente = None
                            else:
                                print(f"⏳ Aguardando... faltam {aguardando_casas} casas.")

                        # 3. NOVOS PADRÕES
                        # ENTRADA IMEDIATA (10 ou 12)
                        if num in [10, 12]:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n🚨 **ENTRADA: PRETO ⚫**\n⚪ Proteção Branco", parse_mode="Markdown")
                            sinal_ativo = 2
                        
                        # ESPERA DE 2 CASAS (11, 8 ou 1)
                        elif num in [11, 8]:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n⚠️ **PADRÃO DETECTADO!**\n⏳ Aguardando 2 casas para entrar no **PRETO ⚫**", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 2
                        
                        elif num == 1:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n⚠️ **PADRÃO DETECTADO!**\n⏳ Aguardando 2 casas para entrar no **VERMELHO 🔴**", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 1

            time.sleep(3)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    bot.send_message(CHAT_ID, "🚀 **BOT MBDM V3 ATIVADO!**\nContagem de espera e placar automáticos.")
    monitorar()
