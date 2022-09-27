
from config import LAST_ID_FILE, MOVIMIENTOS_FILE, NEW_FILE
import os
from flask import redirect, url_for

import csv


def select_all():
    fichero = open(MOVIMIENTOS_FILE,"r")
    csvReader = csv.reader(fichero, delimiter=",", quotechar= '"')
    movimientos = []
    for movimiento in csvReader:
        movimientos.append(movimiento)
    
    fichero.close()
    
    return movimientos



def select_by(id):


    fichero = open(MOVIMIENTOS_FILE, "r", newline="")
    csvReader = csv.reader(fichero, delimiter=",", quotechar= '"')#csv.reader permite leer el fichero
    registro_definitivo = []

    for registro in csvReader:  
        if registro[0] == str(id):
            registro_definitivo = registro
            break
    
    fichero.close()

    return registro_definitivo


def delete_by(id):
    fichero_old = open(MOVIMIENTOS_FILE,"r")
    fichero = open(NEW_FILE, "w", newline="")
    csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

    for registro in csvReader:
        if registro[0] != str(id):
            csvWriter.writerow(registro)
    
    fichero_old.close()
    fichero.close()

    os.remove(MOVIMIENTOS_FILE)
    os.rename(NEW_FILE, MOVIMIENTOS_FILE)
    
def createId():
    fichero = open(LAST_ID_FILE, "r", newline="") #obtener nuevo id
    registro = fichero.read() #te lee todo el fichero
    id = int(registro) + 1
    fichero.close()
    return id
def savesLastId(id):
    fichero = open(LAST_ID_FILE, "w")
    fichero.write(f"{id}")#es igual str(id)
    fichero.close()

def insert(registro):
    #fichero = open(LAST_ID_FILE, "r", newline="") #obtener nuevo id
    #registro = fichero.read() #te lee todo el fichero
    #id = int(registro) + 1
    #fichero.close()
    #id = createId()
    id=createId()
    fichero = open (MOVIMIENTOS_FILE, "a", newline="")
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')



    #csvWriter.writerow(["{}".format(id), registro[0], registro[1], registro[2]]) es lo mismo que la linea de abajo
    csvWriter.writerow([f"{id}"] + registro) #es lo mismo que arriba
    
    fichero.close()


    #fichero = open(LAST_ID_FILE, "w")
    #fichero.write(f"{id}")#es igual str(id)
    #fichero.close()
    savesLastId(id)

def update_by(registro_mod):

    fichero_old = open(MOVIMIENTOS_FILE,"r")
    fichero = open(NEW_FILE, "w", newline="")
    csvReader = csv.reader(fichero_old, delimiter=",", quotechar='"')
    csvWriter = csv.writer(fichero, delimiter=",", quotechar='"')

    for registro in csvReader:
        if registro[0] != registro_mod[0]:
            csvWriter.writerow(registro)
        else:
            csvWriter.writerow(registro_mod)

    fichero_old.close()
    fichero.close()

    os.remove(MOVIMIENTOS_FILE)
    os.rename(NEW_FILE, MOVIMIENTOS_FILE)


