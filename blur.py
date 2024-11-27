import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Función para mostrar el mensaje usando Tkinter
def mostrar_mensaje_inicio():
    # Crear una ventana de Tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter (no la necesitamos)
    
    # Mostrar un mensaje en un cuadro de diálogo
    messagebox.showinfo(
        "Instrucciones", 
        "Este programa aplica filtros sobre una imagen.\n\n"
        "1. Filtro de identidad (sin cambios).\n"
        "2. Filtro 3x3 (suavizado leve).\n"
        "3. Filtro 5x5 (suavizado más fuerte).\n\n"
        "Presiona OK para continuar."
    )

    # Cerrar la ventana de Tkinter después de mostrar el mensaje
    root.destroy()

# Cargar la imagen
img = cv2.imread('input.jpg')
rows, cols = img.shape[:2]

# Definir los kernels
kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])  # Filtro de identidad
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0  # Filtro 3x3 promedio
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0  # Filtro 5x5 promedio

# Mostrar el mensaje de inicio
mostrar_mensaje_inicio()

# Mostrar la imagen original
cv2.imshow('Original', img)

# Aplicar los filtros
output = cv2.filter2D(img, -1, kernel_identity)
cv2.imshow('Filtro de identidad', output)

output = cv2.filter2D(img, -1, kernel_3x3)
cv2.imshow('Filtro 3x3', output)

output = cv2.filter2D(img, -1, kernel_5x5)
cv2.imshow('Filtro 5x5', output)

# Esperar la tecla y cerrar las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()
