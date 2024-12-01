import re
import Recursos as r
class Validacion:

    def __init__(self):
        self.pc = hex(0)
        self.lista_de_simbolos = []

    # !Voy a omitir de momento el tratamiento de segmentos para tratarlos de mejor manera


    # Tratamiento semantico 

    def verificar_en_stack(self,linea):
        for exp in r.stack_patterns:
            if re.match(exp,linea.strip()):
                return True
        return False 
    
    def verificar_en_data(self,linea):
        for exp in r.data_patterns:
            if re.match(exp,linea.strip()):
                return True
        return False 
    

    '''
    Tratamiento del code segment 
    Se requiere validar los registros
    Los operandos
    Etiquetas
    '''

    