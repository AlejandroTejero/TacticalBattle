from personajes import *
from utils import *

class Jugador:
    personajes = [Medico, Artillero, Francotirador, Inteligencia]
    no_militar = 3
    militar = 2

    def __init__(self):
        self.equipo = []
        self.informe = " "

        self.crear_equipo()     #estamos llamando a la accion crear equipo(), ya que lleva los ()
        self.colocar_equipo()

    def vivos(self):
        return len([personaje for personaje in self.equipo if personaje.sigue_vivo()])

    def muertos(self):
        return len([personaje for personaje in self.equipo if not personaje.sigue_vivo()])

    def crear_equipo(self):
        for tipo_personaje in Jugador.personajes:
            personaje = tipo_personaje()
            personaje.definir_equipo(self.equipo)
            self.equipo.append(personaje)


    def situacion_equipo(self):
        print('---SITUACION EQUIPO---')
        for personaje in self.equipo:
            if personaje.vida_actual > 0:
                print(personaje)            #print(f"{i+1}:{aliado._class.name_}...
        print()

    def actualizar_enfriamientos(self):
        for personaje in self.equipo:
            personaje.reducir_enfriamiento_habilidad()         #Lo pondremos a 2. Primero resta el turno que no puedes usarlo (1),
                                                       # y luego resta para que puedas usarlo (0)
    def turno(self):
        if self.informe != "":
            print("---INFORME---")
            print(self.informe)

        self.situacion_equipo()
        self.actualizar_enfriamientos()
        codigo_accion = self.realizar_accion()
        return codigo_accion

    def mostrar_acciones(self):  #Mostrar las elecciones de accion (elegir accion) con un return de la variable accion
        accion = None
        ok = False
        while not ok:
            n_accion = 0
            for personaje in self.equipo:
                if personaje.sigue_vivo():
                    n_accion += 1
                    print(f"{n_accion}: Mover ({personaje.__class__.__name__})")
                    if personaje.puede_usar_la_habilidad():
                        n_accion += 1
                        print(f"{n_accion}: {personaje.habilidad_str()}")
            try:
                accion = int(input("Seleciona la accion de este turno: "))
                if 1 <= accion <= n_accion:
                    ok = True
            except ValueError:
                print(f"Debes indicar una habilidad entre 1 y {n_accion}")
        return accion

    def realizar_accion(self):
        accion = self.mostrar_acciones() #aqui te muestra las acciones que puedes realizar por terminal
        # realizar
        codigo_accion = None
        n_accion = 0
        for personaje in self.equipo:
            if personaje.sigue_vivo():
                n_accion += 1
                if accion == n_accion:
                    codigo_accion = personaje.mover()
                    break
                else:
                    if personaje.puede_usar_la_habilidad():
                        n_accion += 1
                        if accion == n_accion:
                            codigo_accion = personaje.habilidad()
                            break
        return codigo_accion

    def recibir_accion(self, codigo_accion):
        informe = ""
        resultado = None

        def procesar_otro_personaje(celda):
            nonlocal informe
            for personaje in self.equipo:
                if personaje.sigue_vivo() and personaje.conseguir_posicion() == celda:
                    personaje.recibir_ataque(Francotirador.danyo)
                    if personaje.sigue_vivo():
                        informe = (f"{personaje.__class__.__name__} ha sido herido en {personaje.conseguir_posicion()} "
                                   f"[Vida restante: {personaje.conseguir_vida_actual()}]")
                    else:
                        informe = f"{personaje.__class__.__name__} ha sido eliminado"
                    informe += "\n"
            if informe == "":
                informe = "Ningún personaje ha sido herido\n"


        def procesar_inteligencia(celda):
            nonlocal informe
            celdas_afectadas = area2x2(celda)
            for personaje in self.equipo:
                if personaje.sigue_vivo() and personaje.conseguir_posicion() in celdas_afectadas:
                    informe += f"{personaje.__class__.__name__} ha sido avistado en {personaje.conseguir_posicion()}\n"
            if informe == "":
                informe = "Ningún personaje ha sido revelado\n"

        def procesar_artillero(celda):
            nonlocal informe
            celdas_afectadas = area2x2(celda)
            for personaje in self.equipo:
                if personaje.sigue_vivo() and personaje.conseguir_posicion() in celdas_afectadas:
                    personaje.recibir_ataque(Artillero.danyo)
                    if personaje.sigue_vivo():
                        informe += (
                            f"{personaje.__class__.__name__} ha sido herido en {personaje.conseguir_posicion()} "
                            f"[Vida restante: {personaje.conseguir_vida_actual()}]")
                    else:
                        informe += f"{personaje.__class__.__name__} ha sido eliminado"
                    informe += "\n"
            if informe == "":
                informe = "Ningún personaje ha sido herido\n"

        if codigo_accion:
            inicial_personaje = codigo_accion[0]
            celda = codigo_accion[1:]

            if inicial_personaje == Artillero.__name__[0]:
                procesar_artillero(celda)
            elif inicial_personaje == Inteligencia.__name__[0]:
                procesar_inteligencia(celda)
            else:
                procesar_otro_personaje(celda)

        resultado = {'informe': informe, 'terminada': not self.quedan_militares_con_vida()}

        self.informe = informe
        return resultado

    '''def recibir_accion(self, codigo_accion):
        informe = ""
        resultado = None
        if codigo_accion:
            inicial_personaje = codigo_accion[0]
            celda = codigo_accion[1]
            if inicial_personaje == Artillero.__name__[0]:
                celdas_afectadas = area2x2(celda)
                for personaje in self.equipo:
                    if personaje.sigue_vivo() and personaje.posicion() in celdas_afectadas:
                        personaje.recibir_ataque(Artillero.danyo)
                        if personaje.sigue_vivo():
                            informe += (f"{personaje.__class__.__name__} ha sido herido en {personaje.posicion}"
                                        f"Vida restante: {personaje.vida_actual()}")
                        else:
                            informe += f"{personaje.__class__.__name__} ha sido eliminado"
                        informe += "\n"
                if informe == "":
                    informe = "Ningun personaje ha sido herido\n"
            elif inicial_personaje == Inteligencia.__name__[0]:
                celdas_afectadas = area2x2(celda)
                for personaje in self.equipo:
                    if personaje.sigue_vivo() and personaje.posicion() in celdas_afectadas:
                        informe += f"{personaje.__class__.__name__} ha sido avistado en {personaje.posicion}"
                if informe == "":
                    informe = "Ningun personaje ha sido revelado\n"
            else:
                for personaje in self.equipo:
                    if personaje.sigue_vivo() and personaje.posicion() == celda:
                        personaje.recibir_ataque(Francotirador.danyo)
                        if personaje.sigue_vivo():
                            informe += (f"{personaje.__class__.__name__} ha sido herido en {personaje.posicion()}"
                                        f"Vida restante {personaje.vida_actual()}")
                        else:
                            informe += f"{personaje.__class__.__name__} ha sido eliminado"
                        informe += "\n"
                if informe == "":
                    informe = "Ningun personaje ha sido herido\n"
            resultado = {'informe': informe, 'terminada': not self.quedan_militares_con_vida()}

        self.informe = informe
        return resultado'''

    def quedan_militares_con_vida(self):
        quedan = False
        for personaje in self.equipo:
            if (personaje.__class__.__name__ == 'Artillero' or personaje.__class__.__name__ == 'Francotirador') and personaje.sigue_vivo():
                quedan = True
        return quedan

    def indicar_celda(self, personaje):
        celda = input(f'Indica la celda ({min_columna}-{max_columna}, {min_fila}-{max_fila}. p. ej: B2) en la que posicionar al {personaje.__class__.__name__}: ').upper()
        return celda

    def colocar_equipo(self):
        print('Vamos a posicionar a nuestros personajes en el tablero!')
        for personaje in self.equipo:
            salir = False
            while not salir:
                celda = self.indicar_celda(personaje)
                if validar_celda(celda, max_columna, max_fila):
                    if comprobar_celda_disponible(celda, self.equipo):
                        personaje.definir_posicion(celda)
                        salir = True
                    else:
                        print('Ups...la celda ya esta ocupada!, prueba otra vez...')
                else:
                    print('Ups...valor de celda incorrecto!, prueba otra vez...')
        print('Posicionamiento terminado.')
