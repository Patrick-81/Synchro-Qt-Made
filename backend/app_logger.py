# Fichier: Synchro_qt_made/backend/app_logger.py
# Version du code dans cette conversation: 1.3
# Date: 2025-05-19
# Description: Configuration du système de logging pour l'application backend.

import logging
import logging.handlers
import os
import sys
from pathlib import Path

# Chemin du répertoire de logs (doit correspondre à celui utilisé dans api.py)
# Assurez-vous que BASE_DIR est défini comme dans api.py si vous le réutilisez
BASE_DIR = Path.home() / ".synchro"
LOG_DIR = BASE_DIR / "logs"

# Assurez-vous que le répertoire de logs existe
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Chemin du fichier de log principal
DEFAULT_LOG_FILE = LOG_DIR / "app.log" # Nom du fichier log


def setup_logging(log_file_path=DEFAULT_LOG_FILE, level=logging.INFO):
    """
    Configure le système de logging de l'application.
    Crée un logger racine ou spécifié, ajoute des handlers et un formateur.
    """
    # Utiliser le logger racine ou un logger spécifique si nécessaire
    # Pour une application simple, configurer le logger racine est souvent suffisant.
    root_logger = logging.getLogger() # Configure le logger racine
    # root_logger = logging.getLogger("SyncApp") # Alternative : configurer un logger nommé

    root_logger.setLevel(level) # Définir le niveau de log minimum

    # Nettoyer les handlers existants pour éviter la duplication si appelé plusieurs fois
    if root_logger.hasHandlers():
        # Créer une copie de la liste des handlers pour pouvoir la modifier pendant l'itération
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
            handler.close() # Fermer le handler pour libérer les ressources


    # Formateur pour les messages de log
    # Inclut le temps, le nom du logger, le niveau, et le message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler pour écrire les logs dans un fichier (avec rotation)
    # Rotation des logs : crée un nouveau fichier après une certaine taille/intervalle
    # Exemple: rotation quotidienne, garde 5 fichiers de backup
    try:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file_path,
            when='midnight', # Rotation à minuit
            interval=1,      # Tous les jours
            backupCount=5,   # Garde 5 fichiers précédents
            encoding='utf-8' # Gérer l'encodage
        )
        file_handler.setLevel(level) # Définir le niveau pour ce handler
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        # Log informatif sur le handler fichier
        # Note: Ce log pourrait ne pas apparaître si le handler console n'est pas encore ajouté
        # logging.getLogger(__name__).info(f"File logging configured to {log_file_path}")

    except Exception as e:
        # Gérer l'erreur si le handler fichier ne peut pas être créé (ex: permissions)
        root_logger.error(f"Erreur lors de la création du file handler pour le logging: {e}")


    # Handler pour afficher les logs dans la console (stdout)
    # Utile pendant le développement
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level) # Définir le niveau pour ce handler
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Optionnel: Supprimer la propagation au logger parent (pour éviter double logs si configuré ailleurs)
    # root_logger.propagate = False

    # Log de confirmation (apparaîtra dans la console et le fichier si configuration réussie)
    root_logger.info(f"Logging configuré. Log file: {log_file_path}")


# CORRECTION : Ajouter un argument 'name' à la fonction get_logger
def get_logger(name):
    """
    Retourne une instance de logger configurée pour un nom donné.
    Utilisez __name__ comme argument pour le nom du logger dans vos modules.
    """
    # Retourne un logger spécifique, qui hérite de la configuration du logger racine
    return logging.getLogger(name)


# Exemple d'utilisation (peut être retiré pour l'intégration)
if __name__ == "__main__":
    # Configure le logging pour ce script d'exemple
    setup_logging()
    # Obtient un logger pour le script d'exemple
    example_logger = get_logger(__name__)
    example_logger.info("Ceci est un message d'information de l'exemple d'app_logger.py.")
    example_logger.warning("Ceci est un avertissement de l'exemple.")
    example_logger.error("Ceci est une erreur de l'exemple.")
