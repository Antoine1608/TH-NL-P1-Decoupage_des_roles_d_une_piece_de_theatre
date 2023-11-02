import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import requests

class GraphResponse(BaseModel):
    absi: list
    ordo: list
    vale: list
    tota: dict

class GraphResponse2(BaseModel):
    absi: list
    ordo: list
    vale: list
    tota: dict
    datact: dict

list_pers_c = []
liste_stage_r = []

def import_txt(input):
    import os
    text = input.dict()

    # Récupérez l'URL du fichier texte de la pièce qui nous intéresse
    file_url = text['url_']

    # Faites une requête HTTP pour télécharger le contenu du fichier texte
    file_response = requests.get(file_url)

    # Vérifiez si le téléchargement a réussi (statut code 200)
    if file_response.status_code == 200:
        # Enregistrez le contenu dans un fichier local (par exemple "doc.txt")
        doc = os.path.basename(file_url)
        with open(doc, 'wb') as file:
            file.write(file_response.content)
        print("Le fichier a été téléchargé avec succès.\n")
    else:
        pass
        print("Le téléchargement du fichier a échoué avec le code de statut :", file_response.status_code)

    df=pd.read_fwf(doc,header=None,sep=" ",encoding = "ISO-8859-1")
    return df

def supp_intro(df):
# Supposons que vous ayez un DataFrame appelé df
    try:
        # Trouver l'index de la première ligne dont le texte commence par 'ACTE I'
        index_to_keep = df[df.loc[:,0].str.startswith('ACTE I')].index[0]
        
        # Si l'index est différent de zéro, supprimer les lignes au-dessus
        if index_to_keep != 0:
            df = df[index_to_keep:]
            return df
        
        # Réinitialiser les index après la suppression
        df.reset_index(drop=True, inplace=True)
        
        # Maintenant, df contient les lignes après la première ligne commençant par 'ACTE I'
    except:
        return None

def liste_stage(df):

    df_ = df.copy()
    # On enlève la ponctuation et on tokenize
    from nltk.tokenize import RegexpTokenizer
    for c in range(0,df_.shape[1]):
        for r in range(0,len(df_)):
            if type(df_.iloc[r,c]) == str :
                tokenizer = RegexpTokenizer(r'\w+')
                df_.at[r,c] = tokenizer.tokenize(df_.iloc[r,c])

    # A ce state chaque cellule de df_ contient une liste de mots sans ponctutation

    # Rassembler les lignes dans une colonne "cleaned"
    from functools import reduce
    col = []
    for i in range(0, len(df_)):
        col.append(reduce(lambda x,y : x+y if (type(x) == list and type(y) == list) else x, df_[i:i+1].values.tolist()[0]))
    df_["cleaned"] = col

    # A ce state df_ a en plus une colonne 'cleaned' qui contient la liste de tous les mots de la ligne

    # On réduit df_ à une colonne qui contient la liste de tous les mots de la ligne
    df_ = pd.DataFrame(df_["cleaned"])

    # # Labelliser

    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # On rajoute une colonne label avec les valeurs structure ou note   
    def label(x):
        if x[0].isupper():
            return 'structure'
        elif 'Note' in x:
            return 'note'
        else:
            return None  # Si aucune condition n'est satisfaite

    df_['label'] = df_['cleaned'].map(label)

    # A ce stade df_ contient deux colonnes : 'cleaned' et 'label' qui contient structure, note ou None

    data = df_.copy()
    
    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # Supprimer les lignes labellisées note
    df_ = df_[df_['label']!='note'] 

    # A ce stade df_ est complètement nettoyé

    # Liste des éléments de structure
    col_cleaned_struct = df_.loc[df_['label'] == 'structure', 'cleaned']

    def extract_structure(cell):
        struct = [i for i in cell if i.isupper()]
        return struct

    lstruct = [extract_structure(cell) for cell in col_cleaned_struct]

    # Utilisation d'une compréhension de liste pour convertir lstruct en une liste de strings sans doublons
    lstruct = [' '.join(sublist) for sublist in set(tuple(sublist) for sublist in lstruct)]


    # # Récupération de la liste des personnages

    # on supprime les éléments à une lettre
    lstruct = [i for i in lstruct if len(i)>1]

    # lstage est la liste des éléments de découpage de la pièce
    exclusion_list = ['SCÈNE', 'ACTE', 'ENTRÉE', 'INTERMÈDE', 'PROLOGUE', 'ÉGLOGUE']
    lstage = [i for i in lstruct if any(excl in i for excl in exclusion_list)]
    return lstage

