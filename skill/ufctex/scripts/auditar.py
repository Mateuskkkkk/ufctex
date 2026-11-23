#!/usr/bin/env python3
"""Audita um trabalho no modelo ufcTex contra as normas da ABNT e o guia da UFC.

Uso:
    python3 auditar.py <pasta-do-trabalho> [--md relatorio.md]

Confere o código-fonte (documento.tex, pré-textuais, capítulos, apêndices,
referencias.bib, siglas) e, se houver, o documento.pdf. Não altera nada.
O relatório separa:
  BLOQUEIA   a biblioteca recusa ou o PDF sai errado;
  CORRIGIR   fora da norma, mas o trabalho compila e é legível;
  CONFERIR   pode estar certo; precisa de leitura humana.
"""
import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

FICHA_INSTRUCAO_MD5 = "b226c50ca133faf9c8501375e3166770"  # PDF de instruções que vem no modelo
PLACEHOLDERS = [r"\bX[xX]{3,}", r"Nome Sobrenome", r"T[íi]tulo do Trabalho", r"\(Se houver\)",
                r"\(SIGLA\)", r"xx/xx/xxxx", r"Universidade do Membro", r"INSERIR", r"\[Nome\]",
                r"\bTODO\b", r"Texto do resumo", r"Abstract text", r"palavra-chave; palavra-chave"]

achados = []


def add(sev, onde, msg):
    achados.append((sev, onde, msg))


def ler(p):
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="latin-1")


def sem_comentarios(tex):
    return re.sub(r"(?<!\\)%.*", "", tex)


def linhas(tex):
    for i, l in enumerate(tex.split("\n"), 1):
        yield i, re.sub(r"(?<!\\)%.*", "", l)


def palavras_latex(tex):
    t = sem_comentarios(tex)
    t = re.sub(r"\\(palavraschave|keywords)\{.*?\}", " ", t, flags=re.S)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}$]", " ", t)
    return [w for w in t.split() if re.search(r"\w", w)]


def arquivos_texto(raiz, doc):
    """Arquivos .tex incluídos por \\input/\\include ativos no documento.tex."""
    vistos = []
    for m in re.finditer(r"\\(?:input|include|imprimir\w+)\{([^}]+)\}", sem_comentarios(doc)):
        p = raiz / m.group(1)
        if p.suffix != ".tex":
            p = p.with_suffix(".tex")
        if p.exists():
            vistos.append(p)
    return vistos


def auditar_modelo(raiz):
    bst = raiz / "lib" / "abntex2-alf.bst"
    if not bst.exists():
        add("BLOQUEIA", "lib/", "Não é um projeto ufcTex (falta lib/abntex2-alf.bst).")
        return False
    if "ufcTex 2026" not in ler(bst):
        add("CORRIGIR", "lib/",
            "Modelo anterior à atualização de 2026: citações e referências saem pela NBR 10520:2002 "
            "e NBR 6023:2018 (caixa alta em citação de instituição, et al. com três autores, "
            "acentos quebrados). Atualize com scripts/atualizar_lib.sh.")
    pre = raiz / "lib" / "preambulo.tex"
    if pre.exists() and "abnt-etal-cite=2" in ler(pre):
        add("CORRIGIR", "lib/preambulo.tex",
            "abnt-etal-cite=2 põe et al. com três autores; a NBR 10520:2023 (6.1.2) só admite a partir de quatro. Use 3.")
    return True


CAMPOS_POR_TIPO = {
    "graduacaoem": "tccgraduacao", "habilitacao": "tccgraduacao",
    "especializacaoem": "tccespecializacao",
    "programamestrado": "dissertacao", "nomedomestrado": "dissertacao", "mestreem": "dissertacao",
    "areadeconcentracaomestrado": "dissertacao",
    "programadoutorado": "tese", "nomedodoutorado": "tese", "doutorem": "tese",
    "areadeconcentracaodoutorado": "tese",
}


