import wx
import wx.adv

class Empaquetador(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 400))
        # Associate some events with methods of this class
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_MOVE(self, self.OnMove)

        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.calendario = wx.adv.CalendarCtrl(self, 10, wx.DateTime.Now())
        self.calendario.Bind(wx.adv.EVT_CALENDAR, self.OnDate)
        self.Show(True)

    def OnDate(self, event):
        print(self.calendario.GetDate())
        wx.Window.Close(self)
    def OnCloseWindow(self, event):
        # tell the window to kill itself
        self.Destroy()

    # This method is called by the system when the window is resized,
    # because of the association above.
    def OnSize(self, event):
        size = event.GetSize()
        # self.sizeCtrl.SetValue("%s, %s" % (size.width, size.height))

       # tell the event system to continue looking for an event handler,
        # so the default handler will get called.
        event.Skip()

    # This method is called by the system when the window is moved,
    # because of the association above.
    def OnMove(self, event):
        pos = event.GetPosition()
        # self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))


if __name__ == '__main__':
    miApp = wx.App(False)
    frame = Empaquetador(None, 'Empaquetador')
    miApp.MainLoop()