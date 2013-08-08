'''
Created on 30/07/2013

@author: xabi
'''
from __future__ import print_function
from DTOdescarga import DTOdescarga
from threading import Thread
import libtorrent as lt
import sys
import time
import wx



EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):

    def __init__(self, indice, datos):

        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.indice = indice
        self.datos = datos



class HiloDescargaTorrent(Thread):
    
    parar = False
    salir = False
    
    def __init__(self, indice, ficheroTorrent, ventana):
        Thread.__init__(self)
        self.rutaTorrent = ficheroTorrent
        self._ventana = ventana
        self.indice = indice
        self.start()
    
    
    def detener(self):
        self.parar = True
        
    def detenerCerrar(self):
        self.salir = True
        self.parar = True
        
    def reducirIndice(self):
        """ Reduce el indice, para cuando eliminamos una descarga """
        self.indice = self.indice -1
        
    def getIndice(self):
        return self.indice
    
    
    def run(self):     
        
        session = lt.session()
        session.listen_on(6881, 6891)
          
        print(self.rutaTorrent)
        
        e = lt.bdecode(open("../" + self.rutaTorrent, 'rb').read())
        info = lt.torrent_info(e)
        
        h = session.add_torrent({'ti': info, 'save_path': '.'})
        print('starting', h.name())
        
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        
        time.sleep(1)
        
        s = h.status()
        infoDescarga = DTOdescarga(h.name(), "%.2f" % (s.progress * 100) + " %", "0.0", "0.0", "0", "cargando", True)
        
        # while (not h.is_seed() and self.parar==False):  
        while (self.parar == False):
            s = h.status()
          
            print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]), end=' ')
            sys.stdout.flush()
            
            infoDescarga.setPorcentaje("%.2f" % (s.progress * 100) + " %")
            infoDescarga.setVelDescarga("%.2f" % (s.download_rate / 1000) + " Kb/s")
            infoDescarga.setVelSubida("%.2f" % (s.upload_rate / 1000) + " Kb/s")
            infoDescarga.setPeers(s.num_peers)
            
            if (s.progress >= 1.0):
                infoDescarga.setEstado("Completado")
            else:
                infoDescarga.setEstado("Descargando")
            
            
            
            wx.PostEvent(self._ventana, ResultEvent(self.indice, infoDescarga))
              
            time.sleep(1)
        
        if not self.salir:
            infoDescarga.setPorcentaje("%.2f" % (s.progress * 100) + " %")
            infoDescarga.setVelDescarga("-")
            infoDescarga.setVelSubida("-")
            infoDescarga.setPeers("-")
            infoDescarga.setActivo(False)
            infoDescarga.setEstado("Detenido")
            wx.PostEvent(self._ventana, ResultEvent(self.indice, infoDescarga))
        
        print("\n")
        print(h.name(), 'hilo detenido')

