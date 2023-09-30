import os
import pandas as pd

df1 = pd.read_csv("DATA/restaurant_1_week_002.csv")
print(df1)


# Chargement Restaurant 1
# Chemin du répertoire contenant les fichiers CSV
repertoire = "DATA/"

# Liste des fichiers qui commencent par "restaurant_1"
fichiers_a_concatener = [f for f in os.listdir(repertoire) if f.startswith("restaurant_1") and f.endswith(".csv")]

# Initialisation d'un DataFrame vide pour stocker les données concaténées
restaurant_1 = pd.DataFrame()

# Concaténer les fichiers
for fichier in fichiers_a_concatener:
    chemin_fichier = os.path.join(repertoire, fichier)
    donnees = pd.read_csv(chemin_fichier)
    restaurant_1 = pd.concat([restaurant_1, donnees], ignore_index=True)

# Sauvegarder les données concaténées dans un fichier CSV
restaurant_1.to_csv("restaurant_1.csv", index=False)



# Chargement Restaurant 2
# Chemin du répertoire contenant les fichiers CSV
repertoire = "DATA/"

# Liste des fichiers qui commencent par "restaurant_1"
fichiers_a_concatener = [f for f in os.listdir(repertoire) if f.startswith("restaurant_2") and f.endswith(".csv")]

# Initialisation d'un DataFrame vide pour stocker les données concaténées
restaurant_2 = pd.DataFrame()

# Concaténer les fichiers
for fichier in fichiers_a_concatener:
    chemin_fichier = os.path.join(repertoire, fichier)
    donnees = pd.read_csv(chemin_fichier)
    restaurant_2 = pd.concat([restaurant_2, donnees], ignore_index=True)

# Sauvegarder les données concaténées dans un fichier CSV
restaurant_2.to_csv("restaurant_2.csv", index=False)

restaurant_1.columns.tolist()



def extract(data_dir, prefix, start_week, end_week):
    """ Extract a temporal slice of data for a given data source.
    
    Parameters
    ----------
    data_dir: str
        Data directory path.
    start_week: int
        First week number (included)
    end_week: int
        Last week number (included)
    prefix: str
        Data source identification (e.g. restaurant_1)
    """

    df = pd.DataFrame()
    
    for i in range(start_week, end_week+1):
        file_path = os.path.join(data_dir, f'{prefix}_week_{i}.csv')

        if os.path.isfile(file_path):
            batch = pd.read_csv(file_path)
            df = pd.concat([df, batch], sort=True)
    
    return df

df = extract(data_dir= "/c/Users/284749/TP_MLOps/DATA/",
       prefix="restaurant_1" , start_week=108, end_week=110)

df.head()

