import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Función para mostrar las instrucciones
def show_instructions():
    # Crear una ventana de mensaje usando tkinter
    root = tk.Tk()
    root.withdraw()  # Esto oculta la ventana principal de tkinter
    
    # Mostrar el cuadro de mensaje con instrucciones
    messagebox.showinfo("Instrucciones", 
                        "1. Este programa mostrará la imagen con los contornos de las formas detectadas.\n"
                        "2. Los contornos se suavizarán para hacerlos más precisos.\n"
                        "3. La imagen procesada se mostrará con los contornos suavizados dibujados.\n"
                        "4. Cuando termine, se cerrará la ventana de contornos con un clic.\n\n"
                        "Haz clic en 'Aceptar' para continuar.")

# Mostrar las instrucciones antes de procesar la imagen
show_instructions()

# Extracción de todos los contornos de la imagen
def get_all_contours(img):
    ref_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(ref_gray, 127, 255, 0)
    # Encontramos todos los contornos en la imagen límite. Los valores
    # para el segundo y tercer parámetro están restringidos a
    # un cierto número de posibles valores.
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )
    return contours

if __name__=='__main__':
    # Imagen que contiene las distintas formas
    img1 = cv2.imread('img.png')
    
    # Extraemos todos los contornos de la imagen
    input_contours = get_all_contours(img1)

    contour_img = img1.copy()
    smoothen_contours = []
    factor = 0.05

    # Encontramos los contornos más cercanos
    for contour in input_contours:
        epsilon = factor * cv2.arcLength(contour, True)
        smoothen_contours.append(cv2.approxPolyDP(contour, epsilon, True))
        
    # Dibujamos los contornos suavizados en la imagen
    cv2.drawContours(contour_img, smoothen_contours, -1, color=(0,0,0), thickness=3)

    # Mostramos la imagen con los contornos
    cv2.imshow('Contornos Suavizados', contour_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
