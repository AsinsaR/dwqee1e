import random

def obtener_palabras():
    # Lista de palabras para el juego
    lista = ["Manzana", "Pizza", "Delfín", "Coche", "Guitarra"]
    secreta = random.choice(lista)
    return secreta

def asignar_roles(num_jugadores, palabra_secreta):
    # Elegimos un número al azar para ser el impostor
    id_impostor = random.randint(1, num_jugadores)
    roles = {}
    
    for i in range(1, num_jugadores + 1):
        if i == id_impostor:
            roles[i] = "Eres el IMPOSTOR. ¡Miente!"
        else:
            roles[i] = f"La palabra es: {palabra_secreta}"
    return roles