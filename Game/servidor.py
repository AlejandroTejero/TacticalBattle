import socket
import sys  # Hemos cambiado el modulo Parse por el modulo Sys
import threading
import random
import protocol
from queue import Queue
from doubly_linked_list import DoublyLinkedList

numero_partidas_a_la_vez = 0
fichero_rank = ""
rank = DoublyLinkedList()
loby = Queue()
lock = threading.Lock() # Para evitar condiciones de carrera (incoherencias)
juegos = []
Numero_argumentos = 4
tamanyo_buff = 2048


class Cliente:
    def __init__(self, username, socket, address):
        self.username = username
        self.socket = socket
        self.address = address

    def __str__(self):
        return f'{self.username} {self.address}'


class Partida:
    def __init__(self, cliente1, cliente2):
        self.cliente1 = cliente1
        self.cliente2 = cliente2
        self.clientes = [self.cliente1, self.cliente2]
        self.final = False
        self.ganador = None
        self.perdedor = None
        self.turnos = 0
        self.cliente1_puntos = 0
        self.cliente2_puntos = 0
        self.cliente1_vivos = 0
        self.cliente1_muertos = 0
        self.cliente2_vivos = 0
        self.cliente2_muertos = 0

    def __str__(self):
        return f"{self.cliente1} vs {self.cliente2}"

    def aumentar_turnos(self):
        self.turnos += 1

    def finalizado(self):
        return self.final

    def set_ganador(self, ganador):
        self.ganador = ganador

    def set_perdedor(self, perdedor):
        self.perdedor = perdedor

    def acabado(self, ganador, perdedor):
        self.final = True
        self.set_ganador(ganador)
        self.set_perdedor(perdedor)

    def dar_puntos(self):
        if self.ganador.username == self.cliente1.username:
            self.cliente1_puntos = 1000 + max(0, (20 - self.turnos)) * 20
            self.cliente1_puntos += self.cliente1_vivos * 100
            self.cliente1_puntos += self.cliente2_muertos * 100

            if self.turnos > 10:
                self.cliente2_puntos = (self.turnos - 10) * 20
            self.cliente2_puntos += self.cliente2_vivos * 100
            self.cliente2_puntos += self.cliente1_muertos * 100

            if self.cliente2_puntos > self.cliente1_puntos:
                self.cliente1_puntos = 1000
                self.cliente2_puntos = 900
        else:
            self.cliente2_puntos = 1000 + max(0, (20 - self.turnos)) * 20
            self.cliente2_puntos += self.cliente2_vivos * 100
            self.cliente2_puntos += self.cliente1_muertos * 100

            if self.turnos > 10:
                self.cliente1_puntos = (self.turnos - 10) * 20
            self.cliente1_puntos += self.cliente1_vivos * 100
            self.cliente1_puntos += self.cliente2_muertos * 100

            if self.cliente1_puntos > self.cliente2_puntos:
                self.cliente2_puntos = 1000
                self.cliente1_puntos = 900

    def set_vivos(self, cliente, n):
        if self.cliente1.username == cliente.username:
            self.cliente1_vivos = n
        else:
            self.cliente2_vivos = n

    def set_muertos(self, cliente, n):
        if self.cliente1.username == cliente.username:
            self.cliente1.muertos = n
        else:
            self.cliente2.muertos = n

    def cerrar_conexion_clientes(self):
        for cliente in self.clientes:
            try:
                cliente.socket.close()
            except socket.error:    #Sirve para capturar cualquier error relativo de los sockets
                pass


class Ranking:
    def __init__(self, jugador, puntuacion):
        self.jugador = jugador
        self.puntuacion = puntuacion

    def __str__(self):
        return f'{self.jugador}:{self.puntuacion}'

    def __gt__(self, other):    # Para comprarar objetos del tipo ranking (las puntuaciones de los jugadores)
        return self.puntuacion > other.puntuacion


def args_control():
    if len(sys.argv) == Numero_argumentos:
        try:
            port = int(sys.argv[1])
        except ValueError:
            raise Exception("El puerto debe ser un número entero")
        try:
            numero_partidas_a_la_vez = int(sys.argv[2])
        except ValueError:
            raise Exception("El número de partidas simultaneas debe ser un número entero")
        nombre_fichero = sys.argv[3]
        return port, numero_partidas_a_la_vez, nombre_fichero
    else:
        raise Exception("Debes introducir 4 argumentos (nombre del programa, puerto, partidas simultaneas y fichero para guardar el ranking)")


def cargar_rank(nombre):
    global rank
    try:
        with open(nombre, 'r') as fichero:
            for linea in fichero:
                partes = linea.strip().split(':')
                if len(partes) == 2:
                    jugador, puntos = partes[0], int(partes[1])
                    rank.add_ordered(Ranking(jugador, puntos))
    except FileNotFoundError:
        print(f'Archivo "{nombre}" no encontrado')


def guardar_rank(nombre):
    global rank

    with open(nombre, 'w') as fichero:
        for index in range(len(rank)):
            objeto = rank.get_item(index)
            fichero.write(f"{objeto}\n")


def mandar_info(clientes):
    for indice, cliente in enumerate(clientes):
        if indice == 0:
            oponente = clientes[1]
        else:
            oponente = clientes[0]
        msg = oponente.username
        protocol.send_one_message(cliente.socket, msg)


def manejar_juego(juego):
    global lock, loby, juegos, nombre_fichero

    try:
        clientes = juego.clientes
        mandar_info(clientes)

        turno = random.randint(0, 1)
        atacante = clientes[turno]
        protocol.send_one_message(atacante.socket, True, is_text=False)
        if turno == 0:
            defensor = clientes[1]
        else:
            defensor = clientes[0]
        protocol.send_one_message(defensor.socket, False, is_text=False)

        for cliente in clientes:
            protocol.recv_one_message(cliente.socket, is_text=False)
            print(f'El usuario {cliente} terminó de posicionar sus tropas')

        print(f'Comienza la partida de {juego}')
        while not juego.finalizado():
            cliente_atacante = clientes[turno]
            if turno == 0:
                oponente = clientes[1]
            else:
                oponente = clientes[0]

            codigo_accion = protocol.recv_one_message(cliente_atacante.socket, is_text=False)
            protocol.send_one_message(oponente.socket, codigo_accion, is_text=False)
            resultado_accion = protocol.recv_one_message(oponente.socket, is_text=False)
            juego.aumentar_turnos()
            print(f'Turno: {juego.turnos}')
            final = False
            if resultado_accion:
                print(f'El cliente {cliente_atacante} ha llevado a cabo la siguiente acción: '
                      f'{codigo_accion}. El resultado ha sido: {resultado_accion["informe"]}')
                final = resultado_accion['terminada']
                if final:
                    print(f'El cliente {cliente_atacante} ha ganado')
                    print(f'El cliente {oponente} ha perdido')
                    juego.acabado(cliente_atacante, oponente)
            else:
                print(f'La accion que el {cliente_atacante} realizó no causo ningun daño')
            protocol.send_one_message(cliente_atacante.socket, resultado_accion, is_text=False)
            protocol.send_one_message(oponente.socket, final, is_text=False)
            turno = (turno + 1) % len(clientes)

        for cliente in clientes:
            vivos = protocol.recv_one_message(cliente.socket, is_text=False)
            juego.set_vivos(cliente, vivos)
            muertos = protocol.recv_one_message(cliente.socket, is_text=False)
            juego.set_muertos(cliente, muertos)
            print(f'El usuario {cliente} acabó la partida con {vivos} personajes vivos y {muertos} personajes muertos')

        juego.dar_puntos()

        lock.acquire()
        for cliente in clientes:
            if cliente.username == juego.cliente1.username:
                objeto = Ranking(cliente.username, juego.cliente1_puntos)
            else:
                objeto = Ranking(cliente.username, juego.cliente2_puntos)
            rank.add_ordered(objeto)
            protocol.send_one_message(cliente.socket, str(objeto))
        guardar_rank(nombre_fichero)
        lock.release()
    except (ConnectionError, EOFError) as error:
        print(f'Error de conexión: {error}')
    except socket.error:
        print(f'{juego} finalizada')
    finally:
        print(f'La partida {juego} ha acabado')
        lock.acquire()
        juegos.remove(juego)
        if len(loby) >= 2:
            jugador1 = loby.dequeue()
            jugador2 = loby.dequeue()
            print(f'Emparejamiento finalizado entre {jugador1} y {jugador2}')
            juego = Partida(jugador1, jugador2)
            juegos.append(juego)
            lock.release()
            manejar_juego(juego)
        else:
            lock.release()


def manejar_cliente(cliente_socket, cliente_address):
    global lock, loby, juegos, numero_partidas_a_la_vez
    try:
        username = protocol.recv_one_message(cliente_socket)
        cliente = Cliente(username, cliente_socket, cliente_address)
        lock.acquire()
        loby.enqueue(cliente)
        print(f"El cliente {cliente} ha entrado en el lobby")
        print(loby)
        if len(juegos) == numero_partidas_a_la_vez:
            print(f'El usuario {cliente} tiene que esperar a que halla mesas disponibles')
            lock.release()
        else:
            if len(loby) == 2:
                jugador1 = loby.dequeue()
                jugador2 = loby.dequeue()
                print(f'Emparejamiento finalizado entre {jugador1} y {jugador2}')
                juego = Partida(jugador1, jugador2)
                juegos.append(juego)
                lock.release()
                manejar_juego(juego)
            else:
                print(f'El usuario {cliente} tiene que esperar a que otro usuario se conecte')
                lock.release()
    except ConnectionError as error:
        print(f"Error de conexion con el cliente: {error}")
    except Exception as error:
        print(f'Error del programa: {error}')

def crear_servidor_socket():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('', port))
    servidor_socket.listen()
    print(f"Servidor abierto en {servidor_socket.getsockname()}")
    return servidor_socket


def crear_thread():
    thread = threading.Thread(target=manejar_cliente, args=[cliente_socket, cliente_address])
    thread.start()
    return thread


if __name__ == "__main__":
    servidor_socket = None
    try:
        port, numero_partidas_a_la_vez, nombre_fichero = args_control()
        cargar_rank(nombre_fichero)
        servidor_socket = crear_servidor_socket()
        while True:
            cliente_socket, cliente_address = servidor_socket.accept()
            print(f"Nuevo cliente conectado: {cliente_address}")
            thread = crear_thread()
    except socket.error as error:
        print(f"Error de socket: {error}")
    except KeyboardInterrupt:
        print("Servidor detenido con Ctrl+C")
        servidor_socket.close()
    except Exception as error:
        print(f'Error del programa: {error}')

    loby.clear()

    for juego in juegos:
        juego.cerrar_conexion_clientes()
    juegos.clear()

    servidor_socket.close()
