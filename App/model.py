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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import linkedlistiterator as it
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer


def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accident['Start_Time']
    accidentdata = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdata.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdata.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

    #a=gey.......
    #a["fecha"]["root"]["size"]
    #recorrido iterator
    #    iterador["root"]["size"]
    #
    #({fecha1:{"root":info single linked, "comfuntion":None,"":}, "size":1, "compuftion":None},{fecha2:....})

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    Seveindex = datentry['SeverityIndex']
    seventry = m.get(Seveindex, accident['Severity'])
    if (seventry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstSeverities'], accident)
        m.put(Seveindex, accident['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstSeverities'], accident)
    return datentry


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': None, 'lstaccidents': None}
    entry['SeverityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newSeverityEntry(entrada1, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    sepentry = {'severity': None, 'lstSeverities': None}
    sepentry['severity'] = entrada1
    sepentry['lstSeverities'] = lt.newList('SINGLELINKED', compareSeverity)
    return sepentry


# ==============================
# Funciones de consulta
# ==============================


def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de accidentes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    return lst


def getAccidentsByRangeSeverity(analyzer, initialDate, severitycode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    axidate = om.get(analyzer['dateIndex'], initialDate)
    if axidate['key'] is not None:
        severitymap = me.getValue(axidate)['SeverityIndex']
        numseverities = m.get(severitymap, severitycode)
        if numseverities is not None:
            return m.size(me.getValue(numseverities)['lstSeverities'])
        return 0 

def hallar_muyrepetido(lst):
    lista=[]
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        iterator2 = it.newIterator(itet["lstaccidents"])
        while it.hasNext(iterator2):
            itet2=it.next(iterator2)
            fechahora=datetime.datetime.strptime(itet2["Start_Time"], '%Y-%m-%d %H:%M:%S')
            lista.append(fechahora.date())      
    maxi = 0
    ret=None
    for cada_fecha in lista:
        cant=lista.count(cada_fecha)
        if cant > maxi:
            maxi = cant
            ret=cada_fecha
    return (ret,maxi)

#datetime.datetime.strptime(itet2["Start_Time"], '%Y-%m-%d'   --- hora '%Y-%m-%d %H:%M:%S')
#datetime.datetime.hour(fecha completa, %H:%M:%S')  

def hallar_categoria(lst):
    lista=[]
    iterator = it.newIterator(lst)
    while it.hasNext(iterator):
        itet=it.next(iterator)
        iterator2 = it.newIterator(itet["lstaccidents"])
        while it.hasNext(iterator2):
            itet2=it.next(iterator2)
            lista.append(itet2["Severity"])
    maxi = 0
    ret=None
    for severidad in lista:
        cant=lista.count(severidad)
        if cant > maxi:
            maxi = cant
            ret=severidad
    return (ret,maxi)

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareSeverity(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    seve = me.getKey(severity2)
    if (severity1 == seve):
        return 0
    elif (severity1 > seve):
        return 1
    else:
        return -1
