# Fichier: Synchro_backend/api.py
#
# Historique des versions:
#
# Version 3.31 (Révision 3 - 2025-05-21):
#   - Ajout de la fonction de nettoyage des logs : Une nouvelle méthode `clean_old_logs`
#     est ajoutée à la classe `TaskManager`. Cette méthode parcourt les répertoires de logs
#     (`TASK_LOG_DIR` et `LOGS_DIR` pour `backend_app.log`) et supprime les fichiers plus anciens que 7 jours.
#   - Planification du nettoyage : Un QTimer est initialisé dans la classe `TaskManager` pour appeler
#     `clean_old_logs` une fois par jour, assurant ainsi une maintenance régulière des logs.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.31 (Révision 2 - 2025-05-20):
#   - Nettoyage du log du backend : Le message de débogage "DEBUG BACKEND: API /api/sync_tasks renvoie : [...]"
#     est passé du niveau INFO au niveau DEBUG pour une journalisation plus propre en production.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.31 (Révision 1 - 2025-05-20):
#   - Amélioration du parsing des statistiques de synthèse dans `SyncTask.update_status_from_log` :
#     - L'extraction des valeurs numériques pour les répertoires et fichiers ajoutés/modifiés/supprimés
#       est maintenant effectuée à l'aide d'expressions régulières (`re`) pour une plus grande robustesse.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.31 (2025-05-20):
#   - Amélioration du parsing des logs pour les statistiques de synthèse et la progression :
#     - Extraction plus robuste de la partie message de chaque ligne de log (après " - INFO - ").
#     - La logique de détection de la fin du bloc de synthèse est affinée pour mieux correspondre
#       au format de log de `sync_engine.py` (lignes commençant par "  " pour les stats).
#     - Assure que les valeurs numériques sont correctement extraites et attribuées aux attributs de la tâche.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.30 (2025-05-20):
#   - Correction de la logique de parsing du fichier de log dans `SyncTask.update_status_from_log` :
#     - Amélioration de l'extraction de la progression et des statistiques de synthèse
#       (répertoires/fichiers ajoutés/modifiés/supprimés) en s'assurant que l'ordre de lecture
#       et la détection des blocs de synthèse sont corrects.
#     - Le parsing des statistiques de synthèse se fait maintenant en localisant le début du bloc
#       "Synthèse de l'opération :" et en lisant les lignes suivantes.
#     - Le parsing de la progression recherche la dernière occurrence de "Progression:".
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.29 (2025-05-20):
#   - Correction CRITIQUE du chemin et du nom du script de synchronisation :
#     - Le script est désormais correctement identifié comme 'sync_engine.py'.
#     - Le chemin d'accès est ajusté pour le trouver dans le même répertoire que 'api.py'.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.28 (2025-05-20):
#   - Correction critique du chemin d'accès au script de synchronisation (`sync_script.py`) :
#     - Le chemin est désormais construit pour cibler `Synchro_qt_made/sync_script.py`,
#       en se basant sur les logs d'erreur précédents qui indiquaient que le script
#       n'était pas trouvé à l'emplacement attendu.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.27 (2025-05-20):
#   - Amélioration du diagnostic de démarrage de tâche :
#     - Vérification explicite de l'existence du fichier 'sync_script.py' avant de tenter de le lancer.
#     - Capture et log de la sortie d'erreur standard (stderr) du sous-processus si le démarrage échoue,
#       afin de fournir des messages d'erreur plus détaillés dans les logs du backend.
#   - Mise à jour du commentaire de versionnage.
#
# Version 3.26 (2025-05-20):
#   - Correction majeure pour s'assurer que toutes les statistiques de synchronisation
#     (dirs_added, files_added, dirs_modified, files_modified, duration, log_file_name)
#     sont correctement collectées par la classe SyncTask et renvoyées par l'API /api/sync_tasks.
#   - Implémentation complète et vérifiée de la logique de démarrage/arrêt des processus de synchronisation.
#   - Amélioration de la gestion des logs, en particulier pour les logs spécifiques à chaque tâche.
#   - Ajout de messages de débogage clairs dans la console pour l'API /api/sync_tasks,
#     permettant de visualiser le JSON exact envoyé au frontend.
#   - Gestion des erreurs améliorée pour les réponses API.
#
# Version 3.25 (2025-05-20):
#   - Assure que les PIDs des processus sont correctement capturés et exposés par l'API.
#   - Implémentation du passage des données de configuration au script de synchronisation.
#   - Amélioration des messages de log du backend.
#
# Version 3.24 (2025-05-20):
#   - Correction des problèmes de sérialisation JSON pour les objets Path.
#   - Assure que les chemins de log sont correctement construits et accessibles.
#
# Version 3.23 (2025-05-20):
#   - Gestion des tâches de synchronisation (démarrage, arrêt, statut) via une classe dédiée TaskManager.
#   - Utilisation de subprocess pour lancer le script de synchronisation en arrière-plan.
#   - Mise en place de Flask-CORS pour gérer les requêtes cross-origin du frontend.
#
# Version 3.22 (2025-05-20):
#   - Endpoint pour sauvegarder et charger les configurations de synchronisation.
#   - Validation des données de configuration.
#
# Version 3.21 (2025-05-20):
#   - Initialisation de Flask et de l'API REST.
#   - Définition des chemins de base pour les logs et les configurations.
#
# Description Générale du Fichier:
# Ce fichier contient l'implémentation de l'API REST du backend de l'application Synchro Qt Made.
# Il gère les requêtes du frontend pour la gestion des configurations de synchronisation,
# le démarrage, l'arrêt et la récupération du statut des tâches de synchronisation.
# Il utilise Flask pour l'API et gère les processus de synchronisation via des sous-processus.
#
############################################################################################################

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import json
import logging
import subprocess
from pathlib import Path
import os
import datetime
import time # Pour la durée
import re # Importation du module re pour les expressions régulières
from PyQt5.QtCore import QTimer # Importation de QTimer pour le nettoyage des logs

