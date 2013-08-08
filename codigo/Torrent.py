'''
Created on 01/08/2013

@author: xabi
'''


class Torrent:
    """ Clase almacen para cada una de las descargas """
    
    # Nombre del fichero .torrent
    fichero = None
    #Hilo que se encarga de este Torrent
    hilo = None
    # Estado en que se encuentra este .torrent
    ejecutando = False
    
    def __init__(self, fichero, hilo, estado):
        self.fichero = fichero
        self.hilo = hilo
        self.ejecutando = estado


    def setFichero(self, fichero):
        self.fichero=fichero
        
    def getFichero(self):
        return self.fichero
    
    
    def setHilo(self, hilo):
        self.hilo=hilo
        
    def getHilo(self):
        return self.hilo
    
    
    def setEjecutando(self, estado):
        self.ejecutando=estado
        
    def isEjecutando(self):
        return self.ejecutando
    