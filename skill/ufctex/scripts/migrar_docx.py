#!/usr/bin/env python3
"""Primeira passagem da migração de um trabalho em Word (.docx) para o ufcTex.

Uso:
    python3 migrar_docx.py trabalho.docx <pasta-do-trabalho>

A pasta já deve ter o modelo configurado (obter_modelo.sh + novo_trabalho.py
--limpar). O script:
  1. converte o .docx com o pandoc (títulos de nível 1 viram seções primárias);
  2. grava cada seção primária em 2-textuais/NN-nome.tex e atualiza o
     documento.tex;
  3. extrai as imagens para figuras/;
  4. separa a lista de referências em migracao/referencias-originais.txt e os
     pré-textuais (resumo, agradecimentos etc.) em migracao/pre-textuais.tex;
  5. grava migracao/pendencias.md com o que precisa de acabamento manual.

O resultado compila, mas ainda não está no padrão: figuras, tabelas,
citações e referências precisam do acabamento descrito em
references/migracao.md.
"""
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

PRE_TEXTUAIS = re.compile(r"^(resumo|abstract|agradecimentos?|dedicat[óo]ria|ep[íi]grafe|sum[áa]rio|lista de .*|folha de aprova[çc][ãa]o)$", re.I)
POS_REF = re.compile(r"^(refer[êe]ncias( bibliogr[áa]ficas)?|bibliografia)$", re.I)
APENDICE = re.compile(r"^(ap[êe]ndice|anexo)\b", re.I)


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "secao"


