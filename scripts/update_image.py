"""Atualiza a imagem da aplicação no manifesto. Não depende de bibliotecas externas.

O nome da imagem NÃO fica fixo aqui: ele vem do argumento IMAGE (definido no CI).
O script procura no manifesto a única imagem do mesmo dono no GHCR
(ghcr.io/<dono>/...) e troca pelo valor novo, mesmo que o nome antigo seja outro
(ex.: pulso-app -> pulso).
"""
import re
import sys
from pathlib import Path

# Imagem nova: ghcr.io/<dono>/<nome>:<SHA completo de 40 caracteres>
NEW_IMAGE = re.compile(r"ghcr\.io/(?P<owner>[a-z0-9-]+)/[a-z0-9._/-]+:[a-f0-9]{40}")


def line_pattern(owner):
    # Aceita "- image:", aspas simples/duplas, imagem sem tag e comentário no fim
    return re.compile(
        r"""^(?P<prefix>[ \t]*(?:-[ \t]+)?image:[ \t]*)"""
        r"""(?P<quote>["']?)ghcr\.io/""" + re.escape(owner) + r"""/[^\s"'#:]+(?::[^\s"'#]+)?(?P=quote)"""
        r"""(?P<suffix>[ \t]*(?:\#.*)?)$""",
        re.MULTILINE,
    )


def image_lines(text):
    found = [
        f"  linha {n}: {line.strip()}"
        for n, line in enumerate(text.splitlines(), 1)
        if "image:" in line
    ]
    return "\n".join(found) or "  (nenhuma linha com 'image:')"


def update(path, image):
    match = NEW_IMAGE.fullmatch(image)
    if not match:
        raise ValueError(
            "Use ghcr.io/<dono>/<nome> seguido do SHA completo de 40 caracteres. "
            f"Recebi: {image}"
        )
    owner = match["owner"]

    target = Path(path)
    if not target.is_file():
        raise ValueError(f"Manifesto não encontrado: {target}")

    text = target.read_text(encoding="utf-8-sig")
    updated, count = line_pattern(owner).subn(
        lambda m: m["prefix"] + m["quote"] + image + m["quote"] + m["suffix"],
        text,
    )

    if count != 1:
        raise ValueError(
            f"Esperava exatamente uma imagem ghcr.io/{owner}/... em {target}, "
            f"encontrei {count}. Nenhum arquivo alterado.\n"
            "Linhas com 'image:' no arquivo:\n" + image_lines(text)
        )

    target.write_text(updated, encoding="utf-8")
    print(f"Imagem atualizada em {target}: {image}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python scripts/update_image.py ARQUIVO IMAGEM")
    try:
        update(sys.argv[1], sys.argv[2])
    except ValueError as err:
        print(f"Erro: {err}", file=sys.stderr)
        sys.exit(1)