# dardoMaster
Aplicación en Python para registrar partidas de dardos. En su estado actual es compatible con los juegos:

- Cricket

## Cómo iniciar
1. Abrir la consola de Windows (***Ctrl + r*** > escribir "cmd" > ***Enter***)

![image](https://github.com/thesersaer/dardoMaster/assets/54591830/e5b4d916-8459-46a6-8ba0-d7caa56a0dd6)

2. Navegar al directorio del programa (la carpeta que contiene `cricket_main_console.py`, mediante el comando de consola "cd C:/...")

![image](https://github.com/thesersaer/dardoMaster/assets/54591830/5514c7ec-26d6-48e6-8138-78315cfdba10)

4. Abrir el archivo `cricket_main_console.py` con el comando "python cricket_main_console.py NUMERO_DE_JUGADORES NOMBRE_J1 NOMBRE_J2 ..."

![image](https://github.com/thesersaer/dardoMaster/assets/54591830/6ddbd924-cbb5-4500-93d7-de1e2684e0c4)

## Dentro del juego

![image](https://github.com/thesersaer/dardoMaster/assets/54591830/5cedad7f-f9d5-4039-b07a-e543b49b1f84)

El programa muestra (de arriba a abajo):
- Tabla de puntuaciones: NOMBRE_JUGADOR (PUNTOS) {NÚMEROS}

Por defecto todos los números están en -3. Al llegar a 0 se abre el número y si todos los jugadores tienen 0 (o más) en algún número este se cierra y deja de dar puntos.

- Número de ronda
- Turno
- Lanzamientos realizados en el turno (de más a menos reciente)

## Cómo jugar

El programa admite ciertas entradas / comandos:
- "undo": deshace la última tirada. Si no se han hecho tiradas en el turno, deshace el turno.
- "NÚMERO": registra una tirada según el número acertado (p.ej. "15" o "3").
- "NÚMERO, 2": ídem, número doble (p.ej. "15, 2" o "3,2").
- "NÚMERO, 3": ídem, número triple.
- "o": registra una tirada acertada (dentro de la diana) que no ha dado a ningún número.
- "f": registra una tirada nula (fuera de la diana). Se aplica una penalización para los próximos `2` turnos (modificable en `model/definitions.py`).
- ***Enter***: Avanza el turno. Sólo disponible si se han registrado todos los tiros del turno actual (3).

El juego finaliza cuando cualquier jugador tenga todos los números cerrados (>=0) y tenga la máxima puntuación de la partida. Para abandonar el juego, presionar ***Ctrl + z***.
