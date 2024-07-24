import cv2
import matplotlib.pyplot as pyt
import numpy
import tkinter as tk
import customtkinter as ctk
import PIL.Image, PIL.ImageTk
haar_visage = "haarcascade_frontalface_default.xml"
cascade_visage = cv2.CascadeClassifier(cv2.data.haarcascades + haar_visage)


haar_yeux = "haarcascade_eye_tree_eyeglasses.xml"
cascade_yeux = cv2.CascadeClassifier(cv2.data.haarcascades + haar_yeux)
global canal
canal = cv2.VideoCapture(0) #Renvoie un booleen : True si le canal est ouvert, False sinon
fenetre = tk.Tk()
fenetre.title("Détecteur de Visage")
ecranLbl = tk.Label(fenetre)
ecranLbl.grid(row = 0, column = 0, columnspan = 12, rowspan = 1, padx=(10, 10), pady= (20, 30), sticky="E")
ecranLbl.pack()
def ecran():
    """None -> None"""
    if canal.isOpened() :
 #Récupère le vecteur du premier élément du canal
        video = canal.read()[1]
        video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        visage = cascade_visage.detectMultiScale(video)
        yeux = cascade_yeux.detectMultiScale(video)
        visages_lst = list(visage)#Retourne les vecteurs des visages sous formes de listes
        yeux_lst = list(yeux)
    #Imprimerie des visages localisés
        if type(visages_lst) == list and type(yeux_lst) == list:
            for (x, y, w, h) in visages_lst:
                
                cv2.rectangle(video, (x, y), (x+w, y+h), color=(255, 0, 0))#Le visage est cadré en rouge
            for (a, b, c, d) in yeux_lst:
                cv2.rectangle(video, (a, b), (a+c, b+d), color=(0, 255, 0))#Les yeux sont cadrés en vert
                
                
                  
#########PIL & TK################
        h = canal.get(cv2.CAP_PROP_FRAME_HEIGHT) #Capture la longeur ed la video
        w = canal.get(cv2.CAP_PROP_FRAME_WIDTH)
        dimensions = str(int(w))+"x"+str(int(h)) #Dimensions de l'affichage du vidéo
        fenetre.geometry(dimensions)
        imgpil = PIL.Image.fromarray(video)
        imgtk = PIL.ImageTk.PhotoImage(image = imgpil)
        ecranLbl.imgtk = imgtk
        ecranLbl.configure(image=imgtk)
        ecranLbl.after(5, ecran)
    else :
        erreur = t
        fenetre.title("Erreur de lancement ! ")
        fenetre.geometry("380x280")
        police = "Arial", 16, "bold"
        message = ctk.CTkLabel(fenetre, text = "Oups! Veuillez rallumer votre caméra !", font=police, text_color="red")
        message.grid(row = 0, column = 1, columnspan = 12, rowspan = 1, padx=(10, 10), pady= (20, 30), sticky="e")
    
                   
#Imprimerie des vidéos
ecran()
fenetre.mainloop()