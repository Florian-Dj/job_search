# Recherche d'emploi
Exécutable permettant de savoir les dernières offres d'emplois sur vos sites.

## Exigence
- Python >= 3.8
    - BeautifulSoup4 >= 4.9.*
    - Requests >= 2.24.*
    - Playsound >= 1.2.*
    - Django == 3.1

## Utilisation

## Mise à jour
**V0.3**
- Pannel Web Django
- Pannel Admin
- Page Accueil avec les 10 dernières annonces
- Page pour voir les recherche et annonces
- Ajout de paramétres page annonces  *(tout, non lu, postulé, expiré, inadéquate)*
- Ajout de paramétres page annonces *(Leboncoin, Linkedin, Pole-Emploi)*
- Formulaire pour ajouter des recherches
- Bouton pour chercher les nouvelles annonces

V0.2
- Ajout du status des annonces *(non lues, postulées, inadéquite, expirées)*
- Ajout un sous menu dans les annonces *(non lue, postulée, expirée, inadéquate)*
- Possibilité de voir toutes les annonces du même status d'un site
- Ajout d'une  colonne status dans la table annonce

V0.1
- Ajouter et supprimer des recherches
- Liste des annonces et des recherches
- Analyse des offres sur Pôle Emploi, Linkedin et Leboncoin
- Alertes sonnore d'une nouvelle annonce
- Fichier option pour les temps de recharge

## Idées
- Changer les status des annonces directement sur la page
- Savoir si l'annonce est relancée *(redondante pour negocier le salaire)*
