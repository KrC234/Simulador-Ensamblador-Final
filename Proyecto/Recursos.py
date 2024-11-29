'''
Definición de palabras reservadas 
Definición de diccionario de datos 
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
instrucciones_1 = {"int", "not", "idiv", "mul", "jo", "loop"}
instrucciones_2 = {"rcl","shl","xchg", "mov", "jna", "jnc", "jnl", "jbe"}

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

# La mayoría de instrucciones cuentan con una dirección de mod reg r/m
decodificaciones_1 = {
    'int':{
        'operando': 'inmediato',
        'opcode' : '1100101',
    },
    'not':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'mod' : None, 
        'reg' : '010',
        'r/m' : None
    },
    'idiv':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'mod' : None,
        'reg' : '111',
        'r/m' : None
    },
    'mul':{
        'operando': 'reg/mem',
        'opcode' : '1111011w',
        'mod' : None,
        'reg' : '100',
        'r/m' : None
    }
}

decodificaciones_2 = {

}