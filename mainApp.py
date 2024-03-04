
# Importamos las wx
import wx
import wx.adv
import comandos as cmd
import appEmpaquetador_1 as funciones



# Creamos una clase frame que pide un dato.
class frame_secundario(wx.Frame):
    def __init__(self, parent):
        # Este es el constructor. Darse cuenta que se pasa como
        # parámetro parent, esto es, la referencia del frame que instancia
        # a esta clase. La guardamos.
        self.padre = parent
        # Llamamos al constructor de la clase de la que hereda.
        wx.Frame.__init__(self, None, -1, title="Introduce Fecha")

        # Creamos un sizer vertical.
        vsizer = wx.BoxSizer(wx.VERTICAL)

        # Creamos un Calendar
        self.ccalendar = wx.adv.CalendarCtrl(self )
        self.ccalendar.Bind(wx.adv.EVT_CALENDAR, self.cambioFecha)
        vsizer.Add(self.ccalendar, 0, wx.ALL, 5)
        # Creamos una caja de texto.
        self.tbFechaInicio = wx.TextCtrl(self, -1, style=wx.TE_RIGHT)
        # Creamos un botón.
        self.boton = wx.Button(self, -1, "Seleccionar")
        # Añadimos al sizer la caja y el botón.
        vsizer.Add(self.tbFechaInicio, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        vsizer.Add(self.boton, 1, wx.ALL | wx.CENTER, 5)
        # Incluimos el sizer en el frame.
        vsizer.Fit(self)
        self.SetSizer(vsizer)

        # Creamos el binding. Cuando se haga click en el
        # botón se lanzará el manejador de eventos correspondiente.
        self.boton.Bind(wx.EVT_BUTTON, self.OnClickBoton)


    # Manejador de eventos.
    def OnClickBoton(self, event):
        # Obtenemos datos de la caja de texto.
        dato = self.tbFechaInicio.GetValue()
        if dato == '':
            dato = (self.ccalendar.GetDate()).Format(format='%d/%m/%Y')
        # Podríamos escribir directamente en el objeto
        # que se desease.
        self.tbFechaInicio.SetValue(dato)
        self.padre.tbFechaInicio.SetValue(dato)
        # Nos vamos.
        self.Destroy()

    def cambioFecha(self, event):
        self.tbFechaInicio.SetValue((self.ccalendar.GetDate()).Format(format='%d/%m/%Y'))

# Creamos la clase de la ventana principal.
class frame_principal(wx.Frame):
    def __init__(self):
        # Constructor. Llamamos al constructor de la clase wx.Frame.
        wx.Frame.__init__(self, None, -1, title='OPV_Empaquetador')
        # Creamos un sizer horizontal.

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Creamos un botón.
        self.boton = wx.Button(self, -1, "Fecha Inicio")
        self.boton.Bind(wx.EVT_BUTTON, self.OnSelInicioBoton)
        # Creamos una caja de texto de solo lectura.
        self.etfechainicio = wx.StaticText(self, -1, style=wx.ALIGN_LEFT, label = 'Fecha Inicio')
        self.tbFechaInicio = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        self.tbFechaInicio.Bind(wx.EVT_TEXT, self.OnCambioFechaInicio)
        hsizer.Add(self.etfechainicio, 0, wx.CENTER, 5)
        hsizer.Add(self.tbFechaInicio, 0, wx.ALL, 5)

        # Añadimos al sizer la caja y el botón.
        vsizer.Add(hsizer, 0, wx.ALL, 5)
        vsizer.Add(self.boton, 0, wx.ALL, 5)
        # vsizer.Add(self.caja_texto, 0, wx.ALL, 5)

        # Creamos un CheckListBox
        self.clbLista = wx.CheckListBox(self, -1)
        vsizer.Add(self.clbLista, 4, wx.EXPAND | wx.LEFT | wx.RIGHT| wx.BOTTOM, 5 )
        vsizer.SetMinSize(800,400)
        vsizer.Fit(self)

        # Creamos un TextCtrl para escribir lo que vamos haciendo
        self.tclog = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.tclog.SetBackgroundColour(wx.Colour(253, 245, 226, 1))
        vsizer.Add(self.tclog, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        # Creamos un boton para Validar los ficheros.
        self.btValidar = wx.Button(self, -1, "Validar")
        self.btValidar.Bind(wx.EVT_BUTTON, self.OnClickComienzo)
        self.btValidar.Enable(False)
        vsizer.Add(self.btValidar, 0, wx.ALL, 5)

        # Asociamos el sizer al frame.
        self.SetSizer(vsizer)
        # Creamos el binding. Cuando se haga click en el
        # botón se lanzará el manejador de eventos correspondiente.


    # Manejador de eventos.
    def OnSelInicioBoton(self, event):
        # Si se hace click se crea una instancia del frame_secundario.
        frame = frame_secundario(self)
        # Mostramos.
        self.actualizarLog('Seleccionamos la fecha de inicio...')
        frame.Show()

    def OnCambioFechaInicio(self, event):
        # Si se hace click se crea una instancia del frame_secundario.
        listaFicheros = ['Fichero 1', 'Fichero 2', 'Fichero 3', 'Fichero 4', 'Fichero 5']
        self.actualizarLog('Fecha seleccionada: ' + self.tbFechaInicio.GetValue())
        self.clbLista.Clear()
        lista = funciones.obtenerListaFicheros(self.tbFechaInicio.GetValue())
        self.clbLista.AppendItems(lista)
        listareducida = []
        for fichero in lista:
            info = fichero.split(' | ')
            if info[0] != '0' and info[0] != '00000':
                # estos los debemos marcar
                listareducida.append(fichero)
        self.clbLista.SetCheckedStrings(tuple(listareducida))
        self.actualizarLog("Obtenemos los ficheros que se van a consolidar...")
        # Mostramos.
        self.btValidar.Enable(True)
        frame.Show()

    def OnClickComienzo(self, event):
        # Habrá que conectarse a la máquina y ejecutar comandos

        listaFicheros = self.clbLista.GetCheckedStrings()
        lFicheros = []
        for dato in listaFicheros:
            valores = dato.split(' | ')
            lFicheros.append(valores[1])
        # 1 - Comprobaremos el estado de los ficheros en CVS
        listaresultados = self.ejecutarCVSstatus(lFicheros)



    def actualizarLog(self, texto):
        # textoFinal = self.tclog.GetValue() + texto + '\n'
        self.tclog.AppendText(texto + '\n')
        self.tclog.Refresh()

    def ejecutarCVSstatus(self, listaFicheros):
        listaAdd = []
        listaCommit = []
        listaEliminar = []
        # ejecutar comando: cvs -d :pserver:cairo:omega123@172.20.32.29:2412/REPOSITORIO/CAIRO diff
        for fichero in self.clbLista.GetCheckedStrings():
            datos = fichero.split(' | ')
            comando = 'cvs -d :pserver:cairo:omega123@172.20.32.29:2412/REPOSITORIO/CAIRO diff ' + datos[1]

            resultado = cmd.ejecutarComando('cairo_desaomega', comando)
            # print(resultado)
            if resultado.find('I know nothing about') != -1:
                print(f'Fichero: [{fichero}] no está en CVS. Tenemos que hacer un cvs add ...')
                self.actualizarLog(f'Fichero: [{datos[1]}] no está en CVS. Tenemos que hacer un cvs add ... ')
                listaAdd.append(fichero)
            elif resultado.find('No such file or directory') != -1:
                print(f'Fichero: [{fichero}] NO existe en la ruta. Debemos eliminarlo ...')
                self.actualizarLog(f'Fichero: [{datos[1]}] NO existe en la ruta. Debemos eliminarlo ...')
                listaEliminar.append(fichero)
            else:
                print(f'Fichero: [{fichero}] YA está en CVS. Tenemos que hacer un cvs commit ...')
                self.actualizarLog(f'Fichero: [{datos[1]}] YA está en CVS. Tenemos que hacer un cvs commit ...')
                listaCommit.append(fichero)

        self.actualizarLog(f'Vamos a deseleccionar los ficheros no encontrados: \n{listaEliminar}')
        self.deseleccionarFicheros(listaEliminar)
        self.construirPaquete()
        return listaAdd

    def deseleccionarFicheros(self, lista):
        seleccionados = dict()
        listaIndices = self.clbLista.GetCheckedItems()
        listaCadenas = self.clbLista.GetCheckedStrings()
        for indice in range(len(listaIndices)):
            seleccionados[listaIndices[indice]] = listaCadenas[indice]
        for fichero in lista:
            # obtenemos el item del fichero
            indicefichero = self.dameClavePorValor(seleccionados, fichero)
            print(f'El indice es: {indicefichero}')
            item = self.clbLista.GetString(indicefichero)
            self.clbLista.Check(indicefichero, False)
            self.actualizarLog(f'Deseleccionamos <{fichero}>')


    def construirPaquete(self):
        rutaPruebas = '/users/cairo/instalaciones_prueba/'
        # Vamos a crear la estructura necesaria para nuestros ficheros
        '''
        lista = funciones.crearEstructuraDirect(self.clbLista.GetCheckedStrings())

        for ruta in lista:
            comando = 'mkdir instalaciones_prueba' + ruta
            resultado = cmd.ejecutarComando('cairo_desaomega', comando)
            print(f'Resultado del comando <{comando}> es [{resultado}]')


        for dato in self.clbLista.GetCheckedStrings():
            datos_fichero = dato.split(' | ')
            fichero = datos_fichero[1]
        
            cmd.ejecutarComando('cairo_desaomega', 'cp ' + fichero + " " + rutaPruebas + fichero )
        '''
        # ya tenemos los ficheros dentro de su estructura
        # vamos a hacer el paquete:
        comando = cmd.ejecutarScript('cairo_desaomega', ['cd instalaciones_prueba', 'tar -cvf Parche_OPV_GenAutomatica_20240303.tar ./OmegaCAIRO'])
        comando = cmd.ejecutarScript('cairo_desaomega',
                                      ['cd instalaciones_prueba', 'gzip Parche_OPV_GenAutomatica_20240303.tar'])
    def dameClavePorValor(self, my_dict, val):
        for key, value in my_dict.items():
            if val == value:
                return key

        return None


if __name__ == '__main__':
    # Creamos una aplicación wxPython.
    aplicacion = wx.App()
    # Instanciamos el frame principal.
    frame = frame_principal()
    # Y por supuesto, no olvidar mostrarlo.
    frame.Show()
    # Esperamos a capturar eventos.
    aplicacion.MainLoop()