#!/usr/bin/env bash
# Atualiza só o lib/ de um trabalho existente para o ufcTex 2026, guardando o antigo.
# Uso: atualizar_lib.sh <pasta-do-trabalho> [repositorio-ou-zip-local]
set -eu
DIR="${1:?Informe a pasta do trabalho}"
ORIGEM="${2:-https://github.com/Mateuskkkkk/ufctex}"
[ -f "$DIR/lib/ufcTex.sty" ] || { echo "$DIR não tem lib/ufcTex.sty" >&2; exit 2; }
if grep -q "ufcTex 2026" "$DIR/lib/abntex2-alf.bst" 2>/dev/null; then
  echo "O lib/ já é a versão ufcTex 2026."; exit 0
fi
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
bash "$(dirname "$0")/obter_modelo.sh" "$TMP/novo" "$ORIGEM" > /dev/null
STAMP=$(date +%Y%m%d-%H%M)
cp -r "$DIR/lib" "$DIR/lib-antigo-$STAMP"
for f in abntex2.cls abntex2-alf.bst ufcTex.sty ufcTexcite.sty; do
  cp "$TMP/novo/lib/$f" "$DIR/lib/$f"
done
# preambulo.tex costuma ter ajustes do autor (fonte Arial, pacotes): só troca a opção de et al.
sed -i.bak 's/abnt-etal-cite=2/abnt-etal-cite=3/' "$DIR/lib/preambulo.tex" && rm -f "$DIR/lib/preambulo.tex.bak"
# [H] (pacote float), carregado depois do ufcTex.sty, que cria o ambiente quadro
if ! grep -qE '^[^%]*\\usepackage\{float\}' "$DIR/lib/preambulo.tex"; then
  python3 - "$DIR/lib/preambulo.tex" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
s = re.sub(r"^(\\usepackage\{lib/ufcTex\}[^\n]*\n)",
           r"\1\\usepackage{float}             % [H] (ufcTex 2026)\n", s, count=1, flags=re.M)
open(p, "w", encoding="utf-8").write(s)
PY
fi
[ -f "$DIR/latexmkrc" ] || cp "$TMP/novo/latexmkrc" "$DIR/latexmkrc"
echo "lib/ atualizado. Cópia do anterior em $DIR/lib-antigo-$STAMP (apague depois de conferir o PDF)."
echo "Arquivos trocados: abntex2.cls, abntex2-alf.bst, ufcTex.sty, ufcTexcite.sty; preambulo.tex com abnt-etal-cite=3 e pacote float."
