
#### ce script reprend le fichier "allclean" de la tâche d'association et inclut deux colonnes ;
# ordre de présentation des trials ;
# ordre de présentation des blocs ;
# importe la table 1 pour ajouter l'information "groupe" dans le tableau de données ;
# la version intermédiaires avant les analyses ultérieures et exportée  dans
# "C:\\Users\\535607\\PycharmProjects\\test1\\newfile\\Expe2_association_allclean_order.csv')
##########################################################################################################"

### tri des données en retirant les mauvaises réponses et les outliers de temps selon la méthode MAD

##########################################################################################################




import pandas as pd
import os
import numpy as np

# Chemins des fichiers CSV à fusionner
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"

# Lire df
df = pd.read_excel(os.path.join(dossier_path, "Expe2_association_allclean.xlsx"))
df = df.rename(columns={"Nombre du participant": "participant"})
##### créer une colonne donnant l'ordre de présentation des trials sur base des timestamp

# Tri du DataFrame par participant puis par timestamp
df.sort_values(by=['participant', 'timestamp'], inplace=True)

# Réinitialisation des index pour faciliter le calcul ultérieur
df.reset_index(drop=True, inplace=True)

# Création de la colonne "ordre" basée sur la progression des valeurs de timestamp
df['ordre'] = df.groupby('participant').cumcount() + 1

#########  créer une colonne qui donne l'ordre de présentation des blocs

# Filtrer les lignes avec "ordre" égal à 1
condition_1_rows = df[df['ordre'] == 1]

# Créer un dictionnaire pour stocker les valeurs de "condition1" correspondant à "1" dans "ordre" pour chaque participant
#correspondence_dict = dict(zip(condition_1_rows['Nombre du participant'], condition_1_rows['condition1']))

# Filtrer les lignes avec "ordre" égal à 1
condition_1_rows = df[df['ordre'] == 1]

# Créer un dictionnaire pour stocker les valeurs de "condition1" correspondant à "1" dans "ordre" pour chaque participant
correspondence_dict = dict(zip(condition_1_rows['participant'], condition_1_rows['condition1']))

# Fonction pour déterminer la valeur à assigner en fonction du dictionnaire de correspondance
def assign_value(row):
    participant = row['participant']
    if participant in correspondence_dict and row['condition1'] == correspondence_dict[participant]:
        return 1
    return None

# Appliquer la fonction pour créer la colonne "ordreblocs"
df['ordreblocs'] = df.apply(assign_value, axis=1)

# Filtrer les lignes avec "ordre" égal à 60
condition_3_rows = df[df['ordre'] == 60]

# Créer un dictionnaire pour stocker les valeurs de "condition1" correspondant à "1" dans "ordre" pour chaque participant
correspondence_dict3 = dict(zip(condition_3_rows['participant'], condition_3_rows['condition1']))

# Fonction pour déterminer la valeur à assigner en fonction du dictionnaire de correspondance
def assign_value3(row):
    participant = row['participant']
    if participant in correspondence_dict3 and row['condition1'] == correspondence_dict3[participant]:
        return 3
    return None

# Appliquer la fonction pour créer la colonne "ordreblocs"
df['ordreblocs2'] = df.apply(assign_value3, axis=1)

# Convertir les colonnes en numérique
df['ordreblocs'] = pd.to_numeric(df['ordreblocs'])
df['ordreblocs2'] = pd.to_numeric(df['ordreblocs2'])

# Remplacer les valeurs NA par 0 dans la colonne
df['ordreblocs']  = df['ordreblocs'] .fillna(0)
df['ordreblocs2'] = df['ordreblocs2'].fillna(0)
# Fonction pour fusionner deux cellules et retourner leur somme
def sum_columns(row):
    return row['ordreblocs2'] + row['ordreblocs']

# Appliquer la fonction pour créer une nouvelle colonne avec la somme
df['BlocOrdre'] = df.apply(sum_columns, axis=1)

df['BlocOrdre'] = df['BlocOrdre'].replace(0,2)


###########################################################################################################################################

##### importer les données '"groupes" pour les fusionner avec le df

# Chemin vers le fichier Excel
chemin_fichier = "C:\\Users\\535607\\OneDrive - UMONS\\A. Etudes\\DAS 2021 Recherche dépression Alzheimer sémantique\\Expérience 2_2022_2023\\DAS_EXPE2_table1_ALLgroups - après juin 2024.xlsx"

# Nom de la feuille
nom_feuille = 'tab.1'

# Importer la feuille en tant que DataFrame
df2 = pd.read_excel(chemin_fichier, sheet_name=nom_feuille,decimal=',')

# Liste des noms de colonnes que vous voulez conserver
colonnes_a_garder = ['participant', 'GROUP', 'age']  # Remplacez par les noms de vos colonnes

# Sélectionner les colonnes à garder
df2 = df2[colonnes_a_garder]

# Fusionner les DataFrames par la colonne "participant"
merged_df = df.merge(df2, on='participant', how='inner')
print(merged_df.columns)

## trouver les lignes qui n'ont pas fusionné
# Fusionner les DataFrames par la colonne "matricule" en utilisant l'indicateur "_merge"

df_fusionne = pd.merge(df, df2, on="participant", how="outer", indicator=True)
# Filtrer les lignes qui n'ont pas pu être fusionnées
df_non_fusionne = df_fusionne[df_fusionne["_merge"] == "left_only"]

# Afficher le DataFrame des lignes non fusionnées
print("DataFrame des lignes non fusionnées:")
print(df_non_fusionne)

