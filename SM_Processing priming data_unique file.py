
## in terminal ; pip install xlrd
## If you have a lot of data, the processing should take several minutes

import os
import pandas as pd
import numpy as np

print(f"Your code is running. If you have a certain amount of data, this operation can take several minutes")

# WHAT WE DO : you have to adapt here the path for your files (in and out)
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\row_priming"
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\priming"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_all_unique.xlsx')

# This is the file "model" on wich all the other data are join; it will allow to update you data
df1 = pd.read_excel(os.path.join(dossier_path, "Expe2_priming_all.xls"))

# here it will charge all the new files of results and retain if in dataframes
xls_files = [f for f in os.listdir(dossier_path) if f.endswith(".xls")]

dataframes = []

# reading all the new files of results
for filename in xls_files:
    # path to find them
    file_path = os.path.join(dossier_path, filename)

    # import them
    df2 = pd.read_excel(file_path)

    # order the columns so they correspond to the order of the model file (necessary for concatenation)
    df2 = df2.reindex(columns=df1.columns)

    # add the DataFrame
    dataframes.append(df2)

# concatenation of all files in on file
concatenated_df = pd.concat(dataframes, ignore_index=True)

# here indicate the code of the participants for which the results will be excluded from analysis
remplacements = {'AC09': 'AD01', 'AC18': 'AD02', 'AC16': 'AD04', 'AC20': 'AD08'}
# exclude them
concatenated_df['nombre du participant'] = concatenated_df['nombre du participant'].replace(remplacements)

# Export the new file Expe2_priming_all2
concatenated_df.to_excel(output_file_path, index=False)

print(f"The RAW RESULTS of all the participants are concatenated and are now in the file {output_file_path}.")

############################################################################################################################################
############################################################################################################################################
##                                          SECOND STEP - PREPROCESSING OF DATA
############################################################################################################################################
############################################################################################################################################

df = concatenated_df #### restart on the main data frame with all the raw results

# WHAT WE DO : in the main data frame, version_hand contain the single information "version" that we need for fusion with Psycholinguistic informations about the words
# WHAT WE DO :  the number of the version must be united with the number of the row to have a unique identification of the pair in the list of material

# Convert "version_hand" to string and create "pair" column
df['version_hand'] = df['version_hand'].astype(str)
df['pair'] = df['version_hand'] + '_' + df['rowNo'].astype(str)
# Remove ".0" from "pair" column
df['pair'] = df['pair'].str.replace('.0', '', regex=False)

# WHAT WE DO : We are not keeping the training trials; they sould be removed
# Remove training trials with a safe copy
df = df[df["condition"] != "training"].copy()

# WHAT WE DO : For clarity of the reading we also rop unnecessary columns from the main data frame
columns_to_drop = ['filename', 'browser', 'version', 'screenWidth', 'screenHeight', 'OS',
                    'OS_lang', 'GMT_timestamp', 'local_timestamp', 'trial_file_version',
                    'link', 'calibration', 'duration_s', 'duration', 'duration_m',
                    'type', 'stim1', 'stim2', 'stim3', 'random', 'stimFormat', 'keyboard',
                    'feedback', 'presTime', 'ISI', 'condition_trial', 'condition_pair',
                    'presTime_ms', 'presTime_f', 'condition', 'timestamp']
df.drop(columns=columns_to_drop, inplace=True)

# Load psycholinguistic data and merge
df2 = pd.read_excel(os.path.join(output_folder_path, "Authors2023_LDT_stimOSF.xlsx"))
df3 = pd.merge(df, df2, on='pair', how='left')  # Changed to 'left' to keep all rows from df

# WHAT WE DO : we will export two files ; one with the data containing now the psycholinguistic values of the pairs
# WHAT WE DO : we will export a control file containing the line that are not in the new file of data (it sould contain only training data)

# Export cleaned data
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_allclean_unique.xlsx')
df3.to_excel(output_file_path, index=False)
print(f"The cleaned data file is located at {output_file_path}.")

# Find non-matching rows
df_non_matched = pd.merge(df, df2, on='pair', how='outer', indicator=True)
df_non_matched = df_non_matched[df_non_matched["_merge"] == "left_only"]

# Export non-matching data
non_matching_file_path = os.path.join(output_folder_path, 'NON_FUSIONNE_Expe2_priming_allclean_unique.xlsx')
df_non_matched.to_excel(non_matching_file_path, index=False)
print(f"Non-matching data exported to {non_matching_file_path}. This should only contain training trials if any.")

#########  CONTROL OF STEP 2 ############"

# Prompt the user to review the non-matching file
print("\nPlease review the 'NON_FUSIONNE_Expe2_priming_allclean_unique.xlsx' file.")
user_input = input("Type 'yes' to confirm that you have reviewed the file and proceed, or 'no' to cancel: ").strip().lower()

if user_input == 'yes':
    print("Proceeding with the next steps.")
    # Place any additional code here that should run after confirmation
else:
    print("Process canceled. Please review the file and run the script again when ready.")

############################################################################################################################################
############################################################################################################################################
##                                          THIRD STEP
#                                           integration of demographic data of participants
#                                           exclusion of outliers dans processing data for statistical analysis
############################################################################################################################################
############################################################################################################################################

df = df3

# Define paths to seek demographic data of the participants
demographic_data_path = "C:\\Users\\535607\\OneDrive - UMONS\\A. Etudes\\DAS 2021 Recherche dépression Alzheimer sémantique\\Expérience 2 2024\\DAS_EXPE2_table1_ALLgroups - après juin 2024.xlsx"

# Drop unnecessary columns from the exeprimental files
columns_to_drop = ['age', 'gender', 'handedness', 'key', 'response', 'version_hand', 'VERSION', 'construction']
df.drop(columns=columns_to_drop, inplace=True)
df.rename(columns={"nombre du participant": "participant"}, inplace=True)

# Filter out some specific pairs that has been identified in the first pre-processins as not working in the expected sens of their condition
values_to_remove = ['1_40', '2_36', '3_23', '3_33', '3_36', '4_36', '4_40', '4_46']
Excluded_trial = df[df['pair'].isin(values_to_remove)]
df = df[~df['pair'].isin(values_to_remove)]

### Export a file with the trial you excluded for possible further analysis
excluded_file_path = os.path.join(output_folder_path, 'Expe2_Priming_demographic_Excluded_trial.xlsx')
Excluded_trial.to_excel(excluded_file_path, index=False)
print(f"Excluded_trial DataFrame has been exported to {excluded_file_path}")

#########  CONTROL OF STEP 3  ############

# Prompt the user to review the non-matching file
print("\nPlease review the 'Excluded_trial.xlsx' file.")
user_input = input("Type 'yes' to confirm that you have reviewed the file and proceed, or 'no' to cancel: ").strip().lower()

if user_input == 'yes':
    print("Proceeding with the next steps.")
    # Place any additional code here that should run after confirmation
else:
    print("Process canceled. Please review the file and run the script again when ready.")

################  END OF CONTROL STEP 3 ###################

# Load the additional data for merging
df2 = pd.read_excel(demographic_data_path, sheet_name='tab.1', decimal=',')

# Keep only relevant columns in df2  : ADD HERE THE SUPPLEMENTARY DEMOGRAPHIC VALUE YOU WANT IN YOUR ANALYSIS
columns_to_keep = ['participant', 'GROUP', 'age']
df2 = df2[columns_to_keep]

# Merge dataframes
merged_df = pd.merge(df, df2, on='participant', how='inner')
print(merged_df.columns)

# Find non-matching rows
df_fusionne = pd.merge(df, df2, on="participant", how="outer", indicator=True)
df_non_fusionne = df_fusionne[df_fusionne["_merge"] == "left_only"]

# Export non-matching data
non_matching_file_path = os.path.join(output_folder_path, 'Expe2_priming_NON CORRESPONDANCE with demographic data.xlsx')
df_non_fusionne.to_excel(non_matching_file_path, index=True)

# Export merged data
merged_file_path = os.path.join(output_folder_path, 'Expe2_priming_analyses_unique.xlsx')
merged_df.to_excel(merged_file_path, index=True)

print(f"The file Expe2_priming_analyses containing all the data has been exported to {merged_file_path}")

#########  2nd CONTROL OF STEP 3 ############

# Prompt the user to review the non-matching file
print("\nPlease review the 'Expe2_priming_NON CORRESPONDANCE with demographic data.xlsx' file.")
user_input = input("Type 'yes' to confirm that you have reviewed the file and proceed, or 'no' to cancel: ").strip().lower()

if user_input == 'yes':
    print("Proceeding with the next steps.")
    # Place any additional code here that should run after confirmation
else:
    print("Process canceled. Please review the file and run the script again when ready.")

################  END OF 2nd CONTROL STEP 3 ###################

# Filter rows according to condition
filtered_df = merged_df[merged_df['condition'].isin(['HD', 'HS', 'AS', 'NR'])]
print("filtered_df represents raw data, only for conditions of interest HD, HS, AS, NR")

# Process data for response time analysis
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_analyses_MADok_unique.xlsx')

# Total number of lines before filtering
total_lines_before = len(filtered_df)

# Remove incorrect responses
df = filtered_df[filtered_df['correct'] != 0]
percentage_lost_incorrect = ((total_lines_before - len(df)) / total_lines_before) * 100
print(f"Percentage of loss after removing incorrect responses: {percentage_lost_incorrect:.2f}%")

# Filter outliers based on response time
total_lines_after_correct = len(df)
df = df[(df['RT'] >= 100) & (df['RT'] <= 10000)]
percentage_lost_outliers = ((total_lines_after_correct - len(df)) / total_lines_after_correct) * 100
print(f"Percentage of loss after removing outliers based on RT: {percentage_lost_outliers:.2f}%")

# MAD method for outlier detection
k = 1.4826
grouped = df.groupby("participant")["RT"]
medians = grouped.transform("median")
mad = grouped.transform(lambda x: k * np.median(np.abs(x - np.median(x))))
outliers_mask = (df["RT"] < medians - 3 * mad) | (df["RT"] > medians + 3 * mad)
df_filtered2 = df[~outliers_mask]

# Calculate and print percentage of lines removed
lines_removed = len(df) - len(df_filtered2)
total_correct_lines = len(filtered_df[filtered_df['correct'] != 0])
percentage_removed = (lines_removed / total_correct_lines) * 100
print(f"Percentage of lines removed: {percentage_removed:.2f}%")

# Export cleaned data
df_filtered2.to_excel(output_file_path, index=False)
print(f"The new table with cleaned data is saved to: {output_file_path}")

# Create a pivot table for analysis with mean grouped by participants
pivot_table = pd.pivot_table(df_filtered2,
                             values='RT',
                             index=['participant', 'GROUP'],
                             columns='condition',
                             aggfunc={'RT': ['mean', 'std']})

# Flatten the MultiIndex columns
pivot_table.columns = [f'{col}_{agg}' for col, agg in pivot_table.columns]

# Calculate specific performance metrics
pivot_table['SPE_HD'] = ((pivot_table['mean_NR'] - pivot_table['mean_HD']) / pivot_table['mean_NR'] * 100)
pivot_table['SPE_HS'] = ((pivot_table['mean_NR'] - pivot_table['mean_HS']) / pivot_table['mean_NR'] * 100)
pivot_table['SPE_AS'] = ((pivot_table['mean_NR'] - pivot_table['mean_AS']) / pivot_table['mean_NR'] * 100)

# Export the pivot table
pivot_table_file_path = os.path.join(output_folder_path, 'Expe2_priming_TCD_unique.xlsx')
pivot_table.to_excel(pivot_table_file_path, index=True)
print(f"The new pivot table based on priming data, only correct responses, and after MAD outlier removal is saved to {pivot_table_file_path}.")
