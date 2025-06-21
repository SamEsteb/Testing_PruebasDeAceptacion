import os

def generar_arbol_directorio(ruta_directorio, nombre_archivo_salida="arbol_directorio.txt"):
    """
    Genera un archivo de texto con la estructura de árbol de un directorio,
    ignorando directorios específicos y archivos específicos.

    Args:
        ruta_directorio (str): La ruta del directorio del cual se generará el árbol.
        nombre_archivo_salida (str): El nombre del archivo de texto de salida.
    """
    directorios_a_ignorar = ['.git', '__pycache__']
    archivos_a_ignorar = [nombre_archivo_salida, 'directorio.py'] 

    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            for raiz, directorios, archivos in os.walk(ruta_directorio):
                directorios[:] = [d for d in directorios if d not in directorios_a_ignorar]

                if any(ignorado in os.path.basename(raiz) for ignorado in directorios_a_ignorar):
                    continue 

                nivel = raiz.replace(ruta_directorio, '').count(os.sep)
                indentacion = '    ' * nivel
                f.write(f'{indentacion}[D] {os.path.basename(raiz)}/\n')

                for archivo in archivos:
                    if archivo not in archivos_a_ignorar: # Ignorar archivos específicos
                        f.write(f'{indentacion}    [A] {archivo}\n')

        print(f"El árbol del directorio se ha guardado en '{nombre_archivo_salida}'")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    directorio_a_escanear = '.'
    generar_arbol_directorio(directorio_a_escanear)