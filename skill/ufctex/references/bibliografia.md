# Referências no ufcTex 2026

O estilo `lib/abntex2-alf.bst` com o pacote `lib/ufcTexcite.sty` gera as citações autor-data pela NBR 10520:2023 e a lista de referências pela NBR 6023:2025. Este arquivo vale para o modelo atualizado (o `lib/abntex2-alf.bst` contém o texto "ufcTex 2026"). Num projeto com o lib/ antigo, rode `scripts/atualizar_lib.sh` antes de mexer nas referências, ou o resultado vai contrariar o que está aqui.

## Comandos de citação

| Comando | Resultado |
|---|---|
| `\cite{chave}` | (Silva, 2019) |
| `\cite[p.~45]{chave}` | (Silva, 2019, p. 45) |
| `\cite[p.~45, grifo nosso]{chave}` | (Silva, 2019, p. 45, grifo nosso) |
| `\citeonline{chave}` | Silva (2019) |
| `\citeonline[p.~45]{chave}` | Silva (2019, p. 45) |
| `\cite{a,b}` | (Silva, 2019; Costa; Mendes; Andrade, 2017) |
| `\apud[p.~55]{original}{consultada}` | (Cagliari, 1986 *apud* Suassuna, 1995, p. 55) |
| `\apudonline{original}{consultada}` | Cagliari (1986 *apud* Suassuna, 1995) |
| `\citeyear{chave}` | 2019 |

Regras que o estilo já aplica e que não devem ser refeitas à mão:

- Sobrenome em maiúsculas e minúsculas na citação, inclusive de instituição: (Organização Mundial da Saúde, 2010); sigla de instituição em maiúsculas: (IBGE, 2011) (NBR 10520:2023, 6.1.1).
- Até três autores, todos: (Costa; Mendes; Andrade, 2017) e "Costa, Mendes e Andrade (2017)"; a partir de quatro, *et al.* (6.1.2; opção `abnt-etal-cite=3` em `lib/preambulo.tex`). Para listar sempre todos os autores, use `abnt-etal-cite=0`; a norma aceita as duas formas, desde que o critério seja o mesmo no trabalho todo.
- Obra sem autoria: (Anteprojeto [...], 1987); título que começa com artigo ou monossílabo: (A flor [...], 1995) (6.1.1.4).
- Mesmo autor e mesmo ano: 1927a e 1927b, na citação e na lista (6.1.6; guia de citações da UFC, 3.1.1.7). Não escreva a letra no campo `year`.
- *apud* em itálico (guia de citações da UFC, 2.3.3); na lista entra só a fonte consultada (NBR 10520:2023, 7.3).
- Na lista: sobrenome em maiúsculas, título em negrito, intervalo de páginas com hífen (p. 51-60), "Disponível em:" e "Acesso em:" para documentos online, entradas em espaço simples separadas por uma linha em branco (NBR 6023:2025, 6.3 a 6.7).

Citação que o estilo não gera e fica no texto, sem `\cite`: dado não publicado (entrevista, palestra, comunicação pessoal), indicado no texto ou em nota de rodapé, sem entrada na lista (NBR 10520:2023, 5.3 e 7.1.7). Em notas de referência a chamada continua em maiúsculas (MINAYO, 2021, p. 9), porque a mudança para minúsculas da NBR 10520:2023 vale para a chamada no texto (8.1.2).

## Como escrever o .bib

### Nomes de pessoas

- Formato `Sobrenome, Prenome`, em caixa normal: `author = {Gonçalves, Érica and Silva, José Antônio}`. O estilo põe o sobrenome em maiúsculas e abrevia os prenomes (GONÇALVES, É.; SILVA, J. A.), inclusive iniciais acentuadas.
- Nunca escreva o sobrenome em maiúsculas no .bib (`{SILVA, J.}`): a citação sairia (SILVA, 2019), fora da NBR 10520:2023.
- Sobrenome composto (Souza Filho, De Nys, Castelo Branco): `{\relax Souza Filho}, Francisco` ou `{Souza Filho}, Francisco`. Sem as chaves, o BibTeX pode tomar a primeira palavra como prenome.
- Sobrenome de mais de uma palavra que começa com letra acentuada, ou com hífen: entre chaves, `{Ângelo-Ítalo}, Jean-Paul`. O BibTeX trata palavra iniciada por letra acentuada como partícula (como "da", "de").
- Partículas no fim do prenome ("da", "dos") não entram nas iniciais pela NBR 6023; escreva `Silva, Antônio Augusto Moura` ou mova a partícula para o sobrenome conforme a forma usada pelo autor.

