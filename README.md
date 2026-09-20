# Pulso

Aplicação de demonstração do curso 5446, com Flask.

| Rota | Conteúdo |
|---|---|
| / | Página HTML com versão e commit |
| /api/version | Versão e commit em JSON |
| /healthz | Saúde da aplicação |

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/python -m pytest -v
.venv/Scripts/python app.py
```

Abra http://localhost:5000. Para Linux/macOS, use .venv/bin/python.
Para empacotar, use o Dockerfile. Ele inicia Waitress com usuário sem root.
APP_VERSION pode sobrescrever a versão padrão do código. GIT_SHA recebe o commit no build.
