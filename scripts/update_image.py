"""Atualiza exatamente uma imagem do Pulso. Não depende de bibliotecas externas."""
import re
import sys
from pathlib import Path

def update(path, image):
    if not re.fullmatch(r"ghcr\.io/[a-z0-9-]+/pulso:[a-f0-9]{40}", image):
        raise ValueError("Use ghcr.io/felipef2s/pulso seguido do SHA completo de 40 caracteres")
    target = Path(path)
    text = target.read_text(encoding="utf-8-sig")
    pattern = r"(?m)^(\s*image: )ghcr\.io/[^/\s]+/pulso:[^\s]+[ \t]*$"
    updated, count = re.subn(pattern, lambda m: m[1] + image, text)
    if count != 1:
        raise ValueError(f"Esperava uma imagem Pulso, encontrei {count}. Nenhum arquivo alterado.")
    target.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python scripts/update_image.py ARQUIVO IMAGEM")
    update(sys.argv[1], sys.argv[2])
