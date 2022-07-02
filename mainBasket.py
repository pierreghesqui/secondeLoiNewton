from vecteur import Vecteur
from modelisation import Modelisation
import cv2
import matplotlib.pyplot as plt
plt.close('all')

#On commence par régler les paramètres de base
m = 0.6
g = 9.81
deltat = 0.040
alpha = 0.05
modelisation = Modelisation()

#Ensuite, on règle la position initiale et la vitesse initiale du ballon :
position = Vecteur(5.5,4.6)
v = Vecteur(-4.6,4.8)
F = m*Vecteur(0,-g)-alpha*v

#On affiche l'image : 
modelisation.sauvegardeLesNouvellesDonnees(position,v)

for i in range(modelisation.nbImages):
    position = position + v*deltat
    v = v + deltat*F/m
    F = m*Vecteur(0,-g)-alpha*v
    modelisation.sauvegardeLesNouvellesDonnees(position,v)

modelisation.show()
