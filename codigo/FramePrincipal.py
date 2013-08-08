# -*- coding: utf-8 -*- 

from HiloDescargaTorrent import EVT_RESULT, HiloDescargaTorrent
from Torrent import Torrent
from wx._core import Size
import os
import shutil
import wx


BOTON_X = 32
BOTON_Y = 32

class FramePrincipal(wx.Frame):
    """ Clase que gestiona la interfaz principal del programa """


    
    
    # Lista de descargas
    descargas = []
    # Indice de la lista seleccionado
    indice = -1
    
    def __init__(self, parent, iD, title):
        """ metodo construcotr """
        
        wx.Frame.__init__(self, parent, iD, title, size=(800, 400))
        self.SetMinSize(Size(800,400))
        self.SetMaxSize(Size(800,400))
        self.CenterOnScreen()
        
        panel = wx.Panel(self)

        self.CreateStatusBar()
        
        
        loc = wx.IconLocation(r'res/icono.ico', 0)
        self.SetIcon(wx.IconFromLocation(loc))
        
        
        # Boton Add
        imagen = wx.Image("res/add.png", wx.BITMAP_TYPE_ANY).Scale(BOTON_X, BOTON_Y).ConvertToBitmap()
        self.btnAnadir = wx.BitmapButton(panel, id=-1, bitmap=imagen,
            pos=(250, 5), size = (BOTON_X+5, BOTON_Y+5))
        self.btnAnadir.SetToolTipString(u"Añadir nuevo torrent")
        
        
        # Boton play
        imagen = wx.Image("res/play.png", wx.BITMAP_TYPE_ANY).Scale(BOTON_X, BOTON_Y).ConvertToBitmap()
        self.btnPlay = wx.BitmapButton(panel, id=-1, bitmap=imagen,
            pos=(325, 5), size = (BOTON_X+5, BOTON_Y+5))
        self.btnPlay.SetToolTipString("Comenzar descarga")

        # Boton pause
        imagen = wx.Image("res/pause.png", wx.BITMAP_TYPE_ANY).Scale(BOTON_X, BOTON_Y).ConvertToBitmap()
        self.btnPause = wx.BitmapButton(panel, id=-1, bitmap=imagen,
            pos=(400, 5), size = (BOTON_X+5, BOTON_Y+5))
        self.btnPause.SetToolTipString("Pausar descarga")
        
        # Boton eliminar
        imagen = wx.Image("res/delete.png", wx.BITMAP_TYPE_ANY).Scale(BOTON_X, BOTON_Y).ConvertToBitmap()
        self.btnEliminar = wx.BitmapButton(panel, id=-1, bitmap=imagen,
            pos=(475, 5), size = (BOTON_X+5, BOTON_Y+5))
        self.btnEliminar.SetToolTipString("Eliminar torent de la lista")
        
        

        # Anadimos los titulos de las listas
        self.lista = wx.ListCtrl(panel, size=(775,290), pos=(5, 45),style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        
        self.lista.InsertColumn(0, 'Nombre', width=175)
        self.lista.InsertColumn(1, 'Porcentaje', width=100)
        self.lista.InsertColumn(2, 'Vel. Descarga', width=125)
        self.lista.InsertColumn(3, 'Vel. Subida', width=125)
        self.lista.InsertColumn(4, 'Peers', width=100)
        self.lista.InsertColumn(5, 'Estado', width=150)
        
        
        
        os.chdir("torrents/")
        i=0
        for fichero in os.listdir("."):
            if fichero.endswith(".torrent"):
                print("torrents/" + fichero)
                self.lista.InsertStringItem(i, fichero)
                self.descargas.append(Torrent(fichero,None,False))
                i=i+1
                
                
        
        
        # Seteamos los listeners
        self.btnPlay.Bind(wx.EVT_BUTTON, self.botonPlay)
        self.btnPause.Bind(wx.EVT_BUTTON, self.botonPause)
        self.btnEliminar.Bind(wx.EVT_BUTTON, self.eliminarDescarga)
        self.btnAnadir.Bind(wx.EVT_BUTTON, self.anadirDescarga)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        EVT_RESULT(self,self.OnResult)
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionLista)
        self.lista.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deseleccionLista)

    
        
        # Configuramos la vista inicial
        self.btnPlay.Enable(False)
        self.btnPause.Enable(False)
        self.btnEliminar.Enable(False)
        self.cambiarEstado()
        
        
        
    def botonPlay(self, event) :
        """ Comienza a descargar el torrent """
        
        if self.indice > -1:
            self.btnPlay.Enable(False)
            self.btnPause.Enable(True)
            
            
            torrent=self.descargas[self.indice]
            torrent.setEjecutando(True)
            torrent.setHilo(HiloDescargaTorrent(self.indice, "torrents/" + torrent.getFichero(), self))
            self.descargas[self.indice]=torrent 
            self.cambiarEstado()
        
        
    def botonPause(self, event):
        """ Detiene el hilo de descarga """
        
        self.btnPlay.Enable(True)
        self.btnPause.Enable(False)
        
        
        try:
            torrent = self.descargas[self.indice]
            if torrent.isEjecutando():
                torrent.getHilo().detener()
                torrent.setEjecutando(False)
                self.descargas[self.indice] = torrent
        except:
            print("Excepcion al pausar hilo")
        
        self.cambiarEstado()
            
    def OnResult(self, event):
        """ Recibe resultados del hilo de descarga """
        
        if not event.datos.getActivo():
            torrent=self.descargas[event.indice]
            torrent.setEjecutando(False)
            torrent.setHilo(None)
            self.descargas[event.indice]=torrent
            self.btnPlay.Enable(True)
            self.btnPause.Enable(False)
            
        
        self.lista.SetStringItem(event.indice, 0, event.datos.getNombre())
        self.lista.SetStringItem(event.indice, 1, event.datos.getPorcentaje())
        self.lista.SetStringItem(event.indice, 2, event.datos.getVelDescarga())
        self.lista.SetStringItem(event.indice, 3, event.datos.getVelSubida())
        self.lista.SetStringItem(event.indice, 4, event.datos.getPeers())
        self.lista.SetStringItem(event.indice, 5, event.datos.getEstado())
        
        self.cambiarEstado()
        
        
    def OnClose(self, event):
        """ metodo llamado al cerrar la ventana """
        
        print("onClose")
        
        for torrent in self.descargas:
            hilo=torrent.getHilo()
            if hilo:
                hilo.detenerCerrar()
        self.Destroy()
    
    def cambiarEstado(self):
        """ Cambia el texto de la barra de estado"""
        
        conectado = False
        for torrent in self.descargas:
            if torrent.isEjecutando == True:
                self.SetStatusText("Conectado a la red BitTorrent")
                conectado = True
                break
        
        if conectado == False:
            self.SetStatusText("Esperando")
        
    def seleccionLista(self, event):
        """ Metodo lanzado al pulsar un elemento de la lista"""
        
        self.indice=event.GetIndex()
        self.btnEliminar.Enable(True)
        torrent=self.descargas[self.indice]
        
        if not torrent.isEjecutando():
            self.btnPlay.Enable(True)
            self.btnPause.Enable(False)
        else:
            self.btnPlay.Enable(False)
            self.btnPause.Enable(True)


    def deseleccionLista(self, event):
        """ Metodo lanzado al des-seleccionar un elemento de la lista"""
        
        self.indice=-1
            
        self.btnPlay.Enable(False)
        self.btnPause.Enable(False)
        self.btnEliminar.Enable(False)

        
    def eliminarDescarga(self, event):
        """ Metodo lanzado al pulsar sobre el boton eliminar"""
        
        
        if self.indice >-1:
            
            # dialogo para confirmar la eliminacion
            dlg = wx.MessageDialog(self, u"¿Deseas eliminar este torrent?", "Eliminar", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                
                torrent = self.descargas[self.indice]
                fichero = torrent.getFichero()
                if torrent.isEjecutando():
                    try:
                        if not torrent.getHilo() is None:
                            torrent.getHilo().detenerCerrar()
                    except:
                        print("Excepcion al eliminar el torrent")
                    torrent.setEjecutando(False)
                    self.descargas[self.indice] = torrent
                     
                # Lo quitamos de la lista visual
                self.lista.DeleteItem(self.indice)
                 
                # Lo quitamos de la lista de descargas
                self.descargas.remove(self.descargas[self.indice])
                
                for descarga in self.descargas:
                    if not descarga.getHilo() is None:
                        if descarga.getHilo().getIndice() >= self.indice:
                            descarga.getHilo().reducirIndice()
                 
                # Borramos el .torrent para NO volver a cargarlo
                
                try:
                    os.remove("../torrents/" + fichero)
                except:
                    print("El archivo .torrent a borrar ya No existe")
     
                self.btnEliminar.Enable(False)
            dlg.Destroy()
            
            
    def anadirDescarga(self, event):
        """ Metodo lanzado al pulsar sobre el boton anadir """
    
    
        # dialogo para seleccionar el ficero
        openFileDialog = wx.FileDialog(self, "Abrir fichero .torrent", "", "",
                                   "Archivo Torrent (*.torrent)|*.torrent", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() != wx.ID_CANCEL:
            print(openFileDialog.GetPath())
            
            # Copiamos el fichero a nuestro directoro
            shutil.copy2(openFileDialog.GetPath(), "../torrents/" + openFileDialog.GetFilename())
            
            self.lista.InsertStringItem(self.lista.GetItemCount(), openFileDialog.GetFilename())
            self.descargas.append(Torrent(openFileDialog.GetFilename(),None,False))
