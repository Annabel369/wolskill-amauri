#!/bin/bash

# --- CONFIGURAÇÕES PESSOAIS ---
NOME="Amauri Bueno dos Santos"
EMAIL="amauri00007@gmail.com"
CHAVE_PUB="$HOME/.ssh/id_yubikey_wolskill.pub"

echo -e "\033[0;36m--- Configurando Identidade Git ---\033[0m"
git config --global user.name "$NOME"
git config --global user.email "$EMAIL"

echo -e "\033[0;36m--- Configurando Assinatura SSH (YubiKey) ---\033[0m"
if [ -f "$CHAVE_PUB" ]; then
    # Define o formato para SSH
    git config --global gpg.format ssh
    # Aponta para a chave da YubiKey
    git config --global user.signingkey "$CHAVE_PUB"
    # Ativa a assinatura obrigatória em todos os commits
    git config --global commit.gpgsign true
    # Garante que o Git use o ssh-keygen para assinar
    git config --global gpg.ssh.program "ssh-keygen"
    
    echo -e "\033[0;32m[OK] Assinatura configurada com sucesso!\033[0m"
else
    echo -e "\033[0;31m[ERRO] Arquivo de chave pública não encontrado em: $CHAVE_PUB\033[0m"
fi

echo -e "\033[0;34mConfigurações atuais:\033[0m"
git config --list | grep -E "user|gpg|commit"
