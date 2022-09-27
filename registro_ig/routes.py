
from registro_ig.models import select_all, select_by, delete_by, insert, update_by
from flask import redirect, render_template, request, redirect, url_for
from config import *
from registro_ig import app 
import csv
from datetime import date
import os

@app.route("/")
def index():
    movimientos = select_all()
   
    return render_template("index.html", page_title = "Lista", moviments=movimientos)#lo mismo que si em moviments ponemos directamente selec_all()

@app.route("/nuevo", methods=["GET","POST"])
def alta():
    if request.method == "GET":

        return render_template("new.html", page_title = "Alta", dataForm={})
    else:
        errores = validarFormulario(request.form)

        if len(errores) == 0:#tb puede ser ek if asi: if not errores:
        #    fichero = open("data/last_id.txt", "r", newline="") #obtener nuevo id
         #   registro = fichero.read() #te lee todo el fichero
          #  id = int(registro) + 1
           # fichero.close()


#            fichero = open (MOVIMIENTOS_FILE, "a", newline="")
 #           csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')



 #           csvWriter.writerow(["{}".format(id), request.form["date"], request.form["concept"], request.form["quantity"]])
#            fichero.close()

#            fichero = open("data/last_id.txt", "w")
 #           fichero.write(f"{id}")#es igual str(id)
  #          fichero.close()
            insert([request.form["date"], request.form["concept"], request.form["quantity"]])
            return redirect(url_for("index"))

        else:
            return render_template("new.html", page_title = "Alta", msgError = errores, dataForm = dict(request.form))

#def validarFormulario(camposFormulario):
 #   hoy = date.today().isoformat() #tb se puede poner hoy = str(date.today())
  #  if fechaEntrada <= hoy:
  #     return True
   # else:
   #     return False
        #es lo mismo que se ponga en vez del if poner return fechaEntrada <= hoy



def validarFormulario(camposFormulario):
    errores = []
    hoy = date.today().isoformat()
    if camposFormulario["date"] > hoy:
        errores.append("La fecha introducida es el futuro.")
    
    if camposFormulario["concept"] == "":
        errores.append("El campo concepto no puede estar vacio.")

#primera condicion el numero sea distinto 0 y la segunda campo no este vacio
    if camposFormulario["quantity"] == "" or float(camposFormulario["quantity"]) == 0.0 :
        errores.append("No pude ser el valor 0 o sin registro el campo cantidad")

    return errores   

def form_to_list(id, form):
    return [str(id), form['date'],
            form['concept'],
            form['quantity']]

@app.route("/modificar/<int:id>", methods=["GET", "POST"])
def modificacion(id):
    '''''
    if request.method=="GET":
        fichero = open (MOVIMIENTOS_FILE, "r", newline="")
        csvReader = csv.reader(fichero, delimiter=",", quotechar= '"')

        refistro_modificar= []

        for registro in csvReader:
            if registro[0] == str(id):
                refistro_modificar = registro
                break
        fichero.close()

        if refistro_modificar:

            return render_template("modification.html", page_title = "Modificar", registro=refistro_modificar)
        
        else:
           return redirect(url_for("index")) 
    else:
        errores= validarFormulario(request.form)

        if len(errores) == 0:
            
            fichero = open (MOD_FILE, "w", newline="")
            csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')



            csvWriter.writerow(["{}".format(id), request.form["date"], request.form["concept"], request.form["quantity"]])
            fichero.close()

            fichero_old = open(MOVIMIENTOS_FILE,"r") #abrir modo lectura
            fichero_mod = open(MOD_FILE, "r", newline="") #abrir modo escritura
            fichero_new = open(NEW_FILE, "w", newline="")
            csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
            csvReader_mod = csv.reader(fichero_mod, delimiter=",", quotechar='"')
            csvWriter_new = csv.writer(fichero_new, delimiter=',', quotechar='"')

            for registro in csvReader:# copia todo los registeos uno a uno en orden
                if registro[0] != str(id):
                    csvWriter_new.writerow(registro)
                else:
                    for registro2 in csvReader_mod:
                        csvWriter_new.writerow([registro2[0],registro2[1],registro2[2],registro2[3]])

            
            fichero_old.close()
            fichero_mod.close()
            fichero_new.close()

            os.remove(MOVIMIENTOS_FILE)# borra movimientos txt
            os.rename(NEW_FILE, MOVIMIENTOS_FILE)# renombra el nuevo a movimientos.txt
            
            return redirect(url_for("index"))
        else:
            return render_template("modification.html", pageTitle="Modificar", msgErrors=errores, registro=[id,request.form['date'],request.form['concept'],request.form['quantity']])
            
    '''
    if request.method=="GET":
        register = select_by(id)
        return render_template('modification.html', registro = register, pageTitle='Modificacion')
    else:
        errores = validarFormulario(request.form)#toda la informacion del post del navegador viene en el request

        if not errores:
            update_by(form_to_list(id, request.form))
                        
            
            return redirect(url_for("index"))
        else:
            #register= [id,
             #           request.form['date'],todo esto es lo mismo que lo que hay en registro = form to list
              #          request.form['concept'],
               #         request.form['quantity']]

            return render_template("modification.html", registro=form_to_list(id, request.form), pageTitle="Modificacion", msgErrors=errores)




@app.route("/borrar/<int:id>", methods=["GET", "POST"])
def borrar(id):
    if request.method == "GET": 

        #fichero = open(MOVIMIENTOS_FILE, "r", newline="")
        #csvReader = csv.reader(fichero, delimiter=",", quotechar= '"')#csv.reader permite leer el fichero
        #registro_definitivo = []

#        for registro in csvReader:  
 #           if registro[0] == str(id):
  #              registro_definitivo = registro
   #             break
        
    #    fichero.close()
        registro_definitivo = select_by(id)

        if registro_definitivo:

            return render_template("delete.html", registro=registro_definitivo)
        
        else:
            return redirect(url_for("index")) #url for te redirige a donde pongas entre parentesis que es el index
    
    else:
        #fichero_old = open(MOVIMIENTOS_FILE,"r") abrir modo lectura
       # fichero = open(NEW_FILE, "w", newline="") abrir modo escritura
        #csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
        #csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

#        for registro in csvReader: copia todo los registeos uno a uno en orden
 #           if registro[0] != str(id):
  #              csvWriter.writerow(registro)
        
   #     fichero_old.close()
    #    fichero.close()

#        os.remove(MOVIMIENTOS_FILE) borra movimientos txt
 #       os.rename(NEW_FILE, MOVIMIENTOS_FILE) renombra el nuevo a movimientos.txt
        delete_by(id)
        return redirect(url_for("index"))