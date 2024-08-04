import tkinter as tk
from tkinter import filedialog as Fd
from tkinter.messagebox import showinfo as info, showwarning as warning
import customtkinter as ctk
import PIL.Image as plimg , PIL.ImageTk as plimgtk
import cv2 as cv 
import face_recognition as face_recogn
import numpy as np
import mysql.connector as cnx


                
               
               


class Parametre():
    def __init__(self, ecran, haar_vsgFile ="haarcascade_frontalface_default.xml", haar_yeuxFile="haarcascade_eye_tree_eyeglasses.xml"):
        self.ecran = ecran
        self.haar_vsg =  cv.CascadeClassifier(cv.data.haarcascades + haar_vsgFile) #-> Fichier Haar + data 
        self.haar_yeux = cv.CascadeClassifier(cv.data.haarcascades + haar_yeuxFile)
        self.ageProto, self.ageModel="age_deploy.prototxt", "age_net.caffemodel"
        self.genderProto, self.genderModel="gender_deploy.prototxt", "gender_net.caffemodel"
        self.connexion = cnx.connect(host="localhost", user="root", database="FaceId_DB", password="")
    
    def TelechargerFichier(self):
        """ self -> None"""
        types = (('Image files', '*.png'), ('Image files', '*.jpg'), ('Image files', '*.jpeg'))
        fichier = Fd.askopenfilename(title="Télécharger une photo", filetypes=types)
        match fichier:
            case '':
                pass
                
            case _ : #Expression par defaut
                self.FENETRE_IMG()
                #Traitement de l'image : de PIL à Tk
                self.__imgPIL = plimg.open(fichier)
                self.__imgPIL = self.__imgPIL.resize((int(self.fenetre_image.winfo_screenheight()*1/3), int(self.fenetre_image.winfo_screenwidth()*1/3)), plimg.Resampling.BOX)
                self.Informations_Img()
                self.__img = plimgtk.PhotoImage(image=plimg.fromarray(self.__imgCV))# -> On transtype l'image en Tk
                self.canvas.create_image((150,150), image=self.__img)
    def FENETRE_IMG(self):
        """ self -> None
        Crée la fenêtre de traitement du visage """
        #fenêtre
        self.fenetre_image = tk.Toplevel(self.ecran)
        self.fenetre_image.geometry("1000x700+{}+{}".format(self.fenetre_image.winfo_screenwidth() // 2 - 350, self.fenetre_image.winfo_screenheight() // 2 - 350))
        self.fenetre_image.title("FaceScan")
        self.fenetre_image.iconbitmap("logo.ico")
        self.fenetre_image.resizable(False, False)
        lbl = tk.Label(self.fenetre_image, bg="#dce4e8", width=self.fenetre_image.winfo_screenwidth(), height=self.fenetre_image.winfo_screenheight())
        lbl.pack()
        #Canvas
        self.canvas = ctk.CTkCanvas(self.fenetre_image,  height=int(self.fenetre_image.winfo_screenheight()*1/3), width=int(self.fenetre_image.winfo_screenwidth()*2/3))
        self.canvas.place(relx=0.0001,rely=0.2,anchor="w")
        #Ligne séparatrice
        
        #Etat de l'opération
        self.lbl_etat = ctk.CTkLabel(self.canvas, height=90, width=100, corner_radius=15, bg_color="#f4f4f4",font=("Arial",15), text_color="black")
        self.lbl_etat.place(relx=0.9, rely=0.3, anchor="ne")
        #Nombre de visages
        self.informations = ctk.CTkLabel(self.canvas, height=90, width=100, bg_color="#f4f4f4",font=("system",15), text_color="black")
        self.informations.place(relx=0.45, rely=0.3, anchor="n")
        #Informations à saisir 
        self.__prenom = ctk.CTkEntry(self.fenetre_image, bg_color="#dce4e8", fg_color="white", placeholder_text="Prenom", placeholder_text_color="gray")
        self.__prenom.place(relx=0.1, rely=0.55, anchor="w")

        self.__age = ctk.CTkEntry(self.fenetre_image, bg_color="#dce4e8", fg_color="white", placeholder_text="Age réel", placeholder_text_color="gray")
        self.__age.place(relx=0.3, rely=0.55, anchor="w")
        #Insertion des données
        self.bouton_donnee = ctk.CTkButton(self.fenetre_image,corner_radius=20, fg_color="white", bg_color="#dce4e8", hover_color="#de3137",  text="Enregistrer", command = self.InserIDVis)
        self.bouton_donnee.place(relx=0.01,rely=0.7, anchor="sw")
        #Changer de photo
        self.bouton_changer_photo = ctk.CTkButton(self.fenetre_image, corner_radius=20, fg_color="white", bg_color="#dce4e8", hover_color="#de3137",  text="Charger une autre photo", command = lambda : self.changer_photo())
        self.bouton_changer_photo.place(relx=0.5,rely=0.7, anchor="se")
        #consignes
        lbl_consignes = ctk.CTkLabel(self.fenetre_image, height=90, width=600, corner_radius=15, bg_color="#dce4e8", fg_color="white", font=("Arial",10) ,text="*Si un problème s'occure, veuillez vous referez aux consignes ci dessous. Attention, si le problème persiste nous vous prions de nous contacter au 0638012336. :\n-Assurez vous que le format de votre photo soit au format png, jpg ou jpeg. \n-Si le système n'arrive pas à detecter votre profil c'est qu'il y a un problème avec :  la qualité de votre image ou bien la taille de votre image\n-Le système a été conçu pour traiter qu'un seul profil à la fois. Assurez vous qu'il y ai qu'un seul profil dans votre image", text_color="black")
        lbl_consignes.place(relx=0.5, rely=0.9, anchor="s")
        #listes des individus enrégistrés. 
        cercleDraw = tk.Canvas(self.fenetre_image, width=200, height=200, highlightbackground="#dce4e8", bg="#dce4e8")
        cercleDraw.place(relx=0.7, rely=0.45)
        cercleDraw.create_oval((int(cercleDraw['width'])/2) - 100, (int(cercleDraw['height'])/2)-100 , (int(cercleDraw['width'])/2)+ 100, (int(cercleDraw['height'])/2) + 100 , fill="#de3137")
        self.CompteurBD = ctk.CTkLabel(self.fenetre_image, text=self.NbreFaces_DB(), font=("System",10), text_color="white", bg_color="#de3137", fg_color="#de3137")##de3137 -> Rouge et #dce4e8 -> Bleue
        self.CompteurBD.place(relx=0.73, rely=0.55)
    def NbreFaces_DB(self):
        """ self -> None
        Renvoie le nombre d'individus présents dans la BDD"""  
        return "OoPsss !\nSoyez le(la) premier(e)\nà vous enrégistrer !" if len(Donnee().dataEmpreinte())== 0 else " Déjà\n"+str(len(Donnee().dataEmpreinte()))+" profils enrégistrés dans\n notre Base de données !"
    def changer_photo(self):
        """self -> self
            Changement de photo"""
        types = (('Image files', '*.png'), ('Image files', '*.jpg'))
        fichier = Fd.askopenfilename(title="Télécharger une photo", filetypes=types)
        try:
            self.__imgPIL = plimg.open(fichier)
            self.__imgPIL = self.__imgPIL.resize((int(self.fenetre_image.winfo_screenheight()*1/3), int(self.fenetre_image.winfo_screenwidth()*1/3)), plimg.Resampling.BOX)
            self.Informations_Img()
            self.__img = plimgtk.PhotoImage(image=plimg.fromarray(self.__imgCV))# -> On transtype l'image en Tk
            self.canvas.create_image((150,150), image=self.__img)
            for widget in self.fenetre_image.winfo_children():
                widget.update()
                print(widget)
        except :
            pass
        
    def Informations_Img(self):
        """ self -> None
         Detecte les visages sur les photos -> Une assertion va devoir être levée sur plusieurs visages"""
        self.__imgCV = cv.cvtColor(np.array(self.__imgPIL), cv.COLOR_BGR2RGB)
        self.__ID = (face_recogn.face_encodings(self.__imgCV))#Très important -> ID du visage avec IMG en RGB
        if len(self.__ID) != 0: #Si un visage a été detécté
            self.__ID = self.__ID[0] #-> On récupère tout simplement l'empreinte du vecteur
            visages = self.haar_vsg.detectMultiScale(self.__imgCV)
            oeils = self.haar_yeux.detectMultiScale(self.__imgCV)
            
            self.coordonnee_vsg = list(visages)
            coordonnee_yeux = list(oeils) 
            #Une seule personne sur l'image -> Contrôler avec len(visages)
            if len(self.coordonnee_vsg) != 1 or len(coordonnee_yeux) != 2:#Un problème sur la détéction
                if len(coordonnee_yeux) != 2:
                    self.lbl_etat.configure(fg_color="#de3137", text="La détéction des yeux n'a pas été effective *")#Pour les yeux on devrait avoir deux coordonnées car chaque oeil a ses propres coordonnées
                    self.informations.configure(text=self.Detect_Age_genre()+"\n{} visage detecté".format(len(self.coordonnee_vsg)))#-> Le nombre de visages étudiés qu'il y'en est ou non
                elif len(self.coordonnee_vsg) != 1:
                    self.lbl_etat.configure(fg_color="#de3137", text="La détéction du visage n'a pas été effective *")
                    self.informations.configure(text=self.Detect_Age_genre()+"\n{} visages detectés".format(len(self.coordonnee_vsg)))#-> Le nombre de visages étudiés qu'il y'en est ou non
                elif len(self.coordonnee_vsg) != 1 and len(coordonnee_yeux) != 2: 
                    self.lbl_etat.configure(fg_color="#de3137", text="La détéction du visage et des yeux n'a pas été effective*")
            else :#Aucun problème sur la détection
                self.lbl_etat.configure(fg_color="green", text="La détéction du visage et des yeux a réussi")
                self.informations.configure(text=self.Detect_Age_genre()+"\n{} visage detecté".format(len(self.coordonnee_vsg)))#-> Le nombre de visages étudiés qu'il y'en est ou non
                self.Detect_Age_genre()
            for yT, xR,yB, xL in self.coordonnee_vsg:
                cv.rectangle(self.__imgCV, (yT, xR), (yT + yB, xR + xL), color=(0, 0, 255), thickness=2)
            for yT, xR,yB, xL in coordonnee_yeux:
                cv.rectangle(self.__imgCV, (yT, xR), (yT + yB, xR + xL), color=(0, 255, 255), thickness=2)
        else :#Aucun visage n'a été detécté
            self.lbl_etat.configure(fg_color="#de3137", text="Aucun visage n'a été detecté*")
            self.informations.configure(text="Informations:\n\t0 visage detecté ")#-> Le nombre de visages étudiés qu'il y'en est ou non
        self.__imgCV = cv.cvtColor(self.__imgCV, cv.COLOR_BGR2RGBA)#Dans tous les cas on renvoie l'image récolorée
    def Detect_Age_genre(self):
        """self -> None
         Il detecte l'âge et le genre correspondant à la photo"""
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689142744, 114.895847746)
        ageNet = cv.dnn.readNet(self.ageModel, self.ageProto)
        genreNet = cv.dnn.readNet(self.genderModel, self.genderProto)
        
        lst_age=["(4-6)", "(8-12)", "(15-20)", "(25-32)", "(38-43)", "(48-53)", "(60-100)"]
        lst_genre=["Homme", "Femme"]
        
        blob = cv.dnn.blobFromImage(self.__imgCV,1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genreNet.setInput(blob)
        genrePred=genreNet.forward()
        self.genre=lst_genre[genrePred[0].argmax()]

        ageNet.setInput(blob)
        agePred=ageNet.forward()
        age=lst_age[agePred[0].argmax()]
        informations ="Informations et estimations:\nAge = {}ans*\nGenre = {}".format(age,self.genre)
        return informations
        
    def fermeFenetre(self):
        """self -> None
         Permet de fermer l'écran"""
        try :
            for widget in self.ecran.winfo_children() :
                widget.destroy()
            self.ecran.destroy()
            #time.sleep(1)#On attend une seconde après la fermeture de la fenêtre principale
            Splash("splash.gif").ChargementCamera()
        except tk.TclError as e:
            warning("Fenetre principale non fermée", e)

      

    def InserIDVis(self):
        """ self -> None
        Insére l'ID dans la BD"""
        print(self.__prenom.get())
        
        try:
            if (self.__prenom.get() != "" and self.__age.get() != "" and len(self.coordonnee_vsg) == 1): 
                rqt_curs = self.connexion.cursor()
                chaine="["
                for x in self.__ID:
                    chaine+=str(x)+"  "
                chaine = chaine[:len(chaine)-2]+ "]" #-> Enlève le dernier espace
                try:
                    rqt_curs.execute("insert into faces(Marks,Age,Name,Gender) values('" +chaine+"'," + "'"+ self.__age.get()+"','"+ self.__prenom.get()+"','"+self.genre+"')")#-> Marks fait référence à l'empreinte
                    info("Enregistrement réussi !", "Bravo ! Vous êtes enrégistré(e). Veuillez révenir une prochaine fois pour découvrir vos informations. A tout de suite !")
                except:
                    rqt_curs.execute("insert into faces(Marks,Age,Name,Gender) values('" +chaine+"'," + "'"+ self.__age.get()+"','"+ self.__prenom.get()+"','Unknown')")#-> Marks fait référence à l'empreinte
                    info("Enregistrement réussi !", "Bravo ! Vous êtes enrégistré(e). Votre genre n'étant pas reconnu par notre modèle, vôtre genre a été enregistré comme Unknown.")
                    
                rqt_curs.close()
            else :
                info("Erreur !", "Les conditions ne sont pas réunies pour pouvoir ajouter ce profil. Réessayez avec d'autres informations !")
        except cnx.Error as erreur:
            warning("Erreur", str(erreur))      
    def fermeFenetre(self):
        """self -> None
         Permet de fermer l'écran"""
        try :
            for widget in self.ecran.winfo_children() :
                widget.destroy()
            self.ecran.destroy()
            #time.sleep(1)#On attend une seconde après la fermeture de la fenêtre principale
            Splash("splash.gif").Chargement("cam")
        except tk.TclError as e:
            warning("Fenetre principale non fermée", e)

    


    
            
         
    
        
class Main(Parametre):
    def __init__(self, ecran):
        super().__init__(ecran)
        self.labelBg = tk.Label(self.ecran)
        self.labelBg.pack(anchor="center", expand=True)
        self.files = ["background\\C1.mp4.","background\\C2.mp4", "background\\S1.mp4.", "background\\S2.mp4"]
        self.file = self.files[0]
        self.Bgfile= cv.VideoCapture(self.file)
        self.poli_titre= ("System",40)
        self.poli_ss_titre= ("System",15)
        self.poli_droit= ("System",12)
    def boutons(self) :
        #########Enregister un visage##############################################
        img_gallerie = plimg.open('gallerie.png')  
        self.btn_nouveau = ctk.CTkButton(self.ecran, corner_radius=20, fg_color="white", bg_color="#dce4e8", hover_color="#de3137", command =self.TelechargerFichier,  text_color="black", text="Télécharger", image=ctk.CTkImage(light_image=img_gallerie), compound=ctk.LEFT, font=self.poli_ss_titre)
        self.btn_nouveau.place(relx=0.3, rely=0.2, anchor='ne')
        ############################################################################
        ##############Reconnaissance faciale########################################
        img_faceid=plimg.open('face_id.png')
        self.btn_camera = ctk.CTkButton(self.ecran, corner_radius=20, fg_color="white", bg_color="#dce4e8", hover_color="#de3137", command= self.fermeFenetre , text_color="black", text="ID",  image=ctk.CTkImage(light_image=img_faceid), compound=ctk.LEFT, font=self.poli_ss_titre)
        self.btn_camera.place(relx=0.8, rely=0.5, anchor='sw')
        ############################################################################
    def iterateur(self, i, lis):
        if i >= len(lis) - 1: #Si on arrive au dernier indice, on relance la première vidéo 
            return 0
        else:
            return i+1
    def Disparaitre(self):
        for i in range(int(0.3*(self.ecran.winfo_width()))):#indice stop
            self.logo_droite.place(x=-i, y=0)
            self.logo_gauche.place(x=i, y=0)
            self.btn_nouveau.place(x=-i, y=0)
            self.btn_camera.place(x=i, y=0)
            self.ecran.update()
    def Apparaitre(self):
        for j in range(-int(0.3*(self.ecran.winfo_width())), 0):
            self.logo_droite.place(x=j*8, y=0)
            self.logo_gauche.place(x=-j*8, y=0)
            self.btn_nouveau.place(x=j*8, y=0)
            self.btn_camera.place(x=-j*8, y=0)
            self.ecran.update()
            
    #Background Video
    def BgVideo(self):
        _, Bgvideo = self.Bgfile.read()
        try :
            if Bgvideo is not None: #Si la lecture de la vidéo n'est pas terminé donc Bgvideo != None
                Bgvideo= cv.cvtColor(Bgvideo, cv.COLOR_BGR2RGB)
                #On calibre la taille des images à celles des images#
                imgpil = plimg.fromarray(Bgvideo)
                imgpil = imgpil.resize((self.ecran.winfo_width(), self.ecran.winfo_height()))# méthode winfo_.. -> retourne width/height de la fenêtre en int
                ########
                frame = plimgtk.PhotoImage(image=imgpil)
                self.labelBg.image= frame
                self.labelBg.config(image=frame)
                idlbl = self.labelBg.after(10, self.BgVideo)
            else : #Sinon On reinitialise la vidéo puis on rappelle la fonction
                suivant = self.files[self.iterateur(self.files.index(self.file), self.files)] #self.file est le chemin du fichier précédent
                self.Disparaitre()
                self.Apparaitre()
                if self.files.index(suivant) > 1 : #On modifie les widgets une fois le thème est devenu sombre
                    #############titres######################
                    self.logo_droite.configure(text_color="white", bg_color="black")
                    self.logo_gauche.configure(text_color="white", bg_color="black")
                    #self.droit.configure(bg_color="black", text_color="white")
                    #############boutons#####################
                    self.btn_camera.configure(bg_color="black")
                    self.btn_nouveau.configure(bg_color="black")
                else : #sinon
                    #############titres######################
                    self.logo_droite.configure(text_color="black", bg_color="#dce4e8")
                    self.logo_gauche.configure(text_color="black", bg_color="#dce4e8")
                    #self.droit.configure(bg_color="#91a099", text_color="black")
                    #############boutons#####################
                    self.btn_nouveau.configure(bg_color="#dce4e8")
                    self.btn_camera.configure(bg_color="#dce4e8")
                    
                self.Bgfile = cv.VideoCapture(suivant)
                self.file = suivant #On actualise le fichier en cours
                self.BgVideo()
                
               
        except tk.TclError as e:
            try : #Si ces variables existent
                if not(self.ecran.winfo_viewable()):#Si la fenêtre est fermée
                    self.labelBg.after_cancel(idlbl)
                    for c in self.ecran.children():
                        c.destroy() #On détruit tous les widgets de top fenêtre
                else :
                    warning("Erreur !", "Erreur d'affichage du la vidéo de fond")
            except tk.TclError as e:
                warning("Erreur !", "Erreur au niveau de la fenêtre principale")
    def Titres(self):
        """ self -> none
    crée les widgets"""
        self.boutons()
        ###############Logo######################################################
        self.logo_droite = ctk.CTkLabel(self.ecran, fg_color="transparent", corner_radius=0, text="FACE", font=self.poli_titre, bg_color= "#dce4e8", text_color="black")
        self.logo_droite.place(relx=0.2, rely=0.1, anchor='ne')
        
        self.logo_gauche= ctk.CTkLabel(self.ecran, fg_color="transparent", corner_radius=0, text="SCAN", font=self.poli_titre, bg_color= "#dce4e8", text_color="black")
        self.logo_gauche.place(relx=0.8, rely=0.4, anchor='sw')
        ##########################################################################
        
            
        ####################Droit et Legalité#######################################
       
        #self.droit = ctk.CTkLabel(self.ecran, bg_color="#91a099", text_color="black", text="SAIFIDINE © 2024 - All Rights Reserved - Projet sur la reconnaissance faciale.")
        #self.droit.place(relx=0.5, rely=1, anchor="s")
        #############################################################################
            







###################################################################################################################################################

if __name__== "__main__":
    top_fenetre = tk.Tk()
    top_fenetre.title("FaceScan")
    top_fenetre.iconbitmap("logo.ico")
    top_fenetre.geometry("800x600+{}+{}".format(top_fenetre.winfo_screenwidth() // 2 - 400, top_fenetre.winfo_screenheight() // 2 - 300))
    #top_fenetre.resizable(False, False)
    from camera import Splash
    from data import Donnee
    App = Main(top_fenetre)
    App.Titres()
    App.BgVideo()
    tk.mainloop()
    



    
   