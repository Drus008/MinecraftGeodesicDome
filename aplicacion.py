import customtkinter as ctk
from colocarBloques import creacionDomo
from tkinter import filedialog
from listas import *

# Falta crear:
# Un seleccionador de carpeta (potser indicar que si no s'ha trobat el datapack s'ha de crear)



# Ampliacions
# Un seleccionador de versió
# Un seleccionador per a fixar un bloc per a cada part
# Canviar idioma
# Unes instruccions d'us
# Una advertencia si s'espera que la cúpula no surti gaire bé


ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "dark-blue", "green"

app = ctk.CTk()
app.title("DomeCraft")
app.geometry("800x600")  # Ancho x Alto


def solo_numeros(texto):
    return texto.isdigit() or texto == ""

def limitar1caracter(event):
    entrada = event.widget
    # Obtener el texto actual
    texto = entrada.get()

    if event.keysym in teclas_permitidas:
        return None

    if not event.char.isdigit():
        return "break"

    if len(texto) >= 1:
        return "break"

def limitar3caracter(event):
    entrada = event.widget
    # Obtener el texto actual
    texto = entrada.get()

    if event.keysym in teclas_permitidas:
        return None

    if not event.char.isdigit():
        return "break"

    if len(texto) >= 3:
        return "break"

def comprovacionesFinales():
    pass


def ejecutarPrograma():

    comprovacionesFinales()

    carpeta = "C:/Users/druss/AppData/Roaming/.minecraft/saves/Prueba"
    d = int(entryDensidad.get())
    r = int(entryRadio.get())
    c = int(entryCaraTamaño.get())
    a = int(entryAristaTamaño.get())
    e = int(entryEsquinaTamaño.get())
    nombre = entryNombre.get()

    creacionDomo(d, r, c, a, e, carpeta, nombre, True)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(title="Seleccionar una carpeta")  # Abrir el cuadro de diálogo
    if carpeta:  # Si se seleccionó una carpeta
        label_resultado.configure(text=f"Carpeta seleccionada: {carpeta}")
    else:
        label_resultado.configure(text="No se seleccionó ninguna carpeta.")

# Crear un botón que abrirá el cuadro de diálogo para seleccionar una carpeta
boton_seleccionar = ctk.CTkButton(app, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.grid(row=0, column=0, padx=10, pady=10, sticky="w")


# Crear un label para mostrar la carpeta seleccionada
label_resultado = ctk.CTkLabel(app, text="No se ha seleccionado ninguna carpeta.")
label_resultado.grid(row=0, column=2, padx=10, pady=10, sticky="w")


# Función para habilitar/deshabilitar el texto de caras
def toggleEntryCara():
    if VarCheckboxCara.get():
        entryCaraTamaño.configure(state="normal", fg_color="white")
    else:
        entryCaraTamaño.configure(state="disabled", fg_color="#dbdbdb")

def toggleEntryArista():
    if VarCheckboxArista.get():
        entryAristaTamaño.configure(state="normal", fg_color="white")
    else:
        entryAristaTamaño.configure(state="disabled", fg_color="#dbdbdb")

def toggleEntryEsquina():
    if VarCheckboxEsquina.get():
        entryEsquinaTamaño.configure(state="normal", fg_color="white")
    else:
        entryEsquinaTamaño.configure(state="disabled", fg_color="#dbdbdb")

# Variable para la CheckBox
VarCheckboxCara = ctk.BooleanVar(value=True)
VarCheckboxArista = ctk.BooleanVar(value=True)
VarCheckboxEsquina = ctk.BooleanVar(value=True)


# Crear una CheckBox con texto al lado
checkboxCara = ctk.CTkSwitch(
    app, 
    text="Caras",
    variable=VarCheckboxCara, 
    command=toggleEntryCara
)
checkboxArista = ctk.CTkSwitch(
    app, 
    text="Aristas",
    variable=VarCheckboxArista, 
    command=toggleEntryArista
)
checkboxEsquina = ctk.CTkSwitch(
    app, 
    text="Esquinas",
    variable=VarCheckboxEsquina, 
    command=toggleEntryEsquina
)

checkboxCara.grid(row=1, column=0, padx=10, pady=10, sticky="w")
checkboxArista.grid(row=2, column=0, padx=10, pady=10, sticky="w")
checkboxEsquina.grid(row=3, column=0, padx=10, pady=10, sticky="w")




anuchraTamaño = 23
entryCaraTamaño = ctk.CTkEntry(app)
entryCaraTamaño.configure(state="normal", width=anuchraTamaño)
entryCaraTamaño.grid(row=1, column=1, padx=10, pady=10, sticky="w")
entryCaraTamaño.bind("<Key>", limitar1caracter)

entryAristaTamaño = ctk.CTkEntry(app)
entryAristaTamaño.configure(state="normal", width=anuchraTamaño)
entryAristaTamaño.grid(row=2, column=1, padx=10, pady=10, sticky="w")
entryAristaTamaño.bind("<Key>", limitar1caracter)

entryEsquinaTamaño = ctk.CTkEntry(app)
entryEsquinaTamaño.configure(state="normal", width=anuchraTamaño)
entryEsquinaTamaño.grid(row=3, column=1, padx=10, pady=10, sticky="w")
entryEsquinaTamaño.bind("<Key>", limitar1caracter)


barraCara = ctk.CTkProgressBar(app)
barraCara.set(0)
barraCara.grid(row=1, column=2, padx=10, pady=10, sticky="w")

barraArista = ctk.CTkProgressBar(app)
barraArista.set(0)
barraArista.grid(row=2, column=2, padx=10, pady=10, sticky="w")

barraEsquina = ctk.CTkProgressBar(app)
barraEsquina.set(0)
barraEsquina.grid(row=3, column=2, padx=10, pady=10, sticky="w")



frameRadio = ctk.CTkFrame(app)
frameRadio.grid(row=4, column=0, padx=10, pady=10)

textRadio = ctk.CTkLabel(frameRadio,text="Radio")
textRadio.grid(row=1, column=1, padx=10, pady=10, sticky="w")

entryRadio = ctk.CTkEntry(frameRadio)
entryRadio.configure(state="normal", width=40)
entryRadio.bind("<Key>", limitar3caracter)
entryRadio.grid(row=1, column=2)


frameDensidad = ctk.CTkFrame(app)
frameDensidad.grid(row=4, column=1, padx=10, pady=10)

textDensidad = ctk.CTkLabel(frameDensidad,text="Frecuencia geodésica")
textDensidad.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entryDensidad = ctk.CTkEntry(frameDensidad)
entryDensidad.configure(state="normal", width=anuchraTamaño)
entryDensidad.grid(row=0, column=1, padx=10, pady=10, sticky="w")
entryDensidad.bind("<Key>", limitar1caracter)

frameFinal = ctk.CTkFrame(app)
frameFinal.grid(row=4,column=2)

entryNombre = ctk.CTkEntry(frameFinal, placeholder_text="Nombre",)
entryNombre.grid(row=0,column=0)

botonGenerar = ctk.CTkButton(frameFinal, text="Generar", fg_color="green", command=ejecutarPrograma)
botonGenerar.grid(row=0, column=1)

# Ejecutar el bucle principal de la aplicación
app.mainloop()
