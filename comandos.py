import paramiko
import socket
import time


def conectar(serverId):
    ssh_client = paramiko.SSHClient()
    serverList = {'cairo_desaomega': ['10.33.241.120', '22', 'cairo']}
    ip = serverList[serverId][0]
    puerto = serverList[serverId][1]
    usuario = serverList[serverId][2]

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    # Establecer política por defecto para localizar la llave del host localmente
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Conectarse
    ssh_client.connect(ip, puerto, usuario, 'omega123')
    # aqui tenemos que comprobar si hemos recibido el prompt

    print('Conexion establecida con exito !!!')
    return ssh_client


def obtenerCanal(ssh_client):
    transport = ssh_client.get_transport()
    session = transport.open_session()
    session.set_combine_stderr(True)
    mychannel = ssh_client.invoke_shell(term='vt100', width=255, height=24)
    mychannel.settimeout(10)
    return mychannel


def desconectar(ssh_client):
    ssh_client.close()


def ejecutarComando(maquina, miComando):
    ssh_client = conectar(maquina)
    canal = obtenerCanal(ssh_client)
    '''
    patronFinal = '#'
    print('Ejecutando comando: [%s]' % miComando)
    salir = False
    txtsalida = ''
    retorno = ''
    try:
        # esperamos a tener el prompt
        while txtsalida.find('#') == -1:
            time.sleep(0.01)
            salidaparcial = canal.recv(4096)
            txtsalida += salidaparcial.decode('utf-8')
        time.sleep(0.01)
    except socket.timeout as msg:
        salir = True
    # print('Tenemos el prompt... <#>')
    txtsalida = ''

    try:
        canal.send(miComando + '\n')

        salidaparcial = ''
        while txtsalida.find(patronFinal) == -1:
            time.sleep(0.01)
            salidaparcial = canal.recv(4096)
            # print('Recepcion parcial: [%s]' % salidaparcial.decode('utf-8'))
            txtsalida += salidaparcial.decode('utf-8')
            # print('Recibo: [%s]' % txtsalida)
        time.sleep(0.01)
    except socket.timeout as msg:
        salir = True
        print(txtsalida + 'Temporizacion vencida !!!')
    # Vamos a devolver lo que coincida con el patron, si lo hay,
    # y si no, devolvemos todo el texto
    '''
    retorno = obtenerdatoscanal(ssh_client, canal,miComando)
    canal.close()
    desconectar(ssh_client)
    return retorno


def obtenerdatoscanal(ssh_client, canal, miComando):
    patronFinal = '#'
    print('Ejecutando comando: [%s]' % miComando)
    salir = False
    txtsalida = ''
    retorno = ''
    try:
        # esperamos a tener el prompt
        while txtsalida.find('#') == -1:
            time.sleep(0.01)
            salidaparcial = canal.recv(4096)
            txtsalida += salidaparcial.decode('utf-8')
        time.sleep(0.01)
    except socket.timeout as msg:
        salir = True
    # print('Tenemos el prompt... <#>')
    txtsalida = ''

    try:
        canal.send(miComando + '\n')

        salidaparcial = ''
        while txtsalida.find(patronFinal) == -1:
            time.sleep(0.01)
            salidaparcial = canal.recv(4096)
            # print('Recepcion parcial: [%s]' % salidaparcial.decode('utf-8'))
            txtsalida += salidaparcial.decode('utf-8')
            # print('Recibo: [%s]' % txtsalida)
        time.sleep(0.01)
    except socket.timeout as msg:
        salir = True
        print(txtsalida + 'Temporizacion vencida !!!')
    # Vamos a devolver lo que coincida con el patron, si lo hay,
    # y si no, devolvemos todo el texto
    '''
    if miComando.patronTxt == '' :
        retorno = txtsalida
    else :
        m = re.search(miComando.patronTxt, txtsalida)
        if m:
            retorno = txtsalida[m.start(): m.end()]
            print( 'Devolvemos lo que coincide con \'{}\': [{}]'.format(miComando.patronTxt,retorno))
        else:
            retorno = txtsalida
    '''
    return txtsalida

def ejecutarScript(maquina, script):
    ssh_client = conectar(maquina)
    canal = obtenerCanal(ssh_client)
    salida = ''
    for comando in script:
        salida += obtenerdatoscanal(ssh_client, canal, comando)

    canal.close()
    desconectar(ssh_client)
    return salida


if __name__ == '__main__' :
    resultado = ejecutarComando('cairo_desaomega', 'cvs -d :pserver:cairo:omega123@172.20.32.29:2412/REPOSITORIO/CAIRO diff OmegaCAIRO/cfg/GesOPV2/reglas/ASTRO_SOC_BAM_TRAFFICA/patCeseAlarma.cfg')
    print(f'El resultado del comando es: [{resultado}]')
    if resultado.find('I know nothing about') != -1:
        print('Ese fichero no está en CVS. Tenemos que hacer un cvs add ... ')

    resultado = ejecutarComando('cairo_desaomega', 'cp OmegaCAIRO/bin/GesOPV2/FunEntIGRIWS/FunEnt_EjeAccCAIRO_INC_ACTUACION_AMOV /users/cairo/instalaciones_prueba/OmegaCAIRO/bin/GesOPV2/FunEntIGRIWS/FunEnt_EjeAccCAIRO_INC_ACTUACION_AMOV')
    print(f'El resultado del comando es: [{resultado}]')
