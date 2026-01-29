#!/bin/bash
set -e

# --- CONFIGURAÇÕES ---
REPO_DIR="/home/astral/Modelos/wolskill-package"
DEB_NAME="wolskill-amauri.deb"
REMOTE_URL="https://github.com/Annabel369/wolskill-amauri.git"

# Definição de Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--- Iniciando Automação de Release ---${NC}"

# 1. Garantir que estamos na pasta certa e inicializar Git se necessário
cd "$REPO_DIR"
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Inicializando repositório Git...${NC}"
    git init
    git remote add origin "$REMOTE_URL"
    git branch -M main
fi

# 2. Gerar o pacote .DEB atualizado
echo -e "${CYAN}Construindo o pacote .deb...${NC}"
# Ajusta permissões do postinst antes do build
chmod 755 DEBIAN/postinst
dpkg-deb --build . "../$DEB_NAME"
echo -e "${GREEN}Pacote gerado em ~/Modelos/$DEB_NAME${NC}"

# 3. Lógica de Versão (Tags)
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$LAST_TAG" ]; then
    NEW_TAG="v1.0.0"
else
    # v1.0.0 -> v1.0.1
    BASE=$(echo $LAST_TAG | cut -d. -f1,2)
    PATCH=$(echo $LAST_TAG | cut -d. -f3)
    NEW_TAG="$BASE.$((PATCH + 1))"
fi

echo -e "Versão anterior: ${YELLOW}$LAST_TAG${NC}"
echo -e "Lançando versão: ${GREEN}$NEW_TAG${NC}"

# 4. Processo de Git
echo -e "${CYAN}Preparando commit...${NC}"
git add .
# Não vamos subir o .deb para o código fonte (binários ficam em Releases), 
# mas se quiser incluir no commit, o 'git add .' já pegou.
git commit -m "Release $NEW_TAG: Automação Wolskill" || echo "Nada para commitar"

echo -e "${CYAN}Criando tag $NEW_TAG...${NC}"
git tag -a "$NEW_TAG" -m "Versão $NEW_TAG"

# 5. Push para o GitHub
echo -e "${YELLOW}Enviando para o GitHub (Toque na YubiKey se solicitado)...${NC}"
git push origin main --force
git push origin "$NEW_TAG"

echo -e "${GREEN}--- PROCESSO CONCLUÍDO ---${NC}"
echo -e "Acesse: https://github.com/Annabel369/wolskill-amauri/"
