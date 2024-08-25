import pandas as pd
import os

# Chemins des fichiers CSV à fusionner
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\association"


# Lire df
df = pd.read_excel( os.path.join(dossier_path, "Expe2_association_all.xlsx"))

## remplacer réponse du participant par mot choisi

def replace_response_with_stim(row):
    if row['response'] == 'f':
        return row['stim1']
    elif row['response'] == 'g':
        return row['stim2']
    elif row['response'] == 'h':
        return row['stim3']
    elif row['response'] == 'j':
        return row['stim4']
    else:
        return row['response']  # Garder la valeur de 'response' si elle ne correspond à aucune condition

# Appliquer la fonction à chaque ligne du DataFrame
df['response'] = df.apply(replace_response_with_stim, axis=1)

print(df)

# Obtenir les valeurs uniques de la colonne 'column'
valeurs_uniques = df['condition1'].unique()

print(valeurs_uniques)

## voir les noms des colonnes pour supprimer les inutiles

print(df.columns)

## exclure colonnes inutiles pour analyses

colonnes_a_supprimer = {'filename', 'browser', 'screenWidth', 'screenHeight', 'OS',
       'OS_lang', 'GMT_timestamp', 'local_timestamp', 'trial_file_version',
       'link', 'calibration', 'age', 'gender', 'Code etudiant',
        'duration_s', 'duration', 'duration_m',
       'order_trial', 'type', 'stim1', 'stim2', 'stim3', 'stim4',
       'ITI', 'keyboard', 'stimPos', 'stimFormat', 'trialText', 'key',
       'block_order', 'randomBlock',
       'feedback', 'stimPos_actual', 'ITI_ms', 'ITI_f', 'ITI_fDuration',
        }
df.drop(colonnes_a_supprimer, axis=1, inplace=True)
# Exclure les lignes où le trial est un entrainement
trialexclu = ["entraînement"]
nouveau_df = df[~df["condition1"].isin(trialexclu)]

# Exclure les lignes où le participant est "test"
trialexclu2= "test"
nouveau_df2 = nouveau_df[df["Nombre du participant"] != trialexclu2]

### importer tableau de stim pour ajouter données psycholinguistiques
dossier_path2 = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\association"

# Lire df
df2 = pd.read_csv(os.path.join(dossier_path2, "association_stim.csv"), sep=';', encoding='latin1',decimal=',')

#### voir le contenu des colonnes rowNo dans les deux fichiers
valeurs_uniques1 = nouveau_df2['rowNo'].unique()
print(valeurs_uniques1)

valeurs_uniques2 = df2['rowNo'].unique()
print(valeurs_uniques2)

#### fusionner sur base de la colonne commune "rowNo"
df3 = pd.merge(nouveau_df2, df2, on='rowNo')


# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"

output_file_path = os.path.join(output_folder_path, 'Expe2_association_allclean.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
df3.to_excel(output_file_path, index=False)

print(f"le nouveau tableau se trouve dans {output_file_path}.")

###  3  ### montrer un tableau croisé des données principales de ce fichier "clean"
# Créer une nouvelle colonne pour la combinaison de conditions
df3['condition_combination'] = df3['condition1'] + '-' + df3['condition2']

# Créer un tableau croisé dynamique
pivot_table = pd.pivot_table( df3, values='RT', index="Nombre du participant", columns='condition_combination', aggfunc=len )
print (pivot_table)
# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_association_TCD_temp.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
pivot_table.to_excel(output_file_path, index=True)