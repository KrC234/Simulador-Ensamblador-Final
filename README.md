# Proyecto Final: Simulador de un ensamblador
## Equipo: 6

__Autores:__ 
+ Aalan Kalid Ruíz Colín 
+ Daniel García Urbina
+ Juan Luis Gamboa 

El proyecto conjunta las 3 fases de simular un ensamblador, dónde se cuentan con las siguientes 3 fases:
+ Separación de instrucciones: Separa las instrucciones por tipo, y designa el tipo de simbolos.
+ Detección de errores y tabla de simbolos: Análisis semantico y sintactico sobre la codificacion de pila, datos y código, además agrega variables y etiquetas a la tabla de simbolos para su uso posterior.  
+ Codificacion de instrucciones: Codifica las instrucciones haciendo uso de su codigo base, así cómo la direccion.

Para la realización del proyecto se considera la siguiente base de instrucciones. 
__Instrucciones:__
+ Sin operandos: AAM, AAS, IRET, LAHF, STD, STI
+ De un operando: INT, NOT, IDIV, MUL, JO, LOOP, JNA, JNC, JNL, JBE
+ De dos operandos: RCL, SHL, XCHG, MOV

__Consideraciones Adicionales:__
+ Se eliminan lineas de comentarios y espacios en blanco.
+ El sistema solo reconoce archivos con extensión '.ens'.
+ Al detectar errores, retorna el tipo de error encontrado.
+ Instrucciones de salto unicamente reconocen saltos hacía atrás.

__Estructura del programa:__

El programa para la realización se construyo de la siguiente manera:
+ Tratamiento de archivos: Carga y procesa el código fuente, filtrando comentarios y espacios en blanco. 
+ Diccionario de datos: Define recursos globales cómo clasificación de registros, instrucciones, reglas de sintaxis y codificaciones. 
+ Clases individuales: Cada fase se trabaja de manera autonoma, unicamente compartiendo recursos globales. 


