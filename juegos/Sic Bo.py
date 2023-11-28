import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

# Cargar la base de datos
base_datos = pd.read_csv('base_datos.csv')

# Crear el diccionario de jugadores
jugadores = {cedula: {'Nombre': nombre, 'Dinero_inicial': dinero_inicial, 'Dinero_juego2': 0} for _, nombre, cedula, _, dinero_inicial, _, _, _, _, _ in base_datos.itertuples(index=False)}

# Crear listas para cédulas y nombres ordenadas por cédula
cedulas_ordenadas = sorted(jugadores.keys())
nombres_ordenados = [jugadores[cedula]['Nombre'] for cedula in cedulas_ordenadas]

num_jugador_actual = 0
rondas_totales = 10
ronda_actual = 1

def iniciar_juego():
    global num_jugador_actual
    actualizar_labels()
    apostar_button.config(state=tk.NORMAL)

def lanzar_dados():
    dados = [random.randint(1, 6) for _ in range(3)]
    resultado = sum(dados)
    dados_label.config(text=f"¡Resultado de los dados: {dados[0]}, {dados[1]}, {dados[2]}!")
    return resultado

def realizar_apuesta():
    global num_jugador_actual, ronda_actual
    try:
        apuesta_dinero = int(apuesta_entry_dinero.get().strip())
        if 40000 <= apuesta_dinero <= 160000:
            jugadores[cedula]['Dinero_inicial'] -= apuesta_dinero
            jugadores[cedula]['Dinero_juego2'] += apuesta_dinero
            apuesta = int(apuesta_entry.get().strip())
            if 4 <= apuesta <= 18:
                jugadores[cedula]['Apuesta'] = apuesta
                resultado = lanzar_dados()
                verificar_apuestas(resultado)
                ronda_actual += 1
                if ronda_actual > rondas_totales:
                    finalizar_juego()
                else:
                    actualizar_labels()
            else:
                messagebox.showerror("Error", "La apuesta debe estar entre 4 y 18.")
        else:
            messagebox.showerror("Error", "La apuesta de dinero debe estar entre 40000 y 160000.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")

def verificar_apuestas(resultado):
    tablero_text.delete(1.0, tk.END)
    ganadores = [cedula for cedula in jugadores if jugadores[cedula]['Apuesta'] == resultado]
    total_apuesta = sum(jugadores[cedula]['Apuesta'] for cedula in jugadores)

    if ganadores:
        monto_por_ganador = total_apuesta / len(ganadores)
        for ganador in ganadores:
            jugadores[ganador]['Dinero_inicial'] += monto_por_ganador
            jugadores[ganador]['Dinero_juego2'] -= monto_por_ganador
            tablero_text.insert(tk.END, f"{jugadores[ganador]['Nombre']} gana {monto_por_ganador} puntos en la ronda {ronda_actual}!\n")
    else:
        tablero_text.insert(tk.END, f"Nadie ha acertado en esta ronda, no hay ganadores.\n")

    mostrar_puntuaciones()

def mostrar_puntuaciones():
    tablero_text.insert(tk.END, "\nTabla de Puntuaciones:\n")
    for cedula in jugadores:
        tablero_text.insert(tk.END, f"{jugadores[cedula]['Nombre']} - Dinero Inicial: {jugadores[cedula]['Dinero_inicial']} - Dinero Juego 2: {jugadores[cedula]['Dinero_juego2']}\n")

def finalizar_juego():
    tablero_text.insert(tk.END, "\nJuego finalizado. Puntuaciones finales:\n")
    mostrar_puntuaciones()
    apostar_button["state"] = tk.DISABLED

def actualizar_labels():
    apuesta_label.config(text=f"Apuesta - Ronda {ronda_actual}:")

# Crear la ventana principal
root = tk.Tk()
root.title("Sic Bo Game")
root.geometry("400x400")

# Etiquetas
dados_label = tk.Label(root, text="¡Bienvenido a Sic Bo!")
dados_label.pack()

apuesta_label_dinero = tk.Label(root, text="Ingrese su apuesta de dinero (40000-160000):")
apuesta_label_dinero.pack()

apuesta_entry_dinero = tk.Entry(root)
apuesta_entry_dinero.pack()

apuesta_label = tk.Label(root, text="")
apuesta_label.pack()

apuesta_entry = tk.Entry(root)
apuesta_entry.pack()

apostar_button = tk.Button(root, text="Apostar", command=realizar_apuesta, state=tk.DISABLED)
apostar_button.pack()

# Área de texto
tablero_text = tk.Text(root, height=5, width=40)
tablero_text.pack()

# Botones adicionales
jugar_nuevamente_button = tk.Button(root, text="Jugar Nuevamente", command=jugar_nuevamente)
jugar_nuevamente_button.pack()

salir_button = tk.Button(root, text="Salir", command=salir)
salir_button.pack()

# Función para aplicar estilos de casino
def aplicar_estilos_casino():
    root.configure(bg='#1E2124')  # Color de fondo oscuro
    etiquetas = [dados_label, apuesta_label_dinero, apuesta_label]
    for etiqueta in etiquetas:
        etiqueta.configure(fg='white', bg='#1E2124')  # Texto blanco sobre fondo oscuro

    entradas = [apuesta_entry_dinero, apuesta_entry]
    for entrada in entradas:
        entrada.configure(fg='black', bg='white')  # Texto negro sobre fondo claro

    botones = [apostar_button, jugar_nuevamente_button, salir_button]
    for boton in botones:
        boton.configure(fg='white', bg='#4CAF50')  # Texto blanco sobre fondo verde

    tablero_text.configure(fg='white', bg='#1E2124')  # Texto blanco sobre fondo oscuro

# Aplicar estilos de casino
aplicar_estilos_casino()

# Iniciar el bucle principal
root.mainloop()