# Configuration des chemins globaux pour le backend
APP_DIR = Path.home() / ".synchro"
CONFIGS_DIR = APP_DIR / "configs"
LOGS_DIR = APP_DIR / "logs"
APP_LOG_FILE = LOGS_DIR / "backend_app.log" # Renommé pour être clair que c'est le log du backend
TASK_LOG_DIR = LOGS_DIR / "tasks"

# Assurez-vous que les répertoires existent
for d in [APP_DIR, CONFIGS_DIR, LOGS_DIR, TASK_LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Configuration du logging pour le backend
logging.basicConfig(level=logging.INFO, # Le niveau INFO est le niveau par défaut
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(APP_LOG_FILE),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Création du blueprint pour les routes de l'API
api_bp = Blueprint('api', __name__)

# --- Classe pour représenter une tâche de synchronisation ---
class SyncTask:
    def __init__(self, config_name, config_data):
        self.config_name = config_name
        self.config_data = config_data
        self.status = "idle"  # idle, running, completed, stopped, error
        self.process = None   # Processus subprocess
        self.start_time = None
        self.end_time = None
        self.progress = 0     # Progression en pourcentage
        self.log_file_name = f"{config_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file_path = TASK_LOG_DIR / self.log_file_name

        # Statistiques de synchronisation (initialisées à 0 ou None)
        self.dirs_added = 0
        self.files_added = 0
        self.dirs_modified = 0
        self.files_modified = 0
        self.dirs_deleted = 0
        self.files_deleted = 0
        
    def start(self):
        # CORRECTION CRITIQUE DU CHEMIN ET DU NOM DU SCRIPT DE SYNCHRONISATION
        # Le script 'sync_engine.py' est dans le même répertoire que 'api.py'.
        sync_script_path = Path(__file__).parent / "sync_engine.py"
        
        if not sync_script_path.exists():
            logger.error(f"ERREUR: Le script de synchronisation n'a pas été trouvé à: {sync_script_path}. Vérifiez le nom et le chemin.")
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False

        try:
            # Préparer les arguments pour le script de synchronisation
            # Convertir les listes en chaînes séparées par des points-virgules
            blacklist_files_str = self.config_data.get('blacklist_files', '')
            blacklist_dirs_str = self.config_data.get('blacklist_dirs', '')

            cmd = [
                "python",
                str(sync_script_path),
                "--source", str(self.config_data['source']),
                "--destination", str(self.config_data['destination']),
                "--frequency", str(self.config_data['frequency_hours']),
                "--blacklist-files", blacklist_files_str,
                "--blacklist-dirs", blacklist_dirs_str,
                "--log-file", str(self.log_file_path), # Passer le chemin du log au script
                "--config-name", self.config_name, # Passer le nom de la config pour le logging interne du script
                "--max-cached-versions", str(self.config_data.get('max_cached_versions', 2)) # Passer le nouveau paramètre
            ]
            
            # Ouvrir le fichier de log en mode écriture pour le script
            # Utiliser Popen avec PIPE pour stderr pour capturer les erreurs de démarrage du script
            # et rediriger stdout vers le fichier de log.
            with open(self.log_file_path, 'w', encoding='utf-8') as f_log:
                self.process = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.PIPE, text=True, bufsize=1)
            
            # Vérifier si le processus a démarré correctement
            time.sleep(0.1) # Laisser un très court instant au processus pour démarrer ou échouer
            if self.process.poll() is not None:
                # Le processus a déjà terminé, ce qui indique un échec au démarrage
                stderr_output = self.process.stderr.read()
                logger.error(f"ÉCHEC DÉMARRAGE TÂCHE '{self.config_name}': Le script s'est terminé immédiatement. Code de sortie: {self.process.returncode}. Erreur Standard: \n{stderr_output}")
                self.status = "error"
                self.end_time = datetime.datetime.now()
                return False
            
            self.status = "running"
            self.start_time = datetime.datetime.now()
            self.progress = 0
            logger.info(f"Tâche '{self.config_name}' démarrée. PID: {self.process.pid}. Log: {self.log_file_path}")
            return True
        except FileNotFoundError:
            logger.error(f"ERREUR: Commande 'python' ou '{sync_script_path}' introuvable. Vérifiez votre PATH ou le chemin du script.")
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False
        except Exception as e:
            logger.error(f"Erreur inattendue au démarrage de la tâche '{self.config_name}': {e}", exc_info=True) # exc_info=True pour le traceback
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False

    def stop(self):
        if self.process and self.process.poll() is None: # Si le processus est toujours en cours
            try:
                # Envoyer un signal de terminaison au processus (SIGTERM)
                # Cela permet au script de s'arrêter proprement s'il gère ce signal
                self.process.terminate() 
                # Attendre un court instant que le processus se termine
                self.process.wait(timeout=5) 
                if self.process.poll() is not None:
                    self.status = "stopped"
                    logger.info(f"Tâche '{self.config_name}' (PID: {self.process.pid}) arrêtée.")
                else:
                    # Si le processus ne s'est pas terminé après terminate, le tuer
                    self.process.kill()
                    self.status = "stopped" # ou "killed" si vous voulez distinguer
                    logger.warning(f"Tâche '{self.config_name}' (PID: {self.process.pid}) tuée après échec de terminate.")
            except Exception as e:
                logger.error(f"Erreur lors de l'arrêt de la tâche '{self.config_name}': {e}")
                self.status = "error"
            finally:
                self.end_time = datetime.datetime.now()
        elif self.status == "running": # Si on tente d'arrêter une tâche déjà arrêtée mais non nettoyée
             self.status = "stopped"
             self.end_time = datetime.datetime.now()
             logger.info(f"Tâche '{self.config_name}' déjà terminée ou arrêtée.")

    def update_status_from_log(self):
        """
        Analyse le fichier de log de la tâche pour mettre à jour son statut,
        sa progression et ses statistiques de synchronisation.
        """
        if not self.log_file_path.exists():
            if self.status == "running":
                logger.warning(f"Log file for task '{self.config_name}' not found at {self.log_file_path} but task is 'running'. Marking as error.")
                self.status = "error"
                self.end_time = datetime.datetime.now()
            return

        try:
            with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # --- Parsing de la progression (dernière occurrence) ---
            current_progress = 0
            progress_pattern = re.compile(r"Progression:\s*(\d+)%")
            for line in reversed(lines):
                line = line.strip()
                # Extraire la partie message de la ligne de log (après " - INFO - ")
                # Le format est "YYYY-MM-DD HH:MM:SS,ms - LOGGER_NAME - LEVEL - MESSAGE"
                # On veut le MESSAGE
                message_match = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                message_part = message_match.group(1) if message_match else line

                match = progress_pattern.search(message_part)
                if match:
                    try:
                        current_progress = int(match.group(1))
                        self.progress = min(100, max(0, current_progress))
                        break # Trouvé la dernière progression, arrêter la recherche
                    except ValueError:
                        pass # Ignorer les lignes de progression mal formées
            
            # --- Parsing des statistiques de synthèse (bloc spécifique) ---
            summary_start_index = -1
            for i, line in enumerate(lines):
                message_match_header = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                message_part_header = message_match_header.group(1) if message_match_header else line
                
                if "Synthèse de l'opération :" in message_part_header:
                    summary_start_index = i
                    break

            if summary_start_index != -1:
                # Regex patterns for the statistics
                dirs_added_pattern = re.compile(r"Répertoires ajoutés:\s*(\d+)")
                files_added_pattern = re.compile(r"Fichiers ajoutés:\s*(\d+)")
                dirs_modified_pattern = re.compile(r"Répertoires modifiés:\s*(\d+)")
                files_modified_pattern = re.compile(r"Fichiers modifiés:\s*(\d+)")
                dirs_deleted_pattern = re.compile(r"Répertoires supprimés:\s*(\d+)")
                files_deleted_pattern = re.compile(r"Fichiers supprimés:\s*(\d+)")

                # Réinitialiser les stats avant de les parser à nouveau
                self.dirs_added = 0
                self.files_added = 0
                self.dirs_modified = 0
                self.files_modified = 0
                self.dirs_deleted = 0
                self.files_deleted = 0

                # Lire les lignes suivantes pour extraire les statistiques
                for i in range(summary_start_index + 1, len(lines)):
                    line = lines[i].strip()
                    message_match_stats = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                    message_part_stats = message_match_stats.group(1) if message_match_stats else line

                    # Les lignes de synthèse commencent par "  " (deux espaces)
                    # et ne sont pas des lignes vides ou d'autres niveaux de log
                    if not message_part_stats.startswith("  ") or not message_part_stats.strip():
                        break # Fin du bloc de synthèse ou ligne non pertinente

                    # Use regex to find and extract numbers
                    match = dirs_added_pattern.search(message_part_stats)
                    if match: self.dirs_added = int(match.group(1))
                    
                    match = files_added_pattern.search(message_part_stats)
                    if match: self.files_added = int(match.group(1))

                    match = dirs_modified_pattern.search(message_part_stats)
                    if match: self.dirs_modified = int(match.group(1))

                    match = files_modified_pattern.search(message_part_stats)
                    if match: self.files_modified = int(match.group(1))

                    match = dirs_deleted_pattern.search(message_part_stats)
                    if match: self.dirs_deleted = int(match.group(1))

                    match = files_deleted_pattern.search(message_part_stats)
                    if match: self.files_deleted = int(match.group(1))
            
            # Vérifier l'état du processus si running
            if self.status == "running":
                poll_result = self.process.poll()
                if poll_result is not None:
                    # Processus terminé
                    self.end_time = datetime.datetime.now()
                    if poll_result == 0:
                        self.status = "completed"
                        self.progress = 100 # S'assurer que la barre est à 100% à la fin
                        logger.info(f"Tâche '{self.config_name}' terminée avec succès.")
                    else:
                        self.status = "error"
                        logger.error(f"Tâche '{self.config_name}' terminée avec une erreur (code: {poll_result}).")
                # Si le script se termine très vite, la progression peut rester à 0.
                # Si la tâche est en cours et la progression est à 100, on la passe à completed.
                elif self.progress == 100:
                    self.status = "completed" # Le script a indiqué 100% de progression, il est donc probablement terminé.
                    self.end_time = datetime.datetime.now()

        except Exception as e:
            logger.error(f"Erreur lors de la lecture/mise à jour du log pour la tâche '{self.config_name}': {e}", exc_info=True)
            # Ne changez pas le statut en "error" ici, car c'est une erreur de lecture, pas de la tâche elle-même.

    def get_duration(self):
        """Calcule la durée de la tâche en secondes."""
        if self.start_time:
            if self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            else:
                return (datetime.datetime.now() - self.start_time).total_seconds()
        return 0

# --- Gestionnaire de Tâches ---
class TaskManager:
    _instance = None # Singleton pattern

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.tasks = {} # Dictionary to store SyncTask objects by config_name
            
            # Initialisation du timer pour le nettoyage des logs
            cls._instance.log_cleanup_timer = QTimer()
            cls._instance.log_cleanup_timer.setInterval(24 * 60 * 60 * 1000) # Toutes les 24 heures en ms
            cls._instance.log_cleanup_timer.timeout.connect(cls._instance._perform_log_cleanup)
            cls._instance.log_cleanup_timer.start()
            logger.info("Timer de nettoyage des logs démarré (toutes les 24 heures).")
            # Exécuter un nettoyage initial au démarrage
            cls._instance._perform_log_cleanup() 
        return cls._instance

    def _perform_log_cleanup(self):
        """
        Effectue le nettoyage des anciens fichiers de log dans les répertoires gérés par le backend.
        """
        logger.info("Début du nettoyage des anciens logs...")
        max_age_days = 7 # Durée de vie maximale des logs en jours

        # Nettoyage des logs de tâches
        self._clean_directory_logs(TASK_LOG_DIR, max_age_days)
        
        # Nettoyage du log principal du backend
        self._clean_single_file_log(APP_LOG_FILE, max_age_days)
        
        logger.info("Nettoyage des logs terminé.")

    def _clean_directory_logs(self, directory: Path, max_age_days: int):
        """Nettoie les fichiers de log dans un répertoire donné."""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
        
        for log_file in directory.iterdir():
            if log_file.is_file():
                try:
                    file_mod_time = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_mod_time < cutoff_time:
                        os.remove(log_file)
                        logger.info(f"Ancien log de tâche supprimé: {log_file}")
                except Exception as e:
                    logger.error(f"Erreur lors de la suppression du log {log_file}: {e}")

    def _clean_single_file_log(self, file_path: Path, max_age_days: int):
        """Nettoie un fichier de log unique en le recréant s'il est trop ancien."""
        if file_path.exists():
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
            try:
                file_mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mod_time < cutoff_time:
                    # Plutôt que de supprimer le fichier et de le laisser vide,
                    # on peut le vider ou le renommer et en créer un nouveau.
                    # Pour un log principal, le vider est souvent plus simple.
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.truncate(0) # Vide le contenu du fichier
                    logger.info(f"Contenu du log principal du backend vidé car trop ancien: {file_path}")
            except Exception as e:
                logger.error(f"Erreur lors du nettoyage du log principal {file_path}: {e}")

    def get_all_tasks(self):
        # Mettre à jour le statut de toutes les tâches avant de les retourner
        for task in list(self.tasks.values()): # Utiliser list() pour éviter RuntimeError si une tâche est supprimée
            task.update_status_from_log()
        
        # Nettoyer les tâches "complétées", "arrêtées" ou "en erreur" si elles sont restées longtemps
        # Pour éviter que la liste ne s'allonge indéfiniment. On garde les 5 dernières terminées par exemple.
        finished_tasks = {name: task for name, task in self.tasks.items() if task.status in ["completed", "stopped", "error"]}
        running_tasks = {name: task for name, task in self.tasks.items() if task.status == "running"}

        # Garder seulement les X dernières tâches terminées (ici, 5) + toutes les tâches en cours
        if len(finished_tasks) > 5:
            # Trier par date de fin et garder les plus récentes
            sorted_finished = sorted(finished_tasks.values(), key=lambda t: t.end_time if t.end_time else datetime.datetime.min, reverse=True)
            self.tasks = {task.config_name: task for task in sorted_finished[:5]}
            self.tasks.update(running_tasks)
        else:
            # If less than 5 finished tasks, keep all of them
            self.tasks = {name: task for name, task in self.tasks.items() if task.status not in ["completed", "stopped", "error"] or task in finished_tasks.values()}
            self.tasks.update(finished_tasks) # Ensure all finished tasks are included if < 5
            self.tasks.update(running_tasks) # Ensure all running tasks are included

        return list(self.tasks.values())

    def get_task(self, config_name):
        # Mise à jour du statut avant de retourner
        if config_name in self.tasks:
            self.tasks[config_name].update_status_from_log()
        return self.tasks.get(config_name)

    def add_task(self, task):
        self.tasks[task.config_name] = task

    def remove_task(self, config_name):
        if config_name in self.tasks:
            del self.tasks[config_name]

# Initialisation du gestionnaire de tâches
tasks_manager = TaskManager()

# --- Routes API ---

@api_bp.route('/api/configs/<config_name>', methods=['PUT'])
def update_config(config_name):
    """
    Met à jour ou crée une configuration de synchronisation.
    """
    try:
        config_data = request.json
        if not config_data:
            return jsonify({"error": "Données de configuration manquantes."}), 400

        # Valider les données minimales
        required_fields = ["source", "destination", "frequency_hours"]
        for field in required_fields:
            if field not in config_data:
                logger.error(f"Champ '{field}' manquant dans la configuration.")
                return jsonify({"error": f"Champ '{field}' manquant."}), 400

        # Assurer que les chemins sont absolus et valides (côté backend)
        source_path = Path(config_data['source'])
        destination_path = Path(config_data['destination'])
        
        if not source_path.exists():
            logger.warning(f"Chemin source non existant: {source_path}")
            # return jsonify({"error": f"Le chemin source '{source_path}' n'existe pas."}), 400
        # La destination peut ne pas exister, le script de sync la créera

        config_path = CONFIGS_DIR / f"{config_name}.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Configuration '{config_name}' mise à jour/créée.")
        return jsonify({"message": f"Configuration '{config_name}' sauvegardée avec succès."}), 200

    except json.JSONDecodeError:
        logger.error("Requête JSON invalide.")
        return jsonify({"error": "Format JSON invalide."}), 400
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la configuration: {e}", exc_info=True)
        return jsonify({"error": f"Erreur interne du serveur: {e}"}), 500

