import sys
import os

def rutaRelativa(relative_path):
    #Devuelve la ruta correcta del archivo, considerando PyInstaller.
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



