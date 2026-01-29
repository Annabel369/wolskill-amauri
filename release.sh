#!/bin/bash
set -e

# --- CONFIGURAÇÕES CORRIGIDAS ---
REPO_DIR="/home/astral/Modelos/wolskill-package"
DEB_NAME="wolskill-amauri.deb"
# MUDANÇA AQUI: Trocamos HTTPS por SSH para usar a YubiKey
REMOTE_URL="git@github.com:Annabel369/wolskill-amauri.git"

# Definição de Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--- Iniciando Automação de Release (MODO SSH/YUBIKEY) ---${NC}"

cd "$REPO_DIR"

# 1. Garantir que o Git use o endereço SSH
if [ ! -d ".git" ]; then
    git init
    git remote add origin "$REMOTE_URL"
    git branch -M main
else
    # Isso garante que mesmo que já exista um remote, ele mude para SSH
    git remote set-url origin "$REMOTE_URL"
fi

# 2. Gerar o pacote .DEB
echo -e "${CYAN}Construindo o pacote .deb...${NC}"
chmod 755 DEBIAN/postinst
dpkg-deb --build . "../$DEB_NAME"
echo -e "${GREEN}Pacote gerado em ~/Modelos/$DEB_NAME${NC}"

# 3. Lógica de Versão
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
    NEW_TAG="v1.0.0"
else
    BASE=$(echo $LAST_TAG | cut -d. -f1,2)
    PATCH=$(echo $LAST_TAG | cut -d. -f3)
    NEW_TAG="$BASE.$((PATCH + 1))"
fi

# 4. Git Process
git add .
git commit -m "Release $NEW_TAG: Automação Wolskill" || echo "Nada para commitar"
git tag -a "$NEW_TAG" -m "Versão $NEW_TAG"

# 5. Push (Aqui ele vai pedir o toque na YubiKey, e NÃO a senha)
echo -e "${YELLOW}Enviando via SSH (Toque na YubiKey)...${NC}"
git push origin main --force
git push origin "$NEW_TAG"

echo -e "${GREEN}--- PROCESSO CONCLUÍDO COM SUCESSO ---${NC}"
