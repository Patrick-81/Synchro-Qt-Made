# Fichier: Synchro_qt_made/mainwindow.py
#
# Historique des versions:
#
# Version 3.37 (2025-05-21):
#   - Correction de l'AttributeError: 'NoneType' object has no attribute 'setText' dans `update_ui_texts`.
#     L'appel à `self.language_combo.setCurrentIndex()` a été retiré de l'initialisation pour éviter
#     un déclenchement prématuré de `update_ui_texts`.
#     Un appel explicite à `self.update_ui_texts()` a été ajouté à la toute fin de `__init__`,
#     garantissant que tous les éléments UI sont initialisés avant la mise à jour des textes.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.36 (2025-05-21):
#   - Correction critique de l'AttributeError: 'MainWindow' object has no attribute 'max_cached_versions_input'.
#     L'initialisation de `self.max_cached_versions_input` a été déplacée plus tôt dans la méthode `__init__`,
#     avant l'appel à `self.load_external_volume_base_path()`, résolvant ainsi l'erreur d'attribut manquant.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.35 (2025-05-21):
#   - Internationalisation (i18n) du Frontend :
#     - Ajout d'un fichier `texts.json` pour stocker les traductions en français et en anglais.
#     - La classe `MainWindow` charge les textes depuis `texts.json` au démarrage.
#     - Ajout d'un `QComboBox` pour permettre à l'utilisateur de sélectionner la langue (Français/Anglais).
#     - Tous les labels, textes de boutons et messages de log sont mis à jour dynamiquement
#       en fonction de la langue sélectionnée.
#     - La méthode `log_message` utilise désormais les préfixes et messages traduits.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.34 (2025-05-21):
#   - Correction de l'ordre d'initialisation : L'initialisation de `self.max_cached_versions_input`
#     et de `self._max_cached_versions` a été déplacée plus tôt dans la méthode `__init__`,
#     résolvant ainsi l'AttributeError.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.33 (2025-05-21):
#   - Ajout du paramètre `max_cached_versions` :
#     - Un nouveau champ QLineEdit (`max_cached_versions_input`) est ajouté à l'interface utilisateur
#       pour permettre la saisie du nombre maximal de versions antérieures à conserver.
#     - Ce champ est validé pour accepter uniquement des entiers (entre 0 et 99, par défaut 2).
#   - Intégration avec `volume_config.json` :
#     - La méthode `load_external_volume_base_path` est modifiée pour charger la valeur de `max_cached_versions`
#       depuis `volume_config.json`. Si le fichier ou la valeur n'existe pas, une valeur par défaut de `2` est utilisée.
#   - Transmission au backend :
#     - La méthode `get_current_config_data` inclut désormais `max_cached_versions` dans le dictionnaire
#       de configuration envoyé au backend.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.32 (2025-05-20):
#   - Comportement de mise à jour de l'UI affiné : L'état de la barre de progression et du bouton "Start/Stop"
#     est désormais mis à jour spécifiquement pour la configuration actuellement sélectionnée par l'utilisateur.
#   - Déclenchement de la vérification de statut : La méthode `check_sync_status` est appelée lorsque l'utilisateur
#     charge une configuration via le bouton "Charger Configuration".
#   - Logique de `check_sync_status` révisée :
#     - L'UI est d'abord réinitialisée à l'état "idle" pour la configuration courante.
#     - Le statut est ensuite mis à jour uniquement si la configuration actuellement affichée est active sur le backend.
#     - Si la synchronisation de la configuration sélectionnée n'est pas en cours, un message est affiché dans le log.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.31 (2025-05-20):
#   - Chargement de la dernière configuration au démarrage :
#     - Une nouvelle méthode `load_last_used_configuration` est ajoutée. Elle tente de charger
#       la configuration nommée "BacASable.json" au démarrage de l'application. Si elle existe,
#       les champs de l'interface sont pré-remplis avec ses valeurs.
#     - Cette méthode est appelée dans `__init__` avant le premier appel à `check_sync_status`.
#   - Logique de `check_sync_status` améliorée :
#     - La méthode identifie la `current_config_name` basée sur le contenu du champ `source_input`.
#     - Elle parcourt toutes les tâches reçues du backend et met à jour l'état de l'UI
#       (bouton "Start", bouton "Stop", barre de progression) spécifiquement pour la `current_config_name`
#       si elle est trouvée et en cours d'exécution.
#     - Si la `current_config_name` n'est pas trouvée ou n'est plus en cours d'exécution sur le backend,
#       l'UI est réinitialisée à l'état "Start" vert et barre de progression masquée.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.30 (2025-05-20):
#   - Récupération de l'état de synchronisation au démarrage :
#     - La méthode `check_sync_status` est appelée une fois au démarrage de `MainWindow`
#       pour interroger le backend et mettre à jour l'état de l'interface utilisateur
#       (boutons, barre de progression) si une tâche de synchronisation est déjà en cours.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.29 (2025-05-20):
#   - Correction de l'initialisation précoce de `log_output` :
#     - Le `QTextBrowser` pour l'affichage des logs est maintenant initialisé
#       avant tout appel à `self.log_message` dans `__init__`, évitant ainsi
#       le message "Frontend: log_output non prêt".
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.28 (2025-05-20):
#   - Amélioration de la robustesse du logging du frontend :
#     - Ajout d'un message de log de test au tout début de `__init__` pour s'assurer
#       que le fichier `app.log` est correctement écrit dès le démarrage de l'application.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.27 (2025-05-20):
#   - Correction de l'erreur "No document for file://..." pour APP_LOG_FILE :
#     - La méthode `create_app_directories` crée désormais explicitement le fichier `app.log`
#       (en utilisant `touch()`) si celui-ci n'existe pas, après avoir créé les répertoires.
#     - La méthode `log_message` vérifie l'existence du fichier `APP_LOG_FILE` avant de générer
#       un lien cliquable vers celui-ci, évitant ainsi les erreurs si le fichier n'est pas encore présent.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.26 (2025-05-20):
#   - Confirme la restauration complète et la vérification de la méthode `get_synthesis`
#     pour assurer l'affichage de toutes les statistiques détaillées (répertoires/fichiers
#     ajoutés/modifiés, durée, lien de log) telles que fournies par le backend.
#   - S'assure que `get_synthesis` est appelée automatiquement par `check_sync_status`
#     lorsqu'une tâche en cours (la tâche actuellement affichée) passe au statut 'completed', 'stopped' ou 'error'.
#   - Amélioration de l'affichage de la barre de progression en fin de tâche, avec un message de statut clair.
#   - Correction et vérification des chemins de log pour les liens cliquables.
#   - Mise à jour générale des commentaires de versionnage pour clarifier l'historique.
#
# Version 3.25 (2025-05-20):
#   - Correction majeure de l'affichage de la synthèse :
#     - La méthode `get_synthesis` a été entièrement revue et confirmée pour afficher toutes les statistiques détaillées
#       (répertoires/fichiers ajoutés/modifiés, durée, lien de log) telles que fournies par le backend.
#     - S'assure que `get_synthesis` est appelée automatiquement par `check_sync_status` lorsqu'une tâche
#       en cours (la tâche actuellement affichée) passe au statut 'completed', 'stopped' ou 'error'.
#     - Amélioration de l'affichage de la barre de progression en fin de tâche, avec un message de statut clair.
#
# Version 3.24 (2025-05-20):
#   - Amélioration du comportement de la barre de progression :
#     - Reste visible pendant 3 secondes après la fin de la synchronisation (completed, stopped, error).
#     - Affiche un message de statut clair (Terminé, Arrêté, Erreur) dans la barre de progression.
#     - Utilise QTimer.singleShot pour masquer la barre après le délai.
#   - Amélioration de l'affichage de la synthèse :
#     - La méthode `get_synthesis` est appelée automatiquement par `check_sync_status`
#       lorsqu'une tâche termine (completed, stopped, error) pour afficher le résumé dans le log.
#     - La logique d'affichage détaillée de la synthèse (répertoires/fichiers ajoutés/modifiés, durée, lien de log)
#       a été restaurée et confirmée comme étant présente.
#
# Version 3.23 (2025-05-20):
#   - AJOUT DE LA BARRE DE PROGRESSION:
#     - Un QProgressBar est ajouté à l'UI.
#     - update_start_button_state gère son affichage/masquage et sa réinitialisation.
#     - check_sync_status met à jour la valeur de la barre de progression en se basant sur le champ 'progress' du backend.
#   - INTÉGRATION DU QTimer POUR LE STATUT EN TEMPS RÉEL:
#     - Un QTimer est configuré pour interroger périodiquement le backend sur le statut des tâches (check_sync_status).
#     - Le timer est démarré au lancement d'une synchro et arrêté quand toutes les tâches sont terminées.
#   - MAINTIEN DES AMÉLIORATIONS DE LA V3.22:
#     - Rénovation de la méthode get_synthesis pour inclure des statistiques détaillées par tâche:
#       Répertoires ajoutés, Fichiers ajoutés, Répertoires modifiés, Fichiers modifiés,
#       Durée de l'opération, et un lien direct vers le fichier de log spécifique de la tâche.
#     - Ces informations sont affichées si le backend les fournit (clés 'dirs_added', 'files_added',
#       'dirs_modified', 'files_modified', 'duration', 'log_file_name' dans la réponse /api/sync_tasks).
#
# Version 3.22 (2025-05-20):
#   - Amélioration de la synthèse affichée : ajout des répertoires copiés et fichiers copiés,
#     en supposant que ces données sont fournies par le backend dans la réponse /api/sync_tasks
#     pour les tâches terminées (clés 'dirs_copied' et 'files_copied').
#   - La barre de progression est déjà gérée correctement en frontend, la correction dépend
#     principalement de l'envoi de la clé 'progress' par le backend.
#
# Version 3.21 (2025-05-20):
#   - Correction de l'erreur `NameError: name 'TASK_LOG_DIR' est not defined` dans `get_synthesis`.
#     La variable globale `TASK_LOG_DIR` a été ajoutée pour pointer vers le répertoire des logs de tâches,
#     permettant de construire correctement les chemins des fichiers de log pour les liens cliquables.
#
# Version 3.20 (2025-05-20):
#   - Amélioration de la synthèse affichée : ajout des répertoires copiés et fichiers copiés,
#     en supposant que ces données sont fournies par le backend dans la réponse /api/sync_tasks
#     pour les tâches terminées (clés 'dirs_copied' et 'files_copied').
#   - La barre de progression est déjà gérée correctement en frontend, la correction dépend
#     principalement de l'envoi de la clé 'progress' par le backend.
#
# Version 3.19 (2025-05-20):
#   - Correction de l'erreur `NameError: name 'TASK_LOG_DIR' is not defined` dans `get_synthesis`.
#     La variable globale `TASK_LOG_DIR` a été ajoutée pour pointer vers le répertoire des logs de tâches,
#     permettant de construire correctement les chemins des fichiers de log pour les liens cliquables.
#
# Version 3.18 (2025-05-20):
#   - Implémentation d'un QTimer pour interroger périodiquement le backend sur le statut des tâches.
#   - La méthode `check_sync_status` est ajoutée pour appeler l'API `/api/sync_tasks`.
#   - Si une tâche est détectée comme 'completed' ou 'stopped', le bouton 'Start' est réactivé
#     et un message est affiché dans le log du frontend.
#   - Le timer est démarré lorsque la synchronisation commence et arrêté quand toutes les tâches sont terminées.
#
# Version 3.17 (2025-05-20):
#   - Suppression de la validation frontend de l'existence du chemin de destination dans `start_sync_process`.
#     Cette validation est désormais la responsabilité exclusive du backend, qui crée les répertoires
#     si nécessaire. Cela résout l'erreur N°VAL001 affichée par le frontend avant l'appel API.
#
# Version 3.16 (2025-05-20):
#   - Retrait des messages d'avertissement 'ATTENTION:' de la console, car l'erreur JSON est corrigée et ne devrait plus apparaître.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.15 (2025-05-20):
#   - Retrait des prints de débogage.
#   - Confirmation de l'application correcte du style du label de destination via gui_config.json.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.14 (2025-05-20):
#   - Correction de l'application du style pour le label de destination (#destinationPathLabel)
#     en s'assurant que la règle CSS est bien dans 'stylesheet_base' du gui_config.json
#     et est appliquée via setStyleSheet global.
#
# Version 3.13 (2025-05-20):
#   - Ajout d'une marge de 20px sur tous les côtés du layout principal (main_layout.setContentsMargins).
#   - Attribution de l'objectName "destinationPathLabel" au QLabel affichant le chemin de destination.
#   - Ajout d'une section "destination_path_style" dans gui_config.json pour configurer sa taille de police (16px) et son poids (bold).
#   - Adaptation de la méthode apply_gui_styles pour charger et appliquer ce nouveau style.
#
# Version 3.12 (2025-05-20):
#   - Ajout de messages de débogage (DEBUG prints) pour tracer l'exécution et identifier la cause des arrêts silencieux.
#   - Confirmation du bon fonctionnement de l'affichage de la fenêtre principale après ces ajouts.
#
# Version 3.11 (2025-05-19):
#   - Correction de l'AttributeError: 'QTextBrowser' object has no attribute 'linkActivated' en utilisant 'anchorClicked' pour la zone de log.
#
# Version 3.10 (2025-05-19):
#   - Correction de l'AttributeError: 'QTextEdit' object has no attribute 'setOpenLinks' en utilisant QTextBrowser au lieu de QTextEdit.
#
# Version 3.9 (2025-05-19):
#   - Amélioration de l'affichage initial du chemin de destination.
#   - Ajout d'un QLabel pour afficher le chemin de destination sous le titre.
#
# Version 3.8 (2025-05-19):
#   - Suppression du bouton "Ouvrir Volume..." et de sa méthode associée.
#
# Version 3.7 (2025-05-18):
#   - Correction de l'ordre d'initialisation du log_output pour être prêt avant les appels à log_message.
#
# Version 3.6 (2025-05-18):
#   - Gestion du chemin de destination basée sur un chemin de volume externe configurable (volume_config.json).
#   - Ajout de la logique de chargement de volume_config.json.
#   - Mise à jour du calcul du chemin de destination pour inclure le nom du répertoire source.
#
# Version 3.5 (2025-05-17):
#   - Alignement vertical des zones de saisie avec leurs labels dans QFormLayout.
#
# Version 3.4 (2025-05-17):
#   - Meilleure répartition des boutons "Charger/Sauvegarder/Détruire" et "Start/Stop/Synthèse" en utilisant addStretch.
#
# Version 3.3 (2025-05-16):
#   - Ajout d'un bouton "Quitter" pour fermer proprement l'application.
#
# Version 3.2 (2025-05-16):
#   - Chargement des styles depuis gui_config.json pour une personnalisation aisée.
#   - Utilisation d'objectName pour les boutons et la ligne de séparation pour un ciblage CSS spécifique.
#
# Version 3.1 (2025-05-15):
#   - Premières implémentations des éléments UI, des zones de saisie, sliders, et boutons.
#   - Mise en place de la structure de base QMainWindow, QVBoxLayout, QHBoxLayout.
#   - Intégration de la logique de création des répertoires de l'application (.synchro, logs, configs).
#   - Implémentation des fonctions de gestion de configuration (charger, sauvegarder, détruire).
#   - Connexion des boutons d'action aux méthodes du client API.
#   - Gestion des messages de log avec horodatage, niveau d'erreur et lien cliquable pour les erreurs.
#   - Limitations de la zone de log à 100 lignes.
#
# Description Générale du Fichier:
# Ce fichier contient la classe MainWindow, l'interface graphique principale de l'application Synchro Qt Made.
# Il gère l'interaction utilisateur, la collecte des données de configuration, la communication avec le backend
# via ApiClient, et l'affichage des logs et synthèses.
#
############################################################################################################


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QTextBrowser, QFileDialog, QSizePolicy, QFrame,
    QMessageBox, QGridLayout, QFormLayout, QProgressBar, QComboBox
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QDesktopServices, QIntValidator
import json
from pathlib import Path
import os
import datetime # Importation pour le nettoyage des logs

