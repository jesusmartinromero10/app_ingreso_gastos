from flask import redirect, render_template, request, redirect
from registro_ig import app 
import csv


@app.route("/")
def index():
    fichero = open("data/movimientos.txt","r")
    csvReader = csv.reader(fichero, delimiter=",", quotechar= '"')
    movimientos = []
    for movimiento in csvReader:
        movimientos.append(movimiento)
    return render_template("index.html", page_title = "Lista", moviments=movimientos)

@app.route("/nuevo", methods=["GET","POST"])
def alta():
    if request.method == "GET":

        return render_template("new.html", page_title = "Alta")
    else:
        fichero = open ("data/movimientos.txt", "a", newline="")
        csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

        csvWriter.writerow([request.form["date"], request.form["concept"], request.form["quantity"]])
        fichero.close()
        return redirect("/")


@app.route("/modificacion")
def modificacion():
    return render_template("modification.html", page_title = "Modificacion")

@app.route("/borrar")
def baja():
    return render_template("delete.html", page_title = "Borrado")