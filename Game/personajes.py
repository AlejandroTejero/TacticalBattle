from utils import *

class Personaje:
    def __init__(self, vida_maxima, danyo):
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima     # porque al principio las vidas estan al maximo
        self.danyo = danyo
        self.posicion = None
        self.enfriamiento_restante = 0
        self.equipo = None

    def __str__(self):
        return f'{self.__class__.__name__} esta en {self.posicion} [Vida {self.vida_actual}/{self.vida_maxima}]' #Asi se escriben todos los personajes

    def conseguir_vida_actual(self):
        return self.vida_actual

    def conseguir_posicion(self):
        return self.posicion

    def definir_posicion(self, posicion):
        self.posicion = posicion

    def definir_equipo(self, equipo):
        self.equipo = equipo

    def sigue_vivo(self):
        vivo = False
        if self.vida_actual > 0:
            vivo = True
        return vivo

    def vida_diferente_de_la_maxima(self):
        diferente = False
        if self.vida_actual != self.vida_maxima:
            diferente = True
        return diferente

    def herido(self):
        herido = False
        if self.vida_diferente_de_la_maxima() and self.sigue_vivo():
            herido = True
        return herido

    def mover(self):
        salir = False
        while not salir:
            celda = input(f'Indica la celda a la que mover al {self.__class__.__name__} (Posicion actual: {self.posicion}): ').upper()   #Indica la celda a la que mover al (Medico) (posicion actual A2:
            if validar_celda(celda, max_columna, max_fila):                     #Comprueba que la celda esté dentro del tablero
                if validar_celda_contigua(self.posicion, celda):                #Comprueba que la celda se encuentre al lado de donde estas
                    if comprobar_celda_disponible(celda, self.equipo):          #comprueba que la celda no este ocupada
                        self.posicion = celda                                   #Si cumple all la celda actual se transforma en la que te quieres mover
                        salir = True
                    else:
                        print('Ups...la celda ya está ocupada!, prueba otra vez...')
                else:
                    print('Ups...la celda es inalcanzable para la unidad!, prueba otra vez...')
            else:
                print('Ups...valor de celda incorrecto, prueba otra vez...')

    def habilidad(self):
        raise NotImplementedError

    def no_hay_enfiramiento(self):
        no_hay = False
        if self.enfriamiento_restante == 0:
            no_hay = True
        return no_hay

    def puede_usar_la_habilidad(self):
        usar = False
        if self.no_hay_enfiramiento():
            usar = True
        return usar

    def reducir_enfriamiento_habilidad(self):
        if not self.no_hay_enfiramiento():
            self.enfriamiento_restante -= 1

    def curar_personaje(self):
        self.vida_actual = self.vida_maxima

    def recibir_ataque(self, danyo):
        self.vida_actual -= danyo

    def aliado_herido(self):
        herido = False
        for personaje in self.equipo:
            if personaje.herido():
                herido = True
        return herido

class Medico(Personaje):
    vida = 1
    danyo = 0

    def __init__(self):
        super().__init__(Medico.vida, Medico.danyo)     #El super es para que la clase hija (Medico) herede el contructor de la clase padre (Personaje)

    def puede_usar_la_habilidad(self):
        puede = False
        if self.no_hay_enfiramiento() and self.aliado_herido():
            puede = True
        return puede

    def habilidad_str(self):
        return f'Curar a un compañero (Medico)'

    def habilidad(self):
        aliados_heridos = []
        for aliado in self.equipo:
            if aliado.sigue_vivo() and aliado.vida_diferente_de_la_maxima() and aliado.aliado_herido():
                aliados_heridos.append(aliado)
        for i, personaje in enumerate(aliados_heridos):
            print(f'{i + 1}: {personaje.__class__.__name__} [{personaje.vida_actual}/{personaje.vida_maxima}]')

        salir = False
        while not salir:
            try:
                i = int(input('Selecciona el personaje a curar: '))
                if 0 <= i < len(aliados_heridos):
                    aliados_heridos[i - 1].curar_personaje()
                    salir = True
                else:
                    print('...')
            except ValueError:
                print(f'Debes seleccionar un numero entre 0 y {len(aliados_heridos)}')
        self.enfriamiento_restante = 2
        return None

class Artillero(Personaje):
    vida = 2
    danyo = 1

    def __init__(self):
        super().__init__(Artillero.vida, Artillero.danyo)

    def habilidad_str(self):
        return f'Dispara en área (2x2). Daño {Artillero.danyo}. (Artillero)'        #return f'Dispara en área (2x2). Daño {Artillero.danyo}. ({Artillero.__name__}) modo pro para poner el nombre del Artillero

    def habilidad(self):
        coordenada = None
        salir = False
        while not salir:
            celda = input('Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ').upper()        #upper para transformar lo que metas en mayuscula, lower para minusculas
            if validar_celda(celda, max_columna, max_fila):
                coordenada = 'A' + celda
                salir = True
            else:
                print('Ups...valor de celda incorrecto.')
        self.enfriamiento_restante = 2
        return coordenada

class Inteligencia(Personaje):
    vida = 2
    danyo = 0

    def __init__(self):
        super().__init__(Inteligencia.vida, Inteligencia.danyo)

    def habilidad_str(self):
        return f'Revelar a los enemigos en un area 2x2. (Inteligencia)'     #({Inteligencia.__name__})

    def habilidad(self):
        coordenada = None
        salir = False
        while not salir:
            celda = input('Indica las coordenadas de la esquina superior izquierda de la zona de observación (área 2x2): ').upper()
            if validar_celda(celda, max_columna, max_fila):
                coordenada = 'I' + celda
                salir = True
            else:
                print('Ups...valor de celda incorrecto.')
        self.enfriamiento_restante = 2
        return coordenada

class Francotirador(Personaje):
    vida = 3
    danyo = 3

    def __init__(self):
        super().__init__(Francotirador.vida, Francotirador.danyo)

    def habilidad_str(self):
        return f'Dispara a una celda. Daño {Francotirador.danyo}. (Francotirador)'  # ({Francotirador.__name__})

    def habilidad(self):
        coordenada = None
        salir = False
        while not salir:
            celda = input('Indica las coordenadas de la celda a la que disparar: ').upper()
            if validar_celda(celda, max_columna, max_fila):
                coordenada = 'F' + celda
                salir = True
            else:
                print('Ups...valor de celda incorrecto.')
        self.enfriamiento_restante = 2
        return coordenada
