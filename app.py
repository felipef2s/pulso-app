"""
pulso — a aplicação do curso 5446 (Introdução ao GitOps e CI/CD).

Um processo, uma imagem, três rotas:
  GET /             → a telinha (templates/index.html)
  GET /api/version  → a mesma informação, em JSON
  GET /healthz      → o health check que o Kubernetes chama

APP_VERSION pode sobrescrever a versão padrão do código. No fluxo principal,
a versão vem do código e GIT_SHA é gravado na imagem pelo build. O Kubernetes
não sobrescreve esses valores: assim uma imagem nova mostra sua própria versão.
"""
import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
COMMIT = os.getenv("GIT_SHA", "local")


@app.route("/")
def home():
    """A telinha. É ela que prova o GitOps no fim do curso."""
    return render_template("index.html", version=VERSION, commit=COMMIT)


@app.route("/api/version")
def version():
    """A mesma informação da telinha, para conferir com curl."""
    return jsonify(version=VERSION, commit=COMMIT)


@app.route("/healthz")
def healthz():
    """O que o Kubernetes pergunta para saber se o pod está vivo."""
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
