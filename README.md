Para utilizar este template siga o tutorial disponível em: http://www.biblioteca.ufc.br/images/arquivos/instrucoes_modelos/tutorial_sharelatex.pdf

# Últimas alterações
23/11/2026
    -Citações conforme ABNT NBR 10520:2023: autor pessoa física e jurídica em maiúsculas e minúsculas, et al. só a partir de quatro autores (opção abnt-etal-cite=3), obra sem autoria com [...], apud em itálico.
    -Referências conforme ABNT NBR 6023:2025: letras a/b também na lista de referências (1927a, 1927b), hífen em intervalos de páginas (p. 51-60), entrada pelo título com artigo ou monossílabo e a palavra seguinte em maiúsculas (A FLOR prometida).
    -Caixa alta das referências feita pelo LaTeX (\abntupper), o que corrige sobrenomes e instituições acentuados (GONÇALVES, ASSOCIAÇÃO) e iniciais acentuadas (É., Â.).
    -Instituições escritas com author = {{Nome da Instituição}} vão para maiúsculas na lista de referências.
    -Corrigido erro de compilação em \imprimirapendices e \imprimiranexos e o espaço após o traço em "APÊNDICE A – TÍTULO".
    -Filete das notas de rodapé com 5 cm (ABNT NBR 14724:2024, 5.2.1).
    -Indicativo de seção separado do título por um espaço (ABNT NBR 6024:2012).
    -Caminho da errata corrigido no documento.tex.
    -Arquivo de referências de exemplo atualizado e novo documento de teste (teste-normas.tex).
    -Lista de referências ordenada sem considerar acentos (ÁVILA entre ASSOCIAÇÃO e BRASIL; antes ia para o fim).
    -Pacote float carregado depois do ufcTex.sty: [H] fixa figuras, tabelas e quadros no ponto do texto.
    -Capa sem linha vazia quando o campus não tem centro ou departamento (\\departamento{} vazio gerava erro).
    -latexmkrc que roda o makeglossaries: basta latexmk documento.tex (o Overleaf também usa este arquivo).
22/07/2022
    -atualizações em todas as partes do template, visando adequar as novas normas da ABNT, conforme parecer emitido pela Comissão de Normalização do Sistema de Bibliotecas da UFC.

03-07-2017              
    -Contagem de tabelas corrigida;
    -Dois pontos após fonte de figuras e tabelas;       
    -Inclusão do departamento na capa do trabalho;      
    -As equações foram alocadas completamente as esquerda. 
04-07-2017
    -inclusão de pdf em apêndice;
    -inclusão de pdf em anexo.
06-07-2017
    -espaçamento dos títulos de figuras, tabelas e quadros foram alterados de 1.5 para espaçamento simples (1.0);
    -Margens dos títulos das figuras ajustadas para ficar do tamanho da figura;
    -Margens dos títulos das tabelas ajustados para ficar do tamanho da tabela;
    -Quadro circunscrito de figuras retirados exceto, figuras de resultados.
    -espaçamento entre linhas ajustado para espaçamento simples nos títulos e legendas de figuras e tabelas;
10-07-2017
    -Elaboração de textos explicativos sobre figuras e equações;
    -Pasta renomeadas para ficar na ordem de pre, textual e pós;  
12-07-2017
    -O nome da pasta das referência estava errado. Isso fazia aparecer um ponto de interrogação nas citações. Isso já foi corrigido.
14-07-2017
    -Espaçamento corrigido entre o texto de identificação do trabalho e o orientador.
18-09-2017
    -Nome da LISTA DE ILUSTRAÇÕES alterado para LISTA DE FIGURAS
15-01-2018
    -Alteração do ano de 2017 para 2018
20-02-2018
    -Alteração do nome "Coorientador" de acordo com a nova norma ortográfica
24-02-2018
    -Inclusão de um texto chamando a atenção para o usuário configurar a opção referente ao nível do trabalho acadêmico que está sendo desenvolvido (tcc de graduação, trabalho de especialização, dissertação de mestrado ou tese de doutorado) nas primeiras opções do arquivo "documento.tex"
22-03-2018
    -Atualização dos e-mails para dúvidas e sugestões;
21-11-2018
    -Adicionada opção para alterar a fonte de todo o texto de Times New Roman para Arial. Basta descomentar as linhas 80 e 81 do arquivo "preambulo.tex" dentro da pasta "lib".
    -Nota de esclarecimento quanto a limitação da geração do referencial bibliográfico. 
