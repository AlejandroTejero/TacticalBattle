# Tactical Battle - Python

> No requiere entorno virtual ni dependencias externas. Ejecución compatible con **Python 3**.

---

## Tabla de contenidos

- [Tactical Battle](#tactical-battle)
- [Qué es](#qué-es)
- [Características](#características)
- [Cómo ejecutar](#cómo-ejecutar)
- [Cómo se juega](#cómo-se-juega)
- [Unidades y habilidades](#unidades-y-habilidades)
- [Condición de victoria](#condición-de-victoria)
- [Ranking](#ranking)

---

## Tactical Battle

### Qué es
Tactical Battle es un simulador de combate táctico por turnos que utiliza un modelo **cliente/servidor**:
* El **servidor** gestiona las conexiones, el emparejamiento de jugadores (lobby) y las partidas simultáneas.
* El **cliente** ofrece la interfaz de usuario por terminal para posicionar unidades y ejecutar acciones.

La partida ocurre en un tablero de **4x4** (coordenadas A1 a D4) donde cada jugador despliega un escuadrón con roles especializados.

---

### Características
* Soporte para **N partidas simultáneas** (configurable por parámetro).
* **Lobby automático** para emparejamiento de jugadores.
* Unidades con sistema de movimiento y habilidades con enfriamiento (cooldown).
* **Persistencia de datos** en archivo de texto para el ranking.
* Protocolo de red propio con **framing** por tamaño para garantizar la integridad de los mensajes.

---

### Cómo ejecutar

#### 1. Servidor
Desde la carpeta `TacticalBattle/`:
```bash
python3 servidor.py <PUERTO> <PARTIDAS_SIMULTANEAS> <FICHERO_RANKING>
python3 servidor.py 5000 1 ranking_simple.txt


python3 cliente.py <IP_SERVIDOR> <PUERTO>
python3 cliente.py 127.0.0.1 5000

python3 cliente.py <IP_SERVIDOR> <PUERTO>
python3 cliente.py 127.0.0.1 5001
```

---

## Cómo se juega
1. **Identificación**: cada cliente introduce su nombre de usuario.
2. **Emparejamiento**: el servidor empareja a dos jugadores y decide quién empieza.
3. **Despliegue**: cada jugador coloca sus unidades en el tablero.
4. **Turnos**: en tu turno puedes:
   - mover una unidad a una casilla contigua, o
   - usar una habilidad.

> **Nota:** el movimiento es local, pero las habilidades ofensivas/de visión se envían al oponente para procesarse en su tablero.

---

## Unidades y habilidades
- **Francotirador**: disparo a una celda (daño alto).
- **Artillero**: disparo en área **2x2** (daño en zona).
- **Inteligencia**: revela unidades enemigas en un área **2x2**.
- **Médico**: cura a un aliado herido.

---

## Condición de victoria
La partida termina cuando el rival se queda sin unidades militares con vida (**Artillero** y **Francotirador**).

---

## Ranking
Al finalizar, los clientes envían sus estadísticas al servidor. Este calcula la puntuación y actualiza el fichero.
