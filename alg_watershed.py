import cv2
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Función para mostrar las instrucciones
def show_instructions():
    # Crear una ventana de mensaje usando tkinter
    root = tk.Tk()
    root.withdraw()  # Esto oculta la ventana principal de tkinter
    
    # Mostrar el cuadro de mensaje con instrucciones
    messagebox.showinfo("Instrucciones", 
                        "1. Este programa mostrará 4 imágenes procesadas:\n"
                        "   a. Imagen original\n"
                        "   b. Imagen binarizada (umbralizada)\n"
                        "   c. Transformada de distancia\n"
                        "   d. Resultado de segmentación usando Watershed\n"
                        "2. Cada imagen será presentada en una ventana para que las puedas observar.\n"
                        "3. Al finalizar, se cerrará la ventana de imágenes con un clic.\n\n"
                        "Haz clic en 'Aceptar' para continuar.")

# Mostrar las instrucciones antes de procesar la imagen
show_instructions()

# Cargar la imagen
img = cv2.imread("water_coins.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Filtro de suavizado
filtro = cv2.pyrMeanShiftFiltering(img, 20, 40)

# Convertir a escala de grises
gray = cv2.cvtColor(filtro, cv2.COLOR_BGR2GRAY)

# Umbralización de la imagen
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Encontrar los contornos
contornos, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar contornos pequeños
buracos = []
for con in contornos:
    area = cv2.contourArea(con)
    if area < 1000:
        buracos.append(con)

# Dibujar los contornos en la imagen umbralizada
cv2.drawContours(thresh, buracos, -1, 255, -1)

# Transformada de distancia
dist = ndi.distance_transform_edt(thresh)
dist_visual = dist.copy()

# Encontrar los máximos locales
local_max = peak_local_max(dist, min_distance=20, labels=thresh)

# Crear una imagen de marcadores del mismo tamaño que 'thresh'
markers = np.zeros_like(thresh, dtype=int)

# Asignar un valor de marcador único a cada máximo local
for i, (y, x) in enumerate(local_max):  # local_max contiene las coordenadas (y, x)
    markers[y, x] = i + 1  # Asignar un valor único (i + 1) a cada pico local

# Etiquetas de la segmentación
labels = watershed(-dist, markers, mask=thresh)

# Títulos para las imágenes
titulos = ['Imagen Original', 'Imagen Binaria', 'Transformada de Distancia', 'Segmentación Watershed']
imagens = [img, thresh, dist_visual, labels]

# Mostrar las imágenes
fig = plt.gcf()
fig.set_size_inches(16, 12)
for i in range(4):
    plt.subplot(2, 2, i + 1)
    if i == 3:
        cmap = "jet"
    else:
        cmap = "gray"
    plt.imshow(imagens[i], cmap)
    plt.title(titulos[i])
    plt.xticks([]), plt.yticks([])

plt.show()
