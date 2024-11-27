import sys
import cv2
import numpy as np

# Extraer todos los contornos de la imagen
def get_all_contours(img):
    ref_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(ref_gray, 127, 255, 0)
    # Encontrar todos los contornos en la imagen umbralizada. Los valores
    # para el segundo y tercer parámetro están restringidos a un
    # número determinado de valores posibles.
    contours, hierarchy = cv2.findContours(thresh.copy(),
    cv2.RETR_LIST, \
    cv2.CHAIN_APPROX_SIMPLE)
    return contours

if __name__=='__main__':
    img = cv2.imread('imagen30.jpg')
    
    # Iterar sobre los contornos extraídos
    # Usando el método get_all_contours() anterior
    for contour in get_all_contours(img):
        factor = 0.01
        epsilon = factor * cv2.arcLength(contour, True)
        contour = cv2.approxPolyDP(contour, epsilon, True)
        # Extraer el casco convexo del contorno
        hull = cv2.convexHull(contour, returnPoints=False)
        # Extraer los defectos de convexidad del casco anterior
        # Un defecto de convexidad son las cavidades en los segmentos del casco
        defects = cv2.convexityDefects(contour, hull)
        
        if defects is None:
            continue
        
        # Dibujar líneas y círculos para mostrar los defectos
        for i in range(defects.shape[0]):
            start_defect, end_defect, far_defect, _ = defects[i, 0]
            start = tuple(contour[start_defect][0])
            end = tuple(contour[end_defect][0])
            far = tuple(contour[far_defect][0])
            cv2.circle(img, far, 5, [128, 0, 0], -1)
            cv2.drawContours(img, [contour], -1, (0, 0, 0), 3)
    

    cv2.imshow('Defectos de convexidad', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
