# Definicion de las palabras reservadas para el análisis del codigo 

# Pseudoinstrucciones 
pseudoinstrucciones = {"dw","db","equ","end","ends",".code",".stack",".data"}

# Registros 
registros_16 =  {"ax","bx","cx","dx"}

registros_8 = {"ah","al","bh","bl","ch","cl","dh","dl"}

registros_base = {"bp","sp"}

# Instrucciones segun el número de operandos 

instrucciones_0 = {"aam", "aas", "iret", "lahf", "std", "sti"}
instrucciones_1 = {"int", "not", "idiv", "mul", "jo", "loop"}
instrucciones_2 = {"rcl","shl","xchg", "mov", "jna", "jnc", "jnl", "jbe"}