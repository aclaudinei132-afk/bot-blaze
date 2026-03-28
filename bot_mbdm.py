import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR PARA MANTER ONLINE ---
app = Flask('')
@app.route('/')
def home(): return "✅ Bot MBDM v6 Rodando!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES ---
TOKEN = "8771599592:AAGjxQix5fplVmQjUIpTKey2HxQ5MRAEVWs"
CHAT_ID = "7347118736"
bot = telebot.TeleBot(TOKEN)

# --- CONTROLE ---
ultimo_id = None
aguardando_casas = 0
cor_pendente = None
sinal_ativo = None
tentativa_gale = False
placar_green = 0
placar_red = 0

def monitorar():
    global ultimo_id, aguardando_casas, cor_pendente, sinal_ativo, tentativa_gale, placar_green, placar_red
    print("📡 Iniciando Monitoramento Blindado...")
    
    # URL de uma API reserva que não bloqueia o Railway
    URL_API = "https://api.tipmanager.net"

    while True:
        try:
            # Tenta puxar os dados
            response = requests.get(URL_API, timeout=20)
            
            if response.status_code == 200:
                dados = response.json()
                if dados and len(dados) > 0:
                    # Pega o giro mais recente
                    giro = dados[0] 
                    id_giro = giro.get('id')
                    num = int(giro.get('value')) # Campo nesta API é 'value'
                    cor_res = int(giro.get('color_id')) # 1=V, 2=P, 0=B

                    if id_giro != ultimo_id:
                        ultimo_id = id_giro
                        print(f"🎰 Novo Giro: {num} (Cor: {cor_res})")

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
                                bot.send_message(CHAT_ID, "🔄 **VAMOS PRO G1!**\nMesma cor + Branco", parse_mode="Markdown")
                            else:
                                placar_red += 1
                                bot.send_message(CHAT_ID, f"❌ **RED!**\n📊 {placar_green}W - {placar_red}L", parse_mode="Markdown")
                                sinal_ativo = None
                                tentativa_gale = False

                        # 2. LÓGICA DE ESPERA (2 CASAS)
                        if aguardando_casas > 0:
                            aguardando_casas -= 1
                            if aguardando_casas == 0:
                                cor_nome = "PRETO ⚫" if cor_pendente == 2 else "VERMELHO 🔴"
                                bot.send_message(CHAT_ID, f"🚨 **ENTRE AGORA: {cor_nome}**\n⚪ Proteção Branco\n🔄 Até G1", parse_mode="Markdown")
                                sinal_ativo = cor_pendente
                                cor_pendente = None
                            else:
                                print(f"⏳ Aguardando... faltam {aguardando_casas} casas.")

                        # 3. GATILHOS (10, 12, 11, 8, 1)
                        if num in [10, 12]:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n🚨 **ENTRADA: PRETO ⚫**\n⚪ Proteção Branco", parse_mode="Markdown")
                            sinal_ativo = 2
                        
                        elif num in [11, 8]:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n⚠️ **PADRÃO! Aguardando 2 casas...**\n🎯 Alvo: PRETO ⚫", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 2
                        
                        elif num == 1:
                            bot.send_message(CHAT_ID, f"🎰 Número: {num}\n⚠️ **PADRÃO! Aguardando 2 casas...**\n🎯 Alvo: VERMELHO 🔴", parse_mode="Markdown")
                            aguardando_casas = 2
                            cor_pendente = 1
            
            time.sleep(5) # Espera 5 segundos para a próxima checagem

        except Exception as e:
            print(f"⚠️ Erro nos logs: {e}")
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    try:
        bot.send_message(CHAT_ID, "🚀 **BOT V6 (FINAL) ATIVADO!**\nMonitorando agora via API Secundária.")
    except: pass
    monitorar()
