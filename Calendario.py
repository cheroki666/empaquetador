import wx
import wx.adv
from datetime import datetime

class Calendario(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, title=title, size=(300, 300))
        self.panel =MainPanel(self)
        self.Centre()
        self.Show(True)

    def OnDate(self, event):
        global fechaInicio
        fechaInicio = self.calendario.GetDate()
        print(f'Hemos seleccionado la fecha: {fechaInicio}')
        wx.Window.Close(self)
    def OnCloseWindow(self, event):
        # tell the window to kill itself
        self.Destroy()



class MainPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        # Button
        button_sizer = self._button_sizer(frame)
        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(button_sizer,proportion=1, flag=wx.EXPAND)
        self.SetSizer(main_sizer)

        #self.calendario = wx.adv.CalendarCtrl(self, date=wx.DateTime.Now())
        #self.bCambioFecha = wx.Button(self, frame, wx.ID_ANY, 'Seleccionar')
        #self.bCambioFecha.Bind(wx.EVT_BUTTON, self.OnButton)
        #self.calendario.Bind(wx.adv.EVT_CALENDAR, self.OnDate)
        #fecha = self.calendario.GetDate()

        self.Fit()

    def OnButton(selfself, event):
        print('Boton pulsado')

    def _button_sizer(self, frame):
        cmd_fijarFecha = wx.Button(self, label='Selecciona')
        cmd_fijarFecha.Bind(wx.EVT_BUTTON, self.OnButton)
        cmd_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(cmd_fijarFecha)
        button_sizer.Add((-1, -1), proportion=1)
        button_sizer.Add(cmd_cancel)
        return button_sizer

if __name__ == '__main__':
    fechaInicio = datetime.today()
    print(f'La fecha actual es: {fechaInicio}')
    miApp = wx.App(False)
    frame = Calendario(None, 'Empaquetador')
    miApp.MainLoop()