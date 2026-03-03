import tkinter as tk
from tkinter import ttk
import graficos
import partida

class JuegoImpostor:
    def __init__(self):
        self.root = None
        self.tiempo_juego = 30
        self.timer_id = None
        self.opciones_t = {
            "10 segundos": 10, "15 segundos": 15, "30 segundos": 30, 
            "1 minuto": 60, "1 minuto y 30 segundos": 90, "2 minutos": 120
        }

    def iniciar_menu(self):
        self.root = graficos.crear_ventana()
        tk.Frame(self.root, bg=graficos.COLOR_ACENTO, height=8).pack(fill="x")
        
        tk.Label(self.root, text="🕵️ EL IMPOSTOR", font=graficos.FUENTE_LOGO, 
                 bg=graficos.COLOR_FONDO, fg=graficos.COLOR_ACENTO).pack(pady=(40, 5))
        
        card = tk.Frame(self.root, bg=graficos.COLOR_TARJETA, padx=50, pady=30)
        card.pack(pady=20)

        self.crear_label(card, "CANTIDAD DE JUGADORES")
        self.cb_j = ttk.Combobox(card, values=[str(i) for i in range(3, 11)], state="readonly", width=35)
        self.cb_j.set("3"); self.cb_j.pack(pady=(5, 15), ipady=5)

        self.crear_label(card, "TIEMPO POR RONDA")
        self.cb_t = ttk.Combobox(card, values=list(self.opciones_t.keys()), state="readonly", width=35)
        self.cb_t.set("30 segundos"); self.cb_t.pack(pady=(5, 15), ipady=5)

        self.crear_label(card, "CATEGORÍA DEL JUEGO")
        self.cb_m = ttk.Combobox(card, values=partida.obtener_modalidades(), state="readonly", width=35)
        self.cb_m.set("Clásica"); self.cb_m.pack(pady=(5, 15), ipady=5)

        graficos.crear_boton_moderno(self.root, "CREAR PARTIDA", self.comenzar).pack(pady=10)
        self.root.mainloop()

    def crear_label(self, parent, text):
        tk.Label(parent, text=text, font=("Segoe UI", 10, "bold"), 
                 bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_ACENTO).pack(anchor="w")

    def comenzar(self):
        self.tiempo_juego = self.opciones_t[self.cb_t.get()]
        n = int(self.cb_j.get())
        p, pista, imp = partida.generar_partida(self.cb_m.get(), n)
        self.repartir_roles(1, n, p, pista, imp, [])

    def repartir_roles(self, jug_act, total, p, pista, imp, palabras):
        graficos.limpiar_pantalla(self.root)
        tk.Label(self.root, text=f"JUGADOR {jug_act}", font=graficos.FUENTE_LOGO, 
                 bg=graficos.COLOR_FONDO, fg=graficos.COLOR_TEXTO).pack(expand=True)
        
        def mostrar():
            graficos.limpiar_pantalla(self.root)
            es_imp = (jug_act == imp)
            card_rol = tk.Frame(self.root, bg=graficos.COLOR_TARJETA, padx=60, pady=40)
            card_rol.pack(expand=True)
            
            tk.Label(card_rol, text="TU ROL ES:", font=graficos.FUENTE_NORMAL, 
                     bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_TEXTO).pack()
            info = pista.upper() if es_imp else p.upper()
            tk.Label(card_rol, text=info, font=("Verdana", 40, "bold"), 
                     bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_ACENTO if es_imp else graficos.COLOR_EXITO).pack(pady=20)
            
            graficos.crear_boton_moderno(self.root, "ENTENDIDO", 
                lambda: self.repartir_roles(jug_act+1, total, p, pista, imp, palabras) if jug_act < total else self.ronda_descripcion(1, total, imp, palabras)).pack(pady=40)
        
        graficos.crear_boton_moderno(self.root, "VER SECRETO", mostrar).pack(pady=60)

    def ronda_descripcion(self, jug_act, total, imp, palabras):
        graficos.limpiar_pantalla(self.root)
        label_t = tk.Label(self.root, text=str(self.tiempo_juego), font=("Impact", 50), 
                           bg=graficos.COLOR_FONDO, fg=graficos.COLOR_ERROR)
        label_t.pack(pady=20)
        
        tk.Label(self.root, text=f"JUGADOR {jug_act}", font=graficos.FUENTE_TITULO, 
                 bg=graficos.COLOR_FONDO, fg=graficos.COLOR_TEXTO).pack()

        label_error = tk.Label(self.root, text="", font=("Segoe UI", 12, "bold"), 
                               bg=graficos.COLOR_FONDO, fg=graficos.COLOR_ERROR)
        label_error.pack()
        
        entry_f = tk.Frame(self.root, bg=graficos.COLOR_ACENTO, padx=2, pady=2)
        entry_f.pack(pady=10)
        entrada = tk.Entry(entry_f, font=("Segoe UI", 35, "bold"), justify='center', 
                           bg=graficos.COLOR_TARJETA, fg="white", bd=0, insertbackground="white")
        entrada.pack(ipady=10); entrada.focus_set()

        def forzar_envio():
            if self.timer_id: self.root.after_cancel(self.timer_id)
            pal = entrada.get().strip() or "PASÓ"
            palabras.append(f"J{jug_act}: {pal}")
            if jug_act < total: self.ronda_descripcion(jug_act + 1, total, imp, palabras)
            else: self.fase_votacion(1, total, imp, palabras, [])

        def tick(s):
            if s > 0:
                label_t.config(text=str(s)); self.timer_id = self.root.after(1000, tick, s - 1)
            else: forzar_envio()

        def validar_y_enviar():
            if not entrada.get().strip():
                label_error.config(text="⚠️ ¡ESCRIBE ALGO!")
            else: forzar_envio()

        graficos.crear_boton_moderno(self.root, "ENVIAR PALABRA", validar_y_enviar, graficos.COLOR_EXITO).pack(pady=20)
        tick(self.tiempo_juego)

    def fase_votacion(self, jug_vota, total, imp, resumen, votos):
        graficos.limpiar_pantalla(self.root)
        label_t = tk.Label(self.root, text="30", font=("Impact", 40), bg=graficos.COLOR_FONDO, fg=graficos.COLOR_ACENTO)
        label_t.pack(pady=10)
        tk.Label(self.root, text=f"TURNO DE VOTO: JUGADOR {jug_vota}", font=graficos.FUENTE_TITULO, 
                 bg=graficos.COLOR_FONDO, fg=graficos.COLOR_TEXTO).pack()
        
        f_res = tk.Frame(self.root, bg=graficos.COLOR_TARJETA, padx=20, pady=20)
        f_res.pack(pady=20, fill="x", padx=50)
        for i, p in enumerate(resumen):
            tk.Label(f_res, text=p, font=("Consolas", 11, "bold"), 
                     bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_ACENTO).grid(row=i//5, column=i%5, padx=10, pady=5)

        def reg_voto(v):
            if self.timer_id: self.root.after_cancel(self.timer_id)
            votos.append(v)
            if jug_vota < total: self.fase_votacion(jug_vota + 1, total, imp, resumen, votos)
            else: self.mostrar_final(imp, votos)

        btns_f = tk.Frame(self.root, bg=graficos.COLOR_FONDO)
        btns_f.pack(pady=10)
        for i in range(1, total + 1):
            if i != jug_vota:
                graficos.crear_boton_moderno(btns_f, f"J{i}", lambda idx=i: reg_voto(idx), graficos.COLOR_ERROR).pack(side="left", padx=5)
        
        def tick_v(s):
            if s > 0:
                label_t.config(text=str(s)); self.timer_id = self.root.after(1000, tick_v, s-1)
            else: reg_voto(0)
        tick_v(30)

    def mostrar_final(self, imp, votos):
        graficos.limpiar_pantalla(self.root)
        v_v = [v for v in votos if v != 0]
        mas_v = max(set(v_v), key=v_v.count) if v_v else 0
        ganan = (mas_v == imp)
        
        main_f = tk.Frame(self.root, bg=graficos.COLOR_FONDO)
        main_f.pack(expand=True, fill="both", padx=50, pady=20)

        col_izq = tk.Frame(main_f, bg=graficos.COLOR_TARJETA, padx=30, pady=30)
        col_izq.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(col_izq, text="PARTIDA FINALIZADA", font=graficos.FUENTE_NORMAL, bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_ACENTO).pack()
        tk.Label(col_izq, text="GANÓ EL PUEBLO" if ganan else "GANÓ EL IMPOSTOR", font=("Impact", 40), 
                 bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_EXITO if ganan else graficos.COLOR_ERROR).pack(pady=10)
        
        col_der = tk.Frame(main_f, bg=graficos.COLOR_TARJETA, padx=30, pady=30)
        col_der.pack(side="right", expand=True, fill="both", padx=10)
        tk.Label(col_der, text="EL IMPOSTOR ERA:", font=graficos.FUENTE_NORMAL, bg=graficos.COLOR_TARJETA, fg=graficos.COLOR_ACENTO).pack()
        tk.Label(col_der, text=f"JUGADOR {imp}", font=graficos.FUENTE_TITULO, bg=graficos.COLOR_TARJETA, fg="white").pack(pady=10)

        graficos.crear_boton_moderno(self.root, "VOLVER AL INICIO", lambda: [self.root.destroy(), self.iniciar_menu()]).pack(pady=20)

if __name__ == "__main__":
    app = JuegoImpostor()
    app.iniciar_menu()