@api_bp.route('/api/sync_tasks/start/<config_name>', methods=['POST'])
def start_sync_task(config_name):
    """
    Démarre une tâche de synchronisation pour la configuration donnée.
    """
    config_path = CONFIGS_DIR / f"{config_name}.json"
    if not config_path.exists():
        logger.warning(f"Tentative de démarrage de tâche sans configuration trouvée: {config_name}")
        return jsonify({"error": f"Configuration '{config_name}' introuvable."}), 404

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        if config_name in tasks_manager.tasks and tasks_manager.tasks[config_name].status == "running":
            logger.info(f"Tâche '{config_name}' déjà en cours d'exécution.")
            return jsonify({"message": f"Tâche '{config_name}' est déjà en cours d'exécution."}), 200

        task = SyncTask(config_name, config_data)
        if task.start():
            tasks_manager.add_task(task)
            return jsonify({"message": f"Tâche '{config_name}' démarrée avec succès.", "pid": task.process.pid}), 202
        else:
            return jsonify({"error": f"Échec du démarrage de la tâche '{config_name}'."}), 500
    except Exception as e:
        logger.error(f"Erreur au démarrage de la tâche '{config_name}': {e}", exc_info=True)
        return jsonify({"error": f"Erreur interne du serveur: {e}"}), 500

