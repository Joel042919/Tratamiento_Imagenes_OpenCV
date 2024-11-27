import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Función para mostrar el mensaje de inicio
def mostrar_mensaje_inicio():
    # Crear una ventana de Tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter (no la necesitamos)

    # Mostrar un mensaje en un cuadro de diálogo
    messagebox.showinfo(
        "Instrucciones", 
        "Este programa encuentra el contorno más parecido entre dos imágenes.\n\n"
        "1. Aparece la imagen de referencia es la '7.png'. (esc para cerrar)\n"
        "2. Aparece la imagen de entrada es la '8.png'. (esc para cerrar)\n"
        "3. El programa encontrará el contorno más similar.\n"
        "4. Se mostrará el contorno más cercano en la imagen de entrada.\n\n"
        "Presiona OK para continuar."
    )

    # Cerrar la ventana de Tkinter después de mostrar el mensaje
    root.destroy()

# Función para mostrar la imagen de referencia en una ventana de OpenCV
def mostrar_imagen_referencia(img_ref):
    cv2.imshow("Imagen de Referencia", img_ref)
    cv2.waitKey(0)  # Esperar que el usuario presione una tecla
    cv2.destroyAllWindows()

# Función para obtener todos los contornos de una imagen
def get_all_contours(img): 
    ref_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh = cv2.threshold(ref_gray, 127, 255, 0) 
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )
    return contours

# Función para obtener el contorno de referencia basado en un área específica
def get_ref_contour(img): 
    contours = get_all_contours(img)
    for contour in contours: 
        area = cv2.contourArea(contour) 
        img_area = img.shape[0] * img.shape[1] 
        if 0.05 < area/float(img_area) < 0.8: 
            return contour 

# Ejecutar el programa
if __name__ == '__main__': 
    # Mostrar mensaje de inicio
    mostrar_mensaje_inicio()

    # Cargar las imágenes
    img1 = cv2.imread("7.png")  # Imagen de referencia
    img2 = cv2.imread("8.png")  # Imagen de entrada

    # Mostrar la imagen de referencia en una nueva ventana de OpenCV
    mostrar_imagen_referencia(img1)

    # Obtener el contorno de referencia
    ref_contour = get_ref_contour(img1)

    # Obtener todos los contornos de la imagen de entrada
    input_contours = get_all_contours(img2)

    # Inicializar la variable para el contorno más cercano
    closest_contour = None
    min_dist = None
    contour_img = img2.copy()

    # Dibujar todos los contornos en la imagen de entrada
    cv2.drawContours(contour_img, input_contours, -1, color=(0, 0, 0), thickness=3) 
    cv2.imshow('Contornos en imagen de entrada', contour_img)

    # Comparar cada contorno con el contorno de referencia
    for i, contour in enumerate(input_contours): 
        ret = cv2.matchShapes(ref_contour, contour, 3, 0.0)  # Comparar los contornos
        print(f"Contorno {i} tiene un valor de coincidencia de {ret}")
        
        # Si encontramos un contorno más cercano, actualizar la distancia mínima
        if min_dist is None or ret < min_dist:
            min_dist = ret 
            closest_contour = contour

    # Dibujar el contorno más cercano en la imagen de entrada
    cv2.drawContours(img2, [closest_contour], 0 , color=(0, 0, 0), thickness=3) 
    cv2.imshow('Coincidencia con contorno más cercano', img2)

    # Esperar que el usuario presione una tecla para cerrar
    cv2.waitKey(0)
    cv2.destroyAllWindows()
