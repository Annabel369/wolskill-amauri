import websocket
import json
import os
import time
import threading
import subprocess
import requests

# 1. LOCALIZAÇÃO DO CONFIG (Coringa para qualquer usuário)
USER_HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(USER_HOME, "Modelos/wolskill/config.txt")

def carregar_credenciais():
    awsid = ""
    license = ""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                # Cria um dicionário a partir do TXT (chave=valor)
                config = dict(line.strip().split('=') for line in f if '=' in line)
                awsid = config.get("AWSID", "")
                license = config.get("LICENSE", "")
        except Exception as e:
            print(f"Erro ao ler config: {e}")
    return awsid, license

# 2. CARREGAMENTO INICIAL
AWSID, LICENSE = carregar_credenciais()
URL = f"wss://3rbp1kul8g.execute-api.eu-west-1.amazonaws.com/prod?awsid={AWSID}&license={LICENSE}"

def get_my_macs():
    try:
        output = subprocess.check_output("ip link show", shell=True).decode()
        macs = []
        for line in output.split('\n'):
            if "link/ether" in line:
                mac = line.strip().split()[1].upper().replace(':', '-')
                macs.append(mac)
        return macs
    except:
        return []

def acao_boas_vindas():
    print("--- INICIANDO ROTINA DE BOAS-VINDAS ---")
    # 1. Avisar o Creeper
    try:
        r = requests.get("http://creeper.local/aprovado", timeout=5)
        print(f"Creeper: {r.text}")
    except Exception as e:
        print(f"Erro ao avisar Creeper: {e}")

    # 2. Abrir o Opera (Via Flatpak)
    try:
        # env=os.environ é vital para o Flatpak achar o servidor gráfico
        subprocess.Popen(["flatpak", "run", "com.opera.Opera"], env=os.environ)
        print("Opera solicitado via Flatpak.")
    except Exception as e:
        print(f"Erro ao abrir Opera: {e}")

def on_message(ws, message):
    try:
        data = json.loads(message)
        cmd_value = data.get("value", "").upper()
        print(f"Comando recebido: {cmd_value}")

        my_macs = get_my_macs()
        if cmd_value in my_macs:
            acao_boas_vindas()
    except Exception as e:
        print(f"Erro no processamento: {e}")

def on_error(ws, error):
    print(f"Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Conexão perdida. Reconectando em 5s...")
    time.sleep(5)
    start_connection()

def on_open(ws):
    print(f"### WOLSKILL CONECTADO (ID: {AWSID[:5]}...) ###")
    def heartbeat():
        try:
            while ws.sock and ws.sock.connected:
                my_macs = get_my_macs()
                ws.send(json.dumps(my_macs))
                time.sleep(30)
        except:
            pass
    threading.Thread(target=heartbeat, daemon=True).start()

def start_connection():
    if not AWSID or not LICENSE:
        print("ERRO: Credenciais não encontradas em", CONFIG_PATH)
        return
    
    ws = websocket.WebSocketApp(URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    start_connection()
