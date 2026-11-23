#!/usr/bin/env python3
"""Configura um trabalho novo no modelo ufcTex a partir de um arquivo JSON.

Uso:
    python3 novo_trabalho.py <pasta-do-trabalho> dados.json [--limpar]

A pasta precisa já ter o modelo (rode obter_modelo.sh antes). O JSON tem os
campos abaixo; os ausentes ficam como estão no modelo e são listados no fim.

{
  "tipo": "tccgraduacao | tccespecializacao | dissertacao | tese",
  "autor": "Nome Completo",
  "titulo": "Título do trabalho: subtítulo",
  "local": "Crateús",
  "ano": "2027",
  "centro": "Campus de Crateús",
  "departamento": "",
  "curso": "Engenharia Civil",            (TCC de graduação)
  "grau": "bacharel",                      (TCC de graduação: bacharel, licenciado)
  "especializacao": "",                    (TCC de especialização)
  "programa": "Programa de Pós-Graduação em ...",   (dissertação ou tese)
  "nome_curso_pos": "Mestrado Acadêmico em ...",     (dissertação ou tese)
  "titulo_obtido": "Engenharia Civil",     (mestre em / doutor em)
  "area_concentracao": "",                 (dissertação ou tese)
  "orientador": {"nome": "Prof. Dr. ...", "ies": "Universidade Federal do Ceará (UFC)", "centro": "", "feminino": false},
  "coorientador": {"nome": "", "ies": "", "centro": "", "feminino": false},
  "banca": [{"nome": "Prof. Dr. ...", "ies": "...", "centro": ""}]   (até 5 membros além de orientador e coorientador)
}

--limpar troca o conteúdo de exemplo (capítulos, referências, apêndices,
anexos, figuras, resumo) por um esqueleto vazio, mantendo as listas de siglas
e símbolos com exemplos comentados.
"""
import json
import re
import sys
from pathlib import Path

NUMEROS_BANCA = ["dois", "tres", "quatro", "cinco", "seis"]


def set_cmd(tex, cmd, valor):
    """Troca o argumento de um comando \\cmd{...} de linha inteira no preâmbulo."""
    padrao = re.compile(r"^(\s*\\" + cmd + r"\{)(.*?)(\}\s*(%.*)?)$", re.M)
    if not padrao.search(tex):
        raise KeyError(cmd)
    valor = valor.replace("\\", "\\\\")
    return padrao.sub(lambda m: m.group(1) + valor + m.group(3), tex, count=1)


def escolher_tipo(tex, tipo):
    tipos = ["tccgraduacao", "tccespecializacao", "dissertacao", "tese"]
    if tipo not in tipos:
        sys.exit(f"tipo inválido: {tipo}. Use um de {tipos}")
    for t in tipos:
        tex = re.sub(r"^%?\\trabalhoacademico\{" + t + r"\}",
                     ("" if t == tipo else "%") + r"\\trabalhoacademico{" + t + "}", tex, flags=re.M)
    return tex


def configurar(pasta, dados):
    doc = pasta / "documento.tex"
    tex = doc.read_text(encoding="utf-8")
    pendentes = []

    def campo(cmd, chave, obj=dados):
        nonlocal tex
        valor = obj.get(chave)
        if valor is None:
            pendentes.append(cmd)
            return
        tex = set_cmd(tex, cmd, str(valor))

    if "tipo" in dados:
        tex = escolher_tipo(tex, dados["tipo"])
    else:
        pendentes.append("trabalhoacademico")
    campo("autor", "autor")
    campo("titulo", "titulo")
    campo("local", "local")
    campo("data", "ano")
    campo("centro", "centro")
    campo("departamento", "departamento")
    campo("graduacaoem", "curso")
    campo("habilitacao", "grau")
    campo("especializacaoem", "especializacao")
    campo("programamestrado", "programa")
    campo("programadoutorado", "programa")
    campo("nomedomestrado", "nome_curso_pos")
    campo("nomedodoutorado", "nome_curso_pos")
    campo("mestreem", "titulo_obtido")
    campo("doutorem", "titulo_obtido")
    campo("areadeconcentracaomestrado", "area_concentracao")
    campo("areadeconcentracaodoutorado", "area_concentracao")
    # A data de aprovação fica em branco até a defesa (NBR 14724:2024, 4.2.1.3).
    tex = set_cmd(tex, "dataaprovacao", "")

    ori = dados.get("orientador", {})
    for cmd, chave in [("orientador", "nome"), ("orientadories", "ies"), ("orientadorcentro", "centro")]:
        campo(cmd, chave, ori)
    if ori:
        tex = set_cmd(tex, "orientadorfeminino", "sim" if ori.get("feminino") else "nao")

    coo = dados.get("coorientador", {"nome": ""})
    for cmd, chave in [("coorientador", "nome"), ("coorientadories", "ies"), ("coorientadorcentro", "centro")]:
        tex = set_cmd(tex, cmd, coo.get(chave, ""))
    tex = set_cmd(tex, "coorientadorfeminino", "sim" if coo.get("feminino") else "nao")

    banca = dados.get("banca")
    if banca is None:
        pendentes.append("banca")
    else:
        if len(banca) > 5:
            sys.exit("O modelo aceita no máximo 5 membros de banca além de orientador e coorientador.")
        for i, n in enumerate(NUMEROS_BANCA):
            m = banca[i] if i < len(banca) else {}
            tex = set_cmd(tex, f"membrodabanca{n}", m.get("nome", ""))
            tex = set_cmd(tex, f"membrodabanca{n}ies", m.get("ies", ""))
            tex = set_cmd(tex, f"membrodabanca{n}centro", m.get("centro", ""))

    doc.write_text(tex, encoding="utf-8")
    return pendentes


ESQUELETO = {
    "1-introducao.tex": "Introdução",
    "2-fundamentacao-teorica.tex": "Fundamentação teórica",
    "3-metodologia.tex": "Metodologia",
    "4-resultados.tex": "Resultados e discussão",
    "5-conclusao.tex": "Conclusão",
}


def limpar(pasta):
    textuais = pasta / "2-textuais"
    for f in textuais.glob("*.tex"):
        f.unlink()
    for nome, titulo in ESQUELETO.items():
        rotulo = "sec:" + nome.split("-", 1)[1].replace(".tex", "")
        (textuais / nome).write_text(
            f"\\chapter{{{titulo}}}\n\\label{{{rotulo}}}\n\n% Texto da seção.\n", encoding="utf-8")

    pos = pasta / "3-pos-textuais"
    (pos / "referencias.bib").write_text(
        "% Referências do trabalho. Veja as regras de preenchimento no README.md do modelo.\n",
        encoding="utf-8")
    for sub in ("apendices", "anexos"):
        for f in (pos / sub).iterdir():
            f.unlink()
    for f in (pasta / "figuras").iterdir():
        f.unlink()

    pre = pasta / "1-pre-textuais"
    (pre / "resumo.tex").write_text(
        "% Resumo em parágrafo único, de 150 a 500 palavras (NBR 6028:2021, 4.1.2 e 4.1.8).\n"
        "% Palavras-chave em minúsculas (exceto nomes próprios), separadas por ponto e vírgula\n"
        "% e terminadas por ponto (NBR 6028:2021, 4.1.7).\n\n"
        "Texto do resumo.\n\n\\palavraschave{palavra-chave; palavra-chave; palavra-chave.}\n",
        encoding="utf-8")
    (pre / "abstract.tex").write_text(
        "% Tradução do resumo, com o mesmo conteúdo.\n\n"
        "Abstract text.\n\n\\keywords{keyword; keyword; keyword.}\n", encoding="utf-8")

    doc = pasta / "documento.tex"
    tex = doc.read_text(encoding="utf-8")
    # Capítulos do esqueleto
    tex = re.sub(r"(\\textual\n)(?:\s*\\input\{2-textuais/[^}]+\}\n)+",
                 lambda m: m.group(1) + "".join(f"\t\\input{{2-textuais/{n[:-4]}}}\n" for n in ESQUELETO), tex)
    # Apêndices e anexos: comentados até existirem
    tex = re.sub(r"^(\s*)(\\input\{3-pos-textuais/(?:apendices|anexos)/[^}]+\})", r"\1% \2", tex, flags=re.M)
    tex = re.sub(r"^(\s*)(\\imprimir(?:apendices|anexos))\s*$", r"\1% \2", tex, flags=re.M)
    # Elementos opcionais: ficam comentados até o autor escrever
    for cmd in ("imprimirdedicatoria", "imprimiragradecimentos", "imprimirepigrafe",
                "imprimirlistadeilustracoes", "imprimirlistadetabelas", "imprimirlistadesimbolos"):
        tex = re.sub(r"^(\s*)(\\" + cmd + r"\b)", r"\1% \2", tex, flags=re.M)
    tex = tex.replace("\\renewcommand*\\listfigurename{Lista de Figuras}", "% \\renewcommand*\\listfigurename{Lista de Figuras}")
    doc.write_text(tex, encoding="utf-8")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta = Path(sys.argv[1])
    if not (pasta / "lib" / "ufcTex.sty").exists():
        sys.exit(f"{pasta} não tem o modelo. Rode obter_modelo.sh antes.")
    dados = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    pendentes = configurar(pasta, dados)
    if "--limpar" in sys.argv:
        limpar(pasta)
    tipo = dados.get("tipo", "")
    irrelevantes = {
        "tccgraduacao": {"especializacaoem", "programamestrado", "programadoutorado", "nomedomestrado",
                         "nomedodoutorado", "mestreem", "doutorem", "areadeconcentracaomestrado",
                         "areadeconcentracaodoutorado"},
        "tccespecializacao": {"graduacaoem", "habilitacao", "programamestrado", "programadoutorado",
                              "nomedomestrado", "nomedodoutorado", "mestreem", "doutorem",
                              "areadeconcentracaomestrado", "areadeconcentracaodoutorado"},
        "dissertacao": {"graduacaoem", "habilitacao", "especializacaoem", "programadoutorado",
                        "nomedodoutorado", "doutorem", "areadeconcentracaodoutorado"},
        "tese": {"graduacaoem", "habilitacao", "especializacaoem", "programamestrado",
                 "nomedomestrado", "mestreem", "areadeconcentracaomestrado"},
    }.get(tipo, set())
    faltam = [p for p in pendentes if p not in irrelevantes]
    print("documento.tex configurado.")
    if faltam:
        print("Campos sem valor no JSON (continuam com o texto do modelo): " + ", ".join(faltam))


if __name__ == "__main__":
    main()
