---
name: ufctex
description: 'Padroniza TCC, monografia, dissertação e tese da UFC nas normas ABNT com o modelo LaTeX ufcTex: cria, migra do Word, formata, revisa referências e audita antes da entrega.'
---

# ufcTex: trabalhos acadêmicos da UFC na ABNT

O ufcTex é o modelo LaTeX da Biblioteca Universitária da UFC, derivado do abnTeX2. Esta skill usa a versão atualizada em 2026 (repositório https://github.com/Mateuskkkkk/ufctex), que segue a NBR 14724:2024, a NBR 10520:2023 e a NBR 6023:2025. O modelo já aplica a formatação; o trabalho de Claude é pôr o conteúdo do autor nos comandos certos, manter as referências corretas e conferir o resultado contra as normas.

Caminho dos scripts e guias: a pasta desta skill (`<skill>` abaixo). Se ela não tiver `scripts/` e `references/` (skill salva só com este arquivo), baixe o repositório e use a pasta da skill de lá:

```bash
git clone --depth 1 https://github.com/Mateuskkkkk/ufctex /tmp/ufctex-repo
# <skill> = /tmp/ufctex-repo/skill/ufctex
```

Sem acesso ao GitHub, peça ao usuário o zip do repositório (Code > Download ZIP) e descompacte.

## Primeiro passo: em que situação o trabalho está

1. **Não existe projeto** e o autor vai começar: leia `references/novo-trabalho.md`.
2. **O trabalho está em Word ou Google Docs**: leia `references/migracao.md`.
3. **Já existe projeto ufcTex** (`lib/ufcTex.sty`, `documento.tex`): leia o `documento.tex` para saber o tipo de trabalho (`\trabalhoacademico{...}`) e os elementos ativos. Depois confira a versão do modelo:
   ```bash
   grep -q "ufcTex 2026" lib/abntex2-alf.bst && echo atualizado || echo antigo
   ```
   Com o modelo antigo (2022 ou anterior), as citações saem fora da NBR 10520:2023 e sobrenomes acentuados quebram. Proponha `bash <skill>/scripts/atualizar_lib.sh <pasta>`, que troca só o `lib/` e guarda o anterior em `lib-antigo-<data>/`; diga ao autor que a aparência das citações e da lista de referências vai mudar. Não atualize sem o autor concordar: o lib/ pode ter ajustes pedidos pelo orientador.
4. **O autor pede revisão ou "está tudo na norma?"**: rode a auditoria (`references/auditoria.md`).

## Estrutura do projeto

```
documento.tex          tipo de trabalho, autor, banca, ordem dos elementos
latexmkrc              faz o latexmk rodar o makeglossaries (siglas)
lib/                   abntex2.cls, abntex2-alf.bst, ufcTex.sty, ufcTexcite.sty, preambulo.tex
1-pre-textuais/        resumo, abstract, agradecimentos, siglas, símbolos, ficha catalográfica
2-textuais/            um arquivo por seção primária
3-pos-textuais/        referencias.bib, apendices/, anexos/
figuras/
```

Conteúdo vai nos arquivos das seções e dos pré-textuais. `lib/` só muda para corrigir o próprio modelo, e então avise o autor, porque afeta o trabalho inteiro.

## Escrever e formatar

Leia `references/elementos.md` antes de inserir figura, tabela, quadro, código, equação, alínea, sigla, símbolo, apêndice ou anexo. O essencial:

- Seção primária com `\chapter{Título}` (sai "1 TÍTULO"); a NBR 14724:2024 (4.2.2) organiza o trabalho em seções, então nunca escreva "capítulo" no texto.
- Figura: `\Caption{\label{fig:x}Título}` + `\UFCfig{}{conteúdo}{\Fonte{Elaborada pelo autor.}}` dentro de `figure`. Tabela: `\caption`, `\label`, `tabular` com booktabs, `\Fonte`. Toda ilustração e tabela tem fonte e é citada no texto antes de aparecer.
- `[H]` fixa o flutuante no ponto do texto (o pacote float já vem no modelo).
- Remissões sempre com `\ref` (`Figura~\ref{fig:x}`), nunca o número digitado.
- Sigla com `\newacronym` na lista e `\gls{SIGLA}` no texto; símbolo de equação na lista de símbolos, com unidade.

Para texto que Claude escreve ou revisa a pedido do autor, siga `references/redacao.md`; um `CLAUDE.md` do projeto prevalece. Não reescreva o texto do autor sem pedido.

## Citações e referências

Leia `references/bibliografia.md` antes de criar, corrigir ou revisar entradas do .bib. Os pontos que mais erram:

- `\cite{chave}` gera (Silva, 2019); `\citeonline{chave}` gera Silva (2019); página com `\cite[p.~45]{chave}`; citação de citação com `\apud`.
- No .bib, nomes em caixa normal (`Gonçalves, Érica`); instituição entre chaves duplas (`{{Organização Mundial da Saúde}}`); jurisdição com `organization` e `org-short`. O estilo faz as maiúsculas, as letras 2019a/2019b e a ordem alfabética.
- Toda citação tem entrada no .bib e vice-versa. Confira cada referência na fonte (DOI resolve, link abre, sem parâmetros de rastreamento). Dado que falta não se inventa: use `[S. l.]`, `[s. n.]`, `[20--]` e avise o autor.

## Compilar e conferir

```bash
bash <skill>/scripts/compilar.sh <pasta>
```

O script compila com latexmk (ou com a sequência pdflatex, bibtex, makeglossaries), resume erros, referências indefinidas, `Overfull \vbox` (conteúdo cortado no pé da página, quase sempre uma listagem em `minipage` depois de uma figura flutuante) e "??" no PDF, e limpa os auxiliares. Leia o resumo antes de entregar.

Para ver uma página: `pdftoppm -f N -l N -r 70 -png documento.pdf /tmp/p` e leia a imagem; para texto, `pdftotext -layout -f N -l N documento.pdf -`. A página impressa no canto difere da página do PDF (pré-textuais não são numerados); ao falar com o autor, use a impressa.

Faltando LaTeX no ambiente: `apt-get install texlive-latex-extra texlive-lang-portuguese texlive-publishers texlive-science texlive-fonts-recommended latexmk` (o abnTeX2 vem em texlive-publishers). A migração usa também o `pandoc`.

## Auditar

```bash
python3 <skill>/scripts/auditar.py <pasta> --md <pasta>/auditoria.md
```

Depois faça a parte manual de `references/auditoria.md` no PDF e entregue ao autor a lista do que corrigir, por severidade, com arquivo e linha ou página. Não corrija na mesma passada sem o autor pedir.

## Normas

`references/normas.md` lista as edições que o modelo segue, o que mudou em relação ao modelo de 2022 e os erros que mais causam recusa no depósito. Regra do curso ou do programa (por exemplo, limite de palavras do resumo ou fonte Arial) prevalece sobre o guia geral; pergunte quando a decisão depender disso.

## Antes de entregar

1. `compilar.sh` sem erro, sem referência indefinida, sem `Overfull \vbox` e sem "??".
2. `auditar.py` sem itens BLOQUEIA (num trabalho em andamento, os pendentes ficam listados para o autor).
3. Cada figura, tabela, quadro e código com título, rótulo, fonte, citado no texto.
4. Resumo e abstract coerentes com os números do texto, se algum resultado mudou.
5. Ao autor, uma nota curta com o que mudou de fato e o que ficou pendente (ficha catalográfica, dados de referência não encontrados). O texto do trabalho não leva comentários sobre o processo.
