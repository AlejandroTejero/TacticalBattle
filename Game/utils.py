min_columna = 'A'
max_columna = 'D'
min_fila = '1'
max_fila = '4'
longitud_celda = 2


def limpiar_terminal():
    print(chr(27) + '[2J')

def validar_celda(celda, max_column, max_row):
    celda_en_tablero = False
    if len(celda) == longitud_celda:
        columna = celda[0]
        fila = celda[1]
        if min_columna <= columna <= max_column and min_fila <= fila <= max_row:
            celda_en_tablero = True
    return celda_en_tablero

def comprobar_celda_disponible(celda, equipo):
    celda_vacia = True
    for personaje in equipo:
        if personaje.conseguir_posicion() == celda:
            celda_vacia = False
    return celda_vacia

def validar_celda_contigua(celda1, celda2):
    columna1 = celda1[0]
    fila1 = celda1[1]
    columna2 = celda2[0]
    fila2 = celda2[1]
    return ((ord(columna2) - ord(columna1)) == 0 and abs(ord(fila2) - ord(fila1)) == 1) or \
    (abs(ord(columna2) - ord(columna1)) == 1 and (ord(fila2) - ord(fila1)) == 0)

def area2x2(celda):
    resultado = [celda]                                 #Superior izquierda

    celda_aux = chr(ord(celda[0]) + 1) + celda[1]       #Superior derecha
    if validar_celda(celda_aux, max_columna, max_fila):
        resultado.append(celda_aux)

    celda_aux = celda[0] + chr(ord(celda[1]) + 1)       #Inferior izquierda
    if validar_celda(celda_aux, max_columna, max_fila):
        resultado.append(celda_aux)

    celda_aux = chr(ord(celda[0]) + 1) + chr(ord(celda[1]) + 1)     #Inferior derecha
    if validar_celda(celda_aux, max_columna, max_fila):
        resultado.append(celda_aux)

    return resultado
