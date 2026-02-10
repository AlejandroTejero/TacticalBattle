import sys
import socket
from jugador import Jugador
import protocol

Numero_argumentos = 3
# La primera posicion corresponde con el nombre del archivo, la 2 = direccion ip server, 3 = puerto.
def args_control():
    if len(sys.argv) == Numero_argumentos:
        server_ip = sys.argv[1]
        try:
            server_port = int(sys.argv[2])
        except ValueError:
            raise Exception('El puerto debe ser un número entero')
        return server_ip, server_port
    else:
        raise Exception('Debes pasar tres argumentos (nombre del programa, IP y puerto) al inciar el programa')

def crear_cliente_socket():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((ip, port))
    print(f"Cliente corriendo en {cliente_socket.getsockname()}")
    return cliente_socket

def nombre_atacante():
    username = input("Introduzca el nombre de usuario: ")
    protocol.send_one_message(cliente_socket, username)
    return username

def nombre_defensor():
    oponente = protocol.recv_one_message(cliente_socket)
    print(f"Mi oponente es {oponente}")
    return oponente


if __name__ == "__main__":
    cliente_socket = None

    try:
        ip, port = args_control()

        cliente_socket = crear_cliente_socket()
        username = nombre_atacante()
        oponente = nombre_defensor()

        soy_yo_atacante = protocol.recv_one_message(cliente_socket, is_text=False)
        if soy_yo_atacante:
            print("Empiezo atacando")
        else:
            print("Empiezo defendiendo")

        jugador = Jugador()
        protocol.send_one_message(cliente_socket, True, is_text=False)

        juego_acabado = False
        while not juego_acabado:
            if soy_yo_atacante:
                input("Es nuestro turno. Pulsa intro para comenzar")
                codigo_accion = jugador.turno()
                protocol.send_one_message(cliente_socket, codigo_accion, is_text=False)
                resultado_accion = protocol.recv_one_message(cliente_socket, is_text=False)
                if resultado_accion:
                    print("--- RESULTADO DE LA ACCION ---")
                    print(resultado_accion['informe'])
                    juego_acabado = resultado_accion['terminada']
                    if juego_acabado:
                        print('Unidades militares derrotadas...')
                        print("HEMOS GANADO!!!")
            else:
                print(f"Turno de {oponente}")
                codigo_accion = protocol.recv_one_message(cliente_socket, is_text=False)
                resultado_accion = jugador.recibir_accion(codigo_accion)
                protocol.send_one_message(cliente_socket, resultado_accion, is_text=False)
                juego_acabado = protocol.recv_one_message(cliente_socket, is_text=False)
                if juego_acabado:
                    print("Nuestras unidades militares han sido eliminadas...")
                    print('Hemos sido derrotados...')
            soy_yo_atacante = not soy_yo_atacante
        protocol.send_one_message(cliente_socket, jugador.vivos(), is_text=False)
        print(f'Numero de personajes con vida: {jugador.vivos()}')
        protocol.send_one_message(cliente_socket, jugador.muertos(), is_text=False)
        print(f'Número de personajes muertos: {jugador.muertos()}')
        ranking = protocol.recv_one_message(cliente_socket)
        print(ranking)
        cliente_socket.close()

    except (ConnectionError, EOFError) as error:
        print(f"Error de conexion con el servidor: {error}")
    except socket.error as error:
        print(f"Error de socket: {error}")
    except KeyboardInterrupt:
        print("cliente detenido con Ctrl+C")
    except Exception as error:
        print(f'Error en el programa: {error}')