def auditar_documento(raiz, doc):
    d = sem_comentarios(doc)
    tipos = re.findall(r"\\trabalhoacademico\{(\w+)\}", d)
    if len(tipos) != 1:
        add("BLOQUEIA", "documento.tex", f"Deve haver exatamente um \\trabalhoacademico ativo; há {len(tipos)}.")
    tipo = tipos[0] if tipos else ""
    for i, l in linhas(doc):
        m = re.match(r"\s*\\(\w+)\{", l)
        if m and m.group(1) in CAMPOS_POR_TIPO and CAMPOS_POR_TIPO[m.group(1)] != tipo:
            continue  # campo de outro tipo de trabalho: não é impresso
        for ph in PLACEHOLDERS:
            if re.search(ph, l) and not re.search(r"\\(dataaprovacao)", l):
                add("BLOQUEIA", f"documento.tex:{i}", f"Texto de exemplo do modelo: {l.strip()[:90]}")
                break
    m = re.search(r"\\imprimirfichacatalografica\{([^}]+)\}", d)
    if m:
        pdf = raiz / (m.group(1) if m.group(1).endswith(".pdf") else m.group(1) + ".pdf")
        if pdf.exists() and hashlib.md5(pdf.read_bytes()).hexdigest() == FICHA_INSTRUCAO_MD5:
            add("BLOQUEIA", str(pdf.relative_to(raiz)),
                "A ficha catalográfica ainda é a página de instruções do modelo. Gere a ficha em "
                "fichacatalografica.ufc.br e substitua o PDF (o verso da folha de rosto não é contado; NBR 14724:2024, 5.3).")
    if not m:
        add("CONFERIR", "documento.tex",
            "Ficha catalográfica desativada. Na versão de depósito ela é obrigatória no verso da folha de rosto "
            "(NBR 14724:2024, 4.2.1.1.2): gere em fichacatalografica.ufc.br e ative \\imprimirfichacatalografica.")
    m = re.search(r"\\dataaprovacao\{([^}]*)\}", d)
    if m and m.group(1).strip():
        add("CONFERIR", "documento.tex", f"Data de aprovação preenchida ({m.group(1)}): só depois da defesa (NBR 14724:2024, 4.2.1.3).")


def auditar_resumo(raiz, arquivo, cmd_chave, nome):
    p = raiz / "1-pre-textuais" / arquivo
    if not p.exists():
        return
    tex = ler(p)
    corpo = sem_comentarios(tex).split("\\" + cmd_chave)[0]
    n = len(palavras_latex(corpo))
    if n < 150 or n > 500:
        add("CORRIGIR", f"1-pre-textuais/{arquivo}", f"{nome} com {n} palavras; a NBR 6028:2021 (4.1.8) pede de 150 a 500.")
    paragrafos = [b for b in re.split(r"\n\s*\n", corpo.strip()) if b.strip()]
    if len(paragrafos) > 1:
        add("CORRIGIR", f"1-pre-textuais/{arquivo}", f"{nome} em {len(paragrafos)} parágrafos; deve ser parágrafo único (NBR 6028:2021, 4.1.2).")
    m = re.search(r"\\" + cmd_chave + r"\{(.*?)\}", sem_comentarios(tex), flags=re.S)
    if not m:
        add("CORRIGIR", f"1-pre-textuais/{arquivo}", f"Sem \\{cmd_chave}{{...}}.")
        return
    kw = m.group(1).strip()
    if not kw.endswith("."):
        add("CORRIGIR", f"1-pre-textuais/{arquivo}", "Palavras-chave devem terminar em ponto (NBR 6028:2021, 4.1.7).")
    termos = [t.strip(" .") for t in kw.split(";")]
    if len(termos) < 2 and ("," in kw or "." in kw[:-1]):
        add("CORRIGIR", f"1-pre-textuais/{arquivo}", "Separe as palavras-chave por ponto e vírgula (NBR 6028:2021, 4.1.7).")
    maiusc = [t for t in termos if t and t[0].isupper() and not t.isupper()]
    if maiusc and cmd_chave == "palavraschave":
        add("CONFERIR", f"1-pre-textuais/{arquivo}",
            "Palavras-chave com inicial maiúscula (" + ", ".join(maiusc[:4]) + "): só nomes próprios e científicos levam maiúscula.")


