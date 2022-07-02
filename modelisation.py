import cv2
from vecteur import Vecteur
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import imageio

class Modelisation:
    def __init__(self):
        def click_event(event, x, y, flags, params):
            
            f = open("etalonnage.txt",'a')
            if event == cv2.EVENT_LBUTTONDOWN:
                #print(x,y)
                f.write(str(x) +',' )     
                f.write(str(y)+',') 
            f.close()
        self.ecranLargeur = 1920
        self.ecranHauteur = 1080
        f = open("etalonnage.txt",'r+')
        self.imageNb = 11
        self.image  = cv2.imread("frames/basket/frame11.png")
        self.nbLignes = self.image.shape[0]
        self.nbColonnes = self.image.shape[1]
        
        
        self.ratioFenetre =self.nbColonnes/self.nbLignes
        #print ("l'image contient ", self.nbLignes, "lignes et " ,self.nbColonnes, " colonnes")
        filesize = os.path.getsize("etalonnage.txt")
        if filesize==0:
            cv2.namedWindow('mon image', cv2.WINDOW_NORMAL)
            cv2.moveWindow('mon image', int(self.ecranLargeur/2),10)
            cv2.resizeWindow('mon image', int(self.ecranHauteur*0.75*self.ratioFenetre), int(self.ecranHauteur*0.75))
            cv2.setWindowProperty('mon image', cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow('mon image', self.image)   
            cv2.setMouseCallback('mon image', click_event) 
            cv2.waitKey()
            cv2.destroyAllWindows()
            with open("etalonnage.txt", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
            
            nbPixel = int(((int(currentline[3])-int(currentline[1]))**2+(int(currentline[2])-int(currentline[0]))**2)**0.5)
            distanceMetre= float(input("Quelle est la distance mesurée ?"))
            self.pixelSize = distanceMetre/nbPixel
            f = open("etalonnage.txt",'a')
            f.truncate(0)
            f.write(str(self.pixelSize))
            
        else:
            with open("etalonnage.txt", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
            self.pixelSize = float(currentline[0])
        _, _, files = next(os.walk("frames/basket"))
        file_count = len(files)
        self.nbImages = file_count-1
        f.close()
        self.positions = []
        self.vitesses = []
        
    def sauvegardeLesNouvellesDonnees(self,position,vitesse):
        self.positions.append(position)
        self.vitesses.append(vitesse)
        
    def show(self):
        with imageio.get_writer('modelisation.gif', mode='I',fps=2) as writer:
            listFichier = os.listdir('frames/basket')
            #print(listFichier)
            for i  in range(self.nbImages):
                self.image = imageio.imread('frames/basket/'+str(i))
                self.dessineCroix(self.positions[i])
                writer.append_data(self.image)
                
        
    def metersToPixel (self,lc):
        pix = lc/self.pixelSize
        pix = Vecteur(int(pix.x),int(pix.y))
        return pix
    
    def pixelToMeters (self,pix):
        lc = pix*self.pixelSize
        return lc
    
    def dessineCroix(self,position) :
        #print(position)
        pix = self.metersToPixel(position)
        pix = Vecteur(pix.x,self.nbLignes-pix.y)
        #print(pix)
        tailleCroix = 3
        color = (255,255,255)
        cv2.line(self.image, (pix.x-tailleCroix,pix.y-tailleCroix), (pix.x+tailleCroix,pix.y+tailleCroix ), color, 2)
        cv2.line(self.image, (pix.x+tailleCroix,pix.y-tailleCroix ), (pix.x-tailleCroix,pix.y+tailleCroix ), color, 2)
        cv2.putText(self.image,"Modele", (pix.x,pix.y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 1,cv2.LINE_AA)

    
     
  