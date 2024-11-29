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
        codificacion = hex(int(binario,2))

        return codificacion
    
    def decodificar_un_operando(self, instruccion, operando):
        if instruccion not in r.instrucciones_1:
            return 'Instrucción no reconocida'
    
        tipo = None 
        w = None 

        if operando in r.registros_8:
            tipo = 'reg/mem'
            w = '0'
        elif operando in r.registros_16:
            tipo = 'reg/mem'
            w = '1'
        
        instruccion_data = r.decodificaciones_1[instruccion]
        if instruccion_data['operando'] != tipo:
            return 'Operando no valido'
        
        opcode = instruccion_data['opcode'].replace('w',w)
        mod = '11'
        reg = instruccion_data['reg']
        r_m = r.registros_binarios[operando]

        binario = f'{opcode}{mod}{reg}{r_m}'
        codificacion = hex(int(binario,2))
        return codificacion


