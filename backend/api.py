# Fichier: Synchro_backend/api.py
#
# Historique des versions:
#
# Version 3.31 (Révision 4 - 2025-05-21):
#   - Assure que tous les messages de log du backend sont en anglais pour une meilleure cohérence
#     des journaux techniques.
#   - Mise à jour du commentaire de versionnage.
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
#     are correctly collected by the SyncTask class and returned by the /api/sync_tasks API.
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
import time # For duration
import re # Import re module for regular expressions
from PyQt5.QtCore import QTimer # Import QTimer for log cleanup

# Global path configuration for the backend
APP_DIR = Path.home() / ".synchro"
CONFIGS_DIR = APP_DIR / "configs"
LOGS_DIR = APP_DIR / "logs"
APP_LOG_FILE = LOGS_DIR / "backend_app.log" # Renamed to clarify it's the backend log
TASK_LOG_DIR = LOGS_DIR / "tasks"

# Ensure directories exist
for d in [APP_DIR, CONFIGS_DIR, LOGS_DIR, TASK_LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logging configuration for the backend
logging.basicConfig(level=logging.INFO, # INFO level is default
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(APP_LOG_FILE),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Create the blueprint for API routes
api_bp = Blueprint('api', __name__)

# --- Class to represent a synchronization task ---
class SyncTask:
    def __init__(self, config_name, config_data):
        self.config_name = config_name
        self.config_data = config_data
        self.status = "idle"  # idle, running, completed, stopped, error
        self.process = None   # Subprocess
        self.start_time = None
        self.end_time = None
        self.progress = 0     # Progress in percentage
        self.log_file_name = f"{config_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file_path = TASK_LOG_DIR / self.log_file_name

        # Synchronization statistics (initialized to 0 or None)
        self.dirs_added = 0
        self.files_added = 0
        self.dirs_modified = 0
        self.files_modified = 0
        self.dirs_deleted = 0
        self.files_deleted = 0
        
    def start(self):
        # CRITICAL CORRECTION OF SYNC SCRIPT PATH AND NAME
        # The 'sync_engine.py' script is in the same directory as 'api.py'.
        sync_script_path = Path(__file__).parent / "sync_engine.py"
        
        if not sync_script_path.exists():
            logger.error(f"ERROR: Sync script not found at: {sync_script_path}. Check name and path.")
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False

        try:
            # Prepare arguments for the synchronization script
            # Convert lists to semicolon-separated strings
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
                "--log-file", str(self.log_file_path), # Pass log path to script
                "--config-name", self.config_name, # Pass config name for script's internal logging
                "--max-cached-versions", str(self.config_data.get('max_cached_versions', 2)) # Pass new parameter
            ]
            
            # Open log file in write mode for the script
            # Use Popen with PIPE for stderr to capture script startup errors
            # and redirect stdout to the log file.
            with open(self.log_file_path, 'w', encoding='utf-8') as f_log:
                self.process = subprocess.Popen(cmd, stdout=f_log, stderr=subprocess.PIPE, text=True, bufsize=1)
            
            # Check if the process started correctly
            time.sleep(0.1) # Give the process a very short time to start or fail
            if self.process.poll() is not None:
                # The process has already terminated, indicating a startup failure
                stderr_output = self.process.stderr.read()
                logger.error(f"TASK STARTUP FAILED for '{self.config_name}': Script terminated immediately. Exit code: {self.process.returncode}. Standard Error: \n{stderr_output}")
                self.status = "error"
                self.end_time = datetime.datetime.now()
                return False
            
            self.status = "running"
            self.start_time = datetime.datetime.now()
            self.progress = 0
            logger.info(f"Task '{self.config_name}' started. PID: {self.process.pid}. Log: {self.log_file_path}")
            return True
        except FileNotFoundError:
            logger.error(f"ERROR: Command 'python' or '{sync_script_path}' not found. Check your PATH or script path.")
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False
        except Exception as e:
            logger.error(f"Unexpected error starting task '{self.config_name}': {e}", exc_info=True) # exc_info=True for traceback
            self.status = "error"
            self.end_time = datetime.datetime.now()
            return False

    def stop(self):
        if self.process and self.process.poll() is None: # If process is still running
            try:
                # Send termination signal to process (SIGTERM)
                # This allows the script to shut down cleanly if it handles this signal
                self.process.terminate() 
                # Wait a short time for the process to terminate
                self.process.wait(timeout=5) 
                if self.process.poll() is not None:
                    self.status = "stopped"
                    logger.info(f"Task '{self.config_name}' (PID: {self.process.pid}) stopped.")
                else:
                    # If the process did not terminate after terminate, kill it
                    self.process.kill()
                    self.status = "stopped" # or "killed" if you want to distinguish
                    logger.warning(f"Task '{self.config_name}' (PID: {self.process.pid}) killed after terminate failed.")
            except Exception as e:
                logger.error(f"Error stopping task '{self.config_name}': {e}")
                self.status = "error"
            finally:
                self.end_time = datetime.datetime.now()
        elif self.status == "running": # If trying to stop a task already stopped but not cleaned up
             self.status = "stopped"
             self.end_time = datetime.datetime.now()
             logger.info(f"Task '{self.config_name}' already completed or stopped.")

    def update_status_from_log(self):
        """
        Parses the task log file to update its status,
        progress, and synchronization statistics.
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
            
            # --- Parsing progress (last occurrence) ---
            current_progress = 0
            progress_pattern = re.compile(r"Progress:\s*(\d+)%") # Adjusted for English log
            for line in reversed(lines):
                line = line.strip()
                # Extract the message part of the log line (after " - INFO - ")
                # Format is "YYYY-MM-DD HH:MM:SS,ms - LOGGER_NAME - LEVEL - MESSAGE"
                # We want the MESSAGE
                message_match = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                message_part = message_match.group(1) if message_match else line

                match = progress_pattern.search(message_part)
                if match:
                    try:
                        current_progress = int(match.group(1))
                        self.progress = min(100, max(0, current_progress))
                        break # Found last progress, stop searching
                    except ValueError:
                        pass # Ignore malformed progress lines
            
            # --- Parsing summary statistics (specific block) ---
            summary_start_index = -1
            for i, line in enumerate(lines):
                message_match_header = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                message_part_header = message_match_header.group(1) if message_match_header else line
                
                if "Summary of operation :" in message_part_header: # Adjusted for English log
                    summary_start_index = i
                    break

            if summary_start_index != -1:
                # Regex patterns for the statistics (Adjusted for English log)
                dirs_added_pattern = re.compile(r"Directories added:\s*(\d+)")
                files_added_pattern = re.compile(r"Files added:\s*(\d+)")
                dirs_modified_pattern = re.compile(r"Directories modified:\s*(\d+)")
                files_modified_pattern = re.compile(r"Files modified:\s*(\d+)")
                dirs_deleted_pattern = re.compile(r"Directories deleted:\s*(\d+)")
                files_deleted_pattern = re.compile(r"Files deleted:\s*(\d+)")

                # Reset stats before parsing again
                self.dirs_added = 0
                self.files_added = 0
                self.dirs_modified = 0
                self.files_modified = 0
                self.dirs_deleted = 0
                self.files_deleted = 0

                # Read subsequent lines to extract statistics
                for i in range(summary_start_index + 1, len(lines)):
                    line = lines[i].strip()
                    message_match_stats = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - [^ ]+ - INFO - (.*)", line)
                    message_part_stats = message_match_stats.group(1) if message_match_stats else line

                    # Summary lines start with "  " (two spaces)
                    # and are not empty lines or other log levels
                    if not message_part_stats.startswith("  ") or not message_part_stats.strip():
                        break # End of summary block or irrelevant line

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
            
            # Check process status if running
            if self.status == "running":
                poll_result = self.process.poll()
                if poll_result is not None:
                    # Process terminated
                    self.end_time = datetime.datetime.now()
                    if poll_result == 0:
                        self.status = "completed"
                        self.progress = 100 # Ensure bar is 100% at the end
                        logger.info(f"Task '{self.config_name}' completed successfully.")
                    else:
                        self.status = "error"
                        logger.error(f"Task '{self.config_name}' terminated with an error (code: {poll_result}).")
                # If script finishes very quickly, progress may remain at 0.
                # If task is running and progress is 100, set to completed.
                elif self.progress == 100:
                    self.status = "completed" # Script indicated 100% progress, so it's likely finished.
                    self.end_time = datetime.datetime.now()

        except Exception as e:
            logger.error(f"Error reading/updating log for task '{self.config_name}': {e}", exc_info=True)
            # Do not change status to "error" here, as it's a read error, not the task itself.

    def get_duration(self):
        """Calculates task duration in seconds."""
        if self.start_time:
            if self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            else:
                return (datetime.datetime.now() - self.start_time).total_seconds()
        return 0

# --- Task Manager ---
class TaskManager:
    _instance = None # Singleton pattern

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.tasks = {} # Dictionary to store SyncTask objects by config_name
            
            # Initialize timer for log cleanup
            cls._instance.log_cleanup_timer = QTimer()
            cls._instance.log_cleanup_timer.setInterval(24 * 60 * 60 * 1000) # Every 24 hours in ms
            cls._instance.log_cleanup_timer.timeout.connect(cls._instance._perform_log_cleanup)
            cls._instance.log_cleanup_timer.start()
            logger.info("Log cleanup timer started (every 24 hours).")
            # Perform initial cleanup on startup
            cls._instance._perform_log_cleanup() 
        return cls._instance

    def _perform_log_cleanup(self):
        """
        Performs cleanup of old log files in directories managed by the backend.
        """
        logger.info("Starting old log cleanup...")
        max_age_days = 7 # Maximum log lifetime in days

        # Cleanup task logs
        self._clean_directory_logs(TASK_LOG_DIR, max_age_days)
        
        # Cleanup main backend log
        self._clean_single_file_log(APP_LOG_FILE, max_age_days)
        
        logger.info("Log cleanup finished.")

    def _clean_directory_logs(self, directory: Path, max_age_days: int):
        """Cleans log files in a given directory."""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
        
        for log_file in directory.iterdir():
            if log_file.is_file():
                try:
                    file_mod_time = datetime.datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_mod_time < cutoff_time:
                        os.remove(log_file)
                        logger.info(f"Old task log deleted: {log_file}")
                except Exception as e:
                    logger.error(f"Error deleting log {log_file}: {e}")

    def _clean_single_file_log(self, file_path: Path, max_age_days: int):
        """Cleans a single log file by recreating it if it's too old."""
        if file_path.exists():
            cutoff_time = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
            try:
                file_mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mod_time < cutoff_time:
                    # Rather than deleting the file and leaving it empty,
                    # we can clear its content or rename it and create a new one.
                    # For a main log, clearing it is often simpler.
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.truncate(0) # Clears file content
                    logger.info(f"Main backend log content cleared because it was too old: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning main log {file_path}: {e}")

    def get_all_tasks(self):
        # Update status of all tasks before returning them
        for task in list(self.tasks.values()): # Use list() to avoid RuntimeError if a task is deleted
            task.update_status_from_log()
        
        # Clean up "completed", "stopped", or "error" tasks if they have been around for a long time
        # To prevent the list from growing indefinitely. Keep the last 5 completed ones, for example.
        finished_tasks = {name: task for name, task in self.tasks.items() if task.status in ["completed", "stopped", "error"]}
        running_tasks = {name: task for name, task in self.tasks.items() if task.status == "running"}

        # Keep only the last X finished tasks (here, 5) + all running tasks
        if len(finished_tasks) > 5:
            # Sort by end date and keep the most recent ones
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
        # Update status before returning
        if config_name in self.tasks:
            self.tasks[config_name].update_status_from_log()
        return self.tasks.get(config_name)

    def add_task(self, task):
        self.tasks[task.config_name] = task

    def remove_task(self, config_name):
        if config_name in self.tasks:
            del self.tasks[config_name]

# Initialize the task manager
tasks_manager = TaskManager()

# --- API Routes ---

@api_bp.route('/api/configs/<config_name>', methods=['PUT'])
def update_config(config_name):
    """
    Updates or creates a synchronization configuration.
    """
    try:
        config_data = request.json
        if not config_data:
            logger.error("Missing configuration data.")
            return jsonify({"error": "Missing configuration data."}), 400

        # Validate minimal data
        required_fields = ["source", "destination", "frequency_hours"]
        for field in required_fields:
            if field not in config_data:
                logger.error(f"Missing field '{field}' in configuration.")
                return jsonify({"error": f"Missing field '{field}'."}), 400

        # Ensure paths are absolute and valid (backend side)
        source_path = Path(config_data['source'])
        destination_path = Path(config_data['destination'])
        
        if not source_path.exists():
            logger.warning(f"Source path does not exist: {source_path}")
            # return jsonify({"error": f"Source path '{source_path}' does not exist."}), 400
        # Destination may not exist, sync script will create it

        config_path = CONFIGS_DIR / f"{config_name}.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"Configuration '{config_name}' updated/created successfully.")
        return jsonify({"message": f"Configuration '{config_name}' saved successfully."}), 200

    except json.JSONDecodeError:
        logger.error("Invalid JSON request.")
        return jsonify({"error": "Invalid JSON format."}), 400
    except Exception as e:
        logger.error(f"Error updating configuration: {e}", exc_info=True)
        return jsonify({"error": f"Internal server error: {e}"}), 500

@api_bp.route('/api/sync_tasks/start/<config_name>', methods=['POST'])
def start_sync_task(config_name):
    """
    Starts a synchronization task for the given configuration.
    """
    config_path = CONFIGS_DIR / f"{config_name}.json"
    if not config_path.exists():
        logger.warning(f"Attempt to start task without configuration found: {config_name}")
        return jsonify({"error": f"Configuration '{config_name}' not found."}), 404

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        if config_name in tasks_manager.tasks and tasks_manager.tasks[config_name].status == "running":
            logger.info(f"Task '{config_name}' is already running.")
            return jsonify({"message": f"Task '{config_name}' is already running."}), 200

        task = SyncTask(config_name, config_data)
        if task.start():
            tasks_manager.add_task(task)
            return jsonify({"message": f"Task '{config_name}' started successfully.", "pid": task.process.pid}), 202
        else:
            return jsonify({"error": f"Failed to start task '{config_name}'."}), 500
    except Exception as e:
        logger.error(f"Error starting task '{config_name}': {e}", exc_info=True)
        return jsonify({"error": f"Internal server error: {e}"}), 500

@api_bp.route('/api/sync_tasks/stop/<config_name>', methods=['POST'])
def stop_sync_task(config_name):
    """
    Stops a synchronization task.
    """
    task = tasks_manager.get_task(config_name)
    if not task:
        logger.warning(f"Attempt to stop a non-existent task: {config_name}")
        return jsonify({"error": f"Task '{config_name}' not found or already completed."}), 404

    if task.status in ["completed", "stopped", "error"]:
        logger.info(f"Task '{config_name}' already completed or stopped.")
        return jsonify({"message": f"Task '{config_name}' is already completed or stopped."}), 200
    
    task.stop()
    return jsonify({"message": f"Stop signal sent for task '{config_name}'."}), 202

@api_bp.route('/api/sync_tasks', methods=['GET'])
def get_sync_tasks_status():
    """
    Retrieves the status of all active and recent synchronization tasks.
    """
    tasks_data = [] 
    for task in tasks_manager.get_all_tasks(): # get_all_tasks updates status before returning
        task_info = {
            "config_name": task.config_name,
            "status": task.status,
            "progress": task.progress,
            "pid": task.process.pid if task.process else None,
            "duration": int(task.get_duration()), # Ensure this method exists and returns duration in seconds
            "dirs_added": task.dirs_added, 
            "files_added": task.files_added,
            "dirs_modified": task.dirs_modified,
            "files_modified": task.files_modified,
            "log_file_name": task.log_file_name 
        }
        tasks_data.append(task_info)
    
    logger.debug(f"DEBUG BACKEND: API /api/sync_tasks returns : {json.dumps(tasks_data, indent=2)}") 
    
    return jsonify(tasks_data), 200

# --- Main function to launch the Flask application ---
def create_app():
    app = Flask(__name__)
    CORS(app) # Allows frontend to communicate with this backend
    app.register_blueprint(api_bp)
    
    # Add a clear startup message
    @app.route('/')
    def index():
        return "Backend Synchro Qt Made API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting Flask backend on http://127.0.0.1:7555")
    # For development, use debug=True for auto-reloading
    # and direct error viewing. For production, use a WSGI server like Gunicorn.
    # To see DEBUG messages, you would need to change the logging level here to logging.DEBUG
    # For example: logging.basicConfig(level=logging.DEBUG, ...)
    app.run(debug=True, port=7555)

