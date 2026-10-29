
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

caminho_banco = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filmes.db")


def conectar():
    banco = sqlite3.connect(caminho_banco)
    banco.row_factory = sqlite3.Row
    return banco


def criar_banco():
    banco = conectar()
    banco.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota REAL NOT NULL
        )
    """)
    banco.commit()
    banco.close()


@app.route("/")
def index():
    banco = conectar()
    filmes = banco.execute("SELECT * FROM filmes").fetchall()
    banco.close()
    return render_template("index.html", filmes=filmes)


@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        ano = request.form["ano"]
        nota = request.form["nota"]

        banco = conectar()
        banco.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, ano, nota)
        )
        banco.commit()
        banco.close()

        return redirect(url_for("index"))

    return render_template("form.html", filme=None)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    banco = conectar()
    filme = banco.execute(
        "SELECT * FROM filmes WHERE id = ?", (id,)
    ).fetchone()

    if filme is None:
        banco.close()
        return "Filme não encontrado", 404

    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        ano = request.form["ano"]
        nota = request.form["nota"]

        banco.execute(
            "UPDATE filmes SET titulo=?, genero=?, ano=?, nota=? WHERE id=?",
            (titulo, genero, ano, nota, id)
        )
        banco.commit()
        banco.close()

        return redirect(url_for("index"))

    banco.close()
    return render_template("form.html", filme=filme)


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    banco = conectar()
    banco.execute("DELETE FROM filmes WHERE id = ?", (id,))
    banco.commit()
    banco.close()
    return redirect(url_for("index"))


criar_banco()

if __name__ == "__main__":
    app.run(debug=True)