09-01-2019
    -Acrescentado comentário explicando com deixar as equações centralizadas na linas 59 do arquivo "documento"
23-01-2019
    -Correção de erro de compilação na linha 60 do arquivo documentos. 
    -Nota de esclarecimento de como utilizar siglas.
07-06-2019
    -Atualização de contato para dúvidas e sugestões.
18-02-2020
    -Lista de abreviaturas alterada. Estava em ordem alfabética e agora está em ordem que é citada no texto.
    -Seções foram alterada para somente a primeira letra ficar em maiúsculo.
    -Nomes de apêndices e anexos corrigidos para ficarem totalmente em maiúsculo e negrito.
    -Citação com número de página incluída.
    -Marcadores de itens modificados para "-".
21-02-2020    
    -criacao do arquivo "ufcTexcite.sty" na pasta "lib". Esse arquivo substitui o "abntTex2cite" que estava desatualizado perante a ABNT NBR 6023/2018. Nem todos as atualizacoes foram implementadas. Isso requer atencao do usuario para adequar ao guia de normalizacao academico. 
    -Removido os simbolos "<" e ">" dos enderecos eletronicos.
    -Adicionado o arquivo "abntex2-alf.bst" para alterar os simbolos "[S.l.]" e "[S.n.]" para italico e separados por espaco automaticamente. Antes isso so era possivel manualmente. 
24-02-2020
    -Travessão substituído por hífen no arquivo abntex2-alf.bst. 
25-02-2020
    -Correção de citação de estado.    
26-02-2020
    -Espaçamento após hífen removido alterando linha 404 do arquivo "abntex2.cls" e linhas 1280 e 1379 do arquivo "ufcTex.sty"
28-02-2020
    - Acrescentado novo colaborador da biblioteca central.
    - Problema com espaço apos hifem resolvido provisoriamente.

# O que é?

O **ufctex** é um projeto adaptado do [abnTeX2] da Associação Brasileira de normas técnicas [ueceTeX] da Universidade Estadual do Ceará. Essa versão, foi criada para o desenvolvimento de trabalhos acadêmicos de acordo com as normas da Universidade Federal do Ceará. Este template deve ser utilizado online de qualquer computador ou sistema operacional sem a necessidade de instalação e foi disponibilizada no OverLeaf. Entretanto, é possível baixar o template e trabalhar offline também. 

Espera-se que o projeto seja um modelo de trabalho acadêmico que implemente todas as exigências das normas da ABNT sem a necessidade de se preocupar com o estilo ou formatação do documento. Entretanto, a geração de referências bibliográficas automática apresenta limitações quanto a formatação exigida pela biblioteca da UFC. E devem ser ajustadas manualmente estando sujeitas a revisão do bibliotecário.

Atenciosamente,

Prof. Dr. Ednardo Rodrigues
Seara da Ciência
Departamento de Engenharia Elétrica.


### Modelos Disponíveis

**Trabalhos Acadêmicos**

 - Trabalho de Conclusão de Curso de Graduação
 - Trabalho de Conclusão de Curso de Especialização
 - Dissertação de Mestrado Acadêmico e Profissional
 - Tese de Doutorado
 
**Qualificações**

 - Qualificação para Mestrado Acadêmico e Profissional

# Limitações
 
 O modelo atual possui algumas limitações que podem ser corrigidas ou implementadas em alguma versão futura. São elas:
 
  - O modelo permite a participação de somente um co-orientador
  - A folha de aprovação da Dissertação suporta no máximo 5 pessoas (Orientador, Co-orientador e 3 membros externos)
  - A folha de aprovação da Tese suporta no máximo 6 pessoas (Orientador, Co-orientador e 4 membros externos)
  - As referências possuem muitas variações, portanto, o autor deve está atento se o arquivo gerado corresponde ao esperado.
  
# Dicas
Veja a seguir como inserir alguns elementos no seu texto.

### Como inserir uma Tabela
```tex
\begin{table}[h!]	
	\centering
	\Caption{\label{tab:label_da_tabela} Legenda da Tabela}
	\UFCtab{}{
		\begin{tabular}{ccll}
			\toprule
	    		Quisque & pharetra & tempus & vulputate \\
			\midrule \midrule
				E1 & Complete coverage & Both splice sites \\
				E2 & Complete coverage & Both splice sites \\
				E3 & Partial coverage & Both splice sites & Both \\
				E4 & Partial coverage & One splice site & Both \\
				E5 & Complete or coverage & No splice & Both \\
				E6 & No coverage & No splice sites\\
			\bottomrule
		\end{tabular}
	}{
		\Fonte{Elaborado pelo autor}
    }
\end{table}
```

