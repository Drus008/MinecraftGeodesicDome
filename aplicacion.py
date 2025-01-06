import customtkinter as ctk
from listas import *

# Falta crear:
# Un seleccionador de carpeta (potser indicar que si no s'ha trobat el datapack s'ha de crear)
# Un seleccionador de bloc per a cada part
# Un seleccionador de radi
# Un seleccionador de densitat de triangles
# Una advertencia si s'espera que la cúpula no surti gaire bé
# Unes instruccions d'us
# Un seleccionador del nom de la comanda

# Ampliacions
# Un seleccionador de versio




ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "dark-blue", "green"

app = ctk.CTk()
app.title("DomeCraft")
app.geometry("400x200")  # Ancho x Alto


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

vcmd = app.register(solo_numeros)

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

checkboxCara.grid(row=0, column=0, padx=10, pady=10, sticky="w")
checkboxArista.grid(row=1, column=0, padx=10, pady=10, sticky="w")
checkboxEsquina.grid(row=2, column=0, padx=10, pady=10, sticky="w")

checkboxCara.pack(anchor="w")
checkboxArista.pack(anchor="w")
checkboxEsquina.pack(anchor="w")

#

anuchraTamaño = 23
entryCaraTamaño = ctk.CTkEntry(app)
entryCaraTamaño.configure(state="normal", width=anuchraTamaño)
entryCaraTamaño.grid(row=0, column=1, padx=10, pady=10, sticky="w")
entryCaraTamaño.configure(validate="key", validatecommand=(vcmd, "%P"))
entryCaraTamaño.bind("<Key>", limitar1caracter)

entryAristaTamaño = ctk.CTkEntry(app)
entryAristaTamaño.configure(state="normal", width=anuchraTamaño)
entryAristaTamaño.grid(row=1, column=1, padx=10, pady=10, sticky="w")
entryAristaTamaño.configure(validate="key", validatecommand=(vcmd, "%P"))
entryAristaTamaño.bind("<Key>", limitar1caracter)

entryEsquinaTamaño = ctk.CTkEntry(app)
entryEsquinaTamaño.configure(state="normal", width=anuchraTamaño)
entryEsquinaTamaño.grid(row=2, column=1, padx=10, pady=10, sticky="w")
entryEsquinaTamaño.configure(validate="key", validatecommand=(vcmd, "%P"))
entryEsquinaTamaño.bind("<Key>", limitar1caracter)


entryRadio = ctk.CTkEntry(app)
entryRadio.configure(state="normal", width=40)
entryRadio.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entryRadio.configure(validate="key", validatecommand=(vcmd, "%P"))
entryRadio.bind("<Key>", limitar3caracter)

entryDensidad = ctk.CTkEntry(app)
entryDensidad.configure(state="normal", width=anuchraTamaño)
entryDensidad.grid(row=3, column=1, padx=10, pady=10, sticky="w")
entryDensidad.configure(validate="key", validatecommand=(vcmd, "%P"))
entryDensidad.bind("<Key>", limitar1caracter)




# Ejecutar el bucle principal de la aplicación
app.mainloop()
