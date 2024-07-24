import tkinter as tk
import customtkinter as ctk
from tkinter.messagebox import showinfo as info, showwarning as warning
import cv2 as cv
from PIL import Image as plimg, ImageTk as plimgtk, ImageSequence as ImgSequence
import face_recognition as face_recogn
from datetime import datetime
from threading import Thread
from time import sleep
if __name__ != "main":
    from data import Donnee
    from top import Parametre
class Splash():
    def __init__(self, gifChemin):
        self.splashfile = plimg.open(gifChemin)
    def splash(self,cible):
        """None -> None
        Gère loading de fenêtre en fenêtre"""
        self.Splash_fen = tk.Tk()
        self.Splash_fen.overrideredirect(True)
        self.Splash_fen.geometry("500x500+{}+{}".format(self.Splash_fen.winfo_screenwidth()// 2 - 250, self.Splash_fen.winfo_screenheight()//2 - 250))#->Centre le splash au milieu de la fenêtre 
        self.Splash_fen.resizable(False , False)
        self.lblSpl = ctk.CTkLabel(self.Splash_fen, text=None)
        self.lblSpl.pack()
        self.lbl_text = ctk.CTkLabel(self.Splash_fen, text="Chargement...", bg_color="#efefef", font=("System",15), text_color="black")#efefef -> background du splash
        self.lbl_text.place(relx=0.35, rely=0.8)
        self.splashframes = [plimgtk.PhotoImage(frame) for frame in ImgSequence.Iterator(self.splashfile)]
        self.UpdateSplash(0, cible)
    def UpdateSplash(self, indice_frame, cible):
        """ int -> None
            Met à jour chaque frame du gif"""
        if cible == "cam":#Si la cible est le fichier caméra
            print("cam")
            if indice_frame < (len(self.splashframes)-1):#Si on n'a pas encore atteint la dernière frame
                self.lblSpl.configure(image=self.splashframes[indice_frame])#-> On met à jour le label en lui affectant le nouveau frame grâce à son indice
                self.idlbl = self.lblSpl.after(10, self.UpdateSplash, (indice_frame+1),"cam")#-> modulo n car on veut être sur de revenir à l'indice 0
                if indice_frame == int((len(self.splashframes)-1)//4) : #Quand on est à 25% des nombre de frame du splash
                    try :
                        self.lbl_text.configure(text="Ouverture de la caméra...")
                        global capture
                        capture = cv.VideoCapture(0)
                    except cv.Error as e : #S'il y a un problème, on stop le loading en allant après le dernier frame
                        warning("Allumez votre caméra ", e)
                        indice_frame = len(self.splashframes)+1 #Marqueur qui permet de savoir qu'il y a un problème
                elif indice_frame ==  int(6*(len(self.splashframes)-1)//10):#Quand on est au 60% des nombre de frame du splash
                    try :
                        self.lbl_text.configure(text="Chargement des données...")
                        Donnee().dataEmpreinte()
                        self.lbl_text.configure(text="Bonne séance !")
                            
                    except  : #S'il y a un problème, on stope le loading en allant après le dernier frame
                        indice_frame = len(self.splashframes)+1

            else :
                self.lblSpl.after_cancel(self.idlbl)#On détruit l'événement de lecture des frames du gif
                self.Splash_fen.destroy()
                if indice_frame != len(self.splashframes)+1:
                    if cible == "cam":
                        Webcam().ouvre_webcam()
                else :
                        warning("Erreur de chargement !", "Une erreur est survenue !")
        
                
    def Chargement(self, cible):#cible -> target 
        self.splash(cible)
     

    
        
        
class Webcam():
    def __init__(self, haarVisagefile="haarcascade_frontalface_default.xml"):
        self.haarVsg= cv.CascadeClassifier(cv.data.haarcascades + haarVisagefile)
        self.__donneeID = Donnee().dataEmpreinte()
    def eteint(self):
        capture.release()
    def fenetre(self):
        self.__fenetre_camera = tk.Tk()
        self.__fenetre_camera.title("FaceScan")
        self.__fenetre_camera.iconbitmap("logo.ico")
        self.__fenetre_camera.geometry("1200x700+{}+{}".format(self.__fenetre_camera.winfo_screenwidth()//2 - 600, self.__fenetre_camera.winfo_screenheight()//2 - 390))
        self.__fenetre_camera.resizable(height=False, width=False)
        lbl = tk.Label(self.__fenetre_camera,width=self.__fenetre_camera.winfo_screenwidth(), height=self.__fenetre_camera.winfo_screenheight(), bg="#efefef")
        lbl.pack()
        multitab = ctk.CTkTabview(self.__fenetre_camera, corner_radius=20, width=int(self.__fenetre_camera.winfo_screenwidth()*1/5), height=int(self.__fenetre_camera.winfo_screenheight()/5), bg_color="#efefef", fg_color="#efefef", segmented_button_fg_color="#efefef", segmented_button_selected_color="#de3137",segmented_button_selected_hover_color="#de3137")
        multitab.place(relx=0.7, rely=0.01)
        multitab.add("Nom - Age")
        multitab.add("Historiques")
        self.textBox_tab1= ctk.CTkTextbox(multitab.tab("Nom - Age"), text_color="black", bg_color="#efefef", fg_color="white", corner_radius=20, width=int(self.__fenetre_camera.winfo_screenwidth()*1/5), height=int(self.__fenetre_camera.winfo_screenheight()/5), font=("Arial",15))
        self.textBox_tab1.pack()
        self.textBox_tab2= ctk.CTkTextbox(multitab.tab("Historiques"), text_color="black", bg_color="#efefef", fg_color="white",corner_radius=20, width=int(self.__fenetre_camera.winfo_screenwidth()*1/5), height=int(self.__fenetre_camera.winfo_screenheight()/5), font=("Arial",15))
        self.textBox_tab2.pack()
        cercleDraw = tk.Canvas(self.__fenetre_camera, width=300, height=300, highlightbackground="#efefef", bg="#efefef")
        cercleDraw.place(relx=0.7, rely=0.5)
        cercleDraw.create_oval((int(cercleDraw['width'])/2) - 150, (int(cercleDraw['height'])/2)-150 , (int(cercleDraw['width'])/2)+ 150, (int(cercleDraw['height'])/2) + 150 , fill="#dce4e8")
        self.Compteurlbl = ctk.CTkLabel(self.__fenetre_camera, text="0", font=("System",60), text_color="#de3137", bg_color="#dce4e8", fg_color="#dce4e8")##de3137 -> Rouge et #dce4e8 -> Bleue
        self.Compteurlbl.place(relx=0.81, rely=0.63)
        nbrePersonne = ctk.CTkLabel(self.__fenetre_camera, text="Individu(s)", font=("System",20), text_color="black", bg_color="#dce4e8", fg_color="#dce4e8")     #efefef
        nbrePersonne.place(relx=0.8, rely=0.76)
        self.labelcam = ctk.CTkLabel(self.__fenetre_camera, width=650, text=None, height=350, bg_color="#dce4e8")
        self.labelcam.place(relx=0.1, rely=0.01)
        #dictionnaire date
        Dict_mois={"January":"Janvier", "February":"Fevrier", "March":"Mars", "April":"Avril","May":"Mai", "June":"Juin", "July":"Juillet", "August":"Août", "September":"Septembre", "October":"Octobre", "November":"Novembre", "December":"Décembre"}
        Dict_jour={"Monday":"Lundi","Tuesday":"Mardi", "Wednesday":"Mercredi", "Thursday":"Jeudi","Friday":"Vendredi", "Saturday":"Samedi", "Sunday":"Dimanche"}
        jour = Dict_jour[datetime.now().strftime("%A")]
        mois= Dict_mois[datetime.now().strftime("%B")]
        
        lbl_info = ctk.CTkLabel(self.__fenetre_camera, width=650, text="Prise du "+ jour+datetime.now().strftime(" %d ")+mois+" 2024",  font=("System",16), corner_radius=50, text_color="black", bg_color="#efefef", fg_color="white")
        lbl_info.place(relx=0.1, rely=0.7)
        self.lbl_info = ctk.CTkLabel(self.__fenetre_camera, width=650, height=160, text="Lancée il y a Omin", corner_radius=20, text_color="black", bg_color="#efefef", fg_color="white")
        self.lbl_info.place(relx=0.1, rely=0.75)
        
   
    def ouvre_webcam(self):
        self.fenetre()
        self.__montre_webcam()
        if self.ouvert:#Si la caméra est ouverte 
            self.__video = cv.resize(self.__video, (650,350))
        #self.Reconnaissance()
    def __montre_webcam(self):
        """ self ->None 
         Capture la caméra"""
        i = 0
        self.ouvert, self.__video = capture.read()
        while self.ouvert :
            try : 
                self.Compteurlbl.configure(text=str(len(face_recogn.face_locations(self.__video))))#-> Nombre de personnes identifiées
            except :
                self.Compteurlbl.configure(text="0")
            for self.yT, self.xR, self.yB, self.xL in face_recogn.face_locations(self.__video):#start point(top-left) -> end-point(bottom-right)
             
                cv.rectangle(self.__video, (self.xL, self.yT),(self.xR, self.yB) , color=(255, 0, 0), thickness=2)
                if len(face_recogn.face_locations(self.__video)) > 0:
                        inconnu = face_recogn.face_encodings(self.__video, [(self.yT, self.xR, self.yB, self.xL)])
                        for connu in self.__donneeID:#-> connu est un tuple contenant Empreinte, Age puis Prenom
                            if face_recogn.compare_faces([connu[0]], inconnu[0], tolerance=0.7)[0] and connu[2] not in (self.textBox_tab2.get("0.0", "end")):#Si le vecteur est présent dans la BD et qu'il n'est pas présent dans le boite d'affichage et pas présent dans la boite de historique.A noter que la tolérance est plus stricte
                                self.textBox_tab1.insert("1.0"+str(i),connu[2]+" - "+ connu[1]+"ans\n")#-> Présent directement
                                self.textBox_tab2.insert("2.0"+str(i), str(i+1)+ ") "+ connu[2]+" - "+ connu[1]+"ans à "+datetime.now().strftime("%Hh: %Mmin")+"\n")#-> Historiques
                                i+=1
                            else : 
                                break
                else :
                    break
                
            imgtk = plimgtk.PhotoImage(image=plimg.fromarray(self.__video))
            self.labelcam.imgtk = imgtk
            self.labelcam.configure(image=imgtk)
            self.ouvert, self.__video = capture.read()
            self.__video = cv.cvtColor(self.__video, cv.COLOR_BGR2RGB)
            self.__fenetre_camera.update()
        #Sinon on ferme la fenêtre secondaire et on avertit
        capture.release()
        self.labelcam.configure(bg_color="black", text="Caméra fermée !", text_color="red")
               
            
                    
               
                
   
            

        






