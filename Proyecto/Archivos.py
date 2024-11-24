class Archivo:

    # Modulo para el tratamiento y uso de archivos 
    def __init__(self):
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
        if contenido is None:
            return []
        
        lineas = self.separar_lineas(contenido)
        # Se transforma el contenido a minusculas para evitar problemas
        lineas = [linea.lower() for linea in lineas]
        # Se eliminan lineas vacias y de comentarios
        lineas = [linea for linea in lineas if linea.strip() and not linea.startswith(';')]
        return lineas 




