import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Crear la ventana principal
app = ctk.CTk()
app.title("Seleccionar Carpeta")
app.geometry("400x300")

# Función para abrir el cuadro de diálogo y seleccionar una carpeta
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccionar una carpeta")  # Abrir el cuadro de diálogo
    if carpeta:  # Si se seleccionó una carpeta
        label_resultado.configure(text=f"Carpeta seleccionada: {carpeta}")
    else:
        label_resultado.configure(text="No se seleccionó ninguna carpeta.")

# Crear un botón que abrirá el cuadro de diálogo para seleccionar una carpeta
boton_seleccionar = ctk.CTkButton(app, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=20)

# Crear un label para mostrar la carpeta seleccionada
label_resultado = ctk.CTkLabel(app, text="No se ha seleccionado ninguna carpeta.")
label_resultado.pack(pady=20)

# Ejecutar el bucle principal de la aplicación
app.mainloop()