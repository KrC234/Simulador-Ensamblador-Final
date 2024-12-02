'''
Diccionario de datos:
Definicion de registros 
Definicion de instrucciones 
Palabras reservadas
codificacion de instrucciones: registros, direcciones, codigo 
'''
# Pseudoinstrucciones 
pseudoinstrucciones = {"dw","db","equ","end","ends","endp",".code",".stack",".data"}

segmentos = {".stack segment", ".data segment", ".code segment"}

# Registros 
registros_16 =  {"ax","bx","cx","dx"}

registros_8 = {"ah","al","bh","bl","ch","cl","dh","dl"}

registros_base = {"bp","sp", "si"}

# Instrucciones segun el número de operandos 

instrucciones_0 = {"aam", "aas", "iret", "lahf", "std", "sti"}
instrucciones_1 = {"int", "not", "idiv", "mul", "jo", "loop", "jna", "jnc", "jnl", "jbe"}
instrucciones_2 = {"rcl","shl","xchg", "mov"}

# Patrones para el análisis semantico 
stack_patterns = [r"^\s*dw\s+([0-9A-Fa-f]+h|\d+)\s+dup\(([-+]?\d+|‘[^’]*’)\)\s*$"]
#! Verificar operandos entre comillas 
data_patterns = [
    r"(\w+)\s+db\s+['\"]([^'\"]+)['\"]",  # Captura nombre y valor entre comillas
    r"(\w+)\s+db\s+([-+]?\d+|[0-9A-Fa-f]+h)",  # Captura nombre y valor numérico
    r"(\w+)\s+db\s+([0-9A-Fa-f]+h|\d+)\s+dup\((['\"][^'\"]+['\"]|[0-9A-Fa-f]+h|\d+)\)",  # Con DUP
    r"(\w+)\s+dw\s+([-+]?\d+|[0-9A-Fa-f]+h)",  # Captura nombre y valor numérico para DW
    r"(\w+)\s+dw\s+([0-9A-Fa-f]+h|\d+)\s+dup\((['\"][^'\"]+['\"]|[0-9A-Fa-f]+h|\d+)\)",  # DW con DUP
    r"(\w+)\s+equ\s+([-+]?\d+|[0-9A-Fa-f]+h)"
]
# Valores binarios de los registros para operandos reg o r/m 

registros_binarios = {
    'ax': '000', 'al': '000',
    'cx': '001', 'cl': '001',
    'dx': '010', 'dl': '010',
    'bx': '011', 'bl': '011',
    'sp': '100', 'ah': '100',
    'bp': '101', 'ch': '101',
    'si': '110', 'dh': '110',
    'di': '111', 'bh': '111'
}

# Decodificacion de instrucciones segun el número de operandos 

decodificaciones_0 = {
    'aam': '1101010000001010',
    'aas': '00111111',
    'iret':'11001111',
    'std': '11111101',
    'sti': '11111011',
    'lahf':'10011111'
}

# se consideran las formas del codigo base y de la direccion 
decodificaciones_1 = {
    'int':{
        'operando': 'inmediato',
        'opcode' : '1100101',
    },
    'not':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'direccion': 'mod010r/m'
    },
    'idiv':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'direccion': 'mod111r/m'
    },
    'mul':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'direccion': 'mod100r/m'
    },
    'jna':{
        'operando': 'etiqueta',
        'opcode': '0000111110000110',
        'direccion':None
    },
    'jnc':{
        'operando': 'etiqueta',
        'opcode': '0000111110000010',
        'direccion': None 
    },
    'jnl':{
        'operando': 'etiqueta',
        'opcode': '0000111110001101',
        'direccion': None
    },
    'jbe':{
        'operando': 'etiqueta',
        'opcode': '0000111110000110',
        'direccion':None
    },
    'jo':{
        'operando': 'etiqueta',
        'opcode': '0000111110000000',
        'direccion': None
    },
    'loop':{
        'operando': 'etiqueta',
        'opcode': '11100010',
        'direccion' : None 
    }
}

decodificaciones_2 = {
    'mov':{
        'Reg/Mem,Reg':{
            'opcode':'1000100w',
            'direccion':'modregr/m'
        },
        'Reg,Reg/Mem':{
            'opcode':'1000101w',
            'direccion':'modregr/m'
        },
        'Reg/Mem,Inm':{
            'opcode':'1100011w',
            'direccion':'mod000r/m'
        }
    },
    'rcl':{
        'Reg/Mem,Inm.byte':{
            'opcode': '1100000w',
            'direccion':'modTTTr/m'
        }
    },
    'xchg':{
        'Reg,Reg/Mem':{
            'opcode': '1000011w',
            'direccion': 'modregr/m'
        },
        'Acum,Reg':{
            'opcode': '10010reg',
            'direccion': None
        }
    },
    'shl':{
        'Reg/Mem,1':{
            'opcode':'1101000w',
            'direccion': 'modTTTr/m'
        }
    }
}