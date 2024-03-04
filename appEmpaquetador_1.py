import csv
import time
import datetime

import paramiko
import socket
import re
import comandos as cmd


def prueba(a, b):
    print(f'Bytes transferidos: {a}/{b}')


def obtenerFichero(fichero, serverId):
    ssh_client = cmd.conectar(serverId)

    resultado = False
    # Definimos la ruta donde queremos poner el fichero
    # local_file_path = 'D:/T138708/' + fichero
    local_file_path = 'C:/Users/ajgar/' + fichero
    # Definimos la ruta y fichero que queremos traer a local
    remote_file_path = '/users/cairo/instalaciones/' + fichero
    print(f'Vamos a descargar el fichero <{fichero}>')
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path, callback=prueba)
        # aqui ya tenemos el fichero
        resultado = True
        sftp.close()
    except Exception as err:
        print(f'SFTP falló debido al error ' + str(err))
    cmd.desconectar(ssh_client)
    return resultado




def leerFicheroCsv(fichero, fechaInicio):
    fichas = []
    listaFichasFicheros = []
    ficherosAIncluir = []
    # Aqui almacenaremos los ficheros que realmente vamos a consolidar
    dictFicheros = {}

    with open(fichero, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        contador = 0
        for row in spamreader:
            # Columna 1: fecha y hora en DD/MM/YYYY, HH:MI:SS.mmmmmmm
            # Columna 1: Id Desarrollo
            # Columna 2: Nombre del Fichero completo: /users/cairo/OmegaCAIRO/...
            fechaHora = row[0]
            id_desarrollo = row[1]
            nombreFichero = row[2]
            nombreRelativo = nombreFichero[13:]
            fechaFichero = fechaHora.split(' ')
            '''
            if id_desarrollo == '0' or id_desarrollo == '00000':
                # Los que en la id_Desarrollo lleven 0 hay quie anotarlos en algún sitio para luego revisarlos.
                continue
            '''
            if comparaFechas(fechaInicio, fechaFichero[0]):
                contador += 1
                fichas.append(id_desarrollo)
                ficherosAIncluir.append(nombreFichero)
                listaFichasFicheros.append(id_desarrollo + " | " + nombreRelativo)

                # alimentamos nuestro diccionario
                dictFicheros[nombreRelativo] = [fechaHora, id_desarrollo, nombreFichero]
                print(f'Fecha: {fechaHora}\tDesarrollo: {id_desarrollo} \tFichero: {nombreRelativo}')

        print(f'{contador} ficheros.')
        # Vamos a eliminar duplicados
        # n_fichas = list(OrderedDict.fromkeys(fichas))
        fichas.sort()
        listaFichasFicheros.sort()
        ficherosAIncluir.sort()
        # generamos listas unicas de fichas y de ficheros
        u_fichas = list(dict.fromkeys(fichas))
        u_ficheros = list(dict.fromkeys(ficherosAIncluir))
        u_fichasFicheros = list(dict.fromkeys(listaFichasFicheros))

        for ficha in u_fichas:
            print(f'{ficha}')
        # n_ficheros = list(OrderedDict.fromkeys(ficherosAIncluir))

        print(f'Finalmente nos quedan <{len(u_fichas)}> fichas y <{len(u_ficheros)}> ficheros.')
        print(len(dictFicheros.keys()))
    return u_fichasFicheros


# Devolvemos True si fecha1 es menor que fecha2
def comparaFechas( fecha1, fecha2):
    f1 = fecha1.split('/')
    f2 = fecha2.split('/')

    first_date = datetime.date(int(f1[2]), int(f1[1]), int(f1[0]))
    second_date = datetime.date(int(f2[2]), int(f2[1]), int(f2[0]))

    result = first_date < second_date
    return result

def obtenerListaFicheros(fechaInicio):
    listaFicheros=[]
    serverList = {'cairo_desaomega': ['10.33.241.120', '22', 'cairo']}
    serverId = 'cairo_desaomega'
    ficheroOrigen = 'listaSubidasProduccionRealizadas.csv'
    # fechaInicio = '04/12/2023'  # fecha en formato DD/MM/YYYY
    # rutaDestino = 'D:/T138708/'
    rutaDestino = 'C:/Users/ajgar/'

    if (obtenerFichero(ficheroOrigen, serverId)):
        print('Descarga con Éxito!!!')
        listaFicheros = leerFicheroCsv(rutaDestino + ficheroOrigen, fechaInicio)
    return listaFicheros

def crearEstructuraDirect(lista):
    listaDir = []
    for dato in lista:
        datos_fichero = dato.split(' | ')
        fichero = datos_fichero[1]
        directorios = fichero.split('/')
        ruta = ''
        # recorremos toda la ruta menos el ultimo nivel que es el fichero
        for nivel in directorios[:-1]:
            ruta += '/' + nivel
            if ruta not in listaDir:
                listaDir.append(ruta)
                print(ruta)
    return listaDir


if __name__ == '__main__':
    '''
    # ssh_client = paramiko.SSHClient()
    #serverList = {'cairo_desaomega': ['10.33.241.120', '22', 'cairo'] }
    serverId = 'cairo_desaomega'
    ficheroOrigen = 'listaSubidasProduccionRealizadas.csv'
    fechaInicio = '04/12/2023' # fecha en formato DD/MM/YYYY
    rutaDestino = 'D:/T138708/'

    fichas = []
    ficherosAIncluir = []
    # Aqui almacenaremos los ficheros que realmente vamos a consolidar
    dictFicheros = {}
    print(cmd.ejecutarComando(serverId, 'ls -lrt'))
    '''
    lista = ['25572 | OmegaCAIRO/bin/GesOPV2/FunEntIGRIWS/FunEnt_EjeAccCAIRO_INC_ACTUACION_AMOV', '25572 | OmegaCAIRO/bin/GesOPV2/FunEnt/Periquito']
    crearEstructuraDirect(lista)
