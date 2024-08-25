import os
import pandas as pd
import numpy as np
from pandas import DataFrame

# Chemins des fichiers CSV à fusionner
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\row_assocation"

# Lire df1 une seule fois en dehors de la boucle
df1 = pd.read_excel(os.path.join(dossier_path, "file1.xls"))

### optionnel : avoir le nom des colonnes pour adapter les nouveaux fichiers ajoutés
noms_colonnes_df1 = df1.columns.tolist()
print( "Noms des colonnes de df1 :", noms_colonnes_df1 )
# Liste pour stocker tous les DataFrames importés
dataframes = []

# Parcourir tous les fichiers du dossier
for filename in os.listdir( dossier_path ):
    if filename.endswith( ".xls" ):
        # Chemin complet du fichier
        file_path = os.path.join( dossier_path, filename )

        # Importer le fichier CSV en spécifiant le séparateur utilisé (; dans cet exemple)
        df2 = pd.read_excel( file_path )

        # Réorganiser les colonnes dans df2 pour qu'elles soient dans le même ordre que celles de df1
        df2 = df2.reindex( columns=df1.columns )

        # Ajouter le DataFrame à la liste
        dataframes.append( df2 )



# Concaténer tous les DataFrames en un seul DataFrame
concatenated_df = pd.concat( dataframes, ignore_index=True )

# Dictionnaire de remplacement
remplacements = {'AC09': 'AD01', 'AC18': 'AD02', 'AC16': 'AD04', 'AC20': 'AD08'}

# Remplacement des valeurs
concatenated_df['Nombre du participant'] = concatenated_df['Nombre du participant'].replace(remplacements)

print(concatenated_df)

## harmoniser les appellations dans les colonnes condition1 et condition2

# Obtenir les exemplaires uniques de la colonne
valeurs_uniques = concatenated_df['condition1'].unique()
valeurs_uniques2 = concatenated_df['condition2'].unique()

# Afficher les valeurs uniques
print(valeurs_uniques)
print(valeurs_uniques2)

# Définir le dictionnaire de remplacement
remplacements = {
    'congruent synonyme': 'Distracteur R',
    'Incongruent synonyme': 'Distracteur NR',
    'Distrateur Relié': 'Distracteur R'
}

# Effectuer les remplacements dans la colonne condition2
concatenated_df['condition2'] = concatenated_df['condition2'].replace(remplacements)

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\association"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_all.xlsx')

# Écrire le DataFrame concaténé dans un nouveau fichier CSV
concatenated_df.to_excel(output_file_path, index=False)

print(f"Tous les fichiers xlsx du dossier ont été concaténés dans {output_file_path}.")