def texto_titulo(tex):
    t = re.sub(r"\\label\{[^}]*\}", "", tex)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}", r"\2", t)
    t = re.sub(r"^\d+(\.\d+)*\s*", "", t.strip())  # numeração digitada no Word
    return t.strip()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    docx, pasta = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if not (pasta / "documento.tex").exists():
        sys.exit("Configure a pasta com obter_modelo.sh e novo_trabalho.py --limpar antes.")
    if not shutil.which("pandoc"):
        sys.exit("pandoc não encontrado. Instale (apt install pandoc ou pip install pypandoc_binary).")
    mig = pasta / "migracao"
    mig.mkdir(exist_ok=True)
    bruto = subprocess.run(
        ["pandoc", str(docx), "-t", "latex", "--top-level-division=chapter", "--wrap=none",
         f"--extract-media={pasta / 'figuras'}"],
        capture_output=True, text=True, check=True).stdout
    (mig / "pandoc-bruto.tex").write_text(bruto, encoding="utf-8")

    # Imagens: caminho relativo ao projeto, sem a subpasta media/ do pandoc
    media = pasta / "figuras" / "media"
    if media.exists():
        for f in media.iterdir():
            shutil.move(str(f), pasta / "figuras" / f.name)
        media.rmdir()
    bruto = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*?/media/([^}]+)\}",
                   lambda m: "\\includegraphics[width=0.8\\textwidth]{figuras/" + m.group(2) + "}", bruto)
    # O pandoc envolve títulos em \hypertarget; o modelo usa \label
    bruto = re.sub(r"\\hypertarget\{[^}]*\}\{%?\n?(\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\{.*?\}\\label\{[^}]*\})\}",
                   r"\1", bruto)
    # Numeração digitada no Word ("1.1 Objetivos"): o modelo numera sozinho
    bruto = re.sub(r"(\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\{)\d+(?:\.\d+)*\.?\s+", r"\1", bruto)

    partes = re.split(r"(?m)^\\chapter\{", bruto)
    textuais, pre, refs, apendices = [], [], [], []
    for parte in partes[1:]:
        fim = parte.index("}")
        titulo = texto_titulo(parte[:fim])
        corpo = parte[fim + 1:].strip()
        corpo = re.sub(r"^\s*\\label\{[^}]*\}\}?", "", corpo).strip()
        if PRE_TEXTUAIS.match(titulo):
            pre.append(f"% ===== {titulo} =====\n{corpo}\n")
        elif POS_REF.match(titulo):
            refs.append(corpo)
        elif APENDICE.match(titulo):
            apendices.append((titulo, corpo))
        else:
            textuais.append((titulo, corpo))
    if not textuais:
        sys.exit("Não achei títulos de nível 1 no .docx. Peça ao autor para aplicar o estilo Título 1 às seções primárias.")

    destino = pasta / "2-textuais"
    for f in destino.glob("*.tex"):
        f.unlink()
    nomes = []
    for n, (titulo, corpo) in enumerate(textuais, 1):
        nome = f"{n}-{slug(titulo)}"
        titulo_caixa = titulo[:1].upper() + titulo[1:].lower() if titulo.isupper() else titulo
        (destino / f"{nome}.tex").write_text(
            f"\\chapter{{{titulo_caixa}}}\n\\label{{sec:{slug(titulo)}}}\n\n{corpo}\n", encoding="utf-8")
        nomes.append(nome)
    for n, (titulo, corpo) in enumerate(apendices):
        t = re.sub(r"^(ap[êe]ndice|anexo)\s+[A-Z]\s*[–—-]\s*", "", titulo, flags=re.I)
        tipo = "anexos" if titulo.lower().startswith("anexo") else "apendices"
        cmd = "anexo" if tipo == "anexos" else "apendice"
        (pasta / "3-pos-textuais" / tipo / f"{cmd}-{chr(97 + n)}.tex").write_text(
            f"\\{cmd}{{{t}}}\n\\label{{{cmd[:2]}:{slug(t)}}}\n\n{corpo}\n", encoding="utf-8")

    doc = (pasta / "documento.tex").read_text(encoding="utf-8")
    doc = re.sub(r"(\\textual\n)(?:\s*%?\s*\\input\{2-textuais/[^}]+\}\n)+",
                 lambda m: m.group(1) + "".join(f"\t\\input{{2-textuais/{n}}}\n" for n in nomes), doc)
    (pasta / "documento.tex").write_text(doc, encoding="utf-8")

    (mig / "pre-textuais.tex").write_text("\n".join(pre), encoding="utf-8")
    refs_txt = "\n".join(refs)
    refs_txt = re.sub(r"\\(textbf|emph|textit)\{([^}]*)\}", r"\2", refs_txt)
    (mig / "referencias-originais.txt").write_text(refs_txt, encoding="utf-8")

    todo = "\n".join(textuais[i][1] for i in range(len(textuais)))
    n_img = len(re.findall(r"\\includegraphics", todo))
    n_tab = len(re.findall(r"\\begin\{longtable\}", todo))
    n_cit = len(re.findall(r"\([A-ZÀ-Ý][^()]{0,80}?,\s*\d{4}[a-z]?(?:,\s*p\.\s*[\d-]+)?\)", todo))
    n_refnum = len(re.findall(r"\b(Figura|Tabela|Quadro|Equa[çc][ãa]o)\s+\d+", todo))
    (mig / "pendencias.md").write_text(f"""# Pendências da migração de {docx.name}

Seções primárias criadas: {len(textuais)} ({', '.join(t for t, _ in textuais)})
Apêndices e anexos: {len(apendices)}

- [ ] {n_img} imagem(ns) soltas: envolver em figure com \\Caption, \\label, \\UFCfig e \\Fonte (references/elementos.md).
- [ ] {n_tab} tabela(s) em longtable do pandoc: refazer no padrão IBGE (booktabs, \\caption, \\Fonte).
- [ ] cerca de {n_cit} citação(ões) escritas no texto: trocar por \\cite/\\citeonline com chaves do .bib.
- [ ] {n_refnum} remissão(ões) com número digitado ("Figura 3"): trocar por \\ref.
- [ ] Referências em migracao/referencias-originais.txt: converter para 3-pos-textuais/referencias.bib (references/bibliografia.md).
- [ ] Pré-textuais em migracao/pre-textuais.tex: mover resumo, abstract, agradecimentos etc. para 1-pre-textuais/.
- [ ] Siglas e símbolos: cadastrar nas listas e usar \\gls.
- [ ] Numeração digitada nos títulos e listas do Word: conferir se não ficou duplicada.
- [ ] Compilar (scripts/compilar.sh) e rodar a auditoria (scripts/auditar.py).
""", encoding="utf-8")
    print((mig / "pendencias.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
