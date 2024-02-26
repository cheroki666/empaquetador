import paramiko




def conectar( serverId ):
    ip = serverList[serverId][0]
    puerto = serverList[serverId][1]
    usuario = serverList[serverId][2]


    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, puerto, usuario, 'omega123')

    print('Conexion establecida con exito !!!')

def desconectar():
    ssh_client.close()

def prueba(a, b):
    print(f'Bytes transferidos: {a}/{b}')


def obtenerFichero(fichero):
    # Definimos la ruta donde queremos poner el fichero
    local_file_path = 'D:/T138078'
    # Definimos la ruta y fichero que queremos traer a local
    remote_file_path = '/users/cairo/instalaciones/' + fichero
    print(f'Vamos a descargar el fichero <{fichero}>')
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path, callback=prueba)
        # aqui ya tenemos el fichero
        sftp.close()
    except Exception as err:
        print(f'SFTP falló debido al error ' + str(err))

ssh_client = paramiko.SSHClient()
serverList = {'cairo_desaomega': ['10.33.241.120', '22', 'cairo'] }
serverId = 'cairo_desaomega'
conectar(serverId)
obtenerFichero('listaSubidasProduccionRealizadas.csv')
desconectar()