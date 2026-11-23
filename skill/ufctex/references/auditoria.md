# Auditoria de conformidade

Objetivo: dizer ao autor, antes da entrega à banca ou do depósito na biblioteca, o que está fora da ABNT ou do guia da UFC, onde está e como corrigir. A auditoria lê e relata; só corrija o trabalho se o autor pedir.

## 1. Parte automática

```bash
bash <skill>/scripts/compilar.sh <pasta>
python3 <skill>/scripts/auditar.py <pasta> --md <pasta>/auditoria.md
```

Compile antes: o script também lê o `documento.pdf`. Severidades:

- **BLOQUEIA**: a biblioteca recusa ou o PDF sai errado ("??", texto do modelo, ficha de instruções, figura sem fonte, citação sem entrada no .bib).
- **CORRIGIR**: fora da norma, mas o trabalho compila e se lê (citação em caixa alta, remissão digitada, resumo fora de 150 a 500 palavras).
- **CONFERIR**: pode estar certo; decida lendo o trecho (menção a "capítulo", sigla definida e não usada, entrada não citada).

O script tem falsos positivos conhecidos: legenda de figura migrada do Word ("Figura 1 – ...") aparece como remissão digitada; sigla usada só dentro de `\glsadd` em outro arquivo aparece como não usada. Confira antes de repassar ao autor.

Se o relatório acusar "Modelo anterior à atualização de 2026", trate isso primeiro: com o lib/ antigo, metade dos itens de citação e referência é culpa do estilo, não do autor. Proponha `scripts/atualizar_lib.sh` (guarda uma cópia do lib/ anterior) e audite de novo.

## 2. Parte manual (PDF)

Renderize as páginas indicadas e confira o que o script não vê. Use `pdftoppm -f N -l N -r 70 -png documento.pdf /tmp/p` e leia a imagem; para texto, `pdftotext -layout -f N -l N documento.pdf -`.

### Pré-textuais (NBR 14724:2024, 4.1 e 4.2.1)

- [ ] Capa: instituição (centro, departamento ou campus, curso ou programa), autor, título, subtítulo após dois-pontos, cidade, ano de depósito. Cidade e ano batem com a folha de rosto.
- [ ] Folha de rosto: natureza com tipo de trabalho, objetivo (grau pretendido), instituição e, em dissertação e tese, área de concentração; alinhada do meio da página à direita; orientador e coorientador com titulação.
- [ ] Ficha catalográfica no verso da folha de rosto, gerada pelo CATALOG! da UFC (fichacatalografica.ufc.br), com o mesmo título, ano e número de folhas do PDF final. Na versão impressa o verso não é contado (5.3).
- [ ] Folha de aprovação: nome, titulação, instituição e linha de assinatura de cada membro; "Aprovado(a) em" em branco até a defesa.
- [ ] Dedicatória e epígrafe sem título, no pé da página, à direita (5.2.4). Epígrafe com autoria.
- [ ] Resumo: parágrafo único, informativo (objetivo, método, resultados, conclusão), verbo na terceira pessoa, de 150 a 500 palavras; palavras-chave em minúsculas, separadas por ponto e vírgula, com ponto final (NBR 6028:2021, 4.1).
- [ ] Abstract com o mesmo conteúdo do resumo (mesmos números) e keywords correspondentes.
- [ ] Listas de ilustrações, tabelas, siglas e símbolos presentes quando há itens; siglas em ordem alfabética, símbolos na ordem do texto (4.2.1.9 a 4.2.1.12).
- [ ] Sumário: último pré-textual, sem pré-textuais nele, títulos idênticos aos do texto (mesma grafia e destaque), apêndices e anexos com letra e título (NBR 6027:2012).

### Textuais

- [ ] Seções primárias numeradas, cada uma em página nova; nenhuma seção sem texto próprio antes da subseção (NBR 6024:2012, 4.1 e).
- [ ] Toda figura, tabela e quadro: título acima ("Figura 1 – ..."), fonte abaixo, citado no texto antes de aparecer, perto da citação (5.8 e 5.9). Forma de "Fonte:" igual no trabalho todo.
- [ ] Tabelas no padrão IBGE: sem linhas verticais nem fechamento lateral; dados textuais em quadro, com grade.
- [ ] Equações numeradas entre parênteses à direita, símbolos definidos logo depois ("em que ...") e na lista de símbolos.
- [ ] Siglas por extenso na primeira ocorrência (5.6).
- [ ] Citações: maiúsculas e minúsculas na chamada; página em toda citação direta; citação direta longa (mais de três linhas) com recuo, fonte menor, sem aspas; *apud* em itálico (NBR 10520:2023).
- [ ] Dados de entrevista, palestra ou comunicação pessoal indicados em nota, sem entrada na lista (NBR 10520:2023, 5.3).
- [ ] Notas de rodapé com filete de 5 cm e fonte menor (5.2.1).

### Pós-textuais

- [ ] Referências: todas as obras citadas e só elas; ordem alfabética; sobrenome em maiúsculas; destaque do título uniforme; "Disponível em:" e "Acesso em:" em documento online; DOI de artigo quando existir (NBR 6023:2025). Compare duas ou três entradas de cada tipo com o guia de referências da UFC.
- [ ] Mesma autoria e ano com letras iguais na citação e na lista (1927a).
- [ ] Apêndices (material do autor) e anexos (de terceiros) com "APÊNDICE A – TÍTULO", paginação contínua com o texto (5.3).

### Geral

- [ ] PDF sem "??", sem texto de exemplo do modelo, sem comentários do autor esquecidos.
- [ ] Texto em preto; cor só em ilustrações. Links sem caixa colorida (`\removerbordasdohyperlink{sim}`).
- [ ] Número de folhas na ficha e na referência do trabalho igual ao do PDF final.

## 3. Relatório ao autor

Entregue numa lista curta, agrupada por severidade, com arquivo e linha (ou página do PDF) e a correção em uma frase. Cite a norma só quando o autor puder discordar ("a NBR 10520:2023, 6.1.2, só admite et al. a partir de quatro autores"). Não liste o que está conforme.

Se o curso ou o programa tiver regra própria (número de palavras do resumo, uso de Arial), ela prevalece sobre o guia geral da UFC; pergunte ao autor quando a auditoria depender disso.
