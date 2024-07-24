import mysql.connector as cnx
import numpy as np
from tkinter.messagebox import showinfo as info
class Donnee():
    def __init__(self):
        self.__donneeID = []  
    def dataEmpreinte(self) :
        """ self -> None
        Connexion à la base de données et récupère les empreintes faciales"""
        CNX = cnx.connect(host="localhost", user="root", database="FaceId_DB", password="")
        try :
            rqt = CNX.cursor()
            rqt.execute("select * from faces")
            self.__IDDB = rqt.fetchall()
            i=0
            for colonne in self.__IDDB:
                tab = np.fromstring(colonne[3][1:-1], sep=" ")#-> colonne est un tuple (ligne de la table visages) et colonne[3] sa colonne empreinte
                self.__donneeID.append((tab.astype(np.float64), colonne[2], colonne[1]))#-> liste =[ (Empreinte, age, prenom) ]
                i+=1
            return self.__donneeID
        except cnx.Error as erreur :
            info("Erreur de connexion", "Une erreur de connexion est survenu !")
        finally:
            if CNX.is_connected():
                CNX.close()