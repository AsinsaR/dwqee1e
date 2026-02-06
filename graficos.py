import os

def limpiar_pantalla():
    # Esto borra el texto viejo para que el juego se vea limpio
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_cabecera(titulo):
    print("================================")
    print(f"      {titulo.upper()}      ")
    print("================================")

def mostrar_mensaje(mensaje):
    print(f"\n>> {mensaje}\n")