'''
Created on 31/07/2013

@author: xabi
'''
# -*- coding: utf-8 -*- 

from FramePrincipal import FramePrincipal
import wx



class MyApp(wx.App):
    """ Clase que arranca el programa """
    
    def OnInit(self):
        """ Metodo que se llama al iniciar la clase """
    
        frame = FramePrincipal(None, -1, 'Xabi Torrent')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
    

# Arranque de la aplicacion
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
    
