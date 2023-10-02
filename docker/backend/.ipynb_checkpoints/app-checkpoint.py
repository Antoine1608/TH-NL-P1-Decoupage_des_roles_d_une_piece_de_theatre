#import
import pandas as pd
import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import BackendFunc
import re

#instantiation de FastApi
app = FastAPI()

#la liste des url des textes txt_links
import requests
from bs4 import BeautifulSoup

# URL de la page web à scraper
url = 'http://www.theatre-classique.fr/pages/programmes/PageEdition.php'

# Faites une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Vérifiez si la requête a réussi (statut code 200)
if response.status_code == 200:
    # Utilisez BeautifulSoup pour analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Créez une liste vide pour stocker les éléments href se terminant par '.txt'
    txt_links = []
    
    # Trouvez tous les éléments <a> ayant un attribut href se terminant par '.txt'
    elements = soup.find_all('a', href=lambda href: href and href.endswith('.txt'))

    # Parcourez les éléments trouvés et modifiez l'attribut href pour remplacer '../txt/' par 'http://www.theatre-classique.fr/pages/txt/'
    for element in elements:
        href_value = element['href']
        new_href = href_value.replace('../txt/', 'http://www.theatre-classique.fr/pages/txt/')
        element['href'] = new_href
    # et ajoutez leur contenu (liens) à la liste txt_links
        txt_links.append(new_href)
else:
    print('La requête a échoué avec le code de statut :', response.status_code)

class Input(BaseModel):
    url_:str

class Inputb(BaseModel):
    url_:str
    lnom_:str

class Inputc(BaseModel):
    fil_:str

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API de répartion de rôles"}
    print("217") 

#   choisir un texte dans le menu déroulant - appui bouton 1

#   choisir un texte perso - appui bouton 2

#   appui bouton  1 ou 2 => lancer l'analyse brute et afficher :
#   le graphique
@app.post("/visu_gen")
def visu(input:Input):
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

    return BackendFunc.visualisation(df=df, genre="général")

#   la structure dramatique
@app.post("/visu_str")
def visu_str(input:Input):
    import os
    text = input.dict()

    # Récupérez l'URL du fichier texte de la pièce qui nous intéresse
    file_url = text['url_']

    # Faites une requête HTTP pour télécharger le contenu du fichier texte
    file_response = requests.get(file_url)
    print('file_response OK')

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

    return BackendFunc.liste_stage(df)
    
#   la liste des personnage
@app.post("/visu_per")
def visu_per(input:Input):
    import os
    text = input.dict()

    # Récupérez l'URL du fichier texte de la pièce qui nous intéresse
    file_url = text['url_']

    # Faites une requête HTTP pour télécharger le contenu du fichier texte
    file_response = requests.get(file_url)
    print('file_response OK')

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

    return BackendFunc.liste_perso(df)

#   enregistrer le texte labellisé et coloré

#   après correction/personnalisation des listes - appui bouton 3

#   appui bouton 3 => lancer l'analyse personnalisée

@app.post("/visu_perso")
def visu_perso(input:Inputb):
    import os
    text = input.dict()

    # Récupérez l'URL du fichier texte de la pièce qui nous intéresse
    file_url = text['url_']
    print('file_url OK :', file_url)

    # Faites une requête HTTP pour télécharger le contenu du fichier texte
    file_response = requests.get(file_url)
    print('file_response OK')

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

    # on récupère la liste des personnages retenus
    chaine = text['lnom_']
    l_nom = re.findall(r'\b\w+(?:\s+\w+)*\b', chaine)
    l_nom = [nom.strip(', ') for nom in l_nom]

    return BackendFunc.visualisation(df=df, genre="correction", lnom=l_nom)

#   et enregistrer le tableau pour la répartition des rôles

#   après modification du tableau de répartition des rôle - appui bouton 4
#   appui bouton 4 => graphique
    # Après l'avoir modifié on le rappelle   

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)