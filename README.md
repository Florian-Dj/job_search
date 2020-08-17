# Recherche d'emploi
Exécutable permettant de savoir les dernières offres d'emplois sur vos sites.

## Exigence
- BeautifulSoup4 ==> 4.9.*+
- Requests ==> 2.24.*+

## Utilisation

## Mise à jour
**V0.2**
- Ajout du status des annonces *(non lues, postulées, inadéquite, expirées)*

V0.1
- Ajouter et supprimer des recherches
- Liste des annonces et des recherches
- Analyse des offres sur Pôle Emploi, Linkedin et Leboncoin
- Alertes sonnore d'une nouvelle annonce
- Fichier option pour les temps de recharge

## Idées
- Avoir un sous menu dans les annonces *(non lue, postulée, expirée, inadéquate)*
    - Refont BDD ajouter 2 colonnes view et status *(boolean et varchar)* dans la table annonce
- Savoir si l'annonce est relancée *(redondante pour negocier le salaire)*
- Faire 2 executable *(run et autres)* ou lancer le run en fond de tâche