def liste_perso(df):

    df_ = df.copy()
    # On enlève la ponctuation et on tokenize
    from nltk.tokenize import RegexpTokenizer
    for c in range(0,df_.shape[1]):
        for r in range(0,len(df_)):
            if type(df_.iloc[r,c]) == str :
                tokenizer = RegexpTokenizer(r'\w+')
                df_.at[r,c] = tokenizer.tokenize(df_.iloc[r,c])

    # A ce state chaque cellule de df_ contient une liste de mots sans ponctutation

    # Rassembler les lignes dans une colonne "cleaned"
    from functools import reduce
    col = []
    for i in range(0, len(df_)):
        col.append(reduce(lambda x,y : x+y if (type(x) == list and type(y) == list) else x, df_[i:i+1].values.tolist()[0]))
    df_["cleaned"] = col

    # A ce state df_ a en plus une colonne 'cleaned' qui contient la liste de tous les mots de la ligne

    # On réduit df_ à une colonne qui contient la liste de tous les mots de la ligne
    df_ = pd.DataFrame(df_["cleaned"])

    # # Labeliser

    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # On rajoute une colonne label avec les valeurs structure ou note   
    def label(x):
        if x[0].isupper():
            return 'structure'
        elif 'Note' in x:
            return 'note'
        else:
            return None  # Si aucune condition n'est satisfaite

    df_['label'] = df_['cleaned'].map(label)

    # A ce stade df_ contient deux colonnes : 'cleaned' et 'label' qui contient structure, note ou None
    
    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # Supprimer les lignes labellisées note
    df_ = df_[df_['label']!='note'] 

    # A ce stade df_ est complètement nettoyé

    # Liste des éléments de structure
    col_cleaned_struct = df_.loc[df_['label'] == 'structure', 'cleaned']

    def extract_structure(cell):
        struct = [i for i in cell if i.isupper()]
        return struct

    lstruct = [extract_structure(cell) for cell in col_cleaned_struct]
 
    # Utilisation d'une compréhension de liste pour convertir lstruct en une liste de strings sans doublons
    lstruct = [' '.join(sublist) for sublist in set(tuple(sublist) for sublist in lstruct)]

    # # Récupération de la liste des personnages

    # on supprime les éléments à une lettre
    lstruct = [i for i in lstruct if len(i)>1]

    # lnom est la liste des noms
    exclusion_list = ['SCÈNE', 'ACTE', 'ENTRÉE', 'INTERMÈDE', 'PROLOGUE', 'ÉGLOGUE']
    lnom = [i for i in lstruct if not any(excl in i for excl in exclusion_list)]
    return lnom

