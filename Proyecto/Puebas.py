import Archivos as a
import Fase1 as separacion

arch = a.Archivo()

ruta = "C:\emu8086\MySource\suma_matrices2.asm"
contenido = arch.procesar_archivo(ruta)

sep = separacion.Separacion()

elementos = sep.clasificar_tokens(contenido)

for i, (simbolo, tipo) in enumerate(elementos, start=1):
    print(f"{i}. {simbolo} - {tipo}")