### Como inserir um Quadro
```tex
\begin{quadro}[h!]	
	\centering
	\Caption{\label{qua:label_do_quadro} Legenda do Quadro}
	\UFCqua{}{
		\begin{tabular}{|c|c|}
			\hline
			Quisque & pharetra \\
			\hline
			E1 & Complete coverage  \\
			\hline
			E2 & Complete coverage \\
			\hline
		\end{tabular}
	}{
		\Fonte{Elaborado pelo autor}
	}
\end{quadro}
```

### Como inserir uma figura
```tex
\begin{figure}[h!]
	\centering
	\Caption{\label{fig:label_da_figura} Legenda da Figura}	
	\UFCfig{}{
	    \includegraphics[width=8cm]{figuras/figura-1}
	}{
	    \Fonte{Elaborado pelo autor}
	}	
\end{figure}
```

### Como inserir uma alínea
```tex
\begin{alineas}
	\item Lorem ipsum dolor sit amet;
    \item Praesent vitae nulla varius;
	\item Praesent quis erat eleifend;
	\item Mauris facilisis odio eu:
	\begin{subalineas}
		\item Integer non lacinia magna;
		\item Proin mattis placerat risus.
	\end{subalineas}
\end{alineas}
```

### Como criar Seções
A ABNT NBR 14724:2024 (4.2.2) determina que o trabalho seja organizado em seções e não em capítulos. No modelo, a seção primária é criada com `\chapter`, que só gera o número e o título (por exemplo, "1 INTRODUÇÃO"), sem a palavra "Capítulo".
```tex
% Seção Primária
\chapter{Fundamentação Teórica}
\label{sec:fundamentacao-teorica}

% Seções Secundárias
\section{Objetivo Geral 2}
\label{sec:objetivo-geral-2}

% Seções Terciárias
\subsection{Objetivo Geral 3}
\label{sec:objetivo-geral-3}

% Seções Quaternárias
\subsubsection{Objetivo Geral 4}
\label{sec:objetivo-geral-4}

% Seções Quinárias
\subsubsubsection{Objetivo Geral 5}
\label{sec:objetivo-geral-5}
```

### Como inserir um algoritmo
```tex
\begin{algorithm}[h!]
	\SetSpacedAlgorithm
	\caption{\label{alg:algoritmo_de_colonica_de_formigas}Algoritmo de Otimização por Colônia de Formiga}
	\Entrada{Entrada do Algoritmo}
	\Saida{Saida do Algoritmo}
	\Inicio{
		Atribua os valores dos parâmetros\;
		Inicialize as trilhas de feromônios\;
		\Enqto{não atingir o critério de parada}{
			\Para{cada formiga}{
				Construa as Soluções\;
			}
			Aplique Busca Local (Opcional)\;
			Atualize o Feromônio\;
		}	
	}
\end{algorithm}
```

### Como inserir referências

Regras do arquivo .bib para o estilo atualizado (ABNT NBR 6023:2025 e NBR 10520:2023):

 - Escreva os nomes em caixa normal, no formato Sobrenome, Prenome: `author = {Gonçalves, Érica and Silva, José}`. O estilo coloca os sobrenomes em maiúsculas na lista de referências e mantém maiúsculas e minúsculas na citação: (Gonçalves; Silva, 2022).
 - Sobrenome composto com hífen ou que começa com letra acentuada, quando houver mais de uma palavra, vai entre chaves: `author = {{Ângelo-Ítalo}, Jean-Paul}`.
 - Instituição como autor vai entre chaves duplas, em caixa normal: `author = {{Organização Mundial da Saúde}}`.
 - Órgão de jurisdição (Estado, Município): `organization = {São Paulo \NoCaseChange{(Estado). Secretaria do Meio Ambiente}}` e `org-short = {São Paulo}`. Na lista sai "SÃO PAULO (Estado). Secretaria do Meio Ambiente." e no texto "(São Paulo, 1999)".
 - Obra sem autoria: deixe `author` vazio. A entrada usa a primeira palavra do título, ou o artigo ou monossílabo e a palavra seguinte: "ANTEPROJETO de lei", "(Anteprojeto [...], 1987)".
 - Para conferir o estilo depois de qualquer mudança em `lib/`, compile o `teste-normas.tex`, que exercita todos esses casos.


