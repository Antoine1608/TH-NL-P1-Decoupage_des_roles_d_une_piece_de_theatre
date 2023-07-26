# Répartir les rôles dans une pièces de théâtre
Comment répartir équitablement les rôles dans une troupe de x acteurs alors qu'il y a y personnages dans la pièces ?
Cette API en python facilite le calcul.

# Comment ça fonctionne ?
1-Clonez le dépôt sur votre ordinateur

2-Dans la CLI lancez la commande `cd TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre`

3-A la suite lancez la commande `python API\api.py`

4-Vous devriez avoir un message du type:

<img width="497" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/9fa6e241-99c3-45ef-a43c-562752bd8b58"> 

5-Saisissez l'adresse `127.0.0.1:8888/docs` dans votre explorateur internet

6-Vous devriez avoir la fenêtre suivante qui s'ouvre: 

<img width="926" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/6b08a4c5-4cc2-4720-8b64-6ead202ac2d8">

7-Appuyez sur 
  Traitement, 
  Try it out, 
  saisissez `{
  "lnom_": ["argan", "béline", "angélique", "cléante", "béralde", "louison", "toinette"],
  "lnom_comp_": ["monsieur", "thomas"],
  "lstage_": ["ACTE", "Scène", "prologue", "INTERMÈDE"]
}`, 
  appuyez sur Execute
et vous devriez voir apparaître le message 200 Successfull Response

8-Appuyez ensuite sur 
  Show,
  Try it out,
  Execute
et vous devriez voir appraître le graphe suivant:
<img width="738" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/23988653-0366-4941-b4cf-7185951e83ad">

Et voilà pour le moment! Je travaille sur la suite




