import re
import Recursos as r
import Fase3
class Validacion:

    def __init__(self):
        self.pc = '0x250'
        self.lista_de_simbolos = []
        self.variables = []
        self.etiquetas = []
        self.f3 = Fase3.Codificacion(self.variables,self.etiquetas)
        self.lineas_contador = []

    # Tratamiento semantico


    def verificar_en_stack(self,linea):
        for exp in r.stack_patterns:
            if re.match(exp,linea.strip()):
                self.pc = hex(int(self.pc,16)+int('0x100',16))
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

    def verificar_tamaño(self,etiqueta):
        if len(etiqueta) < 10:
            return True
        return False

    def es_String(self, valor):
        # Expresión regular para detectar cadenas entre:
        # - Comillas simples: 'ejemplo'
        # - Comillas dobles: "ejemplo"
        # - Comillas dobles curvadas: “ejemplo” o ”ejemplo”
        patron = r"""^(?:'[^']*'|"[^"]*"|“[^”]*”|”[^”]*”)$"""

        # Validar el valor contra el patrón
        if isinstance(valor, str) and re.match(patron, valor):
            return True
        return False

    def verificar_en_data(self, linea):
        for exp in r.data_patterns:
            match = re.match(exp, linea.strip())
            if match:
                tipo = ''
                bits = 0
                nombre = linea.split()[0]
                valor = match.group(2)
                if not self.verificar_tamaño(nombre):
                    return False

                if self.es_variable_registrada(nombre):
                    print(f"Error: La variable '{nombre}' ya está registrada.")
                    return False

                if 'b' in valor and not self.es_binario(valor):
                    return False

                if self.es_inmediato(valor):
                    codificacion = self.codificar_inmediato(valor)# El valor con 'h' (si lo tiene)
                    print(f"Valor detectado: {valor},Codificacion : {codificacion}")
                else:
                    codificacion = None

                tamaño =  None
                # Determinar el tamaño en función del tipo de variable
                if 'db' in linea:
                    if codificacion is not None:
                        if len(codificacion) > 8:
                            return False
                    if self.es_String(valor):
                        tamaño = len(valor)
                    else:
                        tamaño = 1
                    tipo = 'Variable de 8 bits'
                    bits = 8
                elif 'dw' in linea:
                    if codificacion is not None:
                        if len(codificacion) > 16:
                            return False
                    if self.es_String(valor):
                        tamaño = len(valor) * 2
                    else:
                        tamaño = 2
                    tipo = 'Variable de 16 bits'
                    bits = 16

                # Registrar el símbolo y la variable sin modificar el valor
                self.registrar_simbolo(nombre, tipo=tipo, valor=valor, direccion=self.pc,
                                       tamaño=tamaño)
                self.registrar_variable(nombre, valor, bits,self.pc)
                self.pc = hex(int(self.pc, 16) + tamaño)  # Actualizar la dirección del contador de programa
                return True
        return False

    def es_binario(self, valor):
        # Solo acepta 0 y 1 antes de la "b" final
        if re.match(r'^[01]+b$', valor, re.IGNORECASE):  # Ignora mayúsculas/minúsculas en 'b'
            return True
        return False

    def es_variable_registrada(self, nombre):
        # Implementar la lógica para verificar si el nombre ya existe en el registro de variables
        return any(var['variable'] == nombre for var in self.variables)
    
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
        etiq = {
            'etiqueta': etiqueta,
            'direccion': self.pc
        }
        self.etiquetas.append(etiq)

    def registrar_simbolo(self, simbolo, tipo, valor =  None,direccion = None, tamaño = None):
        simbolo = {
            'nombre' : simbolo, 
            'tipo' : tipo,
            'valor': valor,
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
        elif operando1 in r.registros_16 and self.es_inmediato(operando2):
            valor_inm = ''
            if re.match(r'^[0-9A-Fa-f]+h$', operando2):
                valor_inm = bin(int(operando2[:-1],16))[2:]
            elif re.match(r'^[0-9]+d$', operando2):
                valor_inm = bin(int(operando2[:-1]))
            if len(valor_inm) <= 16:
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
        elif operando in [variable['variable'] for variable in self.variables]:
            return True
        elif self.es_inmediato(operando):
            return True
        elif operando in [etiqueta['etiqueta'] for etiqueta in self.etiquetas]:
            return True
        return False 

    def validar_linea(self,linea):
        if ":" in linea:
            etiqueta = linea.split(':')[0].strip()
            if not self.verificar_tamaño(etiqueta):
                return 'Error: El tamaño excede el limite'
            self.registrar_simbolo(simbolo = etiqueta,tipo = 'etiqueta',direccion = self.pc)
            self.registrar_etiqueta(etiqueta)
            return 'Correcto'

        # instrucciones de dos operandos 
        match_dos = re.match(r"^\s*(\w+)\s+(\w+),\s*(\w+)$", linea.strip()) 
        codificacion_dos = None
        if match_dos:
            instruccion, operandoDestino, operandoFuente = match_dos.groups()
            if not self.validar_instruccion(instruccion, r.instrucciones_2):
                return f'Error: {instruccion} no es una instruccion de dos operandos'
            
            if not self.validar_operandos(operandoDestino,operandoFuente):
                return f'Error: {operandoDestino} y {operandoFuente} no son compatibles o validos'

            self.pc, codificacion_dos = self.f3.codificar_instruccion_2(instruccion,operandoDestino,operandoFuente,self.pc)
            return codificacion_dos
                
        # instrucciones de un operando 
        match_uno = re.match(r"^\s*(\w+)\s+(\w+)$", linea.strip())
        if match_uno:
            instruccion, operando =  match_uno.groups()

            if not self.validar_instruccion(instruccion,r.instrucciones_1):
                return f'Error: {instruccion} no es de un operando'
            if not self.validar_operando(operando):
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
                        return f'Error: el operando {operando} no es compatible con la instruccion'
                    else:
                        self.pc, codificacion_1 = self.f3.codificar_instruccion_1(instruccion, operando, self.pc)
                        return codificacion_1
            self.pc, codificacion_1 = self.f3.codificar_instruccion_1(instruccion,operando,self.pc)
            return codificacion_1
        
        # instrucciones sin operando 
        if re.match(r"^\s*(\w+)\s*$", linea.strip()):
            instruccion = linea.strip()
            if self.validar_instruccion(instruccion,r.instrucciones_0):
                self.pc, codificacion_0 = self.f3.codificar_instruccion_0(instruccion, self.pc)
                return codificacion_0
            else:
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
            self.lineas_contador.append(f'{self.pc}   -   {linea}')
            if linea in r.segmentos:
                segmento_activo = True
                self.pc = '0x250'
                resultados.append(self.retornar_segmento(linea))
            elif linea == 'ends':
                resultados.append('Fin de segmento')
                segmento_activo = False 
            else:
                resultados.append(self.analizar_linea(linea,segmento_activo))
        return resultados

    def retornar_lineas(self):
        return self.lineas_contador


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