import customtkinter as ctk
from colocarBloques import creacionDomo
from tkinter import filedialog
from listas import *

from compilacion import rutaRelativa

import threading
import os

# Falta fer:
# Verificar que si fiques 0 de gruix no genera aquella part
# Una quadro de text per a escriure el que s'ha de fer
# Bloquejar els botons mentres es genera tot


# Ampliacions
# Un seleccionador de versió
# Un botó per a eliminar el datapack
# Un seleccionador per a fixar un bloc per a cada part
# Canviar idioma
# Unes instruccions d'us
# Una advertencia si s'espera que la cúpula no surti gaire bé


ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "dark-blue", "green"

completo = -1

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DomeCraft")
        self.geometry("800x600")  # Ancho x Alto
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

        

        def actualizarBarras(valor:float):
            global completo
            print(valor)
            if completo==-1 and valor==0:
                completo=0
                print("CAMBIANDO 0")
      
            elif completo==0:
                if valor==0:
                    completo=1
                    barraEsquina.set(1)
                    print("CAMBIANDO 1")
                else:
                    barraEsquina.set(valor)

            elif completo ==1:
                if valor == 0:
                    completo=2
                    barraArista.set(1)
                    print("CAMBIANDO 2")
                else:
                    barraArista.set(valor)

            elif completo==2:
                if valor==0:
                    completo=-1
                    barraCara.set(1)
                    print("CAMBIANDO -1")
                else:
                    barraCara.set(valor)


        def comprovacionesFinales():
            listaErrores = []
            carpeta = label_resultado.cget("text")
            if carpeta=="":
                listaErrores.append("Tienes que poner algún nombre")
            d = entryDensidad.get()
            if d=="":
                listaErrores.append("Tienes introducir alguna densidad")    
            r = entryRadio.get()
            c = entryCaraTamaño.get()
            a = entryAristaTamaño.get()
            e = entryEsquinaTamaño.get()
            nombre = entryNombre.get()
            if nombre=="":
                listaErrores.append("Tienes que poner algún nombre")
            return listaErrores


        def guardarDireccion(direccion):
            fitxer = rutaRelativa("doc/carpeta.txt")
            with open(fitxer, "w") as file:
                file.write(direccion)

        def ejecutarPrograma():

            correcto = comprovacionesFinales()

            if len(correcto)==0:
                carpeta = label_resultado.cget("text")
                guardarDireccion(carpeta)
                d = int(entryDensidad.get())
                r = int(entryRadio.get())
                c = int(entryCaraTamaño.get())
                a = int(entryAristaTamaño.get())
                e = int(entryEsquinaTamaño.get())
                nombre = entryNombre.get()
                
            else:
                for i in correcto:
                    print(i)

            threading.Thread(target=creacionDomo, args=(d,r,c,a,e,carpeta,nombre, actualizarBarras, True), daemon=True).start()


        def seleccionar_carpeta():
            carpeta = filedialog.askdirectory(title="Seleccionar una carpeta")  # Abrir el cuadro de diálogo
            if carpeta:  # Si se seleccionó una carpeta
                label_resultado.configure(text=carpeta)
            else:
                label_resultado.configure(text="No se seleccionó ninguna carpeta.")




        # Crear un botón que abrirá el cuadro de diálogo para seleccionar una carpeta
        boton_seleccionar = ctk.CTkButton(self, text="Seleccionar Carpeta", command=seleccionar_carpeta)
        boton_seleccionar.grid(row=0, column=0, padx=10, pady=10, sticky="w")


        # Crear un label para mostrar la carpeta seleccionada
        rutaCarpetaAntarior = rutaRelativa("doc/carpeta.txt") #Segurament millor fer un CSV y guardar diferents carpetes
        if not os.path.exists(rutaCarpetaAntarior):
            label_resultado = ctk.CTkLabel(self, text="No se ha seleccionado ninguna carpeta.")
        else:
            with open(rutaCarpetaAntarior, "r", encoding="utf-8") as file:
                carpetaAntarior = file.readline().strip()
                label_resultado = ctk.CTkLabel(self, text=carpetaAntarior)

            
        label_resultado.grid(row=0, column=2, padx=10, pady=10, sticky="w")


        # Crear una CheckBox con texto al lado
        checkboxCara = ctk.CTkLabel(self, text="Caras")
        checkboxArista = ctk.CTkLabel(self, text="Aristas")
        checkboxEsquina = ctk.CTkLabel(self, text="Esquina")


        checkboxCara.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        checkboxArista.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        checkboxEsquina.grid(row=3, column=0, padx=10, pady=10, sticky="w")


        anuchraTamaño = 23
        entryCaraTamaño = ctk.CTkEntry(self)
        entryCaraTamaño.configure(state="normal", width=anuchraTamaño)
        entryCaraTamaño.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        entryCaraTamaño.bind("<Key>", limitar1caracter)

        entryAristaTamaño = ctk.CTkEntry(self)
        entryAristaTamaño.configure(state="normal", width=anuchraTamaño)
        entryAristaTamaño.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        entryAristaTamaño.bind("<Key>", limitar1caracter)

        entryEsquinaTamaño = ctk.CTkEntry(self)
        entryEsquinaTamaño.configure(state="normal", width=anuchraTamaño)
        entryEsquinaTamaño.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        entryEsquinaTamaño.bind("<Key>", limitar1caracter)


        barraCara = ctk.CTkProgressBar(self)
        barraCara.set(0)
        barraCara.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        barraArista = ctk.CTkProgressBar(self)
        barraArista.set(0)
        barraArista.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        barraEsquina = ctk.CTkProgressBar(self)
        barraEsquina.set(0)
        barraEsquina.grid(row=3, column=2, padx=10, pady=10, sticky="w")



        frameRadio = ctk.CTkFrame(self)
        frameRadio.grid(row=4, column=0, padx=10, pady=10)

        textRadio = ctk.CTkLabel(frameRadio,text="Radio")
        textRadio.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        entryRadio = ctk.CTkEntry(frameRadio)
        entryRadio.configure(state="normal", width=40)
        entryRadio.bind("<Key>", limitar3caracter)
        entryRadio.grid(row=1, column=2)


        frameDensidad = ctk.CTkFrame(self)
        frameDensidad.grid(row=4, column=1, padx=10, pady=10)

        textDensidad = ctk.CTkLabel(frameDensidad,text="Frecuencia geodésica")
        textDensidad.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        entryDensidad = ctk.CTkEntry(frameDensidad)
        entryDensidad.configure(state="normal", width=anuchraTamaño)
        entryDensidad.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        entryDensidad.bind("<Key>", limitar1caracter)

        frameFinal = ctk.CTkFrame(self)
        frameFinal.grid(row=4,column=2)

        entryNombre = ctk.CTkEntry(frameFinal, placeholder_text="Nombre",)
        entryNombre.grid(row=0,column=0)

        botonGenerar = ctk.CTkButton(frameFinal, text="Generar", fg_color="green", command=ejecutarPrograma)
        botonGenerar.grid(row=0, column=1)

# Ejecutar el bucle principal de la aplicación
app = App()
app.mainloop()
