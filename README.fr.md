# **Synchro Qt Made**

[Français](https://github.com/Patrick-81/Synchro-Qt-Made/blob/master/README.fr.md) | [English](http://docs.google.com/README.md)

## **Application de Sauvegarde et Synchronisation de Répertoires**

Synchro Qt Made est une application de bureau robuste et intuitive conçue pour automatiser la sauvegarde et la synchronisation de vos répertoires importants. Elle offre un contrôle précis sur vos données, avec des options de planification, de filtrage et de gestion des versions.

## **Fonctionnalités Clés**

* **Gestion des Configurations :** Créez, sauvegardez, chargez et supprimez des profils de synchronisation personnalisés pour différents répertoires.  
* **Synchronisation Automatisée :** Définissez une fréquence horaire pour que vos répertoires soient automatiquement synchronisés en arrière-plan.  
* **Filtrage Avancé :** Excluez des fichiers et répertoires spécifiques de la synchronisation grâce à des listes noires configurables.  
* **Gestion du Cache des Versions :** Conservez un nombre défini de versions antérieures de vos fichiers modifiés, évitant ainsi la perte de données tout en optimisant l'espace disque.  
* **Suivi en Temps Réel :** Surveillez la progression des synchronisations en cours et leur statut via une interface graphique claire et une barre de progression dynamique.  
* **Synthèse des Tâches :** Obtenez un résumé détaillé des opérations de synchronisation passées, incluant les statistiques (fichiers/répertoires ajoutés, modifiés, supprimés) et un accès direct aux fichiers de log.  
* **Nettoyage Automatique des Logs :** Les logs de l'application et des tâches sont automatiquement purgés après une semaine pour maintenir l'espace disque.  
* **Interface Intuitive :** Une interface utilisateur basée sur PyQt5, facile à utiliser et personnalisable via un fichier de style CSS.

## **Architecture de l'Application**

L'application est structurée en trois composants principaux qui communiquent entre eux :

* **Frontend (mainwindow.py) :** L'interface utilisateur graphique (GUI) construite avec PyQt5. Elle permet à l'utilisateur de configurer les tâches, de les lancer, de les arrêter et de visualiser leur état et leurs logs.  
* **Backend (api.py) :** Un serveur API REST léger basé sur Flask. Il agit comme un intermédiaire, recevant les requêtes du frontend et gérant le lancement, l'arrêt et le suivi des processus de synchronisation.  
* **Moteur de Synchronisation (sync\_engine.py) :** Un script Python exécuté en tant que processus séparé par le backend. C'est le cœur de la logique de synchronisation, responsable de la copie des fichiers, de l'application des filtres, de la gestion de la fréquence et de la conservation des versions.

## **Installation**

Suivez ces étapes pour installer et exécuter l'application.

### **Prérequis**

* **Python 3.x** (recommandé : Python 3.8 ou plus récent)  
* **Git**

### **Étapes d'Installation**

1. Cloner le dépôt Git :  
   Ouvrez votre terminal ou invite de commande et exécutez :  
   git clone https://github.com/votre\_nom\_utilisateur/Synchro-Qt-Made.git \# Remplacez par l'URL de votre dépôt  
   cd Synchro-Qt-Made

2. Créer les fichiers requirements.txt :  
   À la racine de votre projet, créez les fichiers suivants :  
   * Synchro\_backend/requirements.txt avec le contenu :  
     Flask  
     Flask-CORS

   * Synchro\_qt\_made/requirements.txt avec le contenu :  
     PyQt5  
     requests

3. Créer des environnements virtuels (recommandé) et installer les dépendances :  
   Il est fortement recommandé de créer des environnements virtuels séparés pour le frontend et le backend afin de gérer les dépendances.  
   \# Pour le backend  
   python3 \-m venv .venv\_backend  
   source .venv\_backend/bin/activate \# Sur Linux/macOS  
   \# .venv\_backend\\Scripts\\activate \# Sur Windows  
   pip install \-r Synchro\_backend/requirements.txt

   deactivate \# Désactiver l'environnement du backend

   \# Pour le frontend  
   python3 \-m venv .venv\_frontend  
   source .venv\_frontend/bin/activate \# Sur Linux/macOS  
   \# .venv\_frontend\\Scripts\\activate \# Sur Windows  
   pip install \-r Synchro\_qt\_made/requirements.txt

   deactivate \# Désactiver l'environnement du frontend

4. Vérifier la structure des fichiers :  
   Assurez-vous que votre répertoire de projet contient les dossiers Synchro\_backend et Synchro\_qt\_made, ainsi que le fichier api\_client.py à la racine.

## **Configuration Initiale**

Avant de lancer l'application, vous devez configurer certains fichiers.

### **1\. \~/.synchro/volume\_config.json**

Ce fichier gère les chemins de base de votre volume de destination et les paramètres de cache des versions.

* **Création :** Si le répertoire \~/.synchro/ et le fichier volume\_config.json n'existent pas, ils seront créés automatiquement au premier lancement du frontend.  
* **Contenu (exemple) :**  
  {  
      "external\_volume\_base\_path": "/chemin/vers/votre/SynchroDestination",  
      "max\_cached\_versions": 2  
  }

  * Remplacez "/chemin/vers/votre/SynchroDestination" par le chemin absolu de votre répertoire de destination principal. C'est là que les répertoires synchronisés seront créés.  
  * "max\_cached\_versions": Définissez le nombre de versions antérieures d'un fichier modifié à conserver. 0 signifie aucune version, 1 signifie la version actuelle \+ la dernière version modifiée, etc.

### **2\. gui\_config.json**

Ce fichier, situé dans le répertoire Synchro\_qt\_made, permet de personnaliser l'apparence de l'interface utilisateur via des règles CSS. Vous pouvez l'éditer pour modifier les couleurs, les polices, les tailles, etc.

## **Utilisation de l'Application**

### **1\. Démarrer le Backend**

Le backend doit être lancé en premier et rester actif.

1. Ouvrez un nouveau terminal.  
2. Activez l'environnement virtuel du backend :  
   cd Synchro-Qt-Made/Synchro\_backend  
   source ../.venv\_backend/bin/activate \# ou .venv\_backend\\Scripts\\activate sur Windows


3. Lancez le backend :  
   python3 api.py

   Vous devriez voir des messages de log indiquant que le serveur Flask est en cours d'exécution sur http://127.0.0.1:7555.

### **2\. Démarrer le Frontend**

Une fois le backend lancé, vous pouvez démarrer l'interface utilisateur.

1. Ouvrez un **autre** nouveau terminal.  
2. Activez l'environnement virtuel du frontend :  
   cd Synchro-Qt-Made/Synchro\_qt\_made  
   source ../.venv\_frontend/bin/activate \# ou .venv\_frontend\\Scripts\\activate sur Windows

3. Lancez le frontend :  
   python3 mainwindow.py

   L'interface graphique de l'application devrait apparaître.

### **3\. Configurer et Lancer une Synchronisation**

1. **Sélectionner la Source :** Dans le champ "Source", cliquez sur "Parcourir..." pour choisir le répertoire que vous souhaitez synchroniser.  
2. **Vérifier la Destination :** Le champ "Destination" affichera automatiquement le chemin complet où vos fichiers seront sauvegardés.  
3. **Définir la Fréquence :** Utilisez le champ "Fréquence (heures)" ou le slider pour spécifier l'intervalle de synchronisation.  
4. **Configurer les Blacklists :** Ajoutez les motifs de fichiers et répertoires à ignorer dans les champs "Blacklist Fichiers" et "Blacklist Répertoires" (séparés par des points-virgules).  
5. **Définir Max Versions en Cache :** Spécifiez le nombre de versions antérieures à conserver.  
6. **Sauvegarder la Configuration :** Cliquez sur "Sauvegarder Configuration". Le nom de la configuration sera dérivé du nom de votre répertoire source.  
7. **Lancer la Synchronisation :** Cliquez sur le bouton "Start". Le bouton deviendra rouge et la barre de progression s'activera, affichant l'état de la tâche.

### **4\. Gérer les Tâches et les Logs**

* **Stop :** Cliquez sur "Stop" pour arrêter une synchronisation en cours.  
* **Charger Configuration :** Pour reprendre une configuration précédemment sauvegardée. L'interface vérifiera automatiquement si la synchronisation correspondante est déjà en cours sur le backend et mettra à jour son état.  
* **Synthèse :** Affiche un résumé des tâches de synchronisation (actives et terminées) dans la zone de log, avec des statistiques détaillées et des liens cliquables vers les logs spécifiques de chaque tâche.  
* **Clear Log / Copie Log :** Permettent de gérer le contenu de la zone de log de l'interface.

## **Dépannage**

* **"Backend non accessible" :** Assurez-vous que le script api.py est bien lancé dans son propre terminal et qu'il n'y a pas d'erreurs au démarrage du backend. Vérifiez que le port 7555 est libre.  
* **Synchronisation ne démarre pas :** Vérifiez les logs du frontend (\~/.synchro/logs/app.log) et du backend (\~/.synchro/logs/backend\_app.log) pour des messages d'erreur. Assurez-vous que les chemins source et destination sont valides et que vous avez les permissions d'accès.  
* **Barre de progression non mise à jour / Bouton "Start" toujours vert après chargement :** Cela signifie que la synchronisation pour la configuration sélectionnée n'est pas active sur le backend. Lancez-la manuellement ou vérifiez les logs pour comprendre pourquoi elle ne s'est pas lancée ou a été arrêtée.  
* **Problèmes de cache des versions :** Vérifiez la valeur de max\_cached\_versions dans volume\_config.json et dans l'interface. La logique de nettoyage est implémentée dans sync\_engine.py ; consultez les logs de la tâche spécifique pour des informations détaillées.

## **Contribution**

Si vous souhaitez contribuer à ce projet, n'hésitez pas à forker le dépôt, à apporter vos modifications et à soumettre des pull requests.

## **Licence**

\[À ajouter : Spécifiez la licence de votre projet ici (ex: MIT, GPL, Apache 2.0)\]
