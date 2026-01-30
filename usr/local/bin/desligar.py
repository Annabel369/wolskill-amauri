import websocket
import json
import os
import time
import threading
from getmac import get_mac_address

# --- CONFIGURAÇÃO ---
AWSID = ""
LICENSE = "3"
URL = f"wss://3rbp1kul8g.execute-api.eu-west-1.amazonaws.com/prod?awsid={AWSID}&license={LICENSE}"

def get_my_macs():
    # Retorna uma lista de MACs formatados como o seu servidor espera (XX-XX-XX-XX-XX-XX)
    import subprocess
    output = subprocess.check_output("ip link show", shell=True).decode()
    macs = []
    for line in output.split('\n'):
        if "link/ether" in line:
            mac = line.strip().split()[1].upper().replace(':', '-')
            macs.append(mac)
    return macs

def on_message(ws, message):
    data = json.loads(message)
    print(f"Mensagem recebida: {data}")
    
    # Se o valor recebido for um MAC address presente nesta máquina
    target_mac = data.get("value", "").upper()
    my_macs = get_my_macs()
    
    if target_mac in my_macs:
        print("!!! COMANDO DE DESLIGAMENTO RECEBIDO !!!")
        # No Debian 13, o comando mais seguro via Python:
        os.system("systemctl poweroff")
    elif target_mac == "PONG":
        print("Heartbeat OK")

def on_error(ws, error):
    print(f"Erro: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Conexão Fechada ###")
    time.sleep(5)
    start_connection() # Reconectar

def on_open(ws):
    print("### CONECTADO AO WOLSKILL (PYTHON) ###")
    # Envia os MACs para o servidor registrar a presença
    def run():
        while True:
            my_macs = get_my_macs()
            payload = {"action": "register", "macs": my_macs} # Ajuste conforme o protocolo exato
            ws.send(json.dumps(my_macs))
            time.sleep(30) # Envia a cada 30 segundos
    threading.Thread(target=run, daemon=True).start()

def start_connection():
    ws = websocket.WebSocketApp(URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    start_connection()
