import re
import Recursos as r
class Validacion:

    def __init__(self):
        self.pc = hex(0)
        self.lista_de_simbolos = []
        self.variables = []
        self.etiquetas = []

    # Tratamiento semantico 

    def verificar_en_stack(self,linea):
        for exp in r.stack_patterns:
            if re.match(exp,linea.strip()):
                return True
        return False 
    
    def verificar_en_data(self,linea):
        for exp in r.data_patterns:
            match = re.match(exp,linea.strip())
            if match:
                nombre = linea.split()[0]
                valor = match.group(2)
                tamaño =  len(valor)
                self.registrar_simbolo(nombre,tipo='Variable',valor=valor,direccion=self.pc,codificacion='NA',tamaño = tamaño)
                return True
        return False 
    
    #* Registro de variables y etiquetas
    def registrar_variable(self,variable,valor):
        variable = {
            'variable': variable, 
            'valor': valor 
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
        
    def validar_operandos(self,operando1,operando2):

        if operando1 in r.registros_8 and operando2 in r.registros_8:
            return True
        elif operando1 in r.registros_16 and operando2 in r.registros_16:
            return True
        elif operando1 in r.registros_base and operando2 in r.registros_base:
            return True
        elif operando1 in [var['variable'] for var in self.variables] and operando2 in [var['variable'] for var in self.variables]:
            return True
        elif(re.match(r"^\d+$", operando2) or re.match(r"^[0-9A-Fa-f]+h$", operando2)) and (
                operando1 in r.registros_16 or operando1 in r.registros_8):
            return True
        return False 

    def validar_operando(self,operando):
        if self.validar_registro(operando):
            return True
        elif operando in [etiqueta for etiqueta in self.etiquetas]:
            return True
        elif operando in [variable['variable'] for variable in self.variables]:
            return True 
        return False 

    def validar_linea(self,linea):
        if ':' in linea:
            etiqueta = linea.split(':')[0].strip
            self.registrar_etiqueta(etiqueta)

        # instrucciones de dos operandos 
        match_dos = re.match(r"^\s*(\w+)\s+(\w+),\s*(\w+)$", linea.strip()) 
        if match_dos:
            instruccion, operandoDestino, operandoFuente = match_dos.groups()
            if not self.validar_instruccion(instruccion, r.instrucciones_2):
                return f'Error: {instruccion} no es una instruccion de dos operandos'
            
            if not self.validar_operandos(operandoDestino,operandoFuente):
                return f'Error: {operandoDestino} y {operandoFuente} no son compatibles o validos'
            
            return 'Correcta'
        
        # instrucciones de un operando 
        match_uno = re.match(r"^\s*(\w+)\s+(\w+)$", linea.strip())
        if match_uno:
            instruccion, operando =  match_uno.groups()
            if not self.validar_instruccion(instruccion,r.instrucciones_1):
                return f'Error: {instruccion} no es de un operando'
            if not self.validar_operando(operando):
                return f'Error: {operando} no es valido'
            return 'Correcta'
        
        # instrucciones sin operando 
        if re.match(r"^\s*(\w+)\s*$", linea.strip()):
            instruccion = linea.strip()
            if self.validar_instruccion(instruccion,r.instrucciones_0):
                return 'Correcta'
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

            if linea in r.segmentos:
                segmento_activo = True
                resultados.append(self.retornar_segmento(linea))
            elif linea == 'ends':
                resultados.append('{linea} - Fin de segmento')
                segmento_activo = False 
            else: 
                resultados.append(self.analizar_linea(linea,segmento_activo))
        return resultados
    def analisis_final(self,lineas):
        resultados = self.analizar_lineas(lineas)
        return resultados, self.lista_de_simbolos
    
    def retornar_segmento(self,linea):
        if linea == '.stack segment':
            return f'{linea} - Segmento de Pila'
        elif linea == '.data segment':
            return f'{linea} - Segmento de Datos'
        elif linea == '.code segment':
            return f'{linea} - Segmento de Codigo'