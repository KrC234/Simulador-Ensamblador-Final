import re 
import Recursos as r

# Fase 1: Separación de instrucciones
class Separacion:
    
    def __init__(self):
        pass

    def generar_tokens(self,contenido):
        lineas = contenido
        tokens_globales = []
        for linea in lineas:
            if any(linea.strip().lower().startswith(keyword) for keyword in ['.stack segment','.code segment','.data segment']):
                tokens_globales.append(linea.strip())
                continue

            linea = re.split(r';', linea, maxsplit=1)[0]
            partes_preservadas = []
            def reemplazo(m):
                partes_preservadas.append(m.group(0))
                return f'__PLACEHOLDER_{len(partes_preservadas) - 1}__'

            linea_sin_cadenas = re.sub(r'(["\']).*?\1', reemplazo, linea)
            tokens = [token.strip() for token in re.split(r'[,\s]+', linea_sin_cadenas) if token]
            for i, cadena in enumerate(partes_preservadas):
                tokens = [token.replace(f'__PLACEHOLDER_{i}__', cadena) for token in tokens]

            tokens_globales.extend(tokens)
        return [token for token in tokens_globales if token]
    

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
        elif re.match(r"^'[^']+'$",token):
            return "Carácter"
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
            return "Simbolo"
        elif ":" in token:
            return "Etiqueta"
        else:
            return "Elemento desconocido"
        
    def clasificar_tokens(self,contenido):
        tokens = self.generar_tokens(contenido)
        clasificados = [(token,self.identificar_tipo(token)) for token in tokens]
        return clasificados