# Definicion de las palabras reservadas para el análisis del codigo 

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

# Decodificacion de instrucciones segun el número de operandos 

decodificaciones_0 = {
    'aam': '1101010000001010',
    'aas': '00111111',
    'iret':'11001111',
    'std': '11111101',
    'sti': '11111011',
    'lahf':'10011111'
}

decodificaciones_1 = {

}

decodificaciones_2 = {
    
}