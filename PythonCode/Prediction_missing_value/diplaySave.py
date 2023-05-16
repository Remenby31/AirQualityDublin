import matplotlib.pyplot as plt
import os

def afficherMatrice3D(matrice3D):
    # affichage de la matrice 3D
    for i in range(0, matrice3D.shape[0]):
        plt.clf()
        plt.imshow(matrice3D[i])
        plt.show()

def afficherMatrice3D_2(matrice3D_1, matrice3D_2, Lmatrice3D_Name):
    # affichage de la matrice 3D
    for i in range(0, matrice3D_1.shape[0]):
        plt.clf()
        plt.subplot(1, 2, 1)
        plt.title(Lmatrice3D_Name[0])
        plt.imshow(matrice3D_1[i])
        plt.subplot(1, 2, 2)
        plt.title(Lmatrice3D_Name[1])
        plt.imshow(matrice3D_2[i])
        plt.show()

def afficherMatrice3D_3(matrice3D_1, matrice3D_2, matrice3D_3, Lmatrice3D_Name):
    # affichage de la matrice 3D
    for i in range(0, matrice3D_1.shape[0]):
        plt.clf()
        plt.subplot(1, 3, 1)
        plt.title(Lmatrice3D_Name[0])
        plt.imshow(matrice3D_1[i])
        plt.subplot(1, 3, 2)
        plt.title(Lmatrice3D_Name[1])
        plt.imshow(matrice3D_2[i])
        plt.subplot(1, 3, 3)
        plt.title(Lmatrice3D_Name[2])
        plt.imshow(matrice3D_3[i])
        plt.show()

def sauvegarderPNG(matrice3D, nomDossier: str):
    # sauvegarde de la matrice 3D

    #creation du dossier
    if not os.path.exists(nomDossier):
        os.makedirs(nomDossier)

    for i in range(0, matrice3D.shape[0]):
        #on sauvegarde les n premières matrices sous la forme d'une image
        plt.imsave(nomDossier + "/matrice" + str(i) + ".png", matrice3D[i])

def sauvegardePNGAll(Lmatrice3D, Lmatrice3D_Name, nomDossier : str):
    # Lmatrice3D : liste des matrices 3D à sauvegarder
    # Lmatrice3D_Name : liste des noms des matrices 3D à sauvegarder
    # Lposition : liste des positions des matrices 3D à sauvegarder dans le subplot

    #creation du dossier
    if not os.path.exists(nomDossier):
        os.makedirs(nomDossier)

    # On plot les matrices sur différentes figures  et on sauvegarde
    for i in range(0, Lmatrice3D[0].shape[0]):
        plt.clf()
        for j in range(0, len(Lmatrice3D)):
            plt.subplot(1, len(Lmatrice3D), j+1)
            plt.imshow(Lmatrice3D[j][i])
            plt.title(Lmatrice3D_Name[j])
        plt.savefig(nomDossier + "/matrice" + str(i) + ".png")