import sqlite3, os
from typing import Any

class Contacto:
        
    def __init__(self) -> None:
        self.__cnx:sqlite3.Connection|None=None
        self.__cursor:sqlite3.Cursor|None=None
        self.__ruta = 'programacion/flask/data/Contactos.db'   
        if not os.path.exists(self.__ruta):     
            self.__inicializar()
        
    @staticmethod
    def __cnx_db(funcion:Any):
        def cnx(self:'Contacto', *args, **kwargs)->(Any|None):
            fet,dt=0, False
            with sqlite3.connect(self.__ruta) as self.__cnx:                
                self.__cursor=self.__cnx.cursor()          
                comando, *data=funcion(self, *args, **kwargs)
                if isinstance(data[0],int):                    
                    fet, dt=data[0], True
                    if dt==1:self.__cursor.execute(comando)                
                elif len(data)>1 and isinstance(data[1],int):
                    fet, dt=data[1], True
                    self.__cursor.execute(comando, data[0])
                else:self.__cursor.execute(comando, data[0])                                 
            if dt==True:return self.__cursor.fetchone() if fet==0 else self.__cursor.fetchall()
            else:return None
        return cnx
    
    @__cnx_db
    def __inicializar(self):
        return ('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                telefono TEXT,
                correo_electronico TEXT
            )
        ''')
                        
    @__cnx_db
    def eliminar(self, **info_usuario):
        self.__invariante(**info_usuario)
        return ('''
        DELETE FROM contactos
        WHERE nombre = ? AND telefono = ?
    ''', (info_usuario['nombre'], info_usuario['celular']))
    
    @__cnx_db
    def agregar(self, **info_usuario):
        self.__invariante(**info_usuario)
        return ('''
        INSERT INTO contactos (nombre, telefono, correo_electronico)
        VALUES (?, ?, ?)
    ''', (info_usuario['nombre'], info_usuario['celular'], info_usuario['correo']))
    
    @__cnx_db
    def editar(self,**info_usuario):
        self.__invariante(**info_usuario)
        return ('''
        UPDATE contactos
        SET nombre = ?, telefono = ?, correo_electronico = ?
        WHERE nombre = ? AND telefono = ?
    ''', (info_usuario['nombre'], info_usuario['celular'], info_usuario['correo'], info_usuario['b_nombre'], info_usuario['b_celular']))
        
    @__cnx_db
    def buscar(self, **info_usuario):
        self.__invariante(**info_usuario)
        return ('''
        SELECT * FROM contactos
        WHERE nombre = ? AND telefono = ?
    ''', (info_usuario['nombre'], info_usuario['celular']),0)
    
    @__cnx_db
    def listar_contactos(self):
        return 'SELECT * FROM contactos', 1  
    
    def __invariante(self, **info_usuario):
        #palabras_clave=('SELECT','*','FROM','VALUES','TABLE','DATABASE','WHERE')
        for k,v in info_usuario.items():
            assert v and v!='' and v != None, AttributeError(f"El atributo {k} no puede ser None ni vacio")
            #assert v.upper() not in palabras_clave, ValueError(f"El valor del atributo {k} es invalido"