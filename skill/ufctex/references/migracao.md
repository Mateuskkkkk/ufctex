# Migrar um trabalho de Word ou Google Docs

Ponto de partida: um .docx (do Google Docs, Arquivo > Fazer download > .docx). PDF não serve como fonte: a conversão perde estrutura; peça o .docx.

## 1. Preparar

1. Crie o projeto como em `novo-trabalho.md`, com `--limpar`, usando os dados da capa e da folha de rosto do próprio .docx (confirme com o autor o que estiver ambíguo).
2. Confira se o .docx usa estilos de título (Título 1 para seções primárias, Título 2 para secundárias). Sem eles, o pandoc não acha as seções e o script para com aviso; peça ao autor para aplicar os estilos, ou faça a divisão à mão.

## 2. Converter

```bash
python3 <skill>/scripts/migrar_docx.py trabalho.docx <pasta>
```

O script grava uma seção primária por arquivo em `2-textuais/`, atualiza o `documento.tex`, extrai as imagens para `figuras/`, separa apêndices e anexos, e deixa em `<pasta>/migracao/`:

- `pre-textuais.tex`: resumo, abstract, agradecimentos etc. como estavam no Word;
- `referencias-originais.txt`: a lista de referências em texto;
- `pendencias.md`: contagem do que falta (imagens soltas, tabelas, citações, remissões);
- `pandoc-bruto.tex`: a saída completa do pandoc, para consulta.

Ele remove a numeração digitada nos títulos ("1.1 Objetivos") e põe em caixa normal os títulos que vinham em maiúsculas.

## 3. Acabamento, na ordem

1. **Pré-textuais**: mova resumo e abstract para `1-pre-textuais/resumo.tex` e `abstract.tex` (parágrafo único, `\palavraschave{...}`), e agradecimentos, dedicatória, epígrafe para os arquivos correspondentes, ativando-os no `documento.tex`.
2. **Referências**: converta cada item de `referencias-originais.txt` em entrada do .bib, seguindo `bibliografia.md`. Escreva autor em caixa normal (`Silva, José`), mesmo que no Word estivesse SILVA. Crie a chave no formato `sobrenomeAno` (`silva2020`). Não complete dado ausente de memória: busque a fonte (DOI, catálogo da editora, repositório) ou marque `[S. l.]`, `[s. n.]` e avise o autor.
3. **Citações**: troque cada "(SILVA, 2020)" ou "(Silva, 2020, p. 5)" por `\cite[p.~5]{silva2020}`, e "Silva (2020)" por `\citeonline{silva2020}`. Procure com `grep -nE "\([A-ZÀ-Ý][^()]*, [0-9]{4}" 2-textuais/*.tex` e confira se cada chave existe no .bib. Citação de citação vira `\apud`.
4. **Figuras**: cada `\includegraphics` solto vira o bloco de `elementos.md` (figure, `\Caption`, `\label`, `\UFCfig`, `\Fonte`). O título e a fonte estão no parágrafo de texto logo antes ou depois da imagem; apague esse parágrafo depois de mover. Renomeie a imagem (`rId21.png` para `localizacao-bacia.png`).
5. **Tabelas**: o pandoc gera `longtable`. Refaça no padrão de `elementos.md` (tabela IBGE ou quadro), com `\caption`, `\label` e `\Fonte`. Tabela que no Word era imagem fica como figura só se não houver os dados; prefira redigitar.
6. **Equações**: o pandoc converte as do editor do Word em `\[ ... \]` ou `$...$`. Passe as numeradas para `equation` com `\label` e defina os símbolos.
7. **Remissões**: "Figura 3", "Tabela 2", "Seção 4.1" escritos à mão viram `Figura~\ref{fig:...}`.
8. **Siglas**: cadastre as siglas do Word na lista e use `\gls` na primeira ocorrência.
9. **Limpeza**: apague `\tightlist`, `\pandocbounded`, `\emph{}` vazios, quebras `\\` soltas e negritos usados como título. Notas de rodapé o pandoc já converte em `\footnote`.
10. Compile, audite (`auditoria.md`) e apague a pasta `migracao/` quando `pendencias.md` estiver toda marcada.

## Cuidados

- Não reescreva o texto do autor durante a migração. Correções de redação são outro pedido.
- Conteúdo que o pandoc não converte (caixas de texto, SmartArt, comentários do Word) some. Compare o número de páginas e de figuras com o original e avise o autor do que precisou ser refeito.
- Quando o Word tem referências geradas pelo Mendeley ou Zotero, peça ao autor o .bib exportado do gerenciador: é mais fiel que reconverter o texto. Mesmo assim, revise caixa dos nomes e campos com `bibliografia.md`.
