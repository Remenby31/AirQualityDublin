import os
import pandas as pd

# On fusionne les fichiers mobiles et fixes qui portent le meme nom dans un seul fichier

# On recupere la liste des dossier dans le dossier DCU
folders = os.listdir(".")

# Pour chaque dossier
for folder in folders:
    # Si c'est un dossier mobile
    if os.path.isdir(folder) and folder.split('_')[1] == 'mobiles':
        # Nom des dossiers
        mixedFolder = folder.replace('mobiles', 'mixed')
        mobileFolder = folder
        fixedFolder = folder.replace('mobiles', 'fixed').replace('30', '31')

        # On creer le dossier mixte, si il n'existe pas
        if not os.path.exists(mixedFolder):
            os.makedirs(mixedFolder)
        
        # On recupere la liste des fichiers dans le dossier mobile
        mobileFiles = os.listdir(mobileFolder)

        # Pour chaque fichier mobile
        for mobileFile in mobileFiles:

            # ==================== On recupere le fichier mobile ====================
            try:
                mobileDf = pd.read_csv(mobileFolder + '/' + mobileFile, sep=';', header=None)
            except:
                print("Mobile file " + mobileFile + " not found")
                mobileDf = None

            # ==================== On recupere le fichier fixe ====================
            fixedFile = mobileFile.replace('mobile', 'fixed')
            try:                
                fixedDf = pd.read_csv(fixedFolder + '/' + fixedFile, sep=';', header=None)
            except:
                print("Mobile file " + mobileFile + " not found")
                fixedDf = None

            # ==================== On fusionne les deux fichiers ====================
            if mobileDf is not None and fixedDf is not None:
                mixedDf = pd.concat([mobileDf, fixedDf])
            elif mobileDf is not None:
                mixedDf = mobileDf
            elif fixedDf is not None:
                mixedDf = fixedDf

            # ==================== On trie le fichier fusionne ====================
            mixedDf = mixedDf.sort_values(by=mixedDf.columns[0])

            # ==================== On sauvegarde le fichier fusionne ====================
            mixedDf.to_csv(mixedFolder + '/' + mobileFile, index=False, header=False, sep=';')