REF_MANUAL = re.compile(r"\b(Figura|Tabela|Quadro|Equa[çc][ãa]o|Gr[áa]fico|Se[çc][ãa]o|Ap[êe]ndice|Anexo|C[óo]digo)s?\s*~?\s*\(?\d+(\.\d+)*\)?", re.I)
CIT_MANUAL = re.compile(r"\(([A-ZÀ-Ý][A-ZÀ-Ý]+(?:[ ;,][A-ZÀ-Ý ]+)*),\s*\d{4}")


def auditar_textos(raiz, arquivos, chaves_bib, siglas_def):
    citadas = defaultdict(list)
    labels, refs = {}, set()
    siglas_usadas = set()
    for p in arquivos:
        rel = str(p.relative_to(raiz))
        tex = ler(p)
        for i, l in linhas(tex):
            for m in re.finditer(r"\\(?:cite\w*|apud\w*|nocite)(?:\[[^\]]*\])*\{([^}]+)\}(?:\{([^}]+)\})?", l):
                for g in (m.group(1), m.group(2)):
                    if g:
                        for k in g.split(","):
                            citadas[k.strip()].append(f"{rel}:{i}")
            for m in re.finditer(r"\\label\{([^}]+)\}", l):
                labels[m.group(1)] = f"{rel}:{i}"
            refs.update(re.findall(r"\\(?:ref|autoref|pageref|eqref)\{([^}]+)\}", l))
            siglas_usadas.update(re.findall(r"\\(?:gls|Gls|glspl|acrshort|acrlong|acrfull|glsadd)\{([^}]+)\}", l))
            limpa = re.sub(r"\\\w+\{[^}]*\}", "", l)
            if "lstlisting" not in l and REF_MANUAL.search(limpa) and "\\ref" not in l:
                add("CORRIGIR", f"{rel}:{i}", f"Remissão com número escrito à mão ({REF_MANUAL.search(limpa).group(0)}); use \\ref.")
            if CIT_MANUAL.search(l):
                add("CORRIGIR", f"{rel}:{i}", f"Citação escrita à mão em caixa alta ({CIT_MANUAL.search(l).group(0)}...); "
                    "use \\cite. A NBR 10520:2023 (6.1.1) pede maiúsculas e minúsculas.")
            if re.search(r"\bcap[íi]tulos?\b", l, re.I) and "\\chapter" not in l:
                add("CONFERIR", f"{rel}:{i}", "Menção a \"capítulo\": a NBR 14724:2024 (4.2.2) organiza o trabalho em seções.")
            if re.search(r"\*\*[^*]+\*\*|^\s*#{1,6} |\[[^\]]+\]\(https?://", l):
                add("CORRIGIR", f"{rel}:{i}", "Marcação de Markdown no .tex.")
            for ph in PLACEHOLDERS[6:]:
                if re.search(ph, l):
                    add("BLOQUEIA", f"{rel}:{i}", f"Texto provisório: {l.strip()[:80]}")
        auditar_flutuantes(rel, tex)
    for k, onde in citadas.items():
        if k not in chaves_bib:
            add("BLOQUEIA", onde[0], f"Citação de \"{k}\" sem entrada no .bib (sai \"??\" ou some da lista).")
    for k in sorted(chaves_bib - set(citadas)):
        add("CONFERIR", "3-pos-textuais/referencias.bib", f"Entrada \"{k}\" não citada: não aparece na lista; apague se não for usar.")
    for lab, onde in labels.items():
        if lab not in refs and re.match(r"(fig|tab|qua|cod|graf):", lab):
            add("CORRIGIR", onde, f"\"{lab}\" não é citado no texto; ilustrações e tabelas devem ser citadas (NBR 14724:2024, 5.8 e 5.9).")
    for r in refs - set(labels):
        add("BLOQUEIA", "texto", f"\\ref{{{r}}} sem \\label correspondente (sai \"??\").")
    for s in sorted(siglas_usadas - siglas_def):
        add("BLOQUEIA", "texto", f"Sigla \\gls{{{s}}} não definida na lista de siglas.")
    for s in sorted(siglas_def - siglas_usadas):
        add("CONFERIR", "1-pre-textuais/lista-de-abreviaturas-e-siglas.tex", f"Sigla {s} definida e não usada: não entra na lista.")


def auditar_flutuantes(rel, tex):
    t = sem_comentarios(tex)
    fora = re.sub(r"\\begin\{(figure|table|quadro|minipage)\}.*?\\end\{\1\}", "", t, flags=re.S)
    for m in re.finditer(r"\\includegraphics", fora):
        if "\\includepdf" in fora:
            break
        linha = fora[:m.start()].count("\n") + 1
        add("CORRIGIR", f"{rel}", f"Imagem fora de ambiente figure (perto da linha {linha} do texto sem flutuantes): "
            "sem título, número e Fonte (NBR 14724:2024, 5.8).")
    for m in re.finditer(r"\\begin\{longtable\}(.*?)\\end\{longtable\}", t, flags=re.S):
        if "\\Fonte" not in m.group(1) and "\\Fonte" not in t[m.end():m.end() + 200]:
            linha = t[:m.start()].count("\n") + 1
            add("CORRIGIR", f"{rel}:{linha}", "Tabela longa (longtable) sem título no padrão do modelo e sem \\Fonte.")
    for m in re.finditer(r"\\begin\{(figure|table|quadro)\}(.*?)\\end\{\1\}", t, flags=re.S):
        corpo = m.group(2)
        linha = t[:m.start()].count("\n") + 1
        tipo = {"figure": "Figura", "table": "Tabela", "quadro": "Quadro"}[m.group(1)]
        if "\\label" not in corpo:
            add("CORRIGIR", f"{rel}:{linha}", f"{tipo} sem \\label: não dá para citá-la no texto.")
        if "\\Fonte" not in corpo:
            add("BLOQUEIA", f"{rel}:{linha}", f"{tipo} sem \\Fonte{{...}}. A fonte é obrigatória, inclusive \"Elaborada pelo autor\" (NBR 14724:2024, 5.8 e 5.9).")
        if not re.search(r"\\[Cc]aption", corpo):
            add("BLOQUEIA", f"{rel}:{linha}", f"{tipo} sem título (\\Caption ou \\caption).")
        if m.group(1) == "table" and re.search(r"\\begin\{tabular\}\{[^}]*\|", corpo):
            add("CORRIGIR", f"{rel}:{linha}", "Tabela com linhas verticais: o padrão IBGE não fecha as laterais. Texto em grade é Quadro.")


def ler_bib(raiz):
    bib = raiz / "3-pos-textuais" / "referencias.bib"
    if not bib.exists():
        return set()
    tex = ler(bib)
    chaves = set()
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@|\Z)", tex, flags=re.S):
        tipo, chave, corpo = m.group(1).lower(), m.group(2), m.group(3)
        if tipo in ("comment", "string", "preamble"):
            continue
        chaves.add(chave)
        onde = f"referencias.bib ({chave})"
        campos = {k.lower(): v for k, v in re.findall(r"(\w[\w-]*)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*$", corpo, flags=re.M | re.S)}
        campos.update({k.lower(): v for k, v in re.findall(r"^\s*(\w[\w-]*)\s*=\s*(\d{4}\w?)\s*,?\s*$", corpo, flags=re.M)})
        autor = campos.get("author", "")
        if autor and not autor.startswith("{") and re.search(r"\b[A-ZÀ-Ý]{3,}\b,", autor):
            add("CORRIGIR", onde, f"Autor em caixa alta ({autor[:40]}). Escreva Sobrenome, Prenome em caixa normal; o estilo põe as maiúsculas.")
        org = campos.get("organization", "")
        if org.startswith("{") and org.strip("{}").isupper():
            add("CONFERIR", onde, "organization em caixa alta e chaves duplas é a convenção antiga; no modelo 2026 escreva em caixa normal.")
        url = campos.get("url", "")
        if re.search(r"[?&](utm_\w+|fbclid|gclid|referrer|ref_src)=", url):
            add("CORRIGIR", onde, "Link com parâmetros de rastreamento; deixe só o endereço do documento.")
        if url and "urlaccessdate" not in campos:
            add("CORRIGIR", onde, "Documento online sem urlaccessdate (\"Acesso em:\", NBR 6023:2025, 6.6).")
        if "year" not in campos and tipo not in ("misc",):
            add("CORRIGIR", onde, "Sem ano. Use [20--] ou [2024?] quando a data for incerta.")
        if re.fullmatch(r"\d{4}[a-z]", campos.get("year", "")):
            add("CONFERIR", onde, "Letra no ano escrita à mão; no modelo 2026 o estilo põe a/b sozinho quando há mesma autoria e ano.")
    return chaves


