def import_text():
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
    
    # Affichez la liste des liens .txt
    return(txt_links)   

if __name__ == "__main__":
    analyser = AnalyseTheatre()
    # Vous pouvez appeler la méthode `visualisation` ici ou effectuer d'autres opérations avec la classe.
