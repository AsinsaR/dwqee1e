# Importamos las herramientas de los otros archivos
import graficos
import partida

def menu():
    graficos.limpiar_pantalla()
    graficos.mostrar_cabecera("EL IMPOSTOR")
    
    print("1. Comenzar Juego")
    print("2. Salir")
    
    opcion = input("\nElige una opción: ")
    
    if opcion == "1":
        comenzar_partida()
    else:
        print("¡Adiós!")

def comenzar_partida():
    graficos.limpiar_pantalla()
    num = int(input("¿Cuántos jugadores son? "))
    
    palabra = partida.obtener_palabras()
    roles = partida.asignar_roles(num, palabra)
    
    # Por ahora solo mostramos que la lógica funciona
    graficos.mostrar_mensaje("¡Roles asignados con éxito!")
    input("Presiona Enter para volver al menú...")
    menu()

# Esto inicia el juego
if __name__ == "__main__":
    menu()