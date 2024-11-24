import re 
import Recursos as r

# Fase 1: Separación de instrucciones
class Separacion:
    
    def __init__(self):
        pass

    def generar_tokens(self,contenido):
        lineas = contenido
        tokens = []

        for linea in lineas:
            if linea.lower().startswith(('.code segment','.data segment','.stack segment')):
                tokens.append(linea.strip())

            # !Falta corregir la parte para mantener los espacios entre comillas 
            coincidencias = re.findall(r'(["\']).*?\1', linea)
            for coincidencia in coincidencias:
                tokens.append(coincidencia)
                linea = linea.replace(coincidencia,'')

            # Ignora comentarios dentro de la linea 
            linea = linea.split(';')[0]
            if linea:
                # Separar la línea por comas y espacios (de forma simultánea)
                sub_tokens = [sub_token.strip() for sub_token in re.split(r'[,\s]+', linea)]
                tokens.extend(sub_tokens) 
        return [token for token in tokens if token]
    

    # Identifica el tipo de elemento, en caso de que se encuentre en los recursos establecidos
    def identificar_tipo(self,token):
        if (token.lower() in r.pseudoinstrucciones) or (token.lower() in r.segmentos):
            return "Pseudoinstruccion" 
        elif (token.lower() in r.instrucciones_0) or (token.lower() in r.instrucciones_1) or (
            token.lower() in r.instrucciones_2):
            return "Instruccion"
        elif (token.lower() in r.registros_16):
            return "Registro de 16 Bits"
        elif (token.lower() in r.registros_8):
            return "Registro de 8 Bits"
        elif (token.lower() in r.registros_base):
            return "Registro base"
        elif re.match(r'\d+$', token):
            return "Constante Númerica Decimal"
        elif re.match(r'^[0-9A-Fa-f]+h$',token):
            return "Constante Númerica Hexadecimal"
        else:
            return "Elemento desconocido"
        
    def clasificar_tokens(self,contenido):
        tokens = self.generar_tokens(contenido)
        clasificados = [(token,self.identificar_tipo(token)) for token in tokens]
        return clasificados