# Chemin complet pour le fichier de sortie : fichier de récupération des données non fusionnées pour contrôle
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_DONNEES NON FUSIONNEES.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
df_non_fusionne.to_excel(output_file_path, index=True)

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_analyses.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
merged_df.to_excel(output_file_path, index=True)

print("Le fichier Expe2_association_analyses contenant l'ensemble des données a été exporté dans C:\\Users\\535607\\PycharmProjects\\test1\\newfile")
###########################################################################################################################################

###########################################################################################################################################

#### créer le tableau excluant les mauvaises réponses et les outliers de temps pour les analyses sur les temps de réponse

# Éliminer les lignes où "correct" est égal à 0
# Compter le nombre total de lignes dans le DataFrame
lignes_totales = len(merged_df)

df = merged_df[merged_df['correct'] != 0]

# Compter le nombre de lignes éliminées
lignes_eliminees = lignes_totales - len(df)

# Calculer le pourcentage de lignes éliminées
pourcentage_eliminees = (lignes_eliminees / lignes_totales) * 100

print(f"Pourcentage de lignes éliminées car réponses incorrectes : {pourcentage_eliminees:.2f}%")

# éliminer les outliers temps selon une méthode MAD

# Paramètres
k = 1.5  # Facteur pour déterminer la plage d'outliers

# Calculer la médiane et le MAD pour chaque groupe "participant"
grouped = df.groupby("participant")["RT"]
medians = grouped.transform("median")
mad = grouped.transform(lambda x: np.median(np.abs(x - np.median(x))))

# Identifier les valeurs outliers en dehors de la plage [median - k * MAD, median + k * MAD] / en prenant la borne à 3 MAD (convention de Miller 1991)
outliers_mask = (df["RT"] < medians - 3 * k * mad) | (df["RT"] > medians + 3 * k * mad)

# Éliminer les lignes correspondantes
df_filtered = df[~outliers_mask]

### donner le nombre de trials éliminé par rapport à l'ensemble des réponses correctes

# Compter le nombre total de lignes dans le DataFrame
lignes_totales = len(df)

# Compter le nombre de lignes éliminées
lignes_eliminees = lignes_totales - len(df_filtered)

# Calculer le pourcentage de lignes éliminées
pourcentage_eliminees = (lignes_eliminees / lignes_totales) * 100

print(f"Pourcentage de lignes éliminées car en dehors des bornes de MAD : {pourcentage_eliminees:.2f}%")

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_analyses_MADok.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
df_filtered.to_excel(output_file_path, index=True)

print("Le fichier Expe2_association_analyses_MADok contenant les données après retrait des mauvaises réponses et les outliers MAD a été exporté dans C:\\Users\\535607\\PycharmProjects\\test1\\newfile")

###########################################################################################################################################

###########################################################################################################################################

# Créer un tableau croisé dynamique

# Définition des fonctions d'agrégation souhaitées : sum pour correct
aggregation_functions = {
    'correct': 'sum'}

# Création du tableau pivot avec moyenne et écart type
pivot_table2 = pd.pivot_table(df_filtered,
                             values='correct',
                             index=['GROUP', 'participant'],
                             columns=['clue-target','clue-foil'],
                             aggfunc=aggregation_functions)

# Renommer les colonnes pour refléter les fonctions d'agrégation
pivot_table2.columns = [f'{col}_{agg}' for col, agg in pivot_table2.columns]

print(pivot_table2)
print(pivot_table2.columns)
# Définition des fonctions d'agrégation souhaitées : Mean pour RT
aggregation_functions = {
    'RT': 'mean'
}

# Création du tableau pivot avec moyenne et écart type
pivot_table1 = pd.pivot_table(df_filtered,
                             values='RT',
                             index=['GROUP','participant'],
                             columns=['clue-target','clue-foil'],
                             aggfunc=aggregation_functions)

# Renommer les colonnes pour refléter les fonctions d'agrégation
pivot_table1.columns = [f'{col}_{agg}' for col, agg in pivot_table1.columns]

print(pivot_table1)


# Créer colonne proportion accuracy
print(pivot_table2.columns)

pivot_table2['acc_col_inc'] = (100/8*pivot_table2['FEATURE_COLOR_Incongruent'])
pivot_table2['acc_size_inc'] = (100/8*pivot_table2['FEATURE_SIZE_Incongruent'])
pivot_table2['acc_HD_inc'] = (100/7*pivot_table2['HD_Incongruent'])
pivot_table2['acc_HS_inc'] = (100/7*pivot_table2['HS_Incongruent'])

pivot_table2['acc_col_con'] = (100/8*pivot_table2['FEATURE_COLOR_congruent'])
pivot_table2['acc_size_con'] = (100/8*pivot_table2['FEATURE_SIZE_congruent'])
pivot_table2['acc_HD_con'] = (100/7*pivot_table2['HD_congruent'])
pivot_table2['acc_HS_con'] = (100/7*pivot_table2['HS_congruent'])

#### fusionner sur base de la colonne commune "participant"
pivot_table3 = pd.merge(pivot_table2, pivot_table1, on=['participant','GROUP'])

print(pivot_table3)
 ## Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_TCD.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier xlsx
pivot_table3.to_excel(output_file_path, index=True)

print(f"le nouveau TCD basé sur les données d'association, uniquement réponses correctes, sur conditions d'intérêt et après retrait des outliers MAD se trouve dans {output_file_path}.")