### Instituição como autor

```bibtex
@book{oms2010,
    author = {{Organização Mundial da Saúde}},
    title = {Relatório mundial de saúde},
    address = {Genebra},
    publisher = {OMS},
    year = {2010}
}
```

Chaves duplas e caixa normal. Sai ORGANIZAÇÃO MUNDIAL DA SAÚDE na lista e (Organização Mundial da Saúde, 2010) no texto. Para citar pela sigla, use a sigla como autor: `author = {{IBGE}}`.

Hierarquia (órgão subordinado) e jurisdição: use `organization` para a entrada completa da lista e `org-short` para a chamada no texto. O que não vai para maiúsculas fica dentro de `\NoCaseChange`:

```bibtex
@book{saopaulo1999,
    organization = {São Paulo \NoCaseChange{(Estado). Secretaria do Meio Ambiente}},
    org-short = {São Paulo},
    title = {Tratados e organizações ambientais em matéria de meio ambiente},
    address = {São Paulo},
    publisher = {SMA},
    year = {1999},
    url = {http://www.bdt.org.br/sma/entendendo/atual.htm},
    urlaccessdate = {8 mar. 2022}
}
```

Sai "SÃO PAULO (Estado). Secretaria do Meio Ambiente." na lista e (São Paulo, 1999) no texto. O mesmo vale para `organization = {Brasil\NoCaseChange{. Ministério da Saúde}}` com `org-short = {Brasil}`, e para "Ceará", "Fortaleza" etc. (NBR 10520:2023, 6.1.1.3).

Projetos antigos escrevem `organization = {{COMPANHIA DE GESTÃO...}}` em maiúsculas: funciona, mas a citação só sai certa se `org-short` estiver em caixa normal. Ao revisar, prefira a forma em caixa normal.

### Obra sem autoria

Deixe `author` vazio e escreva o título normalmente. O estilo põe em maiúsculas a primeira palavra (ou o artigo/monossílabo e a palavra seguinte): "ANTEPROJETO de lei", "A FLOR prometida". O subtítulo vai em `subtitle`, não no `title`, ou a chamada da citação pega a palavra errada.

### Campos próprios do modelo

| Campo | Uso |
|---|---|
| `subtitle` | subtítulo, impresso após dois-pontos, sem negrito |
| `org-short` | forma da instituição ou jurisdição na citação |
| `urlaccessdate` | data de acesso: `3 out. 2026` (mês abreviado em minúsculas) |
| `type` (teses) | `Mestrado em Engenharia Civil`; o estilo escreve "Dissertação (Mestrado em ...)" |
| `conference-number`, `conference-year`, `conference-location` | número, ano e cidade do evento em `@inproceedings` |
| `editortype` | `ed.` ou `org.` para obra organizada |
| `note` | DOI (`DOI 10.xxxx/...`), versão de software, descrição física |

### Modelos por tipo

Artigo de periódico:
```bibtex
@article{lima2021,
    author = {Lima, José and Costa, Ana},
    title = {Título do artigo},
    journal = {Revista Brasileira de Recursos Hídricos},
    address = {Porto Alegre},
    volume = {26},
    number = {2},
    pages = {10-20},
    month = {mar.},
    year = {2021},
    note = {DOI 10.1590/2318-0331.262120200123},
    url = {https://doi.org/10.1590/2318-0331.262120200123},
    urlaccessdate = {20 jul. 2026}
}
```

Livro:
```bibtex
@book{silva2019,
    author = {Silva, Antônio Augusto},
    title = {Hidrologia aplicada},
    subtitle = {princípios e métodos},
    edition = {2},
    address = {Fortaleza},
    publisher = {Edições UFC},
    year = {2019}
}
```

Capítulo de livro:
```bibtex
@incollection{souza2003,
    author = {{\relax Souza Filho}, F. A.},
    title = {Sistemas de suporte às decisões},
    booktitle = {Gestão de águas},
    editor = {Campos, Nilson and Studart, T. M. C.},
    editortype = {ed.},
    address = {Fortaleza},
    publisher = {[s. n.]},
    pages = {87-110},
    year = {2003}
}
```

Dissertação ou tese:
```bibtex
@mastersthesis{almeida2018,
    author = {Almeida, Maria},
    title = {Avaliação de reservatórios},
    school = {Universidade Federal do Ceará},
    address = {Fortaleza},
    year = {2018},
    type = {Mestrado em Engenharia Civil},
    url = {https://repositorio.ufc.br/handle/riufc/00000},
    urlaccessdate = {3 out. 2026}
}
```
Sai "ALMEIDA, M. **Avaliação de reservatórios**. Dissertação (Mestrado em Engenharia Civil) – Universidade Federal do Ceará, Fortaleza, 2018." Para tese, `@phdthesis` com `type = {Doutorado em ...}`. Se o trabalho tiver número de folhas, use `pages = {144}`.

Trabalho em evento:
```bibtex
@inproceedings{lam2015,
    author = {Lam, Siu Kwan and Pitrou, Antoine and Seibert, Stanley},
    title = {Numba},
    subtitle = {a {LLVM}-based {Python} {JIT} compiler},
    organization = {Workshop on the LLVM Compiler Infrastructure in HPC},
    booktitle = {Proceedings [...]},
    conference-number = {2},
    conference-year = {2015},
    conference-location = {Austin},
    address = {New York},
    publisher = {Association for Computing Machinery},
    year = {2015},
    pages = {1-6}
}
```
Em português, `booktitle = {Anais [...]}`.

Norma técnica:
```bibtex
@book{nbr10520,
    organization = {Associação Brasileira de Normas Técnicas},
    title = {{NBR} 10520},
    subtitle = {informação e documentação: citações em documentos: apresentação},
    edition = {2},
    address = {Rio de Janeiro},
    publisher = {ABNT},
    year = {2023}
}
```

Legislação:
```bibtex
@misc{lei9433,
    organization = {Brasil},
    title = {Lei nº 9.433, de 8 de janeiro de 1997},
    subtitle = {institui a Política Nacional de Recursos Hídricos},
    address = {Brasília, DF},
    publisher = {Presidência da República},
    year = {1997},
    url = {https://www.planalto.gov.br/ccivil_03/leis/l9433.htm},
    urlaccessdate = {10 out. 2026}
}
```

Site, software ou documento só online: `@misc` com `url` e `urlaccessdate`; versão e descrição em `note`.

### Outras convenções

- **Maiúsculas em títulos**: o estilo mantém a caixa do .bib. Escreva como na norma (só a inicial e nomes próprios em maiúscula, em português) e proteja nomes próprios e siglas com chaves: `{Brasil}`, `{Python}`, `{SIGA}`.
- **Sem local, editora ou data**: `address = {[S. l.]}`, `publisher = {[s. n.]}`, `year = {[20--]}` ou `{[2024?]}`.
- **DOI**: em `note` como `DOI 10.xxxx/yyyy` e em `url` como `https://doi.org/10.xxxx/yyyy`. Confira que o DOI resolve para o trabalho citado.
- **Link**: só o endereço do documento, sem parâmetros de rastreamento (`utm_source`, `fbclid`, `referrer`).
- **Páginas**: intervalo com hífen ou `--`, o estilo normaliza para hífen; total de páginas de livro em `pages = {292}`.

## Revisar as referências de um trabalho

1. Rode `scripts/auditar.py`: ele cruza `\cite` com o .bib e aponta autor em caixa alta, link com rastreador, documento online sem data de acesso, letra escrita no ano e entradas não citadas.
2. Para cada entrada, confira contra a fonte: autores e grafia, título e subtítulo, edição, local, editora, ano, páginas, DOI. Abra o DOI ou o link. Não invente dado que falta: use as marcas da ABNT (`[S. l.]`, `[s. n.]`, `[20--]`) e informe o autor do que ficou pendente.
3. Compile e leia a lista no PDF. Compare duas ou três entradas de cada tipo com os exemplos do guia de referências da UFC.
4. Entrada que o estilo não monta direito (tipos raros: patente, mapa, documento sonoro): corrija na própria entrada e diga ao autor que ela precisa de conferência manual. Não edite o .bst por causa de uma entrada.

Referência citada só para conferir a chamada: `\nocite{chave}` põe a entrada na lista sem citação no texto; a NBR 10520 pede correspondência entre citação e lista, então use apenas em listas de "obras consultadas" pedidas pelo curso.
