# Wolskill - Automação Personalizada 🚀

Desenvolvido por **Amauri Bueno dos Santos**. Este projeto é uma ferramenta de automação para uso pessoal, focada em integração e utilitários rodando em ambiente **Debian 13**.

O projeto está estruturado como um pacote Debian (`.deb`), facilitando a instalação e a gestão de scripts Python no sistema.

## 🛠️ Tecnologias Utilizadas
* **Python 3**: Lógica principal do sistema.
* **Bash**: Scripts de automação de build e deploy.
* **YubiKey**: Segurança via hardware para commits e releases.
* **Debian Packaging**: Estrutura padrão para sistemas baseados em Linux.

## 📦 Como Instalar

### 1. Baixar o Binário (.deb)
Se você quer apenas usar a ferramenta, baixe o instalador na aba [Releases](https://github.com/Annabel369/wolskill-amauri/releases) e execute:
```bash
sudo apt install ./wolskill-amauri.deb


Build Manual (Para Desenvolvedores)
Se deseja compilar o pacote a partir do código-fonte:

Bash

# Clone o repositório
git clone [https://github.com/Annabel369/wolskill-amauri.git](https://github.com/Annabel369/wolskill-amauri.git)
cd wolskill-amauri

# Gere o pacote .deb
dpkg-deb --build . ../wolskill-amauri.deb

# Instale
sudo apt install ../wolskill-amauri.deb```

1. Se você usa Windows (NSSM)
A forma mais robusta de rodar scripts Python como serviço no Windows é usando o NSSM (Non-Sucking Service Manager).

Baixe o NSSM.

Abra o Terminal como Administrador e digite: nssm install MonitorWOL.

Na interface que abrir:

Path: O caminho do seu python.exe.

Startup directory: A pasta onde está o seu script.

Arguments: O nome do seu arquivo (ex: monitor.py).

Clique em "Install Service". Agora ele aparecerá no services.msc e iniciará com o Windows.

2. Se você usa Linux/Raspberry Pi (systemd)
Este é o padrão para servidores e dispositivos IoT.

Crie um arquivo de serviço: sudo nano /etc/systemd/system/wol-monitor.service

Cole o seguinte conteúdo:

Ini, TOML

[Unit]
Description=Monitor Wake-on-LAN e Trigger HTTP
After=network.target

[Service]
ExecStart=/usr/bin/python3 /caminho/do/seu/script.py
WorkingDirectory=/caminho/do/seu/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
(Nota: Use User=root porque o bind de portas baixas pode exigir privilégios em alguns sistemas).

Ative o serviço:

Bash

sudo systemctl enable wol-monitor.service
sudo systemctl start wol-monitor.service```



