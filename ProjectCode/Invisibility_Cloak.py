import cv2
import numpy as np
import time

print("Bienvenido a hogwarts, ve por tu capa de invisibilidad!!")
#Captura del video
cap = cv2.VideoCapture(0)

# Tiempo de adaptacion al entorno y inicializacion de variables
time.sleep(3)
background=0

print("Capturando fondo...")
# Captura y almacenamiento del fondo estático 
# (captura de multiple frames para adaptar al entorno y reduccion de ruido)
for i in range(60):
    ret,background = cap.read()
print("Capturando fondo. Terminado!!")
print("Ponte frente a la camara con tu capa. Presiona 's' para salir...")

# Captura del video frame por frame mientras exista
while(cap.isOpened()):
    # Frame del video
    ret, img = cap.read()
    
    # Verificacion
    if not ret:
        break
    
    # Convierte el color del frame RGB a HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ------- Generacion de las mascara para deteccion de color rojo -------
    lower_red = np.array([0,150,40], np.uint8)
    upper_red = np.array([8,255,255], np.uint8)
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,150,40], np.uint8)
    upper_red = np.array([180,255,255], np.uint8)
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

    #mask = cv2.add(mask1, mask2)
    mask = mask1+mask2
    # ----------------------------------------------------------------------
    
    # Aplica Erocion y dilatacion al objeto detectado de color rojo
    mask_medianBlur = cv2.medianBlur(mask, 13)
    #mask_aperture = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations = 2)
    mask_dilate = cv2.dilate(mask_medianBlur,np.ones((3,3),np.uint8),iterations = 2)

    mask_invert = cv2.bitwise_not(mask_dilate)

    # Elimina el objeto de color rojo en el frame
    delete_object = cv2.bitwise_and(img,img,mask=mask_invert)
    
    # Muestra el fondo estático donde se encuentra el objeto de color rojo en el frame
    background_object = cv2.bitwise_and(background,background,mask=mask_dilate)
    
    # Suma ponderada entre el objeto eliminado y fondo estático
    ## Muestra el fondo estatico donde se elimino el objeto de color rojo en el frame
    final_output = cv2.addWeighted(delete_object,1,background_object,1,0)
    
    #Muestra el frame
    cv2.imshow('Original',img)
    cv2.imshow('Final',final_output)

    if cv2.waitKey(10) & 0xFF == ord('s'):
        break
    