def ler_siglas(raiz):
    p = raiz / "1-pre-textuais" / "lista-de-abreviaturas-e-siglas.tex"
    if not p.exists():
        return set()
    return set(re.findall(r"\\newacronym(?:\[[^\]]*\])?\{([^}]+)\}", sem_comentarios(ler(p))))


def auditar_pdf(raiz):
    pdf = raiz / "documento.pdf"
    if not pdf.exists():
        add("CONFERIR", "documento.pdf", "Sem PDF compilado: rode scripts/compilar.sh e audite de novo para conferir o PDF.")
        return
    try:
        texto = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return
    if "??" in texto:
        add("BLOQUEIA", "documento.pdf", f"O PDF tem {texto.count('??')} ocorrência(s) de \"??\" (remissão ou citação sem destino).")
    for l in texto.split("\n"):
        if re.search(r"\([A-ZÀ-Ý]{3,}[A-ZÀ-Ý ]*(?:;[^)]*)?, \d{4}[a-z]?[,)]", l):
            add("CORRIGIR", "documento.pdf", f"Citação com autor em caixa alta no PDF: {l.strip()[:90]}")
            break


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    raiz = Path(sys.argv[1]).resolve()
    docp = raiz / "documento.tex"
    if not docp.exists():
        sys.exit(f"{raiz} não tem documento.tex")
    if auditar_modelo(raiz):
        doc = ler(docp)
        auditar_documento(raiz, doc)
        auditar_resumo(raiz, "resumo.tex", "palavraschave", "Resumo")
        auditar_resumo(raiz, "abstract.tex", "keywords", "Abstract")
        chaves = ler_bib(raiz)
        arqs = [p for p in arquivos_texto(raiz, doc) if "lib" not in p.parts]
        arqs += [p for p in (raiz / "2-textuais").glob("*.tex") if p not in arqs and re.search(re.escape(p.stem), sem_comentarios(doc))]
        auditar_textos(raiz, arqs, chaves, ler_siglas(raiz))
        auditar_pdf(raiz)

    ordem = {"BLOQUEIA": 0, "CORRIGIR": 1, "CONFERIR": 2}
    achados.sort(key=lambda a: (ordem[a[0]], a[1]))
    saida = [f"# Auditoria ufcTex: {raiz.name}", ""]
    cont = {k: sum(1 for a in achados if a[0] == k) for k in ordem}
    saida.append(f"BLOQUEIA: {cont['BLOQUEIA']} | CORRIGIR: {cont['CORRIGIR']} | CONFERIR: {cont['CONFERIR']}")
    for sev in ordem:
        itens = [a for a in achados if a[0] == sev]
        if itens:
            saida += ["", f"## {sev}", ""]
            saida += [f"- {onde}: {msg}" for _, onde, msg in itens]
    saida += ["", "Itens que só a leitura do PDF confirma estão em references/auditoria.md (parte manual)."]
    rel = "\n".join(saida)
    if "--md" in sys.argv:
        Path(sys.argv[sys.argv.index("--md") + 1]).write_text(rel, encoding="utf-8")
    print(rel)


if __name__ == "__main__":
    main()
