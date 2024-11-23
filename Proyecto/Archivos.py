class Archivos:

    # Modulo para el tratamiento y uso de archivos 
    def __init__():
        pass

    def cargar_archivo(self,ruta):
        try:
            with open(ruta, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print('Archivo no encontrado')
            return None 
        

    def separar_lineas(self,contenido):
        lineas = contenido.splitlines()
        return lineas
    
    def procesar_archivo(self,ruta):
        contenido = self.cargar_archivo(ruta)
        lineas = self.procesar_archivo(contenido)
        return lineas 




