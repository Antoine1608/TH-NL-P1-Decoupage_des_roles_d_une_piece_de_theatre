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

st.set_option('deprecation.showPyplotGlobalUse', False)


def main():

    # Titre de la page
    st.title("Répartir les rôles sur une pièce de théâtre")
    st.text("Données client : ")

    #values = df['SK_ID_CURR'].values
    values = ['http://www.theatre-classique.fr/pages/txt/MOLIERE_MALADEIMAGINAIRE.txt','http://www.theatre-classique.fr/pages/txt/ABEILLE_ARGELIE.txt',
     'http://www.theatre-classique.fr/pages/txt/ABEILLE_CORIOLAN.txt',
     'http://www.theatre-classique.fr/pages/txt/ABEILLE_LYNCEE.txt',
     'http://www.theatre-classique.fr/pages/txt/ABOUT_RISETTE.txt',
     'http://www.theatre-classique.fr/pages/txt/ADENIS_HOMMEQUINEPEUTPASSIFFLER.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_AVAREAMOUREUX.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_PANETDORIS.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_POLIXENE.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_PROLOGUE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALAINLEGRAND_EPREUVERECIPROQUE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAINVAL_ECOLEDESBOURGEOIS.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAINVAL_HIVER.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAIS_BONBOUGRE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAIS_MECONTENT.txt',
     'http://www.theatre-classique.fr/pages/txt/ANCELOT-ARAGO_PAPILLOTES.txt',
     'http://www.theatre-classique.fr/pages/txt/ANCELOT-AUGER_SEDUCTION.txt']
    titre = st.sidebar.selectbox(
        "Veuillez sélectionner une pièce de théâtre",
        values)

    #Le bouton de prédiction
    input_data = {'url_':str(titre)}
    print('url_', json.dumps(input_data))

    if st.button("visualisation"):
        t1 = time.time()
        #resultat = requests.post(url="http://monapp.herokuapp.com/predict",data=json.dumps(input_data))
        result = requests.post(url="http://127.0.0.1:8000/visu_gen",data=json.dumps(input_data))
        # Désérialisation du graphe depuis le fichier
        with open('mon_graphe.pickle', 'rb') as f:
            loaded_fig = pickle.load(f)

        # Maintenant, vous pouvez afficher le graphe désérialisé
        #plt.show()
        st.pyplot()
        print('temps de traitement : ',time.time()-t1)
        
if __name__ == '__main__':
    main()


