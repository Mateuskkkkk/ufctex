# Criar um trabalho novo

## Dados para pedir ao autor

Pergunte só o que faltar na conversa. Com AskUserQuestion, junte em uma ou duas perguntas.

| Campo | Exemplo | Observação |
|---|---|---|
| tipo | `tccgraduacao`, `tccespecializacao`, `dissertacao`, `tese` | define capa, folha de rosto e folha de aprovação |
| autor | Francisco Mateus Bezerra Martins | nome completo, caixa normal |
| titulo | Dimensionamento de uma barragem de terra: estudo de caso em Crateús | subtítulo depois de dois-pontos |
| local, ano | Crateús, 2027 | cidade onde o trabalho é apresentado e ano de depósito |
| centro | Campus de Crateús; Centro de Tecnologia | unidade acadêmica |
| departamento | Departamento de Engenharia Hidráulica e Ambiental | deixe vazio se a unidade não tem (campi do interior); a linha some da capa |
| curso, grau | Engenharia Civil, bacharel | TCC de graduação |
| especializacao | Gestão de Recursos Hídricos | TCC de especialização |
| programa, nome_curso_pos, titulo_obtido, area_concentracao | Programa de Pós-Graduação em Engenharia Civil; Mestrado Acadêmico em Engenharia Civil; Engenharia Civil; Recursos Hídricos | dissertação e tese |
| orientador | Prof. Dr. Nome, instituição, centro, feminino sim/não | titulação no nome |
| coorientador | idem, ou vazio | o modelo aceita um |
| banca | até 5 membros além de orientador e coorientador | nome com titulação, instituição |

Não invente nome de orientador, banca ou unidade. Campo que o autor não souber fica vazio no JSON e o script avisa.

## Passos

```bash
bash <skill>/scripts/obter_modelo.sh <pasta>             # baixa o modelo do GitHub
python3 <skill>/scripts/novo_trabalho.py <pasta> dados.json --limpar
bash <skill>/scripts/compilar.sh <pasta>
python3 <skill>/scripts/auditar.py <pasta>
```

`obter_modelo.sh` aceita, no segundo argumento, um zip do modelo baixado à mão (GitHub, Code > Download ZIP) ou uma pasta local, para quando a rede não alcança o GitHub.

`--limpar` troca o conteúdo de exemplo por um esqueleto: cinco seções primárias (Introdução, Fundamentação teórica, Metodologia, Resultados e discussão, Conclusão), resumo e abstract com a regra da NBR 6028 em comentário, referências vazias, siglas e símbolos de exemplo comentados, apêndices, anexos, ficha catalográfica e elementos opcionais desativados no `documento.tex`. Sem `--limpar`, o trabalho mantém o exemplo do modelo, útil para quem quer ver cada recurso funcionando antes de apagar.

Depois do esqueleto, a auditoria acusa só o resumo e o abstract provisórios e a ficha desativada. É o estado esperado de um trabalho novo.

Os nomes das seções primárias são sugestão. Ajuste ao que o curso pede (alguns TCCs têm "Estudo de caso"; trabalhos de revisão, "Revisão sistemática"): renomeie o arquivo, o `\chapter{}` e a linha `\input` no `documento.tex`.

## Ativar elementos depois

| Elemento | No `documento.tex` |
|---|---|
| Dedicatória, agradecimentos, epígrafe | descomente `\imprimirdedicatoria{...}` etc. e escreva o arquivo em `1-pre-textuais/` |
| Lista de figuras, de tabelas, de quadros | descomente `\imprimirlistadeilustracoes`, `\imprimirlistadetabelas`, `\imprimirlistadequadros`; recomenda-se uma lista por tipo de ilustração (NBR 14724:2024, 4.2.1.9) |
| Siglas | cadastre em `lista-de-abreviaturas-e-siglas.tex` e descomente `\imprimirlistadeabreviaturasesiglas` |
| Símbolos | cadastre em `lista-de-simbolos.tex` e descomente `\imprimirlistadesimbolos{...}` |
| Apêndices, anexos | crie o arquivo em `3-pos-textuais/apendices/`, descomente `\imprimirapendices` e acrescente o `\input` |
| Ficha catalográfica | gere no CATALOG! (fichacatalografica.ufc.br) com a versão final, salve como `1-pre-textuais/ficha-catalografica.pdf` e descomente `\imprimirfichacatalografica{...}` |

## Overleaf

Muitos alunos escrevem no Overleaf. Para levar o projeto: compacte a pasta (`cd <pasta> && zip -r ../trabalho.zip . -x '*.aux' '*.log' '*.pdf'`) e, no Overleaf, New Project > Upload Project. O compilador é pdfLaTeX (padrão). O `latexmkrc` do modelo roda o makeglossaries; na primeira compilação no Overleaf, confira se a lista de siglas apareceu.
