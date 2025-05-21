# Fichier: Synchro_qt_made/mainwindow.py
#
# Historique des versions:
#
# Version 3.34 (2025-05-21):
#   - Correction de l'ordre d'initialisation : L'initialisation de `self.max_cached_versions_input`
#     et de `self._max_cached_versions` a été déplacée plus tôt dans la méthode `__init__`,
#     avant l'appel à `self.load_external_volume_base_path()`, résolvant ainsi l'AttributeError.
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
    QMessageBox, QGridLayout, QFormLayout, QProgressBar
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QDesktopServices, QIntValidator
import json
from pathlib import Path
import os

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

        # AJOUT : Message de log de test très tôt pour vérifier l'écriture dans app.log
        self.log_message("Frontend: Initialisation de l'application...", is_error=False)


        self.setWindowTitle("Synchro Qt Made - Sauvegarde/Synchronisation")
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
        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.setObjectName("darkBlueButton")
        self.clear_log_button.clicked.connect(self.log_output.clear)

        self.copy_log_button = QPushButton("Copie Log")
        self.copy_log_button.setObjectName("darkBlueButton")
        self.copy_log_button.clicked.connect(self.copy_log_to_clipboard)

        # Initialisation du chemin de base du volume externe (peut maintenant logger)
        self._external_volume_base_path = Path.home() / "SynchroDestination"
        # Initialisation du paramètre max_cached_versions
        self._max_cached_versions = 2 # Valeur par défaut avant chargement depuis config

        # ---------------------------------------------
        # Ligne 0: Titre principal
        # ---------------------------------------------
        self.title_label = QLabel("Sauvegarde / Synchronisation")
        self.title_label.setAlignment(Qt.AlignCenter)
        # Assurez-vous que le style du titre est appliqué ici, après sa création
        if hasattr(self, '_main_title_style_string') and self._main_title_style_string:
            self.title_label.setStyleSheet(self._main_title_style_string)
        self.main_layout.addWidget(self.title_label)

        # ---------------------------------------------
        # Ligne 1: Affichage du chemin de destination sous le titre
        # ---------------------------------------------
        self.destination_display_label = QLabel("Destination: Non définie") # Valeur par défaut
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
        self.source_browse_button = QPushButton("Parcourir...")
        self.source_browse_button.clicked.connect(self.browse_source)
        self.source_browse_button.setObjectName("darkBlueButton")
        source_h_layout = QHBoxLayout()
        source_h_layout.addWidget(self.source_input)
        source_h_layout.addWidget(self.source_browse_button)
        self.config_form_layout.addRow("Source:", source_h_layout)
        
        self.source_input.textChanged.connect(self.update_destination_path)

        # Ligne 3: Destination (champ non éditable, sans bouton)
        self.destination_input = QLineEdit()
        self.destination_input.setReadOnly(True) # Reste non éditable
        self.destination_input.setToolTip("Le chemin de destination est généré automatiquement (Volume Externe + Nom du Répertoire Source).")
        # Le bouton "Ouvrir Volume..." est supprimé
        self.config_form_layout.addRow("Destination:", self.destination_input)

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
        self.config_form_layout.addRow("Fréquence (heures):", freq_h_layout)

        # Ligne 5: Blacklist fichiers
        self.blacklist_files_input = QLineEdit(".tmp;.log;.bak")
        self.config_form_layout.addRow("Blacklist Fichiers:", self.blacklist_files_input)

        # Ligne 6: Blacklist répertoires
        self.blacklist_dirs_input = QLineEdit(".git;.cache;node_modules")
        self.config_form_layout.addRow("Blacklist Répertoires:", self.blacklist_dirs_input)

        # Ligne 7: Max versions en cache
        # L'initialisation de self._max_cached_versions doit être faite avant load_external_volume_base_path()
        # et le texte du QLineEdit sera défini par load_external_volume_base_path()
        self.max_cached_versions_input = QLineEdit(str(self._max_cached_versions)) # Initialisation avec la valeur par défaut
        self.max_cached_versions_input.setFixedWidth(50)
        self.max_cached_versions_input.setAlignment(Qt.AlignCenter)
        self.max_cached_versions_input.setValidator(QIntValidator(0, 99, self)) # De 0 à 99 versions
        self.config_form_layout.addRow("Max Versions en Cache:", self.max_cached_versions_input)

        self.main_layout.addLayout(self.config_form_layout)

        # ---------------------------------------------
        # Ligne 8: Boutons de configuration (Charger/Sauvegarder/Détruire) - Répartis
        # ---------------------------------------------
        self.config_buttons_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Charger Configuration")
        self.load_config_button.setObjectName("darkBlueButton")
        self.load_config_button.clicked.connect(self.load_configuration)

        self.save_config_button = QPushButton("Sauvegarder Configuration")
        self.save_config_button.setObjectName("darkBlueButton")
        self.save_config_button.clicked.connect(self.save_configuration)
        
        self.delete_config_button = QPushButton("Détruire Configuration")
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
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButtonGreen")
        self.start_button.clicked.connect(self.start_sync_process)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_sync_process)

        self.synthesis_button = QPushButton("Synthèse")
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

        # ---------------------------------------------
        # Ligne 13: Bouton Quitter
        # ---------------------------------------------
        self.quit_button_layout = QHBoxLayout()
        self.quit_button = QPushButton("Quitter")
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
        self.log_message(f"Application démarrée. Fichier de logs backend : {APP_LOG_FILE}", is_error=False)

        # --- AJOUT: Configuration du QTimer pour la vérification du statut ---
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(2000)  # Vérifie toutes les 2 secondes (2000 ms)
        self.status_timer.timeout.connect(self.check_sync_status)
        
        # Le timer sera démarré dans check_sync_status si une tâche est trouvée en cours pour la config actuelle.
        # Pas d'appel initial à check_sync_status ici, car c'est le chargement de config qui le déclenchera.

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

    def log_message(self, message: str, is_error: bool = False, error_code: str = None):
        """
        Ajoute un message à la zone de log de l'interface.
        Gère aussi l'affichage des erreurs avec lien vers le fichier de log.
        """
        # Vérifie si log_output est initialisé avant de tenter de l'utiliser
        if not hasattr(self, 'log_output') or self.log_output is None:
            # Si log_output n'est pas prêt, imprime directement dans la console
            print(f"[FALLBACK LOG - {'ERREUR' if is_error else 'INFO'}]: {message}")
            return
            
        prefix = "<span style='color: #dc3545;'>[ERREUR]</span> " if is_error else "<span style='color: #28a745;'>[INFO]</span> "
        
        if is_error and error_code:
            error_msg = f"{prefix}Erreur N°{error_code}: {message}."
            # AJOUT : Vérifier si le fichier de log existe avant de créer le lien
            if APP_LOG_FILE.exists():
                error_msg += f" <a href='file:///{APP_LOG_FILE}' style='color: #4a90d9;'>Consulter le fichier log</a>."
            else:
                error_msg += " (Fichier log d'application non trouvé)."
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
        self.log_message("Contenu du log copié dans le presse-papiers.")

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
            # Si cette erreur se produit, log_message ne pourra probablement pas non plus écrire dans app.log
            # self.log_message(f"Erreur critique lors de la création des répertoires de l'application ou du fichier log : {e}", is_error=True, error_code="FS001")


    def load_external_volume_base_path(self):
        """
        Charge le chemin de base du volume externe et le paramètre max_cached_versions
        depuis volume_config.json.
        """
        self._external_volume_base_path = Path.home() / "SynchroDestination"
        # self._max_cached_versions est déjà initialisé dans __init__

        if VOLUME_CONFIG_FILE.exists():
            try:
                with open(VOLUME_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    # Charger le chemin de base du volume
                    base_path = config.get("external_volume_base_path")
                    if base_path and Path(base_path).is_dir():
                        self._external_volume_base_path = Path(base_path)
                        self.log_message(f"Chemin de base du volume externe chargé depuis {VOLUME_CONFIG_FILE}: {self._external_volume_base_path}")
                    else:
                        self.log_message(f"Chemin de base du volume externe invalide ou non existant dans {VOLUME_CONFIG_FILE}. Utilisation par défaut.", is_error=True, error_code="CFG008")
                    
                    # Charger le paramètre max_cached_versions
                    max_versions = config.get("max_cached_versions")
                    if isinstance(max_versions, int) and max_versions >= 0:
                        self._max_cached_versions = max_versions
                        self.log_message(f"Max Versions en Cache chargé depuis {VOLUME_CONFIG_FILE}: {self._max_cached_versions}")
                    else:
                        self.log_message(f"Valeur 'max_cached_versions' invalide ou non trouvée dans {VOLUME_CONFIG_FILE}. Utilisation par défaut ({self._max_cached_versions}).", is_error=True, error_code="CFG012")
                        
            except json.JSONDecodeError as e:
                self.log_message(f"Erreur de lecture de {VOLUME_CONFIG_FILE} (JSON invalide): {e}", is_error=True, error_code="CFG009")
            except Exception as e:
                self.log_message(f"Erreur inattendue lors du chargement de {VOLUME_CONFIG_FILE}: {e}", is_error=True, error_code="CFG010")
        else:
            self.log_message(f"Fichier {VOLUME_CONFIG_FILE} non trouvé. Chemin de base du volume externe et Max Versions en Cache par défaut appliqués.", is_error=True, error_code="CFG011")

        # Mettre à jour le champ de l'UI avec la valeur chargée ou par défaut
        self.max_cached_versions_input.setText(str(self._max_cached_versions))


    def update_destination_path(self, source_path_str: str):
        """
        Met à jour le champ de destination en fonction du chemin source sélectionné
        et du chemin de base du volume externe.
        """
        source_path = Path(source_path_str)
        if source_path.is_dir():
            destination_dir_name = source_path.name
            final_destination_path = self._external_volume_base_path / destination_dir_name
            self.destination_input.setText(str(final_destination_path))
            self.destination_display_label.setText(f"Destination: {final_destination_path}") # Mise à jour du label
        else:
            # Si le chemin source n'est pas un répertoire valide (ex: vide ou fichier),
            # on vide le champ destination pour indiquer qu'il n'y a pas de destination calculable.
            self.destination_input.setText("")
            self.destination_display_label.setText("Destination: Non définie") # Mise à jour du label


    # --- Méthodes de sélection de fichiers/répertoires ---

    def browse_source(self):
        """Ouvre un dialogue pour sélectionner le répertoire source."""
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire source", str(self.source_input.text()))
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
        config_file_path, _ = QFileDialog.getOpenFileName(
            self, "Charger une configuration", str(CONFIGS_DIR), "JSON Files (*.json)"
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

                self.log_message(f"Configuration '{Path(config_file_path).stem}' chargée avec succès.")
                
                # --- NOUVEAU : Vérifier l'état de la synchro pour la config chargée ---
                self.check_sync_status() 

            except Exception as e:
                self.log_message(f"Erreur lors du chargement de la configuration: {e}", is_error=True, error_code="CFG001")

    def load_last_used_configuration(self):
        """
        Charge la dernière configuration utilisée (ici, "BacASable.json") au démarrage.
        """
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
                
                self.log_message(f"Configuration '{config_name_to_load}' chargée au démarrage.")
            except Exception as e:
                self.log_message(f"Erreur lors du chargement de la configuration '{config_name_to_load}' au démarrage: {e}", is_error=True, error_code="CFG005")
        else:
            self.log_message(f"Configuration '{config_name_to_load}.json' non trouvée au démarrage. Utilisation des valeurs par défaut.", is_error=False)


    def save_configuration(self):
        """Sauvegarder la configuration actuelle dans un fichier JSON."""
        config_data = self.get_current_config_data()
        config_name = config_data.get("name", "nouvelle_configuration")

        config_file_path, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder la configuration", str(CONFIGS_DIR / f"{config_name}.json"), "JSON Files (*.json)"
        )

        if config_file_path:
            try:
                with open(config_file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=4, ensure_ascii=False)
                self.log_message(f"Configuration sauvegardée vers : {config_file_path}")
            except Exception as e:
                self.log_message(f"Erreur lors de la sauvegarde de la configuration: {e}", is_error=True, error_code="CFG002")

    def delete_configuration(self):
        """Supprimer une configuration existante."""
        config_file_path, _ = QFileDialog.getOpenFileName(
            self, "Supprimer une configuration", str(CONFIGS_DIR), "JSON Files (*.json)"
        )
        if config_file_path:
            reply = QMessageBox.question(self, 'Confirmation de suppression',
                                         f"Êtes-vous sûr de vouloir supprimer la configuration '{Path(config_file_path).stem}' ?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(config_file_path)
                    self.log_message(f"Configuration '{Path(config_file_path).stem}' supprimée avec succès.")
                except FileNotFoundError:
                    self.log_message(f"Erreur: Le fichier de configuration '{Path(config_file_path).stem}' n'existe pas.", is_error=True, error_code="CFG003")
                except Exception as e:
                    self.log_message(f"Erreur lors de la suppression de la configuration: {e}", is_error=True, error_code="CFG004")

    # --- Méthodes de communication avec le Backend ---

    def update_start_button_state(self, is_running: bool, final_status: str = None):
        """
        Met à jour l'état visuel du bouton Start et la barre de progression.
        final_status: 'completed', 'stopped', 'error' si la tâche vient de se terminer.
        """
        self.is_sync_running = is_running
        if is_running:
            self.start_button.setObjectName("startButtonRed")
            self.start_button.setText("En Cours...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("Synchronisation en cours: %p%") # Réinitialise le format
            # self.log_message("Synchronisation démarrée.", is_error=False) # Logué déjà par start_sync_process
        else:
            self.start_button.setObjectName("startButtonGreen")
            self.start_button.setText("Start")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
            if final_status:
                if final_status == "completed":
                    self.progress_bar.setValue(100)
                    self.progress_bar.setFormat("Synchronisation terminée")
                    self.log_message("Synchronisation terminée.", is_error=False)
                elif final_status == "stopped":
                    self.progress_bar.setFormat("Synchronisation arrêtée")
                    self.log_message("Synchronisation arrêtée.", is_error=False)
                elif final_status == "error":
                    self.progress_bar.setFormat("Erreur de synchronisation")
                    self.log_message("Erreur de synchronisation.", is_error=True)
                
                # Laisser la barre visible un court instant, puis la cacher
                QTimer.singleShot(3000, lambda: self.progress_bar.setVisible(False))
            else:
                # Si pas de statut final spécifique (ex: juste après le démarrage ou si aucune tâche n'est active)
                self.progress_bar.setVisible(False)
                self.progress_bar.setValue(0) # Assurez-vous qu'elle est à zéro quand cachée
                self.progress_bar.setFormat("Synchronisation inactive") # Texte par défaut

        # Réappliquer les styles pour s'assurer que le changement d'objet est visible
        self.start_button.setStyleSheet(self.styleSheet())
        self.stop_button.setStyleSheet(self.styleSheet())

    def start_sync_process(self):
        """Démarre le processus de synchronisation via le backend."""
        config_data = self.get_current_config_data()
        config_name = config_data.get("name", "nouvelle_configuration")

        # Vérifier si la destination est définie avant de commencer
        if not config_data["destination"]:
            self.log_message("Erreur: Le chemin de destination n'est pas défini. Veuillez sélectionner un répertoire source valide.", is_error=True, error_code="VAL001")
            return

        success_save, msg_save = self.api_client._make_request('PUT', f'/api/configs/{config_name}', config_data)
        if success_save:
            self.log_message(f"Configuration '{config_name}' envoyée/mise à jour sur le backend. Tentative de démarrage de la synchro...")
            data, status_code = self.api_client._make_request('POST', f'/api/sync_tasks/start/{config_name}')
            if status_code == 202:
                self.log_message(f"Demande de démarrage de la synchronisation pour '{config_name}' envoyée. Message: {data.get('message')}")
                # update_start_button_state(True) sera appelé par check_sync_status qui sera déclenché par le timer
                self.active_sync_tasks[config_name] = "running" # Ajouter la tâche à la liste de suivi
                if not self.status_timer.isActive():
                    self.status_timer.start() # Démarrer le timer si ce n'est pas déjà fait
            else:
                self.log_message(f"Erreur lors du démarrage de la synchronisation: {data.get('error', 'Erreur inconnue')}", is_error=True, error_code="API001")
        else:
             self.log_message(f"Impossible de sauvegarder la configuration sur le backend: {msg_save.get('error', 'Erreur inconnue') if isinstance(msg_save, dict) else msg_save}", is_error=True, error_code="API002")

    def stop_sync_process(self):
        """Arrête le processus de synchronisation sélectionné via le backend."""
        config_name = Path(self.source_input.text()).name or "default_config"

        self.log_message(f"Demande d'arrêt de la synchronisation pour '{config_name}'...")
        data, status_code = self.api_client._make_request('POST', f'/api/sync_tasks/stop/{config_name}')
        if status_code == 202:
            self.log_message(f"Signal d'arrêt envoyé pour '{config_name}'. Le backend attendra la fin du fichier en cours si nécessaire. Message: {data.get('message')}")
            # Ne pas appeler update_start_button_state(False) ici. Le timer le fera quand il détectera le changement de statut.
            self.active_sync_tasks[config_name] = "stopping" # Marquer comme "en cours d'arrêt"
        else:
            self.log_message(f"Erreur lors de l'envoi du signal d'arrêt: {data.get('error', 'Erreur inconnue')}", is_error=True, error_code="API003")

    def check_sync_status(self):
        """
        Vérifie périodiquement le statut de toutes les tâches de synchronisation
        et met à jour l'UI en conséquence, en se concentrant sur la configuration actuelle.
        """
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
                        self.progress_bar.setFormat(f"Synchronisation en cours: {backend_task.get('progress', 0)}%")
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
                    self.log_message(f"Synchronisation pour '{current_config_name}' n'est pas active.", is_error=False)

            # Gérer le timer global en fonction de TOUTES les tâches actives sur le backend
            if self.active_sync_tasks and not self.status_timer.isActive():
                self.status_timer.start()
                self.log_message("Tâches de synchronisation détectées. Timer de statut démarré.")
            elif not self.active_sync_tasks and self.status_timer.isActive():
                self.status_timer.stop()
                self.log_message("Aucune tâche de synchronisation active. Timer de statut arrêté.")

        else:
            self.log_message(f"Erreur lors de la vérification du statut des tâches: {data.get('error', 'Erreur inconnue')} (Statut: {status_code})", is_error=True, error_code="API005")
            # En cas d'erreur de communication avec le backend, on peut décider de stopper le timer
            # ou de le laisser continuer pour retenter. Pour l'instant, on le laisse.


    def get_synthesis(self, specific_task_name: str = None):
        """
        Récupère et affiche la synthèse des synchronisations.
        Si specific_task_name est fourni, tente d'afficher la synthèse pour cette tâche uniquement.
        """
        self.log_output.clear()
        self.log_message("Récupération de la synthèse des synchronisations...\n")
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
                        self.log_message(f"Aucune tâche '{specific_task_name}' trouvée pour la synthèse.")
                        return

                else:
                    # Affiche toutes les tâches si pas de nom spécifique
                    tasks_to_display = data

                self.log_message("--- Synthèse des Tâches de Synchronisation ---")
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

                    log_link = ""
                    if log_file_name:
                        log_path = TASK_LOG_DIR / log_file_name
                        # Vérifiez si le fichier de log existe réellement avant de créer un lien cliquable
                        if log_path.exists():
                            log_link = f" (<a href='file:///{log_path}' style='color: #4a90d9;'>Voir le log</a>)"
                        else:
                            log_link = " (Log non trouvé)" # Si le backend donne le nom mais le fichier n'existe pas


                    # Affichage des informations de base pour la tâche
                    self.log_message(f"--- Tâche: {config_name} (Statut: {status.upper()}) ---")
                    
                    # Affichage des détails si la tâche est terminée/arrêtée/en erreur
                    if status in ["completed", "stopped", "error"]:
                        self.log_message(f"  - Durée de l'opération: {duration_str}")
                        self.log_message(f"  - Répertoires ajoutés: {dirs_added}")
                        self.log_message(f"  - Fichiers ajoutés: {files_added}")
                        self.log_message(f"  - Répertoires modifiés: {dirs_modified}")
                        self.log_message(f"  - Fichiers modifiés: {files_modified}")
                        self.log_message(f"  - {log_link}") # Ajout du lien vers le log ici
                    elif status == "running":
                        pid_info = f" (PID: {task.get('pid')})" if task.get('pid') else ""
                        self.log_message(f"  - Statut: <span style='color: #28a745;'>{status.upper()}</span>{pid_info}, Durée actuelle: {duration_str}")
                        self.log_message(f"  - {log_link}") # Le log peut être utile même pour une tâche en cours
                    else:
                        self.log_message(f"  - Statut: {status.upper()}, Durée: {duration_str}{log_link}")
                    self.log_message("-" * 40) # Séparateur pour chaque tâche
            else:
                self.log_message("Aucune tâche de synchronisation active ou récemment terminée trouvée.")
            
        else:
            self.log_message(f"Erreur lors de la récupération de la synthèse: {data.get('error', 'Erreur inconnue')} (Statut: {status_code})", is_error=True, error_code="API004")
            self.log_message("Vérifiez que le backend est lancé et accessible à http://127.0.0.1:7555/")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)

