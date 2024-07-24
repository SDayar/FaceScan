import cv2
import matplotlib.pyplot as pyt
import numpy
haar_visage = "haarcascade_frontalface_default.xml"
cascade_visage = cv2.CascadeClassifier(cv2.data.haarcascades + haar_visage)

haar_yeux = "haarcascade_eye_tree_eyeglasses.xml"
cascade_yeux = cv2.CascadeClassifier(cv2.data.haarcascades + haar_yeux)

canal = cv2.VideoCapture(0) #Renvoie un booleen : True si le canal est ouvert, False sinon
Est_ouvert = True

while ouvert :
    video = canal.read()[1] #Récupère le vecteur du premier élément du canal
    print(canal.read()[0])
    visage = cascade_visage.detectMultiScale(video)
    yeux = cascade_yeux.detectMultiScale(video)
    visages_lst = list(visage)#Retourne les vecteurs des visages sous formes de listes
    yeux_lst = list(yeux)
    #Imprimerie
    if type(visages_lst) == list and type(yeux_lst) == list:
        for (x, y, w, h) in visages_lst:
            cv2.rectangle(video, (x, y), (x+w, y+h), color=(0, 0, 255))#Le visage est cadré en rouge
        for (a, b, c, d) in yeux_lst:
            cv2.rectangle(video, (a, b), (a+c, b+d), color=(0, 255, 0))#Les yeux sont cadrés en vert 
   
    cv2.imshow("Detecteur de Visage ", video)
    if cv2.waitKey(1) == 13:#Code ASCII pour entrer
        Est_ouvert = False

cv2.destroyAllWindows()