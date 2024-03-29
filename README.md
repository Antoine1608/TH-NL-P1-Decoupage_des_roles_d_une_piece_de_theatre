# Répartir les rôles dans une pièce de théâtre
Comment répartir équitablement les rôles dans une troupe de x acteurs alors qu'il y a y personnages dans la pièce ? Comment faire si un rôle est partagé entre plusieurs acteurs ?
Cette API en python déployable avec docker-compose facilite le calcul.

# Comment ça fonctionne ?
Prérequis : 

-Les OS Windows, Mac OS, Linux sont supportés

-Docker-Desktop

<img width="133" alt="docker-logo" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/f8b2524b-0bf5-4347-abb7-a5fa7bad1189">

-Git

1-Dans git bash lancez la commande `git clone https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre.git` pour cloner le dépôt

2-Lancez Docker Desktop

3-Dans la CLI lancez la commande `C:\Users\John\Desktop\TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre\docker>docker-compose up -d`

4-Saisissez l'adresse `http://localhost:8501` dans votre explorateur internet

5-Vous devriez avoir l'écran suivant:

<img width="845" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/f32cbe5c-712d-4b39-8e85-c99eda29937c">

6-Sélectionnez une pièce dans le menu déroulant à gauche

7-Appuyez sur le bouton `Répartition Personnages - Acte` et vous devriez voir apparaître un graphe de ce type:

<img width="633" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/97278232-0928-4e58-a8b7-22c47509ed10">

8-Parmi les personnages mentionnés sur le graphe, sélectionnez ceux qui vous intéressent et entrez les dans une liste comme ceci par exemple (attention, respectez bien le format) :

<img width="644" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/3ee14e3f-19ae-43d0-88fe-aae2fc03c380">

et appuyez sur `Entrée` 

9-Appuyez ensuite sur `Répartition Personnages retenus - Acte` et vous devriez voir apparaître un graphe de ce type: 

<img width="637" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/7630e146-c1b8-4926-8a41-bd06538dd885">

10-Choisir les acteurs pour chaque personnage dans chaque acte (il n'est pas nécessaire de remplir toutes les cases):

<img width="662" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/a1028d0c-ea7b-4f63-b8aa-6f00f7b77799">

11-Puis appuyez sur `Répartition Acteurs - Acte` et vous devriez voir apparaître un graphe de ce type:

<img width="631" alt="image" src="https://github.com/Antoine1608/TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre/assets/75375490/d48d2156-a350-4b61-a470-2ac62b1e763a">

Et voilà ! A vous de jouer
