"""Atualiza exatamente uma imagem do Pulso no manifesto. Não depende de bibliotecas externas."""
import re
import sys
from pathlib import Path

# Imagem nova: sempre com o SHA completo do commit (40 caracteres)
NEW_IMAGE = re.compile(r"ghcr\.io/[a-z0-9-]+/pulso:[a-f0-9]{40}")

# Linha atual no manifesto. Aceita:
#   image: ghcr.io/dono/pulso:tag
#   - image: ghcr.io/dono/pulso:tag
#   image: "ghcr.io/dono/pulso:tag"   (aspas simples ou duplas)
#   image: ghcr.io/dono/pulso         (sem tag)
#   image: ghcr.io/dono/pulso:tag  # comentario
PULSO_LINE = re.compile(
    r"""^(?P<prefix>[ \t]*(?:-[ \t]+)?image:[ \t]*)"""
    r"""(?P<quote>["']?)ghcr\.io/[^/\s"']+/pulso(?::[^\s"'#]+)?(?P=quote)"""
    r"""(?P<suffix>[ \t]*(?:\#.*)?)$""",
    re.MULTILINE,
)


def image_lines(text):
    """Lista as linhas com 'image:' para facilitar o diagnóstico."""
    found = [
        f"  linha {n}: {line.strip()}"
        for n, line in enumerate(text.splitlines(), 1)
        if "image:" in line
    ]
    return "\n".join(found) or "  (nenhuma linha com 'image:')"


def update(path, image):
    if not NEW_IMAGE.fullmatch(image):
        raise ValueError(
            "Use ghcr.io/<dono>/pulso seguido do SHA completo de 40 caracteres. "
            f"Recebi: {image}"
        )

    target = Path(path)
    if not target.is_file():
        raise ValueError(f"Manifesto não encontrado: {target}")

    text = target.read_text(encoding="utf-8-sig")
    updated, count = PULSO_LINE.subn(
        lambda m: m["prefix"] + m["quote"] + image + m["quote"] + m["suffix"],
        text,
    )

    if count != 1:
        raise ValueError(
            f"Esperava exatamente uma imagem do Pulso em {target}, encontrei {count}. "
            "Nenhum arquivo alterado.\nLinhas com 'image:' no arquivo:\n"
            + image_lines(text)
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