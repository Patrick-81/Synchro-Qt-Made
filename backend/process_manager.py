# Fichier: Synchro_qt_made/backend/process_manager.py
# Version du code dans cette conversation: 1.5
# Date: 2025-05-19
# Description: Gère le démarrage, l'arrêt et le suivi des processus de synchronisation.

import threading
import time
import logging
from pathlib import Path # Potentiellement utile si le ProcessManager gère des fichiers (logs de tâches, etc.)

# Vous aurez besoin d'importer SyncEngine et ConfigManager si ProcessManager les utilise directement
# from .sync_engine import SyncEngine # Exemple d'import relatif si SyncEngine est dans le même package
# from .config_manager import ConfigManager # Exemple d'import relatif si ConfigManager est dans le même package

# Dans notre structure actuelle, api.py importe déjà ces classes
# et les passe à ProcessManager. Il n'est donc pas nécessaire de les importer ici
# SAUF si ProcessManager a besoin d'importer D'AUTRES choses que celles passées à __init__

class ProcessManager:
    # CORRECTION : La méthode __init__ accepte maintenant le logger en plus des autres arguments
    def __init__(self, config_manager, sync_engine_class, logger):
        """
        Initialise le ProcessManager.

        Args:
            config_manager: Une instance de ConfigManager pour charger les configurations.
            sync_engine_class: La classe SyncEngine (pas une instance) à utiliser pour créer des tâches.
            logger: L'objet logger à utiliser pour enregistrer les messages.
        """
        self.config_manager = config_manager
        self.sync_engine_class = sync_engine_class # Stocke la CLASSE SyncEngine
        self.logger = logger # Stocker l'objet logger
        self.active_tasks = {} # Dictionnaire pour stocker les tâches en cours (ex: {config_name: {"thread": thread, "engine": sync_engine_instance, "status": "running"}})
        # Un mécanisme de verrouillage peut être nécessaire pour accéder à active_tasks depuis plusieurs threads/requêtes
        # self._lock = threading.Lock()

        self.logger.info("ProcessManager initialisé.")
        # TODO: Implémenter la logique pour gérer le suivi et le nettoyage des tâches

    def start_sync(self, config_name: str):
        """Démarre une tâche de synchronisation pour la configuration donnée."""
        self.logger.info(f"Requête pour démarrer la synchronisation pour : {config_name}")
        # TODO: Ajouter un mécanisme pour vérifier si une tâche pour cette config est déjà en cours
        if config_name in self.active_tasks and self.active_tasks[config_name].get("status") == "running":
             self.logger.warning(f"Synchronisation pour '{config_name}' déjà en cours.")
             return False, f"Synchronisation pour '{config_name}' est déjà en cours."

        try:
            # Charger la configuration en utilisant ConfigManager
            config_data = self.config_manager.load_config(config_name)
            if config_data is None:
                 self.logger.error(f"Configuration '{config_name}' non trouvée pour démarrer la synchro.")
                 return False, f"Configuration '{config_name}' non trouvée."

            # Créer une instance de SyncEngine
            # Le SyncEngine aura probablement besoin de la config et potentiellement du logger
            sync_engine_instance = self.sync_engine_class(config_data, self.logger) # Passe la config et le logger

            # Exécuter la tâche de synchro dans un thread séparé pour ne pas bloquer le serveur API
            # La méthode 'run_sync' doit exister dans SyncEngine et contenir la logique de synchro
            thread = threading.Thread(target=sync_engine_instance.run_sync, args=(config_name,)) # Passe le nom de la config à la méthode run_sync
            thread.start()

            # Stocker l'information sur la tâche démarrée
            self.active_tasks[config_name] = {
                "thread": thread,
                "engine": sync_engine_instance,
                "status": "running",
                "start_time": time.time() # Temps de début
                # Ajouter d'autres infos pertinentes (pid, progression, etc.)
            }

            self.logger.info(f"Synchronisation démarrée pour '{config_name}'.")
            return True, f"Synchronisation pour '{config_name}' démarrée."

        except Exception as e:
            self.logger.error(f"Échec du démarrage de la synchronisation pour '{config_name}': {e}", exc_info=True)
            # Nettoyer l'entrée de la tâche si elle a été partiellement ajoutée
            if config_name in self.active_tasks and self.active_tasks[config_name].get("status") != "running":
                 del self.active_tasks[config_name]
            return False, f"Échec du démarrage de la synchronisation : {e}"


    def stop_sync(self, config_name: str):
        """Arrête une tâche de synchronisation en cours pour la configuration donnée."""
        self.logger.info(f"Requête pour arrêter la synchronisation pour : {config_name}")
        # TODO: Implémenter la logique pour arrêter une tâche en cours
        if config_name in self.active_tasks and self.active_tasks[config_name].get("status") == "running":
            task_info = self.active_tasks[config_name]
            sync_engine_instance = task_info["engine"]
            # Le SyncEngine doit avoir une méthode pour gérer l'arrêt gracieux
            # Ex: sync_engine_instance.stop_sync()
            # En attendant, on peut juste marquer comme "stopping" ou forcer l'arrêt si nécessaire
            self.logger.warning(f"Arrêt simulé de la synchronisation pour '{config_name}'. L'arrêt réel dépend de l'implémentation de SyncEngine.")
            task_info["status"] = "stopping" # Marque la tâche comme en cours d'arrêt
            # Une méthode stop_sync dans SyncEngine est nécessaire pour un arrêt propre
            # thread.join() pourrait être appelé ici si l'arrêt est bloquant ou ailleurs pour attendre la fin
            return True, f"Signal d'arrêt envoyé pour '{config_name}'."
        else:
             self.logger.warning(f"Aucune tâche de synchronisation en cours pour '{config_name}' à arrêter.")
             return False, f"Aucune tâche de synchronisation en cours pour '{config_name}'."

    def list_tasks(self):
        """Liste les tâches de synchronisation en cours ou planifiées."""
        self.logger.info("Requête pour lister les tâches.")
        # TODO: Retourner l'état réel des tâches à partir de self.active_tasks
        # Exemple de données (similaire à l'ébauche de l'API)
        task_list = []
        for config_name, info in self.active_tasks.items():
             # Calculer la durée si la tâche est en cours
             duration = time.time() - info.get("start_time", time.time()) if info.get("status") == "running" else 0
             task_list.append({
                 "config_name": config_name,
                 "status": info.get("status", "Unknown"),
                 "start_time": info.get("start_time"), # Timestamp ou format date/heure
                 "progress": "N/A", # TODO: Obtenir la progression réelle depuis SyncEngine
                 "task_id": id(info["thread"]), # Utilise l'ID du thread comme ID de tâche simple
                 "duration": duration # Ajouter la durée
             })
        self.logger.info(f"Retourne l'état de {len(task_list)} tâche(s).")
        return task_list # Retourne la liste des tâches


    # TODO: Ajouter d'autres méthodes pour gérer le suivi, les logs des tâches individuelles, etc.


# Exemple d'utilisation (peut être retiré pour l'intégration)
if __name__ == "__main__":
    # Pour tester ce module seul, nous avons besoin d'un logger,
    # d'une ébauche de ConfigManager et d'une ébauche de SyncEngine
    logging.basicConfig(level=logging.INFO)
    test_logger = logging.getLogger(__name__)

    # Ébauche simple de ConfigManager pour le test
    class MockConfigManager:
        def __init__(self, logger):
             self.logger = logger
             self.logger.info("MockConfigManager initialisé.")
        def load_config(self, config_name):
             self.logger.info(f"MockConfigManager charge la config '{config_name}'.")
             # Retourne des données de config minimales
             return {"name": config_name, "source": "/tmp/src", "destination": "/tmp/dest"}

    # Ébauche simple de SyncEngine
    class MockSyncEngine:
        def __init__(self, config_data, logger):
             self.config = config_data
             self.logger = logger
             self._stop_requested = False
             self.logger.info(f"MockSyncEngine initialisé pour config '{self.config.get('name')}'.")

        def run_sync(self, config_name):
             self.logger.info(f"MockSyncEngine lance la synchro pour '{config_name}'.")
             # Simulation d'un travail long
             for i in range(5):
                 if self._stop_requested:
                     self.logger.warning(f"Arrêt de la synchro pour '{config_name}' demandé.")
                     break
                 self.logger.info(f"Synchro pour '{config_name}' - Étape {i+1}/5...")
                 time.sleep(1)
             self.logger.info(f"MockSyncEngine termine la synchro pour '{config_name}'.")

        def stop_sync(self):
             self.logger.info("Signal d'arrêt reçu dans MockSyncEngine.")
             self._stop_requested = True


    mock_config_manager = MockConfigManager(test_logger)
    # Passe la classe MockSyncEngine
    process_manager = ProcessManager(mock_config_manager, MockSyncEngine, test_logger)

    # Exemple: Démarrer une tâche
    print("\nDémarrage d'une tâche...")
    success, message = process_manager.start_sync("TestConfig1")
    print(f"Résultat Start: {success}, {message}")

    # Attendre un peu et lister les tâches
    time.sleep(2)
    print("\nListing tasks...")
    tasks = process_manager.list_tasks()
    print(f"Tasks: {tasks}")

    # Exemple: Arrêter la tâche (simulé)
    print("\nArrêt de la tâche...")
    success, message = process_manager.stop_sync("TestConfig1")
    print(f"Résultat Stop: {success}, {message}")

    # Attendre que le thread de la tâche se termine (si l'arrêt est implémenté)
    # if "TestConfig1" in process_manager.active_tasks:
    #      process_manager.active_tasks["TestConfig1"]["thread"].join()

    print("\nListing tasks after stop...")
    tasks = process_manager.list_tasks()
    print(f"Tasks: {tasks}")
