# Proyecto Final de ensambladores 
## Equipo 6

+ Aalan Kalid Ruíz Colín 
+ Daniel García Urbina
+ Juan Luis Gamboa 

El proyecto conjunta las 3 fases de simular un ensamblador, dónde se cuentan con las siguientes 3 fases:
+ Separación de instrucciones 
+ Detección de errores 
+ Tabla de simbolos (Contador de programa)

De modo que se han repartido en modulos para su trabajo individual de cada fase, asimismo se agregan los modulos de Recursos y Archivos, con el fin de optimizar el uso y manejo de los recursos (archivos ens)

Dónde por parte de los recursos se identifican los registros que conforman el ens, las pseudoinstrucciones, y las instrucciones correspondientes, clasificados por la cantidad de operandos que estás necesitan. 

__Instrucciones:__
Sin operandos: AAM, AAS, IRET, LAHF, STD, STI
De un operando: INT, NOT, IDIV, MUL, JO, LOOP
De dos operandos: RCL, SHL, XCHG, MOV, JNA, JNC, JNL, JBE
