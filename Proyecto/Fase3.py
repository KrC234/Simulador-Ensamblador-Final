import re 
import Recursos as r

# Elaboración de la Fase 3 del proyecto de ensambladores 

class Codificacion:

    def __init__(self,variables,etiquetas):
        self.variables = variables
        self.etiquetas = etiquetas 

    
    '''
    Codificacion de instrucciones 
    dependiendo de la cantidad de operandos que estos tienen     
    '''

    #* Se considera los variables del opcode y direccion para sustituir los valores 
    def reemplazar_valores(self,codigo,reg = None, mod = None, r_m =  None, w = None, d = None):
        if 'mod' in codigo and mod is not None:
            codigo = codigo.replace('mod',mod)
        if 'reg' in codigo and reg is not None:
            codigo = codigo.replace('reg',reg)
        if 'r/m' in codigo and r_m is not None:
            codigo = codigo.replace('r/m',r_m)
        if 'w' in codigo and w is not None:
            codigo = codigo.replace('w',w)
        if 'd' in codigo and d is not None:
            codigo = codigo.replace('d', d)
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
        mod =  None
        r_m = None
        bits_desplazamiento = None
        if self.es_registro(operando) and operando in r.registros_8:
            tipo = 'reg/mem'
            mod = '11'
            w = '0'
            r_m = r.registros_binarios[operando]
        elif self.es_registro(operando) and operando in r.registros_16:
            tipo = 'reg/mem'
            mod = '11'
            w = '1'
            r_m = r.registros_binarios[operando]
        elif self.es_variable(operando):
            tipo =  'reg/mem'
            bits_variable = self.obtener_tamano_variable(operando)
            mod = '00'
            r_m = '110'
            bits_desplazamiento =self.calcular_desplazamiento(operando)
            w = '0' if bits_variable == 8 else '1'
        elif self.es_etiqueta(operando):
            tipo = 'etiqueta'
        elif self.es_inmediato(operando):
            tipo = 'inmediato'

        else:
            tipo = 'Operando no valido'
        
        instruccion_data = r.decodificaciones_1[instruccion]
        if instruccion_data['operando'] != tipo:
            return 'Operando no valido'
        
        opcode = instruccion_data['opcode']
        direccion = instruccion_data['direccion']
        if direccion is not None:
            direccion = self.reemplazar_valores(direccion, mod=mod,r_m=r_m)
        elif direccion is None and tipo == 'inmediato':
            direccion = self.codificar_inmediato(operando).zfill(8)
        else:
            direccion = ''
        if bits_desplazamiento is not None:
            direccion = f'{direccion}{bits_desplazamiento}'
        opcode = self.reemplazar_valores(opcode,w=w)
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
        
    def es_variable(self,operando):
        for variable in self.variables:
            if variable['variable'] == operando:
                return variable
        return False 
    
    def es_etiqueta(self,operando):
        if operando in self.etiquetas:
            return True
        return False

    def es_inmediato(self,operando):
        if re.match(r'^[0-9A-Fa-f]+h$',operando):
            return True
        elif re.match(r'^[0-9]+d$', operando):
            return True
        return False

    def codificar_inmediato(self,operando):
        valor_inm = ''
        if re.match(r'^[0-9A-Fa-f]+h$', operando):
            valor_inm = bin(int(operando[:-1], 16))[2:]
        elif re.match(r'^[0-9]+d$', operando):
            valor_inm = bin(int(operando[:-1]))[2:]
        return valor_inm

    def es_memoria(self,operando):
        pass
    def obtener_direccion(self,variable):
        var_data = self.es_variable(variable)
        if var_data:
            return var_data['direccion']
        return None

    def obtener_tamano_variable(self, variable):
        var_data = self.es_variable(variable)
        if var_data:
            return var_data['bits']  # Retorna 8 o 16
        return None

    def calcular_desplazamiento(self,variable):
        desplazamiento = self.obtener_direccion(variable)
        if desplazamiento:
            bits_desplazamiento = bin(int(desplazamiento,16))[2:].zfill(16)
            return bits_desplazamiento
        else:
            return None

    def codificar_dos_operandos(self,instruccion,operandoDestino,operandoFuente):
        if instruccion not in r.instrucciones_2:
            return 'Instrucción no reconocida'
        
        tipos = r.decodificaciones_2[instruccion]
        tipo = None

        d = None
        mod = None
        if self.es_registro(operandoDestino) and self.es_registro(operandoFuente):
            tipo = 'Reg,Reg/Mem'
            d = '0'
        elif self.es_registro(operandoDestino) and self.es_variable(operandoFuente):
            tipo = 'Reg,Reg/Mem'
            d = '1'
        elif self.es_variable(operandoDestino) and self.es_registro(operandoFuente):
            tipo = 'Reg/Mem,Reg'
            d = '0'
        elif self.es_registro(operandoDestino) and self.es_inmediato(operandoFuente):
            tipo = 'Reg,Inm'
        else:
            return 'Tipo desconocido'

        if tipo not in tipos:
            return 'Tipo desconocido'

        if tipo == 'Reg,Inm' not in tipos:
            tipo = 'Reg/Mem,Inm'
        tipo_seleccionado =  tipos[tipo]

        w = None
        reg = None
        r_m = None
        bits_desplazamiento = None
        direccion = tipo_seleccionado['direccion']
        if tipo == 'Reg/Mem,Reg' and self.es_variable(operandoDestino):
            d = '0'
            mod = '00'
            r_m = '110'
            bits_desplazamiento = self.calcular_desplazamiento(operandoDestino)
            bits_variable = self.obtener_tamano_variable(operandoDestino)
        elif tipo == 'Reg,Reg/Mem' and self.es_registro(operandoFuente):
            d = '1'
            reg = r.registros_binarios[operandoDestino]
            mod = '11'
            if operandoDestino in r.registros_8 or operandoFuente in r.registros_8:
                w = '0'
            elif operandoDestino in r.registros_16 or operandoFuente in r.registros_16:
                w = '1'
            r_m = r.registros_binarios[operandoFuente]
        elif tipo == 'Reg,Reg/Mem' and self.es_variable(operandoFuente):
            d = '1'
            reg = r.registros_binarios[operandoDestino]
            mod = '00'
            r_m = '110'
            bits_desplazamiento = self.calcular_desplazamiento(operandoDestino)
            bits_variable = self.obtener_tamano_variable(operandoDestino)
            w = '0' if bits_variable == 8 else '1'
        elif tipo == 'Reg,Inm' and self.es_registro(operandoDestino):
            mod = '11'
            reg = r.registros_binarios[operandoDestino]
            if operandoDestino in r.registros_8:
                w = '0'
                relleno = 8
            if operandoDestino in r.registros_16:
                w = '1'
                relleno = 16
            direccion = self.codificar_inmediato(operandoFuente).zfill(relleno)

        opcode = tipo_seleccionado['opcode']
        opcode = self.reemplazar_valores(opcode,w = w,d=d, mod = mod, reg = reg, r_m = r_m)

        direccion = self.reemplazar_valores(direccion,mod = mod, reg = reg, r_m = r_m)
        if bits_desplazamiento is not None:
            direccion = f'{direccion}{bits_desplazamiento}'
        binario = f'{opcode}{direccion}'

        codificacion = hex(int(binario,2))

        return codificacion
    
    # Manejo para la tabla de simbolos
    # Instrucciones sin operandos 
    def codificar_instruccion_0(self,instruccion, pc):
        codificacion  = self.codificar_sin_operandos(instruccion)
        simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = 'NA', valor = 'NA',direccion =pc,codificacion=codificacion,tamaño='NA')
        pc = int(pc,16) + int(codificacion,16)
        return pc, simbolo

    # Instrucciones de un operando
    def codificar_instruccion_1(self,instruccion,operando,pc):
        codificacion = self.codificar_un_operando(instruccion,operando)
        nombre = f'{instruccion} {operando}'
        if codificacion == 'Tipo desconocido':
            simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = nombre, valor = 'Error: Operando desconocido',direccion =pc,
                                             codificacion=codificacion,tamaño='NA')
        elif codificacion == 'Operando no valido':
            simbolo = self.registrar_simbolo(tipo='Instruccion', simbolo=nombre, valor='Error: Operando no valido', direccion=pc,
                                             codificacion=codificacion, tamaño='NA')
        else:
            simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = nombre, valor = 'NA',direccion =pc,
                                             codificacion=codificacion,tamaño='NA')
            pc = hex(int(pc,16) + int(codificacion,16))
        return pc, simbolo

    def codificar_instruccion_2(self,instruccion,operandoDestino,operandoFuente,pc):
        codificacion = self.codificar_dos_operandos(instruccion,operandoDestino,operandoFuente)
        nombre = f'{instruccion} {operandoDestino},{operandoFuente}'
        if codificacion == 'Tipo desconocido':
            simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = nombre, valor = 'Error: Operandos no reconocidos',
                                             direccion =pc,codificacion=codificacion,tamaño='NA')
        else:
            simbolo = self.registrar_simbolo(tipo='Instruccion',simbolo = nombre, valor = 'NA',direccion =pc,codificacion=codificacion,tamaño='NA')
            pc = hex(int(pc,16) + int(codificacion,16))
        return pc, simbolo


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
