import tkinter as tk
from tkinter import ttk

# Colores de Alto Contraste
COLOR_FONDO = "#000000"   
COLOR_TARJETA = "#111827" 
COLOR_TEXTO = "#ffffff"    
COLOR_ACENTO = "#00ffff"   
COLOR_ERROR = "#ff0033"    
COLOR_EXITO = "#00ff66"

# Fuentes
FUENTE_LOGO = ("Impact", 60)
FUENTE_TITULO = ("Verdana", 24, "bold")
FUENTE_NORMAL = ("Segoe UI", 12, "bold")
FUENTE_BOTON = ("Segoe UI", 13, "bold")

def crear_ventana():
    ventana = tk.Tk()
    ventana.title("EL IMPOSTOR")
    ventana.geometry("960x540")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", 
                    fieldbackground=COLOR_TARJETA, 
                    background=COLOR_ACENTO, 
                    foreground=COLOR_TEXTO,
                    bordercolor=COLOR_ACENTO,
                    font=("Segoe UI", 11, "bold"))
    
    ventana.option_add("*TCombobox*Listbox.background", COLOR_TARJETA)
    ventana.option_add("*TCombobox*Listbox.foreground", COLOR_TEXTO)
    ventana.option_add("*TCombobox*Listbox.selectBackground", COLOR_ACENTO)
    
    return ventana

def limpiar_pantalla(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.configure(bg=COLOR_FONDO)

def crear_boton_moderno(parent, text, command, color=COLOR_ACENTO):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=COLOR_FONDO,
        font=FUENTE_BOTON, padx=30, pady=12,
        activebackground=COLOR_TEXTO, activeforeground=COLOR_FONDO,
        bd=0, cursor="hand2", relief="flat"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_TEXTO))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn