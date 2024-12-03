import re
import Recursos as r
import Fase3
class Validacion:

    def __init__(self):
        self.pc = hex(0)
        self.lista_de_simbolos = []
        self.variables = []
        self.etiquetas = []
        self.f3 = Fase3.Codificacion(self.variables,self.etiquetas)

    # Tratamiento semantico


    def verificar_en_stack(self,linea):
        for exp in r.stack_patterns:
            if re.match(exp,linea.strip()):
                return True
        return False

    def es_inmediato(self,operando):
        if re.match(r'^[0-9A-Fa-f]+h$',operando):
            return True
        elif re.match(r'^[0-9]+d$', operando):
            return True
        elif re.match(r'^\d+$',operando):
            return True
        return False

    def codificar_inmediato(self,operando):
        valor_inm = ''
        if re.match(r'^[0-9A-Fa-f]+h$', operando):
            valor_inm = bin(int(operando[:-1], 16))[2:]
        elif re.match(r'^[0-9]+d$', operando):
            valor_inm = bin(int(operando[:-1]))[2:]
        elif re.match(r'^\d+$', operando):
            valor_inm = bin(int(operando))[2:]
        return valor_inm

    def verificar_en_data(self, linea):
        for exp in r.data_patterns:
            match = re.match(exp, linea.strip())
            if match:
                tipo = ''
                bits = 0
                nombre = linea.split()[0]
                valor = match.group(2)
                if self.es_inmediato(valor):
                    codificacion = self.codificar_inmediato(valor)# El valor con 'h' (si lo tiene)
                    print(f"Valor detectado: {valor},Codificacion : {codificacion}")
                else:
                    codificacion = None

                # Determinar el tamaño en función del tipo de variable
                tamaño = len(valor)  # Tamaño en base a los caracteres (sin modificar el valor)
                if 'db' in linea:
                    if codificacion is not None:
                        if len(codificacion) > 8:
                            return False

                    tipo = 'Variable de 8 bits'
                    bits = 8
                elif 'dw' in linea:
                    if codificacion is not None:
                        if len(codificacion) > 16:
                            return False
                    tipo = 'Variable de 16 bits'
                    bits = 16

                # Registrar el símbolo y la variable sin modificar el valor
                self.registrar_simbolo(nombre, tipo=tipo, valor=valor, direccion=self.pc, codificacion='NA',
                                       tamaño=tamaño)
                self.registrar_variable(nombre, valor, bits,self.pc)
                self.pc = hex(int(self.pc, 16) + tamaño)  # Actualizar la dirección del contador de programa
                return True
        return False
    
    #* Registro de variables y etiquetas
    def registrar_variable(self,variable,valor,bits,direccion):
        variable = {
            'variable': variable, 
            'valor': valor,
            'bits': bits,
            'direccion':direccion
        }
        self.variables.append(variable)

    def registrar_etiqueta(self,etiqueta):
        self.etiquetas.append(etiqueta)

    def registrar_simbolo(self, simbolo, tipo, valor =  None,direccion = None, codificacion = None, tamaño = None):
        simbolo = {
            'nombre' : simbolo, 
            'tipo' : tipo,
            'valor': valor,
            'codificacion': codificacion,
            'tamaño': tamaño,
            'direccion': direccion,
        }
        self.lista_de_simbolos.append(simbolo)
        
    '''
    Tratamiento del code segment 
    Se requiere validar los registros
    Los operandos
    Etiquetas
    '''

    def validar_instruccion(self,instruccion,instrucciones):
        if instruccion in instrucciones:
            return True
        else:
            return False 
        
    def validar_registro(self,operando):
        if operando in r.registros_8:
            return True
        if operando in r.registros_16:
            return True
        if operando in r.registros_base:
            return True
        return False

    def es_inmediato(self,operando):
        if re.match(r'^[0-9A-Fa-f]+h$',operando):
            return True
        elif re.match(r'^[0-9]+d$', operando):  # Decimal
            return True
        return False

    def validar_operandos(self,operando1,operando2):

        if operando1 in r.registros_8 and operando2 in r.registros_8:
            return True
        elif operando1 in r.registros_16 and operando2 in r.registros_16:
            return True
        elif operando1 in r.registros_base and operando2 in r.registros_base:
            return True
        elif operando1 in [var['variable'] for var in self.variables] and operando2 in [var['variable'] for var in self.variables]:
            return True
        elif operando1 in r.registros_8 and self.es_inmediato(operando2):
            valor_inm = ''
            if re.match(r'^[0-9A-Fa-f]+h$', operando2):
                valor_inm = bin(int(operando2[:-1],16))[2:]
            elif re.match(r'^[0-9]+d$', operando2):
                valor_inm = bin(int(operando2[:-1]))
            if len(valor_inm) <= 8:
                return True
        elif operando1 in [var['variable'] for var in self.variables] and operando2 in [var['variable'] for var in
                                                                     self.variables]:
            # Si ambos operandos son variables y tienen el mismo tamaño, son válidos
            var1 = next(var for var in self.variables if var['variable'] == operando1)
            var2 = next(var for var in self.variables if var['variable'] == operando2)
            if var1['bits'] == var2['bits']:
                return True
        elif operando1 in r.registros_8:
            if operando2 in [var['variable'] for var in self.variables]:
                var2 = next(var for var in self.variables if var['variable'] == operando2)
                if var2['bits'] == 8:
                    return True
        elif operando2 in r.registros_8:
            if operando1 in [var['variable'] for var in self.variables]:
                var1 = next(var for var in self.variables if var['variable'] == operando1)
                if var1['bits'] == 8:
                    return True
        elif operando1 in r.registros_16:
            if operando2 in [var['variable'] for var in self.variables]:
                var2 = next(var for var in self.variables if var['variable'] == operando2)
                if var2['bits'] == 16:
                    return True
        elif operando2 in r.registros_16:
            if operando1 in [var['variable'] for var in self.variables]:
                var1 = next(var for var in self.variables if var['variable'] == operando1)
                if var1['bits'] == 16:
                    return True

        return False 

    def validar_operando(self,operando):
        if self.validar_registro(operando):
            return True
        elif operando in [etiqueta for etiqueta in self.etiquetas]:
            return True
        elif operando in [variable['variable'] for variable in self.variables]:
            return True
        elif self.es_inmediato(operando):
            return True
        return False 

    def validar_linea(self,linea):
        if ":" in linea:
            etiqueta = linea.split(':')[0].strip()
            self.registrar_simbolo(simbolo = etiqueta,tipo = 'etiqueta',direccion = self.pc)
            self.registrar_etiqueta(etiqueta)
            return 'Correcto'

        # instrucciones de dos operandos 
        match_dos = re.match(r"^\s*(\w+)\s+(\w+),\s*(\w+)$", linea.strip()) 
        codificacion_dos = None
        if match_dos:
            instruccion, operandoDestino, operandoFuente = match_dos.groups()
            if not self.validar_instruccion(instruccion, r.instrucciones_2):
                self.registrar_simbolo(linea, tipo='NA', direccion=self.pc, codificacion='Error: Instruccion no valida',
                                       tamaño='NA')
                return f'Error: {instruccion} no es una instruccion de dos operandos'
            
            if not self.validar_operandos(operandoDestino,operandoFuente):
                self.registrar_simbolo(linea, tipo='NA', direccion=self.pc, codificacion='Error: Operandos no validos',
                                       tamaño='NA')
                return f'Error: {operandoDestino} y {operandoFuente} no son compatibles o validos'

            self.pc, codificacion_dos = self.f3.codificar_instruccion_2(instruccion,operandoDestino,operandoFuente,self.pc)
            self.lista_de_simbolos.append(codificacion_dos)
            return 'Correcta'
                
        # instrucciones de un operando 
        match_uno = re.match(r"^\s*(\w+)\s+(\w+)$", linea.strip())
        if match_uno:
            instruccion, operando =  match_uno.groups()

            if not self.validar_instruccion(instruccion,r.instrucciones_1):
                self.registrar_simbolo(linea, tipo='NA', direccion=self.pc, codificacion='Error: Instruccion no valida',
                                       tamaño='NA')
                return f'Error: {instruccion} no es de un operando'
            if not self.validar_operando(operando):
                self.registrar_simbolo(linea, tipo='NA', direccion=self.pc, codificacion='Error: Operando no valido',
                                       tamaño='NA')
                return f'Error: {operando} no es valido'
            # TODO: Caso especial dado que la instruccion Int no acepta inmediatos mayores a 8 bits
            valor_inm = None
            if self.es_inmediato(operando):
                if re.match(r'^[0-9A-Fa-f]+h$', operando):
                    valor_inm = bin(int(operando[:-1], 16))[2:]
                elif re.match(r'^[0-9]+d$', operando):
                    valor_inm = bin(int(operando[:-1]))
                if instruccion.lower() == 'int':
                    if len(valor_inm) > 8:
                        self.registrar_simbolo(linea, tipo='NA', direccion=self.pc,
                                               codificacion='Error: Valor no soportado',
                                               tamaño='NA')
                        return f'Error: el operando {operando} excede los 8 bits permitidos para la instrucción INT'
                    else:
                        self.pc, codificacion_1 = self.f3.codificar_instruccion_1(instruccion, operando, self.pc)
                        self.lista_de_simbolos.append(codificacion_1)
                        return 'Correcta'
            self.pc, codificacion_1 = self.f3.codificar_instruccion_1(instruccion,operando,self.pc)
            self.lista_de_simbolos.append(codificacion_1)
            return 'Correcta'
        
        # instrucciones sin operando 
        if re.match(r"^\s*(\w+)\s*$", linea.strip()):
            instruccion = linea.strip()
            if self.validar_instruccion(instruccion,r.instrucciones_0):
                self.pc, codificacion_0 = self.f3.codificar_instruccion_0(instruccion, self.pc)
                self.lista_de_simbolos.append(codificacion_0)
                return 'Correcta'
            else:
                self.registrar_simbolo(linea,tipo = 'NA', direccion = self.pc, codificacion = 'Error: Instruccion no valida',
                                       tamaño = 'NA')
                return f'Error: {instruccion} no es una instruccion valida'
        return 'Error de declaracion'

    def analizar_linea(self,linea,segmento_activo):
        if not segmento_activo:
            return 'Error: Linea fuera de segmento'
        if self.verificar_en_stack(linea):
            return 'Correcta'
        elif self.verificar_en_data(linea):
            return 'Correcta'
        elif segmento_activo:
            return self.validar_linea(linea)
        else:
            return 'Declaracion incorrecta o desconocida'

    def analizar_lineas(self,lineas):
        resultados = []

        segmento_activo = False

        for linea in lineas:

            if linea in r.segmentos:
                segmento_activo = True
                self.pc = '0x100'
                resultados.append(self.retornar_segmento(linea))
            elif linea == 'ends':
                resultados.append('Fin de segmento')
                segmento_activo = False 
            else:
                resultados.append(self.analizar_linea(linea,segmento_activo))
        return resultados
    def analisis_final(self,lineas):
        resultados = self.analizar_lineas(lineas)
        return resultados, self.lista_de_simbolos
    
    def retornar_segmento(self,linea):
        if linea == '.stack segment':
            return f'Segmento de Pila'
        elif linea == '.data segment':
            return f'Segmento de Datos'
        elif linea == '.code segment':
            return f'Segmento de Codigo'