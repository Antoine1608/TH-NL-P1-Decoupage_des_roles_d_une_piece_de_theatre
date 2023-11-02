## -*- coding: utf-8 -*-

import streamlit as st
st.set_page_config(layout="wide")
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import requests
import time
import re
import FrontendFunc


st.set_option('deprecation.showPyplotGlobalUse', False)

repartition = pd.DataFrame()
data_visu_correc = {}
def main():
    global repartition
    global data_visu_correc

# Choisir en mettant entre triple apostrophes la deuxième option ou pas

# LOCAL
    fastapi_url = "http://127.0.0.1:8000/visu_gen"  # Update with your FastAPI server URL LOCAL    
    fastapi_struct = "http://127.0.0.1:8000/visu_str"  # Update with your FastAPI server URL => en LOCAL  
    fastapi_per = "http://127.0.0.1:8000/visu_per"  # Update with your FastAPI server URL => en LOCAL    
    fastapi_correc = "http://127.0.0.1:8000/visu_perso"  # Update with your FastAPI server URL LOCAL    

# DOCKER
    fastapi_url = "http://fastapi:8000/visu_gen"  # Update with your FastAPI server URL DOCKER
    fastapi_struct = "http://fastapi:8000/visu_str"  # Update with your FastAPI server URL => pour DOCKER
    fastapi_per = "http://fastapi:8000/visu_per"  # Update with your FastAPI server URL => pour DOCKER
    fastapi_correc = "http://fastapi:8000/visu_perso"  # Update with your FastAPI server URL DOCKER
    
    # Titre de la page
    st.title("Répartir les rôles sur une pièce de théâtre")
    
    values = FrontendFunc.import_text()[0]
    titles = FrontendFunc.import_text()[1]
    
    titre = st.sidebar.selectbox(
        "Veuillez sélectionner une pièce de théâtre",
        values)

    idx = values.index(titre)
    
    st.title(titles[idx])
    #Le bouton de prédiction
    input_data = {'url_':str(titre)}

    if st.button("Répartition Personnages - Acte"):

        # Define the FastAPI endpoint URL# Voir au début 
        # Voir au début fastapi_url
        

        # Make a POST request to the FastAPI endpoint
        response = requests.post(fastapi_url, json=input_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_visu = response.json()  # Parse the JSON response
        else:
            st.error(f"Error: {response.status_code}")

        # Construction du graphe
        fig, ax = plt.subplots(figsize=(15, 6))

        ax.scatter(data_visu['absi'], data_visu['ordo'],
                   s=data_visu['vale'], alpha=0.7)

        # Ajouter des boules pour le total par personnage
        for personnage, total in data_visu['tota'].items():
            ax.scatter(personnage, "Total", s=total, c='green', alpha=0.7)#, label=f'Total {personnage}')

        # Configuration des axes et du titre
        ax.set_xlabel('Personnage')
        ax.set_ylabel('Acte')
        ax.set_title('Graphique en boules - Nb de mots')
        plt.xticks(rotation=45)

        # Afficher la valeur dans la boule pour le graphique initial
        for x, y, val in zip(data_visu['absi'], data_visu['ordo'], data_visu['vale']):
            ax.annotate(str(val), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

        # Afficher la valeur dans la boule pour le total par personnage
        for personnage, total in data_visu['tota'].items():
            ax.annotate(str(total), (personnage, "Total"), textcoords="offset points", xytext=(0, 10), ha='center')

        # Affichage du graphique
        st.pyplot()       
        
    # Enregistrement de la liste des personnages retenus :
    st.write("## Choisir les personnages")   
    per_ret = st.text_input("Mettez ici la liste des personnages retenus (format [ARGAN, TOINETTE, ...] : ")
    
    # Adaptation du format

    chaine = str(per_ret)  # Convertir la liste en une chaîne de texte
    per_ret = re.sub(r"['\"]", "", chaine)  # Retirer les guillemets simples et doubles

    
    #création d'un nouvel input
    input_datab = {'url_':str(titre),'lnom_':str(per_ret)}

    # Define the FastAPI endpoint URL
    # Voir au début fastapi_correc
    
    # Make a POST request to the FastAPI endpoint
    response = requests.post(fastapi_correc, json=input_datab)  # Modify the JSON input as needed

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_visu_correc = response.json()  # Parse the JSON response
        #st.write(data_visu_correc)  # Display the data in Streamlit
    else:
        st.error(f"Error: {response.status_code}")
    
    if st.button("Répartition Personnages retenus - Acte"):
        # construction du graphe
        fig, ax = plt.subplots(figsize=(15, 6))
    
        ax.scatter(data_visu_correc['absi'], data_visu_correc['ordo'],
                   s=data_visu_correc['vale'], alpha=0.7)
    
        # Ajouter des boules pour le total par personnage
        for personnage, total in data_visu_correc['tota'].items():
            ax.scatter(personnage, "Total", s=total, c='green', alpha=0.7)#, label=f'Total {personnage}')
    
        # Configuration des axes et du titre
        ax.set_xlabel('Personnage')
        ax.set_ylabel('Acte')
        ax.set_title('Graphique en boules - Nb de mots')
        plt.xticks(rotation=45)
    
        # Afficher la valeur dans la boule pour le graphique initial
        for x, y, val in zip(data_visu_correc['absi'], data_visu_correc['ordo'], data_visu_correc['vale']):
            ax.annotate(str(val), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
    
        # Afficher la valeur dans la boule pour le total par personnage
        for personnage, total in data_visu_correc['tota'].items():
            ax.annotate(str(total), (personnage, "Total"), textcoords="offset points", xytext=(0, 10), ha='center')
    
        # Affichage du graphique
        st.pyplot()

############Déporter toute cette partie##############################           
    # On affiche le graphique de répartition des rôles           
    repartition = pd.DataFrame()
    
    # Define the FastAPI endpoint URL
    # Voir fastapi_correc au début
    
    # Make a POST request to the FastAPI endpoint
    response = requests.post(fastapi_correc, json=input_datab)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_visu = response.json()  # Parse the JSON response
    else:
        st.error(f"Error: {response.status_code}")
    
    # récupération des données d'entrée (faire attention à avoir bien rempli le tableau)
           
    repartition = pd.DataFrame(data_visu['datact'])
    # On groupe par Acte et Acteur et on somme le nombre de mots
    repartition_ = repartition.groupby(['Acte','Personnage'])['Nb de mots'].sum().reset_index()
    repartition_['Acteur'] = ""
    st.write('## Choisir les acteurs')
          
    acteur = []  # Créez une liste vide
    for i, row in repartition_.iterrows():
        acteur = st.text_input(f"Acteur pour {row['Personnage']} dans {row['Acte']}", key=i)
        repartition_.at[i, 'Acteur'] = acteur
        print("-repart : ",repartition_.at[i, 'Acteur'])
    
    st.write('Répartition des rôles :')
    st.write(repartition_)
    
    # Ensuite, vous pouvez utiliser la ligne suivante pour regrouper par 'Acteur'
    total_par_acteur = repartition_.groupby(['Acteur'])['Nb de mots'].sum().reset_index()
    
    repartition = repartition_
            
    if st.button("Répartition Acteurs - Acte"):
    
        # Calculer le total par acteur
        total_par_acteur = repartition.groupby(['Acteur'])['Nb de mots'].sum()
        
        # Création du graphique en boules initial
        
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.scatter(repartition['Acteur'], repartition['Acte'],
                   s=repartition['Nb de mots'], alpha=0.7)
    
        # Ajouter des boules pour le total par acteur
        for acteur, total in total_par_acteur.items():
            ax.scatter(acteur, "Total", s=total, c='green', alpha=0.7)
    
        # Configuration des axes et du titre
        ax.set_xlabel('Acteur')
        ax.set_ylabel('Acte')
        ax.set_title('Graphique en boules - Nb de mots')
        plt.xticks(rotation=45)
            
        # Afficher la valeur dans la boule pour le graphique initial
        for x, y, val in zip(repartition['Acteur'], repartition['Acte'], repartition['Nb de mots']):
            ax.annotate(str(val), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
    
        # Afficher la valeur dans la boule pour le total par acteur
        for acteur, total in total_par_acteur.items():
            ax.annotate(str(total), (acteur, "Total"), textcoords="offset points", xytext=(0, 10), ha='center')
    
        # Affichage du graphique
        st.pyplot() 
############Déporter toute cette partie##############################  
        
if __name__ == '__main__':
    main()
