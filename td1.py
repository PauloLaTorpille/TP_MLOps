import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


#df1 = pd.read_csv(r'\\ad.univ-lille.fr\Etudiants\Homedir3\284749\Desktop\M2\devops\batch\restaurant_1_week_002.csv')
#print(df1)


# Chargement Restaurant 1
# Chemin du répertoire contenant les fichiers CSV
#repertoire = r"\\ad.univ-lille.fr\Etudiants\Homedir3\284749\Desktop\M2\devops\batch"

# Liste des fichiers qui commencent par "restaurant_1"
#fichiers_a_concatener = [f for f in os.listdir(repertoire) if f.startswith("restaurant_1") and f.endswith(".csv")]

# Initialisation d'un DataFrame vide pour stocker les données concaténées
#restaurant_1 = pd.DataFrame()

# Concaténer les fichiers
#for fichier in fichiers_a_concatener:
   # chemin_fichier = os.path.join(repertoire, fichier)
   # donnees = pd.read_csv(chemin_fichier)
   # restaurant_1 = pd.concat([restaurant_1, donnees], ignore_index=True)

# Sauvegarder les données concaténées dans un fichier CSV
#restaurant_1.to_csv("restaurant_1.csv", index=False)



# Chargement Restaurant 2
# Chemin du répertoire contenant les fichiers CSV
#repertoire = r"\\ad.univ-lille.fr\Etudiants\Homedir3\284749\Desktop\M2\devops\batch"

# Liste des fichiers qui commencent par "restaurant_1"
#fichiers_a_concatener = [f for f in os.listdir(repertoire) if f.startswith("restaurant_2") and f.endswith(".csv")]

# Initialisation d'un DataFrame vide pour stocker les données concaténées
#restaurant_2 = pd.DataFrame()

# Concaténer les fichiers
#for fichier in fichiers_a_concatener:
   # chemin_fichier = os.path.join(repertoire, fichier)
   # donnees = pd.read_csv(chemin_fichier)
   # restaurant_2 = pd.concat([restaurant_2, donnees], ignore_index=True)

# Sauvegarder les données concaténées dans un fichier CSV
#restaurant_2.to_csv("restaurant_2.csv", index=False)

#restaurant_1.columns.tolist()
#restaurant_2.columns.tolist()  #les noms de colonnes sont différents
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
        file_path = os.path.join(data_dir, r'\\ad.univ-lille.fr\Etudiants\Homedir3\284749\Desktop\M2\devops\batch', f'{prefix}_week_{i}.csv')

        if os.path.isfile(file_path):
            batch = pd.read_csv(file_path)
            df = pd.concat([df, batch], sort=True)
    
    return df

def clean(df):
    """Clean dataframe."""
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df = df.rename(columns={'order_number': 'order_id'})
    df = df.sort_values('order_date')
    df['total_product_price'] = df['quantity'] * df['product_price']
    df['cash_in'] = df.groupby('order_id')['total_product_price'].transform(np.sum)
    df = df.drop(columns=['item_name', 'quantity', 'product_price', 
                          'total_products', 'total_product_price'],
                errors="ignore")
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df

def merge(df1, df2):
    df = pd.concat([df1, df2])
    df = df.drop(columns = ['order_id'])
    df = df.sort_values('order_date')
    df = df.reset_index(drop=True)
    return df

def resample(df): 
    df = df.resample('1H', on='order_date').sum().reset_index()
    return df

# restaurant 1
df1 = extract(data_dir= r"\\ad.univ-lille.fr\Etudiants\Homedir3\284749\Desktop\M2\devops",
       prefix="restaurant_1" , start_week=108, end_week=110)

df1 = clean(df1)

# restaurant 2
df2 = extract(data_dir= "c:/Users/284749/TP_MLOps/DATA/",
       prefix="restaurant_2" , start_week=108, end_week=110)

df2 = clean(df2)

df = merge(df1, df2)
df = resample(df)
df.head()


fig, ax = plt.subplots(1,1, figsize=(10,5))
ax.plot(df['order_date'], df['cash_in'])
ax.set_title('Chiffre d affaire des restaurants en fonction du temps')
ax.set_xlabel('Temps')
ax.set_ylabel('cash in')
plt.grid(True)


#créer jour de la semaine (2017)
df['year'] = df['order_date'].dt.year
#créer mois (1,2,...)
df['month'] = df['order_date'].dt.month
#créer jour de la semaine (0,1,2,3,4,5,6)
df['day'] = df['order_date'].dt.weekday
#créer l'heure (9,10,11,...)
df['hours'] = df['order_date'].dt.hour

df.head



#dummies jours
df = pd.get_dummies(df, columns=['day'])




