@api_bp.route('/api/sync_tasks/stop/<config_name>', methods=['POST'])
def stop_sync_task(config_name):
    """
    Arrête une tâche de synchronisation.
    """
    task = tasks_manager.get_task(config_name)
    if not task:
        logger.warning(f"Tentative d'arrêt d'une tâche non trouvée: {config_name}")
        return jsonify({"error": f"Tâche '{config_name}' non trouvée ou déjà terminée."}), 404

    if task.status in ["completed", "stopped", "error"]:
        logger.info(f"Tâche '{config_name}' déjà terminée ou arrêtée.")
        return jsonify({"message": f"Tâche '{config_name}' est déjà terminée ou arrêtée."}), 200
    
    task.stop()
    return jsonify({"message": f"Signal d'arrêt envoyé pour la tâche '{config_name}'."}), 202

@api_bp.route('/api/sync_tasks', methods=['GET'])
def get_sync_tasks_status():
    """
    Récupère le statut de toutes les tâches de synchronisation actives et récentes.
    """
    tasks_data = [] 
    for task in tasks_manager.get_all_tasks(): # get_all_tasks met à jour le statut avant de les retourner
        task_info = {
            "config_name": task.config_name,
            "status": task.status,
            "progress": task.progress,
            "pid": task.process.pid if task.process else None,
            "duration": int(task.get_duration()), # Assurez-vous que cette méthode existe et retourne la durée en secondes
            "dirs_added": task.dirs_added, 
            "files_added": task.files_added,
            "dirs_modified": task.dirs_modified,
            "files_modified": task.files_modified,
            "log_file_name": task.log_file_name 
        }
        tasks_data.append(task_info)
    
    # --- LIGNE DE DÉBOGAGE MODIFIÉE ---
    logger.debug(f"DEBUG BACKEND: API /api/sync_tasks renvoie : {json.dumps(tasks_data, indent=2)}") 
    
    return jsonify(tasks_data), 200

# --- Fonction principale pour lancer l'application Flask ---
def create_app():
    app = Flask(__name__)
    CORS(app) # Permet au frontend de communiquer avec ce backend
    app.register_blueprint(api_bp)
    
    # Ajoutez un message de démarrage clair
    @app.route('/')
    def index():
        return "Backend Synchro Qt Made API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Démarrage du backend Flask sur http://127.0.0.1:7555")
    # Pour le développement, utilisez debug=True pour recharger automatiquement
    # et voir les erreurs directement. Pour la production, utilisez un serveur WSGI comme Gunicorn.
    # Pour voir les messages DEBUG, il faudrait changer le niveau de logging ici à logging.DEBUG
    # Par exemple: logging.basicConfig(level=logging.DEBUG, ...)
    app.run(debug=True, port=7555)

