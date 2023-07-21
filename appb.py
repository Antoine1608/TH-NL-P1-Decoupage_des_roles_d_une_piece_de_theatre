#!/usr/bin/env python
# coding: utf-8

# In[1]:

#général
import pandas as pd
import numpy as np
import time
import io
import base64
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import json
from typing import List
from fastapi import FastAPI
import pickle
import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import uvicorn
from pydantic import BaseModel


# In[2]:


# Initialisation de l'application FastAPI
app = FastAPI()
graphe_path = r"C:\Users\John\Desktop\Formation\TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre\graphe.png"

# Fonction de Traitement
def treat(lnom, lnom_comp, lstage):


    #traitement texte
    import re

    #visualisation
    import matplotlib.pyplot as plt


    # In[2]:

    #données d'entrée
    df=pd.read_fwf(r"C:\Users\John\Desktop\Formation\TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre\Le_Malade_imaginaire.txt",header=None,sep=" ")
    # # Exploration

    # In[3]:


    # extrait du df
    df[300:350]


    # ## 1-Cleaning

    # In[4]:

    # In[5]:


    # On enlève la ponctuation et on tokenize
    #from nltk.tokenize import word_tokenize
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    df = df.applymap(lambda x : tokenizer.tokenize(x) if type(x) == str else x)
    
    # In[6]:


    # Rassembler les lignes dans une colonne "cleaned"
    from functools import reduce
    col = []
    for i in range(0, len(df)):
        col.append(reduce(lambda x,y : x+y if (type(x) == list and type(y) == list) else x, df[i:i+1].values.tolist()[0]))
    df["cleaned"] = col


    # ## 2-Extraction des données

    # In[8]:


    # Création d'un tableau réduit aux lignes étapes et personnages. Les lignes sont identifiées par leur index
    data = [['Index', 'Acte', 'Scène', 'Personnage', 'Nb de mots']]
    print("line 108")

    # In[9]:


    # On itère le tableau data
    # pour chaque ligne
    for r in range(0, len(df)):
        # si elle contient un mot de lnom ou lstage
        for nom in lnom + lstage + lnom_comp:
            try:
                if nom in df["cleaned"][r][0:1]:
                    # on appende la ligne
                    data.append([r,df["cleaned"][r][0:2],0,0,0])
            except:
                continue

    print("line 125")
    # In[10]:


    # stockage des noms au type texte au lieu de liste
    for i in range(0,len(data)):
        for n in lnom:
            if n in data[i][1]:
                data[i][1] = n
        for n in lnom_comp:
            if n in data[i][1]:
                data[i][1] = ' '.join(data[i][1])


    # In[11]:


    # petite vérification sur les actes et intermèdes
    ext = [sous_liste for sous_liste in data if any(isinstance(item, list) and ('INTERMÈDE' in item or 'ACTE' in item) for item in sous_liste if isinstance(item, (str, list)))]
    ext
    print("line 145")

    # In[12]:


    # on cherche l'index du df de la première ligne qui contient 'ACTE' dans data
    start_index = data.index([303, ['ACTE', 'PREMIER'], 0, 0, 0])


    # In[13]:


    # on redessine data en data_ à partir de cette ligne
    data_ = data.copy()
    data_ = data_[0:1]+data_[6:]


    # In[14]:


    # on met les noms à leur place
    for r in range(1, len(data_)):
        if isinstance(data_[r][1],str):
            
            data_[r][3]=data_[r][1]
            data_[r][1]=0


    # In[15]:


    # CORRECTIF : On remplace les monsieur de par monsieur de bonnefoi
    for i in range(0,len(data_)):
        if data_[i][3] == 'monsieur de':
            data_[i][3] = 'monsieur de bonnefoi'    


    # In[16]:


    # on fait la même chose pour ACTE
    for r in range(1, len(data_)):
        try:
            if 'ACTE' in data_[r][1]:
                new = data_[r][1][0] + " " + data_[r][1][1]
                data_[r][1] = new
        except:
            continue


    # In[17]:


    # on fait la même chose pour Scène
    for r in range(1, len(data_)):
        try:
            if 'Scène' in data_[r][1]:
                new = data_[r][1][0] + " " + data_[r][1][1]
                data_[r][2] = new
                data_[r][1] = 0
        except:
            continue


    # In[18]:


    # Maintenant dans les lignes où on a le nom des personnages on va compter le nb de mot dans la tirade
    # On stock le n° de la ligne considérée
    list_l = [data_[i][0] for i in range(1,len(data_)) if data_[i][3]!=0]


    # In[19]:


    # On stocke dans des variable l'index des lignes de départ (exlus) et de fin de la tirade (exclus)
    for i in range(0,len(list_l)):
        db = list_l[i]
        try :
            fi = list_l[i+1]
        except :
            fi = db + 2
        # On stocke dans une variable le nombre de mots entre db exclus jusqu'à fi exclus
        nb = reduce(lambda x,y : x+y, [len(df.loc[df.index ==r,"cleaned"].values.tolist()[0]) for r in range(db+1,fi)])
        # Et on met ce nombre dans la dernière cellule de la ligne correspondant à db dans data_
        index = None
        for i, row in enumerate(data_):
            if row[0] == db:
                index = i
                break
        data_[index][-1] = nb


    # In[20]:
    print("line 239")

    #on va colorer les lignes caractéristiques détectées et voir ce que ça donne sur un doc excel

    # Indices des lignes à colorer
    indices_to_color = [data[r][0] for r in range(1, len(data))]

    # Création de la fonction de mise en forme pour colorer les lignes spécifiques
    def highlight_row(row):
        if row.name in indices_to_color:
            return ['background-color: yellow'] * len(row)
        else:
            return [''] * len(row)

    # Application de la fonction de mise en forme au DataFrame
    styled_df = df.style.apply(highlight_row, axis=1)

    # Affichage du DataFrame stylisé
    #styled_df.to_excel("df_color.xlsx")


    # In[21]:


    # Maintenant on mais les acte et les scènes dans les lignes au même niveau que les personnages dans data_
    # Si la ligne contient Acte on copie cette données dans les cellules du dessous jusqu'à rencontrer une 
    # nouvelle cellule différente de 0
    for r in range(1,len(data_)):
        if data_[r][1] != 0:
            i = r+1
            try:
                while data_[i][1] == 0:
                    data_[i][1] = data_[r][1]
                    i = i+1
            except:
                break


    # In[22]:


    # Même chose avec les scène
    for r in range(1,len(data_)):
        if data_[r][2] != 0:
            i = r+1
            try:
                while data_[i][2] == 0:
                    data_[i][2] = data_[r][2]
                    i = i+1
            except:
                break


    # In[23]:


    # Et pour terminer on supprime toutes les lignes qui n'ont pas de personnage
    data_f = [row for row in data_ if row[3]!=0]


    # In[24]:


    # On convertif en df
    df_t = pd.DataFrame(data_f[1:], columns = data_f[0])


    # In[25]:


    series = df_t.groupby(['Acte','Personnage'])['Nb de mots'].sum()


    # ## Visualisation

    # In[26]:

    print("line 316")
    # Calculer le total par personnage
    total_par_personnage = series.groupby(level='Personnage').sum()

    return[series, total_par_personnage]

 # In[3]:


@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API de répartion de rôles"}


# In[4]:


# In[5]:


class Input(BaseModel):
    #url_:str
    lnom_:list  
    lnom_comp_:list
    lstage_:list        


# In[12]:


@app.post("/traitement")
def graphe(input:Input):
    data_in = input.dict()
    print(data_in)
    #df = pd.read_fwf(data['url_'])
    #df=pd.read_fwf(r"C:\Users\John\Desktop\Formation\TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre\Le_Malade_imaginaire.txt",header=None,sep=" ")
    lnom = data_in['lnom_']
    lnom_comp = data_in['lnom_comp_']
    lstage = data_in['lstage_']
    print('line 400')
    series = treat(lnom, lnom_comp, lstage)[0]
    total_par_personnage = treat(lnom, lnom_comp, lstage)[1]

    # Création du graphique en boules initial
    print('line 405')
    # Sauvegarder l'image en mémoire BytesIO
    buffer = io.BytesIO()
    fig, ax = plt.subplots(figsize=(15, 6))


    
    print('line 407')
    print(series.index.get_level_values('Personnage'))
    print(series.index.get_level_values('Acte'))
    ax.scatter(series.index.get_level_values('Personnage'), series.index.get_level_values('Acte'),
               s=series.values, alpha=0.7)
    print('line 410')
    # Ajouter des boules pour le total par personnage
    for personnage, total in total_par_personnage.items():
        ax.scatter(personnage, "Total", s=total, c='green', alpha=0.7)#, label=f'Total {personnage}')

    # Configuration des axes et du titre
    ax.set_xlabel('Personnage')
    ax.set_ylabel('Acte')
    ax.set_title('Graphique en boules - Nb de mots')
    plt.xticks(rotation=45)

    # Afficher la valeur dans la boule pour le graphique initial
    for x, y, val in zip(series.index.get_level_values('Personnage'), series.index.get_level_values('Acte'), series.values):
        ax.annotate(str(val), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # Afficher la valeur dans la boule pour le total par personnage
    for personnage, total in total_par_personnage.items():
        ax.annotate(str(total), (personnage, "Total"), textcoords="offset points", xytext=(0, 10), ha='center')

    # Légende pour les boules du total par personnage
    ax.legend()
 
    # Affichage du graphique
    #plt.show()
    
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir l'image en base64
    image_base_64 = base64.b64encode(buffer.getvalue()).decode()
   
    #return {"graph_image": image_base_64}

    # Enregistrer l'image sur le disque
    plt.savefig(graphe_path, format='png')

    # Fermer le graphe pour libérer les ressources
    plt.close()
    print("temps de traitement =", time.time()-t1)
    #return {"graph_image": image_base_64}

    return graphe_path
#Avec cette modification, l'image sera enregistrée sous le chemin spécifié dans la variable graphe_path. Assurez-vous de remplacer "/chemin/vers/votre/dossier/image.png" par le chemin absolu où vous souhaitez enregistrer l'image.


#Après avoir enregistré l'image sur le disque, vous pouvez renvoyer le chemin d'accès à l'image dans la réponse JSON de votre fonction graphe.
#Vous pouvez ensuite utiliser cette URL d'image dans votre frontend pour afficher l'image dans le navigateur.


@app.get("/show/")
async def read_file():
    from fastapi import FastAPI, File, UploadFile
    from fastapi.responses import FileResponse
 
    # get file path
    file = f"{graphe_path}"
     
    return FileResponse(file)


# In[7]:


if __name__ == "__main__":
    t1 = time.time()
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print("temps de traitement = ", time.time()-t1)


# In[ ]:




