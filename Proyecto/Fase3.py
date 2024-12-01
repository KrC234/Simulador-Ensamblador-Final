import re 
import Recursos as r

# Elaboración de la Fase 3 del proyecto de ensambladores 

class Codificacion:

    def __init__(self):
        pass

    '''
    Codificacion de instrucciones 
    dependiendo de la cantidad de operandos que estos tienen     
    '''

    #* Se considera los variables del opcode y direccion para sustituir los valores 
    def reemplazar_valores(self,codigo,reg = None, mod = None, r_m =  None):
        if 'mod' in codigo and mod is not None:
            codigo = codigo.replace('mod',mod)
        if 'reg' in codigo and reg is not None:
            codigo = codigo.replace('reg',reg)
        if 'r/m' in codigo and r_m is not None:
            codigo = codigo.replace('r/m',r_m)
        return codigo 
    
    # * Codificaciones: Realiza las codificaciones segun el número de operandos

    def codificar_sin_operandos(self,instruccion):
        if instruccion not in r.instrucciones_0:
            return 'Instruccion no reconocida'
        
        binario = r.decodificaciones_0[instruccion]
        codificacion = hex(int(binario,2))

        return codificacion
    
    def codificar_un_operando(self, instruccion, operando):
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


# TODO: Es necesario validar los operandos para las codificaciones de dos operandos, dado los multiples casos que hay
    def es_registro(self,operando):
        if operando in r.registros_8: 
            return True
        elif operando in r.registros_16:
            return True
        else: 
            return False 
        
    def codificar_dos_operandos(self,instruccion,operandoDestino,operandoFuente):
        if instruccion not in r.instrucciones_2:
            return 'Instrucción no reconocida'
        
        tipos = r.decodificaciones_2[instruccion]
        tipo = None

        d = None
        mod = None
        if self.es_registro(operandoDestino) and self.es_registro(operandoFuente):
            tipo = 'Reg,Reg/Mem'

        tipo_seleccionado =  tipos[tipo]

        if operandoDestino in r.registros_8 or operandoFuente in r.registros_8:
            w = '0'
        elif operandoDestino in r.registros_16 or operandoFuente in r.registros_16:
            w = '1'

        reg = None
        r_m = None
        if tipo == 'Reg/Mem,Reg':
            d = '0'
            reg = r.registros_binarios[operandoFuente]
            mod = '11'
            r_m =  r.registros_binarios[operandoDestino]

        elif tipo == 'Reg,Reg/Mem':
            reg = r.registros_binarios[operandoDestino]
            mod = '11'
            r_m = r.registros_binarios[operandoFuente]

        opcode = tipo_seleccionado['opcode'].replace('w',w)
        direccion = tipo_seleccionado['direccion']
        direccion = self.reemplazar_valores(direccion,mod = mod, reg = reg, r_m = r_m)

        binario = f'{opcode}{direccion}'

        codificacion = hex(int(binario,2))

        return codificacion
    
    # Manejo para la tabla de simbolos
    # Instrucciones sin operandos 
    def codificar_instruccion(self,instruccion, cp):
        codificacion  = self.codificar_sin_operandos(instruccion)
        simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = 'NA', valor = 'NA',direccion =cp,codificacion=codificacion,tamaño='NA')
        cp = int(cp,16) + int(codificacion,16)
        return cp, simbolo

    def codificar_instruccion(self,instruccion,operando):
        codificacion = self.codificar_un_operando(instruccion,operando)
        simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = 'NA', valor = 'NA',direccion =cp,codificacion=codificacion,tamaño='NA')
        cp = int(cp,16) + int(codificacion,16)
        return cp, simbolo

    def codificar_instruccion(self,instruccion,operandoDestino,operandoFuente):
        codificacion = self.codificar_dos_operandos(instruccion,operandoFuente,operandoDestino)
        simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = 'NA', valor = 'NA',direccion =cp,codificacion=codificacion,tamaño='NA')
        cp = int(cp,16) + int(codificacion,16)
        return cp, simbolo


    def registrar_simbolo(self,tipo, simbolo=None,valor=None,direccion=None,codificacion=None,tamaño=None):
        simbolo = {
            'nombre' : simbolo, 
            'tipo' : tipo,
            'valor': valor,
            'codificacion': codificacion,
            'tamaño': tamaño,
            'direccion':direccion
        }
        return simbolo
