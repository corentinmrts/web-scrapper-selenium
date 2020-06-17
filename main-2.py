# Objectif de ce web scrapper est de récupérer les infos suivantes
# sur les startups référencées sur le site de la BPI :
# nom, date de création, montant levé, noms et prénoms de responsables
# On utilise un web brower (selenium). Il doit être situé dans un path exécutable
# en local




# --------------------- MODULES ---------------------

from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from IPython.display import clear_output
import csv

# --------------------- end modules ---------------------




# ------------------------ Début: Fonction pour tester la taille d'échantillon du driver ------------------------

def test_driver(new_sample, ref_sample_length):
# Arguments: 1. Echantillon après itération / 2. Longueur de l'échantillon de départ
# Script: Pause le script tant que la taille des résultats d'itération n'est pas la même que celle de l'échantillon de départ
# Retourne: Le nombre d'essais nécessaires

    # On compte le nombre d'essais nécessaires avant que le driver ne capte les résultats de la page
    attempts = 0

    # Tant que le driver n'a pas capté les résultats de la page ...
    while len(new_sample) != ref_sample_length:

        # On incrémente le compteur de tentatives d'une unité
        attempts += 1

        # On pause pendant 4 secondes supplémentaires
        time.sleep(4)

        # On réessaie de récupérer les résultats
        new_sample = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[6]/div/div/div')

    # On indique le nombre d'essais nécessaires avant résolution du problème
    print("Nombre d'essais nécessaires avant résolution du problème de taille d'échantillon: {}".format(attempts))

    # On retourne le nouvel échantillon
    return new_sample

# ------------------------ Fin: Fonction pour tester la taille d'échantillon du driver ------------------------




# ------------------------ Début: Accéder à la première page ------------------------

# On récupère l'url de la page (ici filtrée sur B2B & Banque)
url = 'https://lehub.web.bpifrance.fr/search?advancedmode=1&refinementList%5BbusinessModels%5D%5B0%5D=B2B&refinementList%5Bmarkets%5D%5B0%5D=Banque%20%2F%20Finance&page=1'

# On exécute le webdriver
driver = selenium.webdriver.Firefox(executable_path = '/Users/maertens/Desktop/path/geckodriver')

# On charge la page souhaitée
driver.get(url)

# On pause 2 secondes
time.sleep(2)

# On vérifie qu'il y a un bouton d'acceptation des cookies
try:

    # On récupère le xpath du bouton cookies
    cookies_button = driver.find_element_by_xpath('//*[@id="footer_tc_privacy_button"]')

    # On fait disparaître le bandeau cookies
    cookies_button.click()

# S'il n'y a pas de bouton d'acceptation des cookies, on ne fait rien
except:
    pass

# ------------------------ Fin: Accéder à la première page ------------------------




# ------------------------ Début: Boucler sur les startups de la page 1 ------------------------

# On récupère les infos des startups de cette page
startups = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[6]/div/div/div')

# On stocke le nombre de startups présentes sur cette page
results_length = len(startups)

# On créé une liste vide pour stocker les données
# On veut constituer une liste de dictionnaires
data = []

# On initialise le compte d'itérations
count = 0

# On boucle sur le nombre de startups présentes sur cette page
for i in range(results_length):

    # On récupère son nom (on l'affiche) et sa date de création
    name = startups[i].find_element_by_class_name('ais-Highlight-nonHighlighted').text
    print(name)
    creation = int(startups[i].find_elements_by_class_name('sc-hqyNC')[0].text)

    # S'il est indiqué, on récupère son montant total levé
    try:
        money = startups[i].find_elements_by_class_name('sc-hqyNC')[1].text
    except IndexError:
        money = 'Unknown'

    # On ajoute ses informations aux données de la startup considérée
    startup_data = {'Nom': name, 'Date de création': creation, 'Montant total levé': money}

    # On accède aux informations détaillées sur cette startup
    startups[i].find_element_by_class_name('ais-Highlight-nonHighlighted').click()

    # On pause le script pendant 2 secondes
    time.sleep(2)

    # On récupère les infos sur ses contacts et ses postes
    contacts = [contact.text for contact in driver.find_elements_by_class_name('sc-fhYwyz.gCIxFv')]
    positions = [position.text for position in driver.find_elements_by_class_name('sc-jzgbtB.dujiXt')]

    # On ajoute ses informations aux données de la startup considérée
    # en fonction du nombre de contacts présent sur la fiche de la startup
    if len(contacts) == 0:
        pass

    elif len(contacts) == 1:
        startup_data['Contact 1'] = contacts[0]
        startup_data['Poste 1'] = positions[0]

    elif len(contacts) == 2:
        startup_data['Contact 1'] = contacts[0]
        startup_data['Poste 1'] = positions[0]
        startup_data['Contact 2'] = contacts[1]
        startup_data['Poste 2'] = positions[1]

    elif len(contacts) == 3:
        startup_data['Contact 1'] = contacts[0]
        startup_data['Poste 1'] = positions[0]
        startup_data['Contact 2'] = contacts[1]
        startup_data['Poste 2'] = positions[1]
        startup_data['Contact 3'] = contacts[2]
        startup_data['Poste 3'] = positions[2]
    else:
        startup_data['Contact 1'] = contacts[0]
        startup_data['Poste 1'] = positions[0]
        startup_data['Contact 2'] = contacts[1]
        startup_data['Poste 2'] = positions[1]
        startup_data['Contact 3'] = contacts[2]
        startup_data['Poste 3'] = positions[2]
        startup_data['Contact 3'] = contacts[3]
        startup_data['Poste 3'] = positions[3]

    # On ajoute la fiche startup au dataset
    data.append(startup_data)

    # On revient à la page précédente
    driver.get(url)

    # On pause le script pendant 2 secondes
    time.sleep(2)

    # On réactualise les infos des startups de cette page
    startups = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[6]/div/div/div')

    # On vérifie qu'il n'y ait pas de problèmes d'échantillons
    startups = test_driver(startups, results_length)

    # On affiche le statut de la boucle
    count += 1
    print('{} itérations effectuées.'.format(count))
    print('-----------------------')
    #clear_output(wait = True)

# ------------------------ Fin: Boucler sur les startups de la page 1------------------------




# ------------------------ Début: Export CSV ------------------------

with open("data.csv", "w", newline="") as csv_file:
  cols = ["Nom","Date de création","Montant total levé","Contact 1","Poste 1",
  "Contact 2", "Poste 2", "Contact 3", "Poste 3"]
  writer = csv.DictWriter(csv_file, fieldnames=cols)
  writer.writeheader()
  writer.writerows(startup_data)
