# Recherche d'emploi
Application Web permettant d'avoir les dernières offres d'emplois *Linkedin / Pôle-Emploi*.

## Exigence
- Python >= 3.8
    - BeautifulSoup4 >= 4.9.*
    - Requests >= 2.24.*
    - Django == 3.1

## Installation

###Linux
```
dnf install vim python3.8 git screen firewalld
git clone https://github.com/Florian-Dj/job_search.git
cd job_search
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
chmod ug+x run.sh
```
Ajouter l'Ip ou DNS de votre machine dans les options de Django
```
vim /home/projet/job_search/admin/settings.py
ALLOWED_HOSTS = ['Your-IP']
```
Si vous avez installé firewalld
```
firewall-cmd --zone=public --add-port=8000/tcp --permanent
firewall-cmd --reload
```

## Crontab
```
*/15 * * * * cd /home/projet/job_search/scripts && ../env/bin/python3 scrape.py
05 */1 * * * cd /home/projet/job_search/scripts && ../env/bin/python3 analysis.py
```

## Utilisation
```
cd /home/projet/job_search
sh run.sh
```

Renseignez bien un compte de superuser au premier lancement du fichier 'run.sh'.

Vous pouvez lancer votre navigateur web avec l'url ip:8000

Je vous conseille d'en refaire un plus sécuriser et de supprimer le ocmpte root.

## Mise à jour
**V0.4.1**
- Optimisation analyse des annonces
- Ajoute statistiques sur la page d'accueil

V0.4
- Suppression des offres Leboncoin
- Identifier les annonces expirées *(niveau 1)*
- Refonte des statistiques
- Annonces en inadéquate suivant des mots clefs dans une liste
- Limite de 100 annonces sur la page
- Ajout un Footer
- Refaire le CSS *(agrandir la page, fixer la navbar)*

V0.3
- Pannel Web Django
- Pannel Admin
- Page Accueil avec les statistiques des annonces
- Page pour voir les recherche et annonces
- Formulaire pour ajouter des recherches
- Logo *(supprimer et modifier)* les recherches
- Ajout de filtres pour annonces  *(Tout, Non Lu, Postulé, Expiré, Inadéquate, Autres)*
- Ajout de filtres pour annonces *(Leboncoin, Linkedin, Pole-Emploi)*
- Bouton pour chercher les nouvelles annonces
- Changer les status des annonces sur la page admin

## Idées
- Ajouter d'autres site de recherche
- Faire un fichier d'options pour les mots clef inadéquate
- Formulaire de contact
- Stocker toute la description de l'annonce
- Ajouter une date pour les annonces *(ajout et mise à jour)*
    - Par villes
    - Pourcentages des stats
- Filtre par Villes/Régions
- Savoir si l'annonce est relancée *(redondante pour negocier le salaire)*
- Logs *(backup et crontab)*
