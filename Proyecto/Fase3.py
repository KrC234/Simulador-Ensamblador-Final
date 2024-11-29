import re 
import Recursos as r

# Elaboración de la Fase 3 del proyecto de ensambladores 

class Decodificacion:

    def __init__(self):
        pass

    '''
    Decodificación de instrucciones 
    dependiendo de la cantidad de operandos que estos tienen     
    '''
    def decodificar_sin_operandos(self,instruccion):
        if instruccion not in r.instrucciones_0:
            return 'Instruccion no reconocida'
        
        binario = r.decodificaciones_0[instruccion]
        hexadecimal = hex(int(binario,2))

        return hexadecimal


