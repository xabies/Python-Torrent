'''
Created on 31/07/2013

@author: xabi
'''

class DTOdescarga:
    """ Clase almacen para la barra de descargas """
    
    nombre = None
    porcentaje = None
    velDescarga = None
    velSubida = None
    peers = None
    ejecutando = None
    activo = False
    
    def __init__(self, nombre, porcentaje, velDescarga, velSubida, peers, estado, activo):
        self.nombre=nombre
        self.porcentaje=porcentaje
        self.velDescarga=velDescarga
        self.velSubida=velSubida
        self.peers=peers
        self.ejecutando=estado
        self.activo = activo


    def setNombre(self, nombre):
        self.nombre=nombre
        
    def getNombre(self):
        return self.nombre
    
    
    def setPorcentaje(self, porcentaje):
        self.porcentaje=porcentaje
    
    def getPorcentaje(self):
        return self.porcentaje
    
    
    def setVelDescarga(self, velocidad):
        self.velDescarga=velocidad
    
    def getVelDescarga(self):
        return self.velDescarga
    
    
    def setVelSubida(self, velocidad):
        self.velSubida=velocidad
    
    def getVelSubida(self):
        return self.velSubida
    
    
    def setPeers(self, peers):
        self.peers=peers
    
    def getPeers(self):
        return str(self.peers)
    
    
    def setEstado(self, estado):
        self.ejecutando=estado
    
    def getEstado(self):
        return self.ejecutando
    
    def setActivo(self, activo):
        self.activo=activo
    
    def getActivo(self):
        return self.activo
    
    