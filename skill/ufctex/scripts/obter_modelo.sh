#!/usr/bin/env bash
# Copia o modelo ufcTex atualizado para uma pasta de trabalho.
# Uso: obter_modelo.sh <pasta-destino> [repositorio-ou-zip-local]
# O destino não pode já ter documento.tex (para não sobrescrever um trabalho).
set -eu
REPO_PADRAO="https://github.com/Mateuskkkkk/ufctex"
DEST="${1:?Informe a pasta de destino}"
ORIGEM="${2:-$REPO_PADRAO}"

if [ -f "$DEST/documento.tex" ]; then
  echo "Já existe $DEST/documento.tex. Escolha outra pasta ou use atualizar_lib.sh para só atualizar o lib/." >&2
  exit 2
fi
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

if [ -f "$ORIGEM" ]; then
  # zip baixado manualmente (Code > Download ZIP no GitHub)
  unzip -q "$ORIGEM" -d "$TMP/zip"
  SRC=$(dirname "$(find "$TMP/zip" -name documento.tex -not -path '*/skill/*' | head -1)")
elif [ -d "$ORIGEM" ] && [ -f "$ORIGEM/documento.tex" ]; then
  SRC="$ORIGEM"
else
  if git clone --depth 1 -q "$ORIGEM" "$TMP/repo" 2>/dev/null; then
    SRC="$TMP/repo"
  elif curl -fsSL "$ORIGEM/archive/refs/heads/main.zip" -o "$TMP/m.zip" 2>/dev/null; then
    unzip -q "$TMP/m.zip" -d "$TMP/zip"
    SRC=$(dirname "$(find "$TMP/zip" -name documento.tex -not -path '*/skill/*' | head -1)")
  else
    echo "Não consegui baixar $ORIGEM. Peça ao usuário o zip do modelo (Code > Download ZIP) e rode de novo passando o caminho do zip." >&2
    exit 3
  fi
fi
[ -f "$SRC/lib/ufcTex.sty" ] || { echo "A origem não tem lib/ufcTex.sty: não parece o modelo ufcTex." >&2; exit 3; }

mkdir -p "$DEST"
# Tudo do modelo, menos a skill, o histórico Git e os arquivos de teste do estilo.
( cd "$SRC" && tar cf - --exclude=./skill --exclude=./dist --exclude=./.git --exclude=./.github \
    --exclude='./teste-normas.*' --exclude='*.pdf' \
    --exclude='*.aux' --exclude='*.log' --exclude='*.bbl' --exclude='*.blg' --exclude='*.toc' \
    --exclude='*.lof' --exclude='*.lot' --exclude='*.loq' --exclude='*.out' --exclude='*.glo' \
    --exclude='*.gls' --exclude='*.glg' --exclude='*.acn' --exclude='*.acr' --exclude='*.alg' \
    --exclude='*.ist' --exclude='*.idx' --exclude='*.ind' --exclude='*.ilg' --exclude='*.lol' \
    --exclude='*.fls' --exclude='*.fdb_latexmk' --exclude='*.synctex.gz' --exclude='*.brf' . ) | ( cd "$DEST" && tar xf - )
# PDFs do modelo que fazem parte do exemplo (ficha catalográfica de instrução, anexos e apêndices em PDF)
( cd "$SRC" && find . -name '*.pdf' -not -path './skill/*' -not -name 'documento.pdf' -not -name 'teste-normas.pdf' -print0 \
    | tar cf - --null -T - ) | ( cd "$DEST" && tar xf - )
echo "Modelo copiado para $DEST"
grep -h "ufcTex 2026" "$DEST/lib/abntex2-alf.bst" > /dev/null && echo "Versão: ufcTex 2026 (NBR 10520:2023, NBR 6023:2025, NBR 14724:2024)"
