"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import linkedlistiterator as it
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Requerimiento 1 (Accidentes por severidad en una fecha determinada)")
    print("4- Requerimiento 2 (Accidentes antes de una fecha)")
    print("5- Requerimiento 3 (Conocer accidentes en un rango de fechas)")
    print("6- Requerimiento 4 (Conocer el estado con más accidentes en un rango de fechas)")
    print("7- Requerimiento 5 (Conocer los accidentes por rango de horas)")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont,accidentsfile)
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del reto 3: ")
        print("\nBuscando accidentes por severidad en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        severity = input("Severidad del accidente: ")
        total_accidentes = controller.getAccidentsByRangeSeverity(cont, initialDate,severity)
        print("\nTotal de accidentes tipo: " + str(severity) + " en esa fecha:  "+ str(total_accidentes))
        
    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del reto 3: ")
        print("\nBuscando accidentes antes de una fecha: ")
        total=0
        MinDate = str(controller.minKey(cont))
        MaxDate = input("Fecha (YYYY-MM-DD): ")
        total_acci=controller.getAccidentsByRange(cont, MinDate, MaxDate)
        iterator = it.newIterator(total_acci)
        while it.hasNext(iterator):
            ietar=it.next(iterator)
            total=(ietar["lstaccidents"]["size"])+total
        print("\nTotal de accidentes antes de "+str(MaxDate)+" son: "+ str(total))
        repetido=controller.getMasRepetido(total_acci)
        print("\nLa fecha con más accidentes es:"+str(repetido[0])+" con "+str(repetido[1])+" accidentes")
    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        print("\nBuscando accidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        lst = controller.getAccidentsByRange(cont, initialDate, finalDate)
        iterator = it.newIterator(total_acci)
        if it.hasNext(iterator):
            ietar=it.next(iterator)
            print("\nTotal de accidentes en el rango: " + str(ietar["lstaccidents"]["size"]))
        tupla=controller.getCategoriaInRange(lst)
        print("La severidad de accidentes más reportada de "+str(initialDate)+" a "+str(finalDate)+" es: "+str(tupla[0])+", cantidad: "+str(tupla[1]))
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del reto 3: ")
        print("\nBuscando estado en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        lstt = controller.getAccidentsByRange(cont, initialDate, finalDate)
        seb=controller.getStateInRange(lstt)
        repetir=controller.getMasRepetido(lstt)
        print("El estado con más accidentes reportados es: "+str(seb[0])+" con una cantidad de "+str(seb[1]))
        print("La fecha con más accidentes es: "+str(repetir[0])+" con "+str(repetir[1]))
    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del reto 3: ")
        print("\nBuscando accidentes en un rango de horas: ")
        print("Por la seguridad del programa, inserte las fechas con formato 00:00:00 hasta 23:59:00")
        initialHour = input("Rango Inicial (HH-MM-SS): ")
        finalHour = input("Rango Final (HH-MM-SS): ")
        initialHour=controller.ajustarhora(initialHour)
        finalHour=controller.ajustarhora(finalHour)
        linked=controller.getAccidentsByRangeHora(cont, initialHour, finalHour)
        acc=controller.getAccidentesPorHora(linked)
        print("Los accidentes ocurridos entre: "+str(initialHour)+" y "+str(finalHour)+" son: "+str(acc[0][0]))
        print("Accidentes por severidad 1: "+str(acc[1]["Severidad1"]))
        print("Accidentes por severidad 2: "+str(acc[1]["Severidad2"]))
        print("Accidentes por severidad 3: "+str(acc[1]["Severidad3"]))
        print("Accidentes por severidad 4: "+str(acc[1]["Severidad4"]))
        print("__________________________________________________________")
        print("El porcentaje de accidentes de severidad 1: "+str(acc[0][1]))
        print("El porcentaje de accidentes de severidad 2: "+str(acc[0][2]))
        print("El porcentaje de accidentes de severidad 3: "+str(acc[0][3]))
        print("El porcentaje de accidentes de severidad 4: "+str(acc[0][4]))
        v=(acc[0][0]/controller.accidentsSize(cont))*100
        print("Porcentaje de accidentes ocurridos entre: "+str(initialHour)+" y "+str(finalHour)+" vs los totales son: "+str(round(v,2)))
    else:
        sys.exit(0)
sys.exit(0)