# Importez votre nouvelle classe ApiClient
from api_client import ApiClient

# Définition des chemins globaux basés sur le cahier des charges
APP_DIR = Path.home() / ".synchro"
CONFIGS_DIR = APP_DIR / "configs"
LOGS_DIR = APP_DIR / "logs"
APP_LOG_FILE = LOGS_DIR / "app.log"
VOLUME_CONFIG_FILE = APP_DIR / "volume_config.json"
GUI_CONFIG_FILE = Path(__file__).parent / "gui_config.json"
TASK_LOG_DIR = LOGS_DIR / "tasks"
TEXTS_FILE = Path(__file__).parent / "texts.json" # Chemin vers le fichier de textes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- DÉPLACÉ ICI : Initialisation de la zone de log TRÈS TÔT ---
        self.log_output = QTextBrowser()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(200)
        self.log_output.setLineWrapMode(QTextBrowser.NoWrap)
        self.log_output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.log_output.textChanged.connect(self.limit_log_lines)
        self.log_output.setOpenLinks(True)
        self.log_output.anchorClicked.connect(QDesktopServices.openUrl)

        # Initialisation du chemin de base du volume externe
        self._external_volume_base_path = Path.home() / "SynchroDestination"
        # Initialisation du paramètre max_cached_versions
        self._max_cached_versions = 2 # Valeur par défaut avant chargement depuis config

        # --- DÉPLACÉ ICI : Initialisation de max_cached_versions_input avant son utilisation ---
        self.max_cached_versions_input = QLineEdit(str(self._max_cached_versions)) # Initialisation avec la valeur par défaut
        self.max_cached_versions_input.setFixedWidth(50)
        self.max_cached_versions_input.setAlignment(Qt.AlignCenter)
        self.max_cached_versions_input.setValidator(QIntValidator(0, 99, self)) # De 0 à 99 versions


        # --- Chargement des textes et langue par défaut ---
        self.texts = self._load_texts()
        self.current_lang = "fr" # Langue par défaut
        
        # AJOUT : Message de log de test très tôt pour vérifier l'écriture dans app.log
        self.log_message("app_init", is_formatted_key=True)


        self.setWindowTitle(self.texts[self.current_lang]["app_title"])
        self.setGeometry(100, 100, 1000, 800)

        # ---------------------------------------------
        # Chargement et application du thème et des styles depuis gui_config.json
        # ---------------------------------------------
        self.apply_gui_styles()

        # Initialisation du client API
        self.api_client = ApiClient(base_url="http://127.0.0.1:7555")

        # Configuration du widget central et du layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # AJOUT : Marge autour du layout principal
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Les boutons de log sont aussi initialisés ici pour être liés au log_output
        self.clear_log_button = QPushButton(self.texts[self.current_lang]["clear_log_button"])
        self.clear_log_button.setObjectName("darkBlueButton")
        self.clear_log_button.clicked.connect(self.log_output.clear)

        self.copy_log_button = QPushButton(self.texts[self.current_lang]["copy_log_button"])
        self.copy_log_button.setObjectName("darkBlueButton")
        self.copy_log_button.clicked.connect(self.copy_log_to_clipboard)

        self.load_external_volume_base_path() # Charge les valeurs réelles depuis volume_config.json

        # ---------------------------------------------
        # Ligne 0: Titre principal
        # ---------------------------------------------
        self.title_label = QLabel(self.texts[self.current_lang]["app_title"])
        self.title_label.setAlignment(Qt.AlignCenter)
        # Assurez-vous que le style du titre est appliqué ici, après sa création
        if hasattr(self, '_main_title_style_string') and self._main_title_style_string:
            self.title_label.setStyleSheet(self._main_title_style_string)
        self.main_layout.addWidget(self.title_label)

        # ---------------------------------------------
        # Ligne 1: Affichage du chemin de destination sous le titre
        # ---------------------------------------------
        self.destination_display_label = QLabel(self.texts[self.current_lang]["destination_label_default"]) # Valeur par défaut
        self.destination_display_label.setAlignment(Qt.AlignCenter)
        # AJOUT : Assigner un objectName pour pouvoir cibler le style via gui_config.json
        self.destination_display_label.setObjectName("destinationPathLabel")
        self.main_layout.addWidget(self.destination_display_label)

        # ---------------------------------------------
        # Lignes 2 à 7: Champs de configuration (utilisent QFormLayout pour l'alignement)
        # ---------------------------------------------
        self.config_form_layout = QFormLayout()
        self.config_form_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.config_form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.config_form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Ligne 2: Source
        self.source_input = QLineEdit(str(Path.home()))
        self.source_browse_button = QPushButton(self.texts[self.current_lang]["browse_button"])
        self.source_browse_button.clicked.connect(self.browse_source)
        self.source_browse_button.setObjectName("darkBlueButton")
        source_h_layout = QHBoxLayout()
        source_h_layout.addWidget(self.source_input)
        source_h_layout.addWidget(self.source_browse_button)
        self.config_form_layout.addRow(self.texts[self.current_lang]["source_label"], source_h_layout)
        
        self.source_input.textChanged.connect(self.update_destination_path)

        # Ligne 3: Destination (champ non éditable, sans bouton)
        self.destination_input = QLineEdit()
        self.destination_input.setReadOnly(True) # Reste non éditable
        self.destination_input.setToolTip(self.texts[self.current_lang]["destination_tooltip"])
        # Le bouton "Ouvrir Volume..." est supprimé
        self.config_form_layout.addRow(self.texts[self.current_lang]["destination_label"], self.destination_input)

        # Ligne 4: Fréquence de synchro
        self.frequency_input = QLineEdit("1")
        self.frequency_input.setFixedWidth(50)
        self.frequency_input.setAlignment(Qt.AlignCenter)
        self.frequency_input.setValidator(QIntValidator(1, 24, self))
        
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setMinimum(1)
        self.frequency_slider.setMaximum(24)
        self.frequency_slider.setValue(1)
        self.frequency_slider.setTickPosition(QSlider.TicksBelow)
        self.frequency_slider.setTickInterval(1)
        
        self.frequency_slider.valueChanged.connect(lambda value: self.frequency_input.setText(str(value)))
        self.frequency_input.textChanged.connect(self.update_slider_from_input)
        freq_h_layout = QHBoxLayout()
        freq_h_layout.addWidget(self.frequency_input)
        freq_h_layout.addWidget(self.frequency_slider)
        self.config_form_layout.addRow(self.texts[self.current_lang]["frequency_label"], freq_h_layout)

        # Ligne 5: Blacklist fichiers
        self.blacklist_files_input = QLineEdit(".tmp;.log;.bak")
        self.config_form_layout.addRow(self.texts[self.current_lang]["blacklist_files_label"], self.blacklist_files_input)

        # Ligne 6: Blacklist répertoires
        self.blacklist_dirs_input = QLineEdit(".git;.cache;node_modules")
        self.config_form_layout.addRow(self.texts[self.current_lang]["blacklist_dirs_label"], self.blacklist_dirs_input)

        # Ligne 7: Max versions en cache (maintenant initialisé plus tôt)
        self.config_form_layout.addRow(self.texts[self.current_lang]["max_cached_versions_label"], self.max_cached_versions_input)

        self.main_layout.addLayout(self.config_form_layout)

        # ---------------------------------------------
        # Ligne 8: Boutons de configuration (Charger/Sauvegarder/Détruire) - Répartis
        # ---------------------------------------------
        self.config_buttons_layout = QHBoxLayout()
        self.load_config_button = QPushButton(self.texts[self.current_lang]["load_config_button"])
        self.load_config_button.setObjectName("darkBlueButton")
        self.load_config_button.clicked.connect(self.load_configuration)

        self.save_config_button = QPushButton(self.texts[self.current_lang]["save_config_button"])
        self.save_config_button.setObjectName("darkBlueButton")
        self.save_config_button.clicked.connect(self.save_configuration)
        
        self.delete_config_button = QPushButton(self.texts[self.current_lang]["delete_config_button"])
        self.delete_config_button.setObjectName("stopButton")
        self.delete_config_button.clicked.connect(self.delete_configuration)

        self.config_buttons_layout.addStretch(1)
        self.config_buttons_layout.addWidget(self.load_config_button)
        self.config_buttons_layout.addStretch(1)
        self.config_buttons_layout.addWidget(self.save_config_button)
        self.config_buttons_layout.addStretch(1)
        self.config_buttons_layout.addWidget(self.delete_config_button)
        self.config_buttons_layout.addStretch(1)
        self.main_layout.addLayout(self.config_buttons_layout)

        # ---------------------------------------------
        # Ligne 9: Ligne de séparation graphique
        # ---------------------------------------------
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)
        self.separator_line.setObjectName("separatorLine")
        self.main_layout.addWidget(self.separator_line)

        # ---------------------------------------------
        # Ligne 10: Boutons d'action (Start/Stop/Synthèse) - Répartis
        # ---------------------------------------------
        self.action_buttons_layout = QHBoxLayout()
        self.start_button = QPushButton(self.texts[self.current_lang]["start_button"])
        self.start_button.setObjectName("startButtonGreen")
        self.start_button.clicked.connect(self.start_sync_process)

        self.stop_button = QPushButton(self.texts[self.current_lang]["stop_button"])
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_sync_process)

        self.synthesis_button = QPushButton(self.texts[self.current_lang]["synthesis_button"])
        self.synthesis_button.setObjectName("darkBlueButton")
        self.synthesis_button.clicked.connect(self.get_synthesis)

        self.action_buttons_layout.addStretch(1)
        self.action_buttons_layout.addWidget(self.start_button)
        self.action_buttons_layout.addStretch(1)
        self.action_buttons_layout.addWidget(self.stop_button)
        self.action_buttons_layout.addStretch(1)
        self.action_buttons_layout.addWidget(self.synthesis_button)
        self.action_buttons_layout.addStretch(1)
        self.main_layout.addLayout(self.action_buttons_layout)

        # --- AJOUT: Barre de progression (initialement cachée) ---
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False) # Cachée par défaut
        self.main_layout.addWidget(self.progress_bar)

        # ---------------------------------------------
        # Ligne 11: Zone de log output (AJOUTÉE ICI MAINTENANT)
        # ---------------------------------------------
        self.main_layout.addWidget(self.log_output)
        
        # ---------------------------------------------
        # Ligne 12: Boutons Clear et Copie du log (AJOUTÉS ICI MAINTENANT)
        # ---------------------------------------------
        self.log_buttons_layout = QHBoxLayout()
        self.log_buttons_layout.addStretch(1)
        self.log_buttons_layout.addWidget(self.clear_log_button)
        self.log_buttons_layout.addStretch(1)
        self.log_buttons_layout.addWidget(self.copy_log_button)
        self.log_buttons_layout.addStretch(1)
        self.main_layout.addLayout(self.log_buttons_layout)

        # --- AJOUT: Sélecteur de langue ---
        self.language_selector_layout = QHBoxLayout()
        self.language_label = QLabel(self.texts[self.current_lang]["language_label"])
        self.language_combo = QComboBox()
        self.language_combo.addItem(self.texts["fr"]["lang_fr"], "fr")
        self.language_combo.addItem(self.texts["en"]["lang_en"], "en")
        # self.language_combo.setCurrentIndex(self.language_combo.findData(self.current_lang)) # <-- Ligne supprimée
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.language_selector_layout.addStretch(1)
        self.language_selector_layout.addWidget(self.language_label)
        self.language_selector_layout.addWidget(self.language_combo)
        self.main_layout.addLayout(self.language_selector_layout)

        # ---------------------------------------------
        # Ligne 13: Bouton Quitter
        # ---------------------------------------------
        self.quit_button_layout = QHBoxLayout()
        self.quit_button = QPushButton(self.texts[self.current_lang]["quit_button"])
        self.quit_button.setObjectName("stopButton")
        self.quit_button.clicked.connect(self.close)
        
        self.quit_button_layout.addStretch(1)
        self.quit_button_layout.addWidget(self.quit_button)
        self.main_layout.addLayout(self.quit_button_layout)


        # ---------------------------------------------
        # Initialisation et utilitaires (à la fin de __init__)
        # ---------------------------------------------
        self.create_app_directories()
        self.is_sync_running = False
        # Dictionnaire pour stocker les noms des tâches actives et leur état pour le timer
        self.active_sync_tasks = {} 

        # --- NOUVEAU : Charger la dernière configuration utilisée au démarrage ---
        self.load_last_used_configuration()
        # Mise à jour initiale du chemin de destination pour afficher la valeur dès le démarrage
        self.update_destination_path(self.source_input.text())
        self.frequency_input.textChanged.connect(self.update_slider_from_input)
        self.log_message("app_started", is_formatted_key=True, file_path=str(APP_LOG_FILE))

        # --- AJOUT: Configuration du QTimer pour la vérification du statut ---
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(2000)  # Vérifie toutes les 2 secondes (2000 ms)
        self.status_timer.timeout.connect(self.check_sync_status)

        # --- AJOUT: Configuration du QTimer pour le nettoyage des logs du frontend ---
        self.frontend_log_cleanup_timer = QTimer(self)
        self.frontend_log_cleanup_timer.setInterval(24 * 60 * 60 * 1000) # Toutes les 24 heures en ms
        self.frontend_log_cleanup_timer.timeout.connect(self._clean_frontend_log)
        self.frontend_log_cleanup_timer.start()
        self._clean_frontend_log() # Exécuter un nettoyage initial au démarrage
        
        # Le timer de statut sera démarré dans check_sync_status si une tâche est trouvée en cours pour la config actuelle.
        # Pas d'appel initial à check_sync_status ici, car c'est le chargement de config qui le déclenchera.

        # --- APPEL FINAL : Mettre à jour tous les textes de l'UI après que tout soit initialisé ---
        self.update_ui_texts() # <-- Ligne ajoutée ici

    def _load_texts(self):
        """Charge les textes traduits depuis le fichier JSON."""
        try:
            with open(TEXTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Erreur: Fichier de textes non trouvé: {TEXTS_FILE}. L'application utilisera des textes par défaut/anglais.")
            return {
                "fr": {"app_title": "Synchro Qt Made", "start_button": "Démarrer", "log_app_init": "Initialisation..."},
                "en": {"app_title": "Synchro Qt Made", "start_button": "Start", "log_app_init": "Initializing..."}
            }
        except json.JSONDecodeError as e:
            print(f"Erreur: Fichier de textes JSON invalide: {e}. L'application utilisera des textes par défaut/anglais.")
            return {
                "fr": {"app_title": "Synchro Qt Made", "start_button": "Démarrer", "log_app_init": "Initialisation..."},
                "en": {"app_title": "Synchro Qt Made", "start_button": "Start", "log_app_init": "Initializing..."}
            }

    def change_language(self, index):
        """Change la langue de l'interface utilisateur."""
        self.current_lang = self.language_combo.itemData(index)
        self.update_ui_texts()
        # Re-log le message de démarrage dans la nouvelle langue
        self.log_message("app_started", is_formatted_key=True, file_path=str(APP_LOG_FILE))

    def update_ui_texts(self):
        """Met à jour tous les textes de l'interface utilisateur en fonction de la langue actuelle."""
        texts = self.texts.get(self.current_lang, self.texts["en"]) # Fallback to English

        self.setWindowTitle(texts["app_title"])
        self.title_label.setText(texts["app_title"])
        self.destination_display_label.setText(texts["destination_label_default"])
        self.source_browse_button.setText(texts["browse_button"])
        
        # Mettre à jour les labels des QFormLayout
        # Il faut accéder au QLabel qui est le parent du champ ou à la méthode labelForField
        # La méthode labelForField est plus robuste si le layout est bien géré
        # Vérification ajoutée pour s'assurer que labelForField retourne un objet valide
        label_source = self.config_form_layout.labelForField(self.source_input.parent())
        if label_source:
            label_source.setText(texts["source_label"])
        
        label_destination = self.config_form_layout.labelForField(self.destination_input)
        if label_destination:
            label_destination.setText(texts["destination_label"])
        self.destination_input.setToolTip(texts["destination_tooltip"])
        
        label_frequency = self.config_form_layout.labelForField(self.frequency_input.parent())
        if label_frequency:
            label_frequency.setText(texts["frequency_label"])
        
        label_blacklist_files = self.config_form_layout.labelForField(self.blacklist_files_input)
        if label_blacklist_files:
            label_blacklist_files.setText(texts["blacklist_files_label"])
        
        label_blacklist_dirs = self.config_form_layout.labelForField(self.blacklist_dirs_input)
        if label_blacklist_dirs:
            label_blacklist_dirs.setText(texts["blacklist_dirs_label"])
        
        label_max_cached_versions = self.config_form_layout.labelForField(self.max_cached_versions_input)
        if label_max_cached_versions:
            label_max_cached_versions.setText(texts["max_cached_versions_label"])
        
        self.load_config_button.setText(texts["load_config_button"])
        self.save_config_button.setText(texts["save_config_button"])
        self.delete_config_button.setText(texts["delete_config_button"])
        self.start_button.setText(texts["start_button"])
        self.stop_button.setText(texts["stop_button"])
        self.synthesis_button.setText(texts["synthesis_button"])
        self.clear_log_button.setText(texts["clear_log_button"])
        self.copy_log_button.setText(texts["copy_log_button"])
        self.quit_button.setText(texts["quit_button"])
        self.language_label.setText(texts["language_label"])
        
        # Mettre à jour les textes du QComboBox sans changer la sélection
        current_index = self.language_combo.currentIndex()
        self.language_combo.setItemText(0, self.texts["fr"]["lang_fr"])
        self.language_combo.setItemText(1, self.texts["en"]["lang_en"])
        self.language_combo.setCurrentIndex(current_index) # Restaurer la sélection

        # Mise à jour de l'état du bouton Start/Stop pour refléter la langue
        self.update_start_button_state(self.is_sync_running)

    def apply_gui_styles(self):
        """Charge les styles depuis gui_config.json et les applique à l'application."""
        full_stylesheet = ""
        self._main_title_style_string = "" 
        
        try:
            with open(GUI_CONFIG_FILE, 'r', encoding='utf-8') as f:
                gui_config = json.load(f)

            for selector, properties in gui_config.get("stylesheet_base", {}).items():
                style_rules = "; ".join(f"{prop}: {value}" for prop, value in properties.items())
                full_stylesheet += f"{selector} {{ {style_rules} }}\n"

            for selector, properties in gui_config.get("stylesheet_specific_buttons", {}).items():
                style_rules = "; ".join(f"{prop}: {value}" for prop, value in properties.items())
                full_stylesheet += f"{selector} {{ {style_rules} }}\n"
            
            # Charger directement la règle pour le titre principal
            title_properties = gui_config.get("main_title_style", {})
            self._main_title_style_string = "; ".join(f"{prop}: {value}" for prop, value in title_properties.items())
            
            # Style spécifique pour le label de destination (important pour la v3.13)
            dest_label_properties = gui_config.get("destination_path_style", {})
            dest_label_style_rules = "; ".join(f"{prop}: {value}" for prop, value in dest_label_properties.items())
            full_stylesheet += f"#destinationPathLabel {{ {dest_label_style_rules} }}\n"

        except FileNotFoundError:
            print(f"Erreur: Fichier de configuration GUI non trouvé: {GUI_CONFIG_FILE}. Utilisation des styles par défaut.")
            full_stylesheet = """
                QMainWindow { background-color: #333; color: #f0f0f0; }
                QLabel { color: #f0f0f0; font-size: 12px; }
                QLineEdit { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 12px; }
                QPushButton { background-color: #555; color: white; border: none; padding: 8px 12px; border-radius: 4px; font-size: 12px; }
                QTextBrowser { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 11px; }
                QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; color: black; background-color: #555; }
                QProgressBar::chunk { background-color: #28a745; width: 20px; }
                #destinationPathLabel { font-size: 16px; font-weight: bold; color: #add8e6; margin-top: 5px; margin-bottom: 15px; } /* Style par défaut pour la destination */
                #separatorLine { background-color: #555; height: 2px; margin: 10px 0; }
                QPushButton#darkBlueButton { background-color: #4a69bd; }
                QPushButton#darkBlueButton:hover { background-color: #5a7ad6; }
                QPushButton#startButtonGreen { background-color: #28a745; }
                QPushButton#startButtonGreen:hover { background-color: #218838; }
                QPushButton#startButtonRed { background-color: #dc3545; }
                QPushButton#startButtonRed:hover { background-color: #c82333; }
                QPushButton#stopButton { background-color: #dc3545; }
                QPushButton#stopButton:hover { background-color: #c82333; }
            """
            self._main_title_style_string = "font-size: 30px; font-weight: bold; margin-bottom: 15px; color: #f0f0f0;"
        except json.JSONDecodeError as e:
            print(f"Erreur: Erreur de lecture du fichier de configuration GUI (JSON invalide): {e}. Utilisation des styles par défaut.")
            full_stylesheet = """
                QMainWindow { background-color: #333; color: #f0f0f0; }
                QLabel { color: #f0f0f0; font-size: 12px; }
                QLineEdit { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 12px; }
                QPushButton { background-color: #555; color: white; border: none; padding: 8px 12px; border-radius: 4px; font-size: 12px; }
                QTextBrowser { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 11px; }
                QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; color: black; background-color: #555; }
                QProgressBar::chunk { background-color: #28a745; width: 20px; }
                #destinationPathLabel { font-size: 16px; font-weight: bold; color: #add8e6; margin-top: 5px; margin-bottom: 15px; } /* Style par défaut pour la destination */
                #separatorLine { background-color: #555; height: 2px; margin: 10px 0; }
                QPushButton#darkBlueButton { background-color: #4a69bd; }
                QPushButton#darkBlueButton:hover { background-color: #5a7ad6; }
                QPushButton#startButtonGreen { background-color: #28a745; }
                QPushButton#startButtonGreen:hover { background-color: #218838; }
                QPushButton#startButtonRed { background-color: #dc3545; }
                QPushButton#startButtonRed:hover { background-color: #c82333; }
                QPushButton#stopButton { background-color: #dc3545; }
                QPushButton#stopButton:hover { background-color: #c82333; }
            """
            self._main_title_style_string = "font-size: 30px; font-weight: bold; margin-bottom: 15px; color: #f0f0f0;"
        except Exception as e:
            print(f"Erreur: Erreur inattendue lors du chargement des styles GUI: {e}. Utilisation des styles par défaut.")
            full_stylesheet = """
                QMainWindow { background-color: #333; color: #f0f0f0; }
                QLabel { color: #f0f0f0; font-size: 12px; }
                QLineEdit { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 12px; }
                QPushButton { background-color: #555; color: white; border: none; padding: 8px 12px; border-radius: 4px; font-size: 12px; }
                QTextBrowser { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 4px; font-size: 11px; }
                QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; color: black; background-color: #555; }
                QProgressBar::chunk { background-color: #28a745; width: 20px; }
                #destinationPathLabel { font-size: 16px; font-weight: bold; color: #add8e6; margin-top: 5px; margin-bottom: 15px; } /* Style par défaut pour la destination */
                #separatorLine { background-color: #555; height: 2px; margin: 10px 0; }
                QPushButton#darkBlueButton { background-color: #4a69bd; }
                QPushButton#darkBlueButton:hover { background-color: #5a7ad6; }
                QPushButton#startButtonGreen { background-color: #28a745; }
                QPushButton#startButtonGreen:hover { background-color: #218838; }
                QPushButton#startButtonRed { background-color: #dc3545; }
                QPushButton#startButtonRed:hover { background-color: #c82333; }
                QPushButton#stopButton { background-color: #dc3545; }
                QPushButton#stopButton:hover { background-color: #c82333; }
            """
            self._main_title_style_string = "font-size: 30px; font-weight: bold; margin-bottom: 15px; color: #f0f0f0;"

        # Applique la feuille de style complète à la QMainWindow.
        # Les styles définis par objectName (#destinationPathLabel, #separatorLine, etc.)
        # dans full_stylesheet seront automatiquement appliqués aux widgets ayant cet objectName.
        self.setStyleSheet(full_stylesheet)


    # --- Méthodes utilitaires et de gestion d'UI ---

    def _clean_frontend_log(self):
        """
        Nettoie le fichier de log du frontend (app.log) en le vidant s'il est plus ancien qu'une semaine.
        """
        max_age_days = 7
        if APP_LOG_FILE.exists():
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
            try:
                file_mod_time = datetime.datetime.fromtimestamp(APP_LOG_FILE.stat().st_mtime)
                if file_mod_time < cutoff_time:
                    with open(APP_LOG_FILE, 'w', encoding='utf-8') as f:
                        f.truncate(0) # Vide le contenu du fichier
                    self.log_message("Contenu du log principal du frontend vidé car trop ancien.", is_error=False, is_formatted_key=False)
            except Exception as e:
                self.log_message(f"Erreur lors du nettoyage du log principal du frontend {APP_LOG_FILE}: {e}", is_error=True, error_code="LOG001", is_formatted_key=False)


    def update_slider_from_input(self):
        """Met à jour le slider de fréquence en fonction de la valeur saisie dans l'input."""
        text = self.frequency_input.text()
        if text.isdigit():
            value = int(text)
            min_val = self.frequency_slider.minimum()
            max_val = self.frequency_slider.maximum()
            
            if min_val <= value <= max_val:
                self.frequency_slider.setValue(value)
            else:
                if value < min_val:
                    self.frequency_input.setText(str(min_val))
                elif value > max_val:
                    self.frequency_input.setText(str(max_val))

    def log_message(self, message_key: str, is_error: bool = False, error_code: str = None, **kwargs):
        """
        Ajoute un message à la zone de log de l'interface, en utilisant les textes traduits.
        `message_key`: Clé du message dans le dictionnaire `self.texts[self.current_lang]`.
        `is_formatted_key`: Si True, `message_key` est une clé de traduction. Sinon, `message_key` est le message brut.
        `kwargs`: Arguments supplémentaires pour le formatage du message (ex: config_name, error_message).
        """
        # Vérifie si log_output est initialisé avant de tenter de l'utiliser
        if not hasattr(self, 'log_output') or self.log_output is None:
            # Si log_output n'est pas prêt, imprime directement dans la console
            print(f"[FALLBACK LOG - {'ERROR' if is_error else 'INFO'}]: {message_key}")
            return
        
        current_texts = self.texts.get(self.current_lang, self.texts["en"]) # Fallback to English

        # Si is_formatted_key est True, on cherche la clé dans les textes traduits
        if message_key in current_texts and kwargs.get('is_formatted_key', False):
            message_template = current_texts[message_key]
        else:
            # Sinon, on utilise message_key comme message brut
            message_template = message_key
        
        # Formater le message avec les arguments supplémentaires
        try:
            message = message_template.format(**kwargs)
        except KeyError as e:
            message = f"ERROR: Missing key for log message formatting: {e}. Original template: '{message_template}'"
            is_error = True
            error_code = "LOG002"
        except Exception as e:
            message = f"ERROR: Could not format log message '{message_template}': {e}"
            is_error = True
            error_code = "LOG003"


        prefix = current_texts["log_prefix_error"] if is_error else current_texts["log_prefix_info"]
        
        if is_error and error_code:
            error_msg = f"{prefix}{current_texts['log_error_code_prefix']}{error_code}: {message}."
            if APP_LOG_FILE.exists():
                error_msg += f" <a href='file:///{APP_LOG_FILE}' style='color: #4a90d9;'>{current_texts['log_consult_file']}</a>."
            else:
                error_msg += current_texts['log_file_not_found']
            self.log_output.append(error_msg)
        else:
            self.log_output.append(f"{prefix}{message}")
        
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def limit_log_lines(self):
        """Limite la zone de log aux 100 dernières lignes."""
        text = self.log_output.toPlainText()
        lines = text.split('\n')
        if len(lines) > 100:
            self.log_output.setPlainText('\n'.join(lines[-100:]))

    def copy_log_to_clipboard(self):
        """Copie le contenu de la zone de log dans le presse-papiers."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.log_output.toPlainText())
        self.log_message("log_clipboard_copied", is_formatted_key=True)

    def create_app_directories(self):
        """
        Crée les répertoires nécessaires à l'application (.synchro, logs, configs)
        et s'assure que le fichier app.log existe.
        """
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            TASK_LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            # AJOUT : Créer le fichier app.log s'il n'existe pas
            if not APP_LOG_FILE.exists():
                APP_LOG_FILE.touch() # Crée un fichier vide
                # Ne pas utiliser self.log_message ici, car log_output pourrait ne pas être prêt
                print(f"Frontend: Fichier de log d'application créé : {APP_LOG_FILE}")

            # Ne pas utiliser self.log_message ici pour éviter les boucles infinies ou les erreurs si log_output n'est pas prêt
            print(f"Frontend: Répertoires de l'application vérifiés/créés : {APP_DIR}")
        except Exception as e:
            # Ici, nous ne pouvons pas utiliser log_message avec le lien si le fichier n'existe pas
            # et que la création a échoué. On loguera directement dans la console.
            print(f"CRITICAL ERROR: Failed to create application directories or app.log file: {e}")
            # self.log_message(f"Erreur critique lors de la création des répertoires de l'application ou du fichier log : {e}", is_error=True, error_code="FS001")


    def load_external_volume_base_path(self):
        """
        Charge le chemin de base du volume externe et le paramètre max_cached_versions
        depuis volume_config.json.
        """
        self._external_volume_base_path = Path.home() / "SynchroDestination"
        # self._max_cached_versions est déjà initialisé dans __init__

        current_texts = self.texts.get(self.current_lang, self.texts["en"])

        if VOLUME_CONFIG_FILE.exists():
            try:
                with open(VOLUME_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    # Charger le chemin de base du volume
                    base_path = config.get("external_volume_base_path")
                    if base_path and Path(base_path).is_dir():
                        self._external_volume_base_path = Path(base_path)
                        self.log_message("log_external_volume_loaded", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE), path=str(self._external_volume_base_path))
                    else:
                        self.log_message("log_external_volume_invalid", is_error=True, error_code="CFG008", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE))
                    
                    # Charger le paramètre max_cached_versions
                    max_versions = config.get("max_cached_versions")
                    if isinstance(max_versions, int) and max_versions >= 0:
                        self._max_cached_versions = max_versions
                        self.log_message("log_max_versions_loaded", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE), count=self._max_cached_versions)
                    else:
                        self.log_message("log_max_versions_invalid", is_error=True, error_code="CFG012", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE), default_value=self._max_cached_versions)
                        
            except json.JSONDecodeError as e:
                self.log_message("log_external_volume_json_error", is_error=True, error_code="CFG009", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE), error_message=str(e))
            except Exception as e:
                self.log_message("log_external_volume_unexpected_error", is_error=True, error_code="CFG010", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE), error_message=str(e))
        else:
            self.log_message("log_external_volume_not_found", is_error=True, error_code="CFG011", is_formatted_key=True, file_path=str(VOLUME_CONFIG_FILE))

        # Mettre à jour le champ de l'UI avec la valeur chargée ou par défaut
        self.max_cached_versions_input.setText(str(self._max_cached_versions))


    def update_destination_path(self, source_path_str: str):
        """
        Met à jour le champ de destination en fonction du chemin source sélectionné
        et du chemin de base du volume externe.
        """
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        source_path = Path(source_path_str)
        if source_path.is_dir():
            destination_dir_name = source_path.name
            final_destination_path = self._external_volume_base_path / destination_dir_name
            self.destination_input.setText(str(final_destination_path))
            self.destination_display_label.setText(f"{current_texts['destination_label']}: {final_destination_path}") # Mise à jour du label
        else:
            # Si le chemin source n'est pas un répertoire valide (ex: vide ou fichier),
            # on vide le champ destination pour indiquer qu'il n'y a pas de destination calculable.
            self.destination_input.setText("")
            self.destination_display_label.setText(current_texts["destination_label_default"]) # Mise à jour du label


    # --- Méthodes de sélection de fichiers/répertoires ---

    def browse_source(self):
        """Ouvre un dialogue pour sélectionner le répertoire source."""
        directory = QFileDialog.getExistingDirectory(self, self.texts[self.current_lang]["source_label"], str(self.source_input.text()))
        if directory:
            self.source_input.setText(directory)

    # Le bouton "Ouvrir Volume..." et sa méthode open_destination_base_path sont supprimés

    # --- Méthodes de gestion de configuration ---

    def get_current_config_data(self):
        """Récupère les données de configuration actuelles de l'interface."""
        source_path_obj = Path(self.source_input.text())
        config_name = source_path_obj.name if source_path_obj.is_dir() and source_path_obj.name else "default_config" # Fix if name is empty
        
        return {
            "name": config_name,
            "source": self.source_input.text(),
            "destination": self.destination_input.text(),
            "frequency_hours": int(self.frequency_input.text()),
            "blacklist_files": self.blacklist_files_input.text(),
            "blacklist_dirs": self.blacklist_dirs_input.text(),
            "max_cached_versions": int(self.max_cached_versions_input.text()) # AJOUT
        }

    def load_configuration(self):
        """Charger une configuration depuis un fichier JSON."""
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_file_path, _ = QFileDialog.getOpenFileName(
            self, current_texts["load_config_button"], str(CONFIGS_DIR), "JSON Files (*.json)"
        )
        if config_file_path:
            try:
                with open(config_file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                self.source_input.setText(config_data.get("source", ""))
                # Important: update_destination_path est appelée automatiquement par textChanged de source_input
                # donc pas besoin de définir destination_input directement ici.
                
                freq_val = config_data.get("frequency_hours", 1)
                self.frequency_input.setText(str(freq_val))
                
                self.blacklist_files_input.setText(config_data.get("blacklist_files", ""))
                self.blacklist_dirs_input.setText(config_data.get("blacklist_dirs", ""))
                
                # Charger la valeur de max_cached_versions
                max_versions_val = config_data.get("max_cached_versions", self._max_cached_versions)
                self.max_cached_versions_input.setText(str(max_versions_val))

                self.log_message("log_config_loaded", is_formatted_key=True, config_name=Path(config_file_path).stem)
                
                # --- NOUVEAU : Vérifier l'état de la synchro pour la config chargée ---
                self.check_sync_status() 

            except Exception as e:
                self.log_message("log_config_load_error", is_error=True, error_code="CFG001", is_formatted_key=True, error_message=str(e))

    def load_last_used_configuration(self):
        """
        Charge la dernière configuration utilisée (ici, "BacASable.json") au démarrage.
        """
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_name_to_load = "BacASable" # Nom de la config à charger par défaut
        config_path = CONFIGS_DIR / f"{config_name_to_load}.json"

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                self.source_input.setText(config_data.get("source", str(Path.home())))
                self.frequency_input.setText(str(config_data.get("frequency_hours", 1)))
                self.blacklist_files_input.setText(config_data.get("blacklist_files", ".tmp;.log;.bak"))
                self.blacklist_dirs_input.setText(config_data.get("blacklist_dirs", ".git;.cache;node_modules"))
                # Charger la valeur de max_cached_versions
                self.max_cached_versions_input.setText(str(config_data.get("max_cached_versions", self._max_cached_versions)))
                
                self.log_message("log_config_loaded", is_formatted_key=True, config_name=config_name_to_load)
            except Exception as e:
                self.log_message("log_config_load_error", is_error=True, error_code="CFG005", is_formatted_key=True, config_name=config_name_to_load, error_message=str(e))
        else:
            self.log_message("log_config_not_found", is_error=False, is_formatted_key=True, config_name=f"'{config_name_to_load}.json'")


    def save_configuration(self):
        """Sauvegarder la configuration actuelle dans un fichier JSON."""
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_data = self.get_current_config_data()
        config_name = config_data.get("name", "nouvelle_configuration")

        config_file_path, _ = QFileDialog.getSaveFileName(
            self, current_texts["save_config_button"], str(CONFIGS_DIR / f"{config_name}.json"), "JSON Files (*.json)"
        )

        if config_file_path:
            try:
                with open(config_file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=4, ensure_ascii=False)
                self.log_message("log_config_saved", is_formatted_key=True, file_path=config_file_path)
            except Exception as e:
                self.log_message("log_config_save_error", is_error=True, error_code="CFG002", is_formatted_key=True, error_message=str(e))

    def delete_configuration(self):
        """Supprimer une configuration existante."""
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_file_path, _ = QFileDialog.getOpenFileName(
            self, current_texts["delete_config_button"], str(CONFIGS_DIR), "JSON Files (*.json)"
        )
        if config_file_path:
            config_name_to_delete = Path(config_file_path).stem
            reply = QMessageBox.question(self, current_texts['confirm_delete_title'],
                                         current_texts['confirm_delete_message'].format(config_name=config_name_to_delete),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(config_file_path)
                    self.log_message("log_config_deleted", is_formatted_key=True, config_name=config_name_to_delete)
                except FileNotFoundError:
                    self.log_message("log_config_not_found", is_error=True, error_code="CFG003", is_formatted_key=True, config_name=config_name_to_delete)
                except Exception as e:
                    self.log_message("log_config_delete_error", is_error=True, error_code="CFG004", is_formatted_key=True, error_message=str(e))

    # --- Méthodes de communication avec le Backend ---

    def update_start_button_state(self, is_running: bool, final_status: str = None):
        """
        Met à jour l'état visuel du bouton Start et la barre de progression.
        final_status: 'completed', 'stopped', 'error' si la tâche vient de se terminer.
        """
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        self.is_sync_running = is_running
        if is_running:
            self.start_button.setObjectName("startButtonRed")
            self.start_button.setText(current_texts["start_button"]) # Texte "En Cours..."
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat(current_texts["log_sync_in_progress"].format(progress=0)) # Réinitialise le format
        else:
            self.start_button.setObjectName("startButtonGreen")
            self.start_button.setText(current_texts["start_button"])
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
            if final_status:
                if final_status == "completed":
                    self.progress_bar.setValue(100)
                    self.progress_bar.setFormat(current_texts["log_sync_completed"])
                    self.log_message("log_sync_completed", is_formatted_key=True)
                elif final_status == "stopped":
                    self.progress_bar.setFormat(current_texts["log_sync_stopped"])
                    self.log_message("log_sync_stopped", is_formatted_key=True)
                elif final_status == "error":
                    self.progress_bar.setFormat(current_texts["log_sync_error"])
                    self.log_message("log_sync_error", is_error=True, is_formatted_key=True)
                
                # Laisser la barre visible un court instant, puis la cacher
                QTimer.singleShot(3000, lambda: self.progress_bar.setVisible(False))
            else:
                # Si pas de statut final spécifique (ex: juste après le démarrage ou si aucune tâche n'est active)
                self.progress_bar.setVisible(False)
                self.progress_bar.setValue(0) # Assurez-vous qu'elle est à zéro quand cachée
                self.progress_bar.setFormat(current_texts["log_sync_inactive"]) # Texte par défaut

        # Réappliquer les styles pour s'assurer que le changement d'objet est visible
        self.start_button.setStyleSheet(self.styleSheet())
        self.stop_button.setStyleSheet(self.styleSheet())

    def start_sync_process(self):
        """Démarre le processus de synchronisation via le backend."""
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_data = self.get_current_config_data()
        config_name = config_data.get("name", "default_config")

        # Vérifier si la destination est définie avant de commencer
        if not config_data["destination"]:
            self.log_message("log_destination_not_defined", is_error=True, error_code="VAL001", is_formatted_key=True)
            return

        success_save, msg_save = self.api_client._make_request('PUT', f'/api/configs/{config_name}', config_data)
        if success_save:
            self.log_message("log_config_sent", is_formatted_key=True, config_name=config_name)
            data, status_code = self.api_client._make_request('POST', f'/api/sync_tasks/start/{config_name}')
            if status_code == 202:
                self.log_message("log_start_request_sent", is_formatted_key=True, config_name=config_name, message=data.get('message'))
                # update_start_button_state(True) sera appelé par check_sync_status qui sera déclenché par le timer
                self.active_sync_tasks[config_name] = "running" # Ajouter la tâche à la liste de suivi
                if not self.status_timer.isActive():
                    self.status_timer.start() # Démarrer le timer si ce n'est pas déjà fait
            else:
                self.log_message("log_start_error", is_error=True, error_code="API001", is_formatted_key=True, error_message=data.get('error', 'Erreur inconnue'))
        else:
             self.log_message("log_backend_save_error", is_error=True, error_code="API002", is_formatted_key=True, error_message=msg_save.get('error', 'Erreur inconnue') if isinstance(msg_save, dict) else str(msg_save))

    def stop_sync_process(self):
        """Arrête le processus de synchronisation sélectionné via le backend."""
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        config_name = Path(self.source_input.text()).name or "default_config"

        self.log_message("log_stop_request", is_formatted_key=True, config_name=config_name)
        data, status_code = self.api_client._make_request('POST', f'/api/sync_tasks/stop/{config_name}')
        if status_code == 202:
            self.log_message("log_stop_signal_sent", is_formatted_key=True, config_name=config_name, message=data.get('message'))
            # Ne pas appeler update_start_button_state(False) ici. Le timer le fera quand il détectera le changement de statut.
            self.active_sync_tasks[config_name] = "stopping" # Marquer comme "en cours d'arrêt"
        else:
            self.log_message("log_stop_error", is_error=True, error_code="API003", is_formatted_key=True, error_message=data.get('error', 'Erreur inconnue'))

    def check_sync_status(self):
        """
        Vérifie périodiquement le statut de toutes les tâches de synchronisation
        et met à jour l'UI en conséquence, en se concentrant sur la configuration actuelle.
        """
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        current_config_data = self.get_current_config_data()
        current_config_name = current_config_data.get("name", "default_config")

        # Réinitialiser l'état de l'UI pour la configuration actuelle.
        # Cela assure que si la tâche n'est plus en cours, l'UI revient à l'état "idle".
        self.update_start_button_state(False) 

        data, status_code = self.api_client.get_sync_tasks()
        
        if status_code == 200:
            active_tasks_from_backend = {task['config_name']: task for task in data}
            
            # Mettre à jour la liste des tâches actives que le frontend suit (pour le timer global)
            # et trouver la tâche correspondant à la configuration actuellement affichée.
            found_current_config_on_backend = False
            for task_name, backend_task in active_tasks_from_backend.items():
                status = backend_task.get('status')
                
                if status == "running":
                    self.active_sync_tasks[task_name] = "running" # Suivre toutes les tâches en cours
                elif task_name in self.active_sync_tasks:
                    del self.active_sync_tasks[task_name] # Retirer les tâches non running de notre suivi

                if task_name == current_config_name:
                    found_current_config_on_backend = True
                    if status == "running":
                        self.update_start_button_state(True) # Met l'UI en état "en cours"
                        self.progress_bar.setValue(backend_task.get('progress', 0))
                        self.progress_bar.setFormat(current_texts["log_sync_in_progress"].format(progress=backend_task.get('progress', 0)))
                    elif status in ["completed", "stopped", "error"]:
                        self.update_start_button_state(False, final_status=status)
                        self.get_synthesis(specific_task_name=task_name)
                        # Le timer sera arrêté plus bas si aucune tâche n'est active.
            
            # Si la configuration actuellement affichée n'est pas trouvée comme "running"
            # sur le backend, et qu'elle n'est pas déjà dans un état final qui a été traité.
            # (Le `update_start_button_state(False)` initial a déjà réinitialisé l'UI).
            if not found_current_config_on_backend:
                # Loguer un message si la synchronisation pour la config actuelle n'est pas active.
                # Éviter de loguer si le champ source est vide (au démarrage avant chargement de config)
                if current_config_name != "default_config" and self.source_input.text():
                    self.log_message("log_sync_not_active", is_formatted_key=True, config_name=current_config_name)

            # Gérer le timer global en fonction de TOUTES les tâches actives sur le backend
            if self.active_sync_tasks and not self.status_timer.isActive():
                self.status_timer.start()
                self.log_message("log_tasks_detected", is_formatted_key=True)
            elif not self.active_sync_tasks and self.status_timer.isActive():
                self.status_timer.stop()
                self.log_message("log_no_active_tasks", is_formatted_key=True)

        else:
            self.log_message("log_synthesis_error", is_error=True, error_code="API004", is_formatted_key=True, error_message=data.get('error', 'Erreur inconnue'), status_code=status_code)
            self.log_message("log_backend_check", is_formatted_key=True)


    def get_synthesis(self, specific_task_name: str = None):
        """
        Récupère et affiche la synthèse des synchronisations.
        Si specific_task_name est fourni, tente d'afficher la synthèse pour cette tâche uniquement.
        """
        current_texts = self.texts.get(self.current_lang, self.texts["en"])
        self.log_output.clear()
        self.log_message("log_synthesis_retrieval", is_formatted_key=True)
        self.log_output.append("") # Ligne vide pour espacement

        data, status_code = self.api_client.get_sync_tasks()

        if status_code == 200:
            if data:
                tasks_to_display = []
                if specific_task_name:
                    # Cherche la tâche spécifique
                    for task in data:
                        if task.get('config_name') == specific_task_name:
                            tasks_to_display.append(task)
                            break # Trouvé, on sort
                    if not tasks_to_display:
                        self.log_message("log_task_not_found", is_formatted_key=True, config_name=specific_task_name)
                        return

                else:
                    # Affiche toutes les tâches si pas de nom spécifique
                    tasks_to_display = data

                self.log_message("log_synthesis_header", is_formatted_key=True)
                for task in tasks_to_display:
                    status = task.get('status')
                    config_name = task.get('config_name')
                    duration_sec = int(task.get('duration', 0))
                    
                    # Convertir la durée en un format plus lisible (heures, minutes, secondes)
                    hours, remainder = divmod(duration_sec, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
                    
                    # Récupérer les nouvelles métriques de synthèse
                    dirs_added = task.get('dirs_added', 'N/A')
                    files_added = task.get('files_added', 'N/A')
                    dirs_modified = task.get('dirs_modified', 'N/A')
                    files_modified = task.get('files_modified', 'N/A')
                    log_file_name = task.get('log_file_name') # Nom du fichier de log spécifique à cette tâche

                    log_link_text = current_texts["log_synthesis_log_link"]
                    log_link = ""
                    if log_file_name:
                        log_path = TASK_LOG_DIR / log_file_name
                        # Vérifiez si le fichier de log existe réellement avant de créer un lien cliquable
                        if log_path.exists():
                            log_link = f" (<a href='file:///{log_path}' style='color: #4a90d9;'>{log_link_text}</a>)"
                        else:
                            log_link = current_texts["log_synthesis_log_not_found"]


                    # Affichage des informations de base pour la tâche
                    self.log_message("log_synthesis_task_header", is_formatted_key=True, config_name=config_name, status=status.upper())
                    
                    # Affichage des détails si la tâche est terminée/arrêtée/en erreur
                    if status in ["completed", "stopped", "error"]:
                        self.log_message("log_synthesis_duration", is_formatted_key=True, duration=duration_str)
                        self.log_message("log_synthesis_dirs_added", is_formatted_key=True, count=dirs_added)
                        self.log_message("log_synthesis_files_added", is_formatted_key=True, count=files_added)
                        self.log_message("log_synthesis_dirs_modified", is_formatted_key=True, count=dirs_modified)
                        self.log_message("log_synthesis_files_modified", is_formatted_key=True, count=files_modified)
                        self.log_output.append(f"{current_texts['log_prefix_info']}  - {log_link}") # Ajout du lien vers le log ici
                    elif status == "running":
                        pid_info = f" (PID: {task.get('pid')})" if task.get('pid') else ""
                        self.log_message("log_synthesis_running_status", is_formatted_key=True, status_upper=status.upper(), pid_info=pid_info, duration=duration_str)
                        self.log_output.append(f"{current_texts['log_prefix_info']}  - {log_link}") # Le log peut être utile même pour une tâche en cours
                    else:
                        # Fallback pour les statuts non gérés dans les clés de traduction
                        self.log_output.append(f"{current_texts['log_prefix_info']}  - Statut: {status.upper()}, Durée: {duration_str}{log_link}")
                    self.log_output.append("-" * 40) # Séparateur pour chaque tâche
            else:
                self.log_message("log_no_tasks_found", is_formatted_key=True)
            
        else:
            self.log_message("log_synthesis_error", is_error=True, error_code="API004", is_formatted_key=True, error_message=data.get('error', 'Erreur inconnue'), status_code=status_code)
            self.log_message("log_backend_check", is_formatted_key=True)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)