@article{article,
  author  = {Peter Adams}, 
  title   = {The title of the work},
  journal = {The name of the journal},
  year    = 1993,
  number  = 2,
  pages   = {201-213},
  month   = 7,
  note    = {An optional note}, 
  volume  = 4
}

@book{book,
  author    = {Peter Babington}, 
  title     = {The title of the work},
  publisher = {The name of the publisher},
  year      = 1993,
  volume    = 4,
  series    = 10,
  address   = {The address},
  edition   = 3,
  month     = 7,
  note      = {An optional note},
  isbn      = {3257227892}
}

@booklet{booklet,
  title        = {The title of the work},
  author       = {Peter Caxton}, 
  howpublished = {How it was published},
  address      = {The address of the publisher},
  month        = 7,
  year         = 1993,
  note         = {An optional note}
}

@conference{conference,
  author       = {Peter Draper}, 
  title        = {The title of the work},
  booktitle    = {The title of the book},
  year         = 1993,
  editor       = {The editor},
  volume       = 4,
  series       = 5,
  pages        = 213,
  address      = {The address of the publisher},
  month        = 7,
  organization = {The organization},
  publisher    = {The publisher},
  note         = {An optional note}  
}

@inbook{inbook,
  author       = {Peter Eston}, 
  title        = {The title of the work},
  chapter      = 8,
  pages        = {201-213},
  publisher    = {The name of the publisher},
  year         = 1993,
  volume       = 4,
  series       = 5,
  address      = {The address of the publisher},
  edition      = 3,
  month        = 7,
  note         = {An optional note}
}

@incollection{incollection,
  author       = {Peter Farindon}, 
  title        = {The title of the work},
  booktitle    = {The title of the book},
  publisher    = {The name of the publisher},
  year         = 1993,
  editor       = {The editor},
  volume       = 4,
  series       = 5,
  chapter      = 8,
  pages        = {201-213},
  address      = {The address of the publisher},
  edition      = 3,
  month        = 7,
  note         = {An optional note}
}


@manual{manual,
  title        = {The title of the work},
  author       = {Peter Gainsford}, 
  organization = {The organization},
  address      = {The address of the publisher},
  edition      = 3,
  month        = 7,
  year         = 1993,
  note         = {An optional note}
}

@mastersthesis{mastersthesis,
  author       = {Peter Harwood}, 
  title        = {The title of the work},
  school       = {The school where the thesis was written},
  year         = 1993,
  address      = {The address of the publisher},
  month        = 7,
  note         = {An optional note}
}

@misc{misc,
  author       = {Peter Isley}, 
  title        = {The title of the work},
  howpublished = {How it was published},
  month        = 7,
  year         = 1993,
  note         = {An optional note}
}

@phdthesis{phdthesis,
  author       = {Peter Joslin}, 
  title        = {The title of the work},
  school       = {The school where the thesis was written},
  year         = 1993,
  address      = {The address of the publisher},
  month        = 7,
  note         = {An optional note}
}

@proceedings{proceedings,
  title        = {The title of the work},
  year         = 1993,
  editor       = {Peter Kidwelly},
  volume       = 4,
  series       = 5,
  address      = {The address of the publisher},
  month        = 7,
  organization = {The organization},
  publisher    = {The name of the publisher},
  note         = {An optional note}
}

@techreport{techreport,
  author       = {Peter Lambert}, 
  title        = {The title of the work},
  institution  = {The institution that published},
  year         = 1993,
  number       = 2,
  address      = {The address of the publisher},
  month        = 7,
  note         = {An optional note}
}

@unpublished{unpublished,
  author       = {Peter Marcheford}, 
  title        = {The title of the work},
  note         = {An optional note},
  month        = 7,
  year         = 1993
}


# Atenção

O ufcteX é fornecido gratuitamente e sem garantias e pode ser redistribuído livremente para fins acadêmicos. 

# Agradecimentos

![alt tag](http://www.goes.uece.br/style/images/logo_goes.png)

Grupo de Otimização em Engenharia de Software



[Por Onde Comecar]:https://code.google.com/p/abntex2/wiki/PorOndeComecar

Projeto original da UECE: [http://www.goes.uece.br]:http://www.goes.uece.br
[http://www.goes.uece.br]
[abnTeX2]:https://code.google.com/p/abntex2/
[http://miktex.org/download]:http://miktex.org/download
[http://texstudio.sourceforge.net/]:http://texstudio.sourceforge.net/


