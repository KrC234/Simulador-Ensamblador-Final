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

    def reemplazar_valores(self,codigo,reg = None, mod = None, r_m =  None):
        if 'mod' in codigo and mod is not None:
            codigo = codigo.replace('mod',mod)
        if 'reg' in codigo and reg is not None:
            codigo = codigo.replace('reg',reg)
        if 'r/m' in codigo and r_m is not None:
            codigo = codigo.replace('r/m',r_m)
        return codigo 

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
        direccion = instruccion_data['direccion']
        mod = '11'
        r_m = r.registros_binarios[operando]
        direccion = self.reemplazar_valores(direccion, mod=mod,r_m=r_m)
        binario = f'{opcode}{direccion}'
        codificacion = hex(int(binario,2))
        return codificacion