def visualisation(df, genre, lstage=None, lnom=None):

    if genre not in ('général', 'correction', 'répartition'):
        raise ValueError("La valeur doit être 'général', 'correction' ou 'répartition'")

    # Init
    df_ = df.copy()

    # On enlève la ponctuation et on tokenize
    from nltk.tokenize import RegexpTokenizer
    for c in range(0,df_.shape[1]):
        for r in range(0,len(df_)):
            if type(df_.iloc[r,c]) == str :
                tokenizer = RegexpTokenizer(r'\w+')
                df_.at[r,c] = tokenizer.tokenize(df_.iloc[r,c])

    # A ce state chaque cellule de df_ contient une liste de mots sans ponctutation

    # Rassembler les lignes dans une colonne "cleaned"
    from functools import reduce
    col = []
    for i in range(0, len(df_)):
        col.append(reduce(lambda x,y : x+y if (type(x) == list and type(y) == list) else x, df_[i:i+1].values.tolist()[0]))
    df_["cleaned"] = col

    # A ce state df_ a en plus une colonne 'cleaned' qui contient la liste de tous les mots de la ligne

    # On réduit df_ à une colonne qui contient la liste de tous les mots de la ligne
    df_ = pd.DataFrame(df_["cleaned"])

    # # Labelliser

    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # On rajoute une colonne label avec les valeurs structure ou note   
    def label(x):
        if x[0].isupper():
            return 'structure'
        elif 'Note' in x:
            return 'note'
        else:
            return None  # Si aucune condition n'est satisfaite

    df_['label'] = df_['cleaned'].map(label)

    # Supprimer les lignes où la col 'cleaned' contient une liste vide
    df_ = df_[df_['cleaned'].apply(lambda x: len(x) > 0)]

    # Réinitialiser l'index du DataFrame 
    df_.reset_index(drop=True, inplace=True)

    # Supprimer les lignes labellisées note
    df_ = df_[df_['label']!='note'] 

    # A ce stade df_ est complètement nettoyé

    # Liste des éléments de structure
    col_cleaned_struct = df_.loc[df_['label'] == 'structure', 'cleaned']
    
    def extract_structure(cell):
        struct = [i for i in cell if i.isupper()]
        return struct

    lstruct = [extract_structure(cell) for cell in col_cleaned_struct]

    # Utilisation d'une compréhension de liste pour convertir lstruct en une liste de strings sans doublons
    lstruct = [' '.join(sublist) for sublist in set(tuple(sublist) for sublist in lstruct)]

    # # Récupération de la liste des personnages

    # on supprime les éléments à une lettre
    lstruct = [i for i in lstruct if len(i)>1]

    # lstage est la liste des éléments de découpage de la pièce
    exclusion_list = ['SCÈNE', 'ACTE', 'ENTRÉE', 'INTERMÈDE', 'PROLOGUE', 'ÉGLOGUE']
    if lstage is None:
        lstage = [i for i in lstruct if any(excl in i for excl in exclusion_list)]

    # lnom est la liste des noms
    exclusion_list = ['SCÈNE', 'ACTE', 'ENTRÉE', 'INTERMÈDE', 'PROLOGUE', 'ÉGLOGUE']
    if lnom is None:
        lnom = [i for i in lstruct if not any(excl in i for excl in exclusion_list)]

    # # Exploration

    # On transforme les listes de df_['cleaned'] en string
    df_['cleaned'] = list(map(lambda x : ' '.join(x),df_['cleaned']))

    # ## 1-Cleaning

    # A cde stade les listes ont été transformées en strings

    # ## 2-Extraction des données

    # Création d'un tableau réduit aux lignes étapes et personnages
    # On remplit de lignes data en in itèrant sur le DataFrame df_ en utilisant iterrows()
    data =  [['Index', 'Acte', 'Scène', 'Personnage', 'Nb de mots']] + [
        [index, nom, 0, 0, 0]
        for index, row in df_.iterrows()
        for nom in lnom + lstage
        if nom in row["cleaned"]]

    # Il y a un petit soucis avec les chiffres romains. On va supprimer les lignes inutiles donnant la priorité par rapport 
    # à une liste
    lstage.sort(reverse=True)

    def del_doublons(data):
        # Crée un dictionnaire pour marquer les doublons
        duplicates = {}

        for i in range(len(data) - 1):
            if data[i][0] == data[i+1][0]:
                # On vérifie quel genre de doublon c'est
                if data[i][1] in lstage:
                    i_ = lstage.index(data[i][1])
                    i__ = lstage.index(data[i+1][1])
                    if i__ > i_:
                        duplicates[i+1] = True
                    else:
                        duplicates[i] = True
                else:
                    duplicates[i+1] = True

        # On supprime les doublons marqués
        data = [x for i, x in enumerate(data) if i not in duplicates]

        return data

    # Supprimons les doublons
    while len(data) != len(set(x[0] for x in data)) :
        #print(len(data)-len(set(x[0] for x in data)))
        data = del_doublons(data)

    # on met les noms et les scènes à leur place
    for r in range(1, len(data)):
        if data[r][1] in lnom:
            data[r][3] = data[r][1]
            data[r][1] = 0  # on fait la même chose pour Scène

        try:
            if 'SCÈNE' in data[r][1]:
                data[r][2] = data[r][1]
                data[r][1] = 0
        except:
            continue

    # on fait la même chose pour Acte
    # Pas besoin il est déjà à sa place

    # Maintenant dans les lignes où on a le nom des personnages on va compter le nb de mot dans la tirade
    # On stock le n° de la ligne considérée
    list_nom_vide = [data[i][0] for i in range(1,len(data)) if data[i][3]!=0]

    # On stocke dans des variable l'index des lignes de départ (exlus) et de fin de la tirade (exclus)
    for i in range(0,len(list_nom_vide)):
        db = list_nom_vide[i]
        try :
            fi = list_nom_vide[i+1]
        except :
            fi = db + 2
        try :
            # On stocke dans une variable le nombre de mots entre db exclus jusqu'à fi exclus
            nb = reduce(lambda x,y : x+y, [len(df_.loc[df_.index ==r,"cleaned"].values.tolist()[0]) for r in range(db+1,fi)])
            # Et on met ce nombre dans la dernière cellule de la ligne correspondant à db dans data_
            index = None
            for i, row in enumerate(data):
                if row[0] == db:
                    index = i
                    break
            data[index][-1] = nb
        except :
            continue

    # Maintenant on met les actes et les scènes dans les lignes au même niveau que les personnages dans data_
    for r in range(1, len(data)):
        if data[r][1] != 0:
            i = r + 1
            try:
                while data[i][1] == 0:
                    data[i][1] = data[r][1]
                    i = i + 1
            except:
                pass

        if data[r][2] != 0:
            i = r + 1
            try:
                while data[i][2] == 0:
                    data[i][2] = data[r][2]
                    i = i + 1
            except:
                pass

    # Et pour terminer on supprime toutes les lignes qui n'ont pas de structure ou de personnage
    data = [row for row in data if row[2]!=0 and row[3]!=0]

    # On convertit ce tableau récapitulatif en df_ pour la visualisation
    data = pd.DataFrame(data[1:], columns = data[0])

    if genre == 'général':
        series = data.groupby(['Acte','Personnage'])['Nb de mots'].sum()

        # Calculer le total par personnage
        total_par_personnage = series.groupby(level='Personnage').sum()

        # définir les données du graphes
        absi = series.index.get_level_values('Personnage')
        ordo = series.index.get_level_values('Acte')

         # Créez une instance de la classe GraphResponse avec les données
        response_data = GraphResponse(
            absi=absi,
            ordo=ordo,
            vale=series.values.tolist(),
            tota=total_par_personnage.to_dict()
            )
        print("tota : ", total_par_personnage, "type :", type (total_par_personnage))
    
        content = jsonable_encoder(response_data)
        return JSONResponse(content=content)

    elif genre == 'correction':
        # Filtrage des éléments de visualisation

        # ATTENTION : on définit cette variable glbale pour pouvoir l'utiliser avec la fonction visualisation genre="répartition"
        global list_pers_c

        list_pers_c = lnom#['ANGÉLIQUE', 'ARGAN', 'BÉLINE', 'LE NOTAIRE', 'TOINETTE', 'ANGÉLIQUE','BÉRALDE', 'CLÉANTE', 'LOUIS', 'MONSIEUR DIAFOIRUS',                 'THOMAS DIAFOIRUS',  'MONSIEUR FLEURANT', 'MONSIEUR PURGON', 'LOUISON']

        list_stage = [i for i in lstage if 'ACTE' in i]#['ACTE I','ACTE II', 'ACTE III']

        data_select = data[data['Acte'].isin(list_stage) & data['Personnage'].isin(list_pers_c)]
        
        # On va lui rajouter une colonne 'acteur'
        data_select['Acteur'] = ""

        # On enregistre ce tableau au format csv
        data_select.to_csv("repartition.csv",index=False, sep=';')

        series = data_select.groupby(['Acte','Personnage'])['Nb de mots'].sum()

        # Calculer le total par personnage
        total_par_personnage = series.groupby(level='Personnage').sum()
        
        # définir les données du graphes
        absi = series.index.get_level_values('Personnage')
        ordo = series.index.get_level_values('Acte')

         # Créez une instance de la classe GraphResponse avec les données
        response_data = GraphResponse2(
            absi=absi,
            ordo=ordo,
            vale=series.values.tolist(),
            tota=total_par_personnage.to_dict(),
            datact=data_select.to_dict())
        #print(response_data['data_'])
        # Renvoyez la réponse JSON avec les données => personnages, actes, nb de mots, total, data_select
        content = jsonable_encoder(response_data)
        return JSONResponse(content=content)           

if __name__ == "__main__":
    analyser = AnalyseTheatre()
    # Vous pouvez appeler la méthode `visualisation` ici ou effectuer d'autres opérations avec la classe.