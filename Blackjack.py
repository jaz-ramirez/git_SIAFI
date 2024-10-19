from random import shuffle, randint
import os
import random

# Función para limpiar la pantalla de la consola
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Definición de la clase Carta
class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    def ver_carta(self):
        # Devuelve la representación en cadena de la carta
        return f"{self.valor} de {self.palo}"

# Definición de la clase Mazo
class Mazo:
    def __init__(self, num_mazos):
        if num_mazos < 4 or num_mazos > 8:
            raise ValueError("El número de mazos debe estar entre 4 y 8.")
        self.num_mazos = num_mazos
        self.cartas = []
        self.cut_card = Carta("CUT", "CARD")
        self.crear_mazo()
        self.barajar()

    def crear_mazo(self):
        palos = ('corazones', 'treboles', 'diamantes', 'picas')
        valores = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        self.cartas = []
        for _ in range(self.num_mazos):
            for palo in palos:
                for valor in valores:
                    self.cartas.append(Carta(valor, palo))
        
        # Insertar la cut card en una posición aleatoria dentro del primer 75% del mazo
        num_cartas = len(self.cartas)
        min_pos = int(num_cartas * 0)
        max_pos = int(num_cartas * 0.75)
        pos_cut_card = random.randint(min_pos, max_pos)
        self.cartas.insert(pos_cut_card, self.cut_card)
        #print(f"La cut card está en la posición {pos_cut_card + 1} (contando desde 1) en el mazo inicial.")

    def barajar(self):
        if self.cut_card in self.cartas:
            shuffle(self.cartas)
            # Encontrar la posición de la cut card después de barajar
            pos_actual_cut_card = self.cartas.index(self.cut_card)
            if pos_actual_cut_card >= (len(self.cartas) * 0.75):
                # Si la cut card está en el último 25%, volver a colocarla en una posición válida
                #print("La cut card está en el último 25% después de barajar. Reubicando.")
                # Eliminar la cut card y volver a insertarla en una posición válida
                self.cartas.remove(self.cut_card)
                pos_cut_card = random.randint(0, int(len(self.cartas) * 0.75) - 1)
                self.cartas.insert(pos_cut_card, self.cut_card)
                pos_actual_cut_card = pos_cut_card
                print(f"La cut card está ahora en la posición {pos_actual_cut_card + 1} (contando desde 1) después de barajar.")
        else:
            shuffle(self.cartas)

    def entregar_carta(self):
        carta = self.cartas.pop()
        if carta == self.cut_card:
            print("\n¡Se ha encontrado la tarjeta de corte! Rebarajando el mazo.")
            self.barajar()
            carta = self.entregar_carta()  # Tomar otra carta
        return carta

    def reintegrar_cartas(self):
        self.crear_mazo()
        self.barajar()
        print("¡El mazo ha sido rebarajado y todas las cartas han sido reintegradas, incluyendo una nueva tarjeta de corte!")

    def obtener_porcentaje_cartas_restantes(self):
        total_cartas_original = self.num_mazos * 52
        return (len(self.cartas) / total_cartas_original) * 100

    def necesita_rebarajar(self):
        return self.obtener_porcentaje_cartas_restantes() < 25

    def mostrar_posicion_cut_card(self):
        pos_cut_card = self.cartas.index(self.cut_card) + 1
        #print(f"La cut card está en la posición {pos_cut_card} (contando desde 1).")

# Definición de la clase Jugador
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def tomar_carta(self, mazo):
        # El jugador toma una carta del mazo
        self.mano.append(mazo.entregar_carta())

    def mostrar_mano(self):
        # Muestra la mano del jugador
        print(f'\n{self.nombre}')
        print('===========')
        for carta in self.mano:
            print(carta.ver_carta())
        print('___________')
        print(f'Total: {self.calcular_mano()}')

    def calcular_mano(self):
        # Calcula el valor total de la mano del jugador, considerando las reglas de los ases
        valor_cartas = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                        'J': 10, 'Q': 10, 'K': 10, 'A': 1}
        puntaje = 0
        aces = 0
        for carta in self.mano:
            if carta.valor == 'A':
                aces += 1
            puntaje += valor_cartas[carta.valor]
        for _ in range(aces):
            if puntaje + 10 <= 21:
                puntaje += 10
        return puntaje

# Definición de la clase Repartidor
class Repartidor:
    def __init__(self):
        self.nombre = "Repartidor"
        self.mano = []

    def tomar_carta(self, mazo):
        # El repartidor toma una carta del mazo
        self.mano.append(mazo.entregar_carta())

    def mostrar_mano(self, etapa_inicial=True):
        # Muestra la mano del repartidor, ocultando la primera carta si es necesario
        print(f'\n{self.nombre}')
        print('===========')
        for i, carta in enumerate(self.mano):
            if etapa_inicial and i == 0:
                print('- de -')
            else:
                print(carta.ver_carta())
        if not etapa_inicial:
            print('___________')
            print(f'Total: {self.calcular_mano()}')

    def calcular_mano(self):
        # Calcula el valor total de la mano del repartidor
        valor_cartas = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                        'J': 10, 'Q': 10, 'K': 10, 'A': 1}
        puntaje = 0
        aces = 0
        for carta in self.mano:
            if carta.valor == 'A':
                aces += 1
            puntaje += valor_cartas[carta.valor]
        for _ in range(aces):
            if puntaje + 10 <= 21:
                puntaje += 10
        return puntaje

# Función principal para jugar Blackjack
def jugar_blackjack():
    clear_screen()
    
    # Pregunta al usuario cuántos mazos desea usar
    while True:
        try:
            num_mazos = int(input("¿Cuántos mazos deseas usar (entre 4 y 8)? "))
            if 4 <= num_mazos <= 8:
                break
            else:
                print("Por favor, ingresa un número entre 4 y 8.")
        except ValueError:
            print("Entrada inválida. Por favor ingresa un número.")
    
    # Crea el mazo con el número seleccionado de mazos
    juego = Mazo(num_mazos)
    
    # Preguntar por el nombre solo una vez
    nombre_jugador = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre_jugador)

    while True:
        clear_screen()
        repartidor = Repartidor()

        # Inicia con dos cartas
        for _ in range(2):
            jugador.tomar_carta(juego)
            repartidor.tomar_carta(juego)

        # Verificar si el jugador tiene 21 puntos al inicio
        if jugador.calcular_mano() == 21:
            clear_screen()
            jugador.mostrar_mano()
            repartidor.mostrar_mano(etapa_inicial=False)
            print("\n¡Felicidades! Tienes 21. ¡Ganaste!")
            respuesta = input("\n¿Quieres jugar otra partida? (si/no): ")
            if respuesta.lower() != 'si':
                print("\nGracias por jugar, ¡hasta la próxima!\n")
                break
            else:
                jugador.mano.clear()
                continue

        while True:
            clear_screen()
            jugador.mostrar_mano()
            repartidor.mostrar_mano(etapa_inicial=True)

            if jugador.calcular_mano() > 21:
                print("\nTe pasaste. Perdiste.")
                break

            if jugador.calcular_mano() == 21:
                print("\n¡Tienes 21! Ganaste automáticamente.")
                break

            if input("\n¿Quieres otra carta? (si/no): ").lower() != 'si':
                break

            jugador.tomar_carta(juego)

            # Verificar nuevamente si el jugador tiene 21 puntos tras tomar una nueva carta
            if jugador.calcular_mano() == 21:
                print("\n¡Tienes 21! Ganaste automáticamente.")
                break

        if jugador.calcular_mano() <= 21:
            while repartidor.calcular_mano() < 17:
                repartidor.tomar_carta(juego)

        clear_screen()
        jugador.mostrar_mano()
        repartidor.mostrar_mano(etapa_inicial=False)

        print("\nResultado:")
        if jugador.calcular_mano() > 21:
            print("PERDISTE, te pasaste de 21")
        elif repartidor.calcular_mano() > 21 or repartidor.calcular_mano() < jugador.calcular_mano():
            print("GANASTE")
        elif repartidor.calcular_mano() > jugador.calcular_mano():
            print("PERDISTE")
        else:
            print("EMPATE")

        # Mostrar las cartas restantes y el porcentaje del mazo
        cartas_restantes = juego.obtener_porcentaje_cartas_restantes()
        print(f"\nCartas restantes en el mazo: {len(juego.cartas)} ({cartas_restantes:.2f}%)")

        # Mensaje sobre la necesidad de rebarajar si se cumple la condición
        if juego.necesita_rebarajar():
            juego.reintegrar_cartas()

        respuesta = input("\n¿Quieres jugar otra partida? (si/no): ")
        if respuesta.lower() != 'si':
            print("\nGracias por jugar, ¡hasta la próxima!\n")
            break
        else:
            jugador.mano.clear()
            repartidor.mano.clear()
            clear_screen()

if __name__ == '__main__':
    jugar_blackjack()


