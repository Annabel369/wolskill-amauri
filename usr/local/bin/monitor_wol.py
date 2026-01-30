import socket
import requests
import itertools
import logging

logging.basicConfig(
    filename='wol_monitor.log', 
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def monitor_wol():
    # Configuração do alvo HTTP
    base_url = "http://creeper.local/select?id="
    # Cria um iterador infinito na ordem: -1, -2, -3, -4, -5, -1...
    ids_ciclo = itertools.cycle([-1, -2, -3, -4, -5])
    
    # Criando o socket UDP para Wake-on-LAN (Porta 9)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # O bind '' permite ouvir em todas as interfaces de rede locais
        sock.bind(('', 9)) 
        print("### MONITOR WOL + HTTP TRIGGER ATIVADO ###")
        print("Aguardando sinal Wake-on-LAN para disparar comandos...")
        
        while True:
            data, addr = sock.recvfrom(1024)
            
            # Verifica se é um Magic Packet (102 bytes)
            if len(data) == 102:
                proximo_id = next(ids_ciclo)
                url_final = f"{base_url}{proximo_id}"
                
                print(f"\n[!] WOL recebido de: {addr}")
                print(f">>> Disparando: {url_final}")
                
                try:
                    # Faz a requisição HTTP com um timeout curto para não travar o loop
                    response = requests.get(url_final, timeout=3)
                    print(f"--- Resposta do Servidor: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"--- Erro ao conectar em creeper.local: {e}")
            else:
                print(f"\n[?] Dados recebidos de {addr}, mas não é um Magic Packet padrão.")
                
    except Exception as e:
        print(f"Erro no Socket: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    monitor_wol()
