# Fichier: Synchro_qt_made/backend/config_manager.py
# Version du code dans cette conversation: 1.1
# Date: 2025-05-19
# Description: Gestionnaire des configurations de synchronisation.

import json
import os
from pathlib import Path
# Importez le logger si la classe l'utilise directement, ou faites confiance à celui passé dans __init__
# import logging # Si vous avez besoin du module logging ici

class ConfigManager:
    # CORRECTION : La méthode __init__ accepte maintenant le chemin du répertoire ET l'objet logger
    def __init__(self, config_dir_path: Path, logger):
        """
        Initialise le ConfigManager.

        Args:
            config_dir_path: Le chemin du répertoire où les fichiers de configuration sont stockés.
            logger: L'objet logger à utiliser pour enregistrer les messages.
        """
        self.config_dir = config_dir_path
        self.logger = logger # Stocker l'objet logger en tant qu'attribut

        # S'assurer que le répertoire de configuration existe
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"ConfigManager initialisé. Répertoire de configs: {self.config_dir}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du répertoire de configs {self.config_dir}: {e}")
            # Optionnel: lever une exception ou gérer l'erreur de manière plus robuste

    def _get_config_path(self, config_name: str) -> Path:
        """Retourne le chemin complet du fichier de configuration pour un nom donné."""
        # Assurez-vous que le nom est propre pour éviter les problèmes de chemin
        # On peut ajouter une validation ou un nettoyage du nom ici
        cleaned_name = "".join(c for c in config_name if c.isalnum() or c in ('_', '-')).rstrip()
        if not cleaned_name:
             cleaned_name = "default_config" # Nom par défaut si le nom est vide ou invalide
             self.logger.warning(f"Nom de configuration invalide ou vide fourni, utilisation de '{cleaned_name}'.")


        return self.config_dir / f"{cleaned_name}.json"

    def list_configs(self) -> list[str]:
        """Liste les noms de toutes les configurations disponibles (fichiers .json)."""
        self.logger.info(f"Liste des configurations dans {self.config_dir}...")
        configs = []
        try:
            if not self.config_dir.exists():
                self.logger.warning(f"Répertoire de configuration non trouvé pour liste : {self.config_dir}")
                return [] # Retourne une liste vide si le répertoire n'existe pas (devrait pas arriver avec mkdir)

            for item in self.config_dir.iterdir():
                if item.is_file() and item.suffix == ".json":
                    configs.append(item.stem) # .stem donne le nom du fichier sans l'extension
            self.logger.info(f"Configurations trouvées : {configs}")
            return configs
        except Exception as e:
             self.logger.error(f"Erreur lors de la liste des fichiers de configuration dans {self.config_dir}: {e}", exc_info=True)
             return [] # Retourne une liste vide en cas d'erreur


    def load_config(self, config_name: str) -> dict | None:
        """Charge une configuration spécifique par son nom."""
        config_file_path = self._get_config_path(config_name)
        self.logger.info(f"Chargement de la configuration depuis {config_file_path}...")
        if not config_file_path.exists():
            self.logger.warning(f"Fichier de configuration non trouvé : {config_file_path}")
            return None # Retourne None si le fichier n'existe pas

        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self.logger.info(f"Configuration '{config_name}' chargée avec succès.")
                return config_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur de décodage JSON lors du chargement de {config_file_path}: {e}", exc_info=True)
            return None # Retourne None en cas d'erreur JSON
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la configuration {config_file_path}: {e}", exc_info=True)
            return None # Retourne None en cas d'autre erreur


    def save_config(self, config_name: str, config_data: dict) -> bool:
        """Sauvegarde une configuration dans un fichier JSON."""
        config_file_path = self._get_config_path(config_name)
        self.logger.info(f"Sauvegarde de la configuration '{config_name}' vers {config_file_path}...")

        # TODO: Ajouter une validation basique de config_data ici avant de sauvegarder

        try:
            with open(config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4) # Indentation pour une meilleure lisibilité
            self.logger.info(f"Configuration '{config_name}' sauvegardée avec succès.")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la configuration {config_file_path}: {e}", exc_info=True)
            return False # Retourne False en cas d'échec


    def delete_config(self, config_name: str) -> bool:
        """Supprime un fichier de configuration."""
        config_file_path = self._get_config_path(config_name)
        self.logger.info(f"Suppression de la configuration '{config_name}' à {config_file_path}...")

        if not config_file_path.exists():
            self.logger.warning(f"Tentative de suppression de configuration non trouvée : {config_file_path}")
            return False # Retourne False si le fichier n'existe pas (déjà supprimé ou n'a jamais existé)

        try:
            config_file_path.unlink() # Supprime le fichier
            self.logger.info(f"Configuration '{config_name}' supprimée avec succès.")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression de la configuration {config_file_path}: {e}", exc_info=True)
            return False # Retourne False en cas d'échec


# Exemple d'utilisation (peut être retiré)
if __name__ == "__main__":
     # Pour tester ce module seul, nous avons besoin d'un logger
     # et de créer un répertoire temporaire pour les configs
     logging.basicConfig(level=logging.INFO) # Configuration basique pour le test
     test_logger = logging.getLogger(__name__)
     test_config_dir = Path("./test_configs")
     test_config_dir.mkdir(exist_ok=True)

     test_manager = ConfigManager(test_config_dir, test_logger)

     # Exemple: Créer une config
     test_config_data = {
         "name": "TestConfig1",
         "source": "/path/to/source",
         "destination": "/path/to/dest",
         "frequency": 1.0,
         "blacklist_files": ".tmp;.bak",
         "blacklist_dirs": "cache;temp"
     }
     test_manager.save_config(test_config_data["name"], test_config_data)

     # Exemple: Lister les configs
     test_manager.list_configs()

     # Exemple: Charger une config
     loaded_config = test_manager.load_config("TestConfig1")
     print(f"Loaded config: {loaded_config}")

     # Exemple: Supprimer une config
     test_manager.delete_config("TestConfig1")
     test_manager.list_configs() # Vérifier qu'elle est supprimée

     # Nettoyer le répertoire de test
     # os.rmdir(test_config_dir) # Supprime le répertoire s'il est vide
