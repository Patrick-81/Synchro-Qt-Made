# Fichier : sync_engine.py
# Description : Script de synchronisation de fichiers et répertoires.
#
# Historique des versions :
#
# Version 1.2 (2025-05-20)
#    - Ajout de compteurs pour les statistiques de synchronisation (répertoires/fichiers ajoutés/modifiés).
#    - Implémentation du calcul et de l'écriture de la progression dans le fichier de log.
#    - Écriture d'une synthèse détaillée des opérations à la fin de la synchronisation dans le log.
#    - Ces informations sont formatées pour être lues par le backend (api.py).
#
# Version 1.1 (2025-05-20)
#    - Import du module 'time' pour obtenir le timestamp.
#    - Correction de la NameError.
#
# Version 1.0 (2025-05-20)
#    - Version initiale du script.
#    - Synchronisation unidirectionnelle de fichiers et répertoires.
#    - Gestion des exclusions (fichiers et répertoires).
#    - Journalisation des opérations.
#    - Gestion des erreurs et des cas limites.
#
############################################################################################################

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
import sys
import filecmp
import time # Import the time module


def create_logger(config_name, log_file_path):
    """
    Crée un logger pour enregistrer les opérations de synchronisation.

    Args:
        config_name (str): Le nom de la configuration de synchronisation.
        log_file_path (Path): Le chemin complet du fichier de log.

    Returns:
        logging.Logger: Le logger configuré.
    """
    logger = logging.getLogger(config_name)
    logger.setLevel(logging.INFO)  # Définir le niveau de logging

    # Créer le dossier de logs s'il n'existe pas
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Créer un handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler(str(log_file_path), encoding='utf-8')
    file_handler.setLevel(logging.INFO)  # Définir le niveau du handler

    # Créer un handler pour afficher les logs dans la console
    console_handler = logging.StreamHandler(sys.stdout) # Utilisez sys.stdout pour éviter les problèmes d'encodage
    console_handler.setLevel(logging.INFO)  # Définir le niveau du handler

    # Créer un formatter pour les logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Ajouter les handlers au logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class SyncEngine:
    """
    Classe principale pour la synchronisation de fichiers et répertoires.
    """
    def __init__(self, source, destination, frequency_hours, blacklist_files, blacklist_dirs, config_name, log_file_path):
        """
        Initialise le moteur de synchronisation.

        Args:
            source (str): Chemin du répertoire source.
            destination (str): Chemin du répertoire de destination.
            frequency_hours (int): Fréquence de synchronisation en heures.
            blacklist_files (list): Liste des noms de fichiers à exclure.
            blacklist_dirs (list): Liste des noms de répertoires à exclure.
            config_name (str): Nom de la configuration (pour le logger).
            log_file_path (Path): Chemin du fichier de log.
        """
        self.source = Path(source).resolve()
        self.destination = Path(destination).resolve()
        self.frequency_hours = frequency_hours
        self.blacklist_files = blacklist_files
        self.blacklist_dirs = blacklist_dirs
        self.config_name = config_name
        self.logger = create_logger(config_name, log_file_path) # Utiliser le chemin direct
        self.cache_dir = self.destination / ".cache"  # Répertoire cache pour les versions précédentes
        self.logger.info(f"SyncEngine initialisé pour config: '{config_name}'")

        # Statistiques de synchronisation
        self.dirs_added = 0
        self.files_added = 0
        self.files_modified = 0
        self.files_deleted = 0 # Pourrait être ajouté si la suppression est suivie
        self.dirs_deleted = 0 # Pourrait être ajouté si la suppression est suivie

        # Pour la progression
        self.total_files_to_process = 0
        self.processed_files_count = 0
        self.last_progress_report = -1 # Pour éviter de loguer la progression trop souvent

    def _verify_paths(self):
        """
        Vérifie que les répertoires source et de destination existent.
        Crée le répertoire de destination et le répertoire cache si nécessaire.
        """
        if not self.source.is_dir():
            raise NotADirectoryError(f"Le répertoire source n'existe pas : {self.source}")
        if not self.destination.is_dir():
            self.logger.info(f"Le répertoire de destination n'existe pas. Création : {self.destination}")
            self.destination.mkdir(parents=True, exist_ok=True)
            self.dirs_added += 1 # Compter le répertoire de destination comme ajouté
        self.cache_dir.mkdir(parents=True, exist_ok=True) # Créer le répertoire cache

    def _is_excluded_file(self, file_path):
        """
        Vérifie si un fichier doit être exclu de la synchronisation.

        Args:
            file_path (Path): Chemin du fichier à vérifier.

        Returns:
            bool: True si le fichier doit être exclu, False sinon.
        """
        return file_path.name in self.blacklist_files

    def _is_excluded_dir(self, dir_path):
        """
        Vérifie si un répertoire doit être exclu de la synchronisation.

        Args:
            dir_path (Path): Chemin du répertoire à vérifier.

        Returns:
            bool: True si le répertoire doit être exclu, False sinon.
        """
        # Exclure par le nom de base du répertoire
        if dir_path.name in self.blacklist_dirs:
            return True
        return False

    def _copy_file_and_version(self, src_file_path, dest_file_path):
        """
        Copie un fichier de la source vers la destination.
        Si le fichier existe déjà dans la destination, il est versionné.

        Args:
            src_file_path (Path): Chemin du fichier source.
            dest_file_path (Path): Chemin du fichier de destination.
        """
        file_action = "copié/mis à jour" # Default action
        if dest_file_path.exists():
            # Comparer les fichiers pour voir s'ils sont différents
            if not filecmp.cmp(src_file_path, dest_file_path, shallow=False):
                # Le fichier de destination existe et est différent du fichier source
                self.logger.info(f"Fichier modifié : {src_file_path}. Versionnement de l'ancienne version.")
                timestamp = int(time.time()) # Get timestamp
                versioned_path = self.cache_dir / f"{dest_file_path.name}.{timestamp}"
                try:
                    shutil.copy2(dest_file_path, versioned_path)
                    self.logger.info(f"Ancienne version sauvegardée : {dest_file_path} -> {versioned_path}")
                    self.files_modified += 1 # Incrémenter le compteur de fichiers modifiés
                    file_action = "modifié"
                except Exception as e:
                    self.logger.error(f"Erreur lors du versionnement du fichier : {e}")
                    raise  # Relaisser l'exception pour être gérée plus haut
            else:
                # Fichier identique, pas besoin de copier ou versionner
                self.logger.info(f"Fichier identique, ignoré : {src_file_path}")
                self.processed_files_count += 1 # Compter quand même comme traité pour la progression
                self._report_progress()
                return # Sortir si le fichier est identique
        else:
            self.files_added += 1 # Incrémenter le compteur de fichiers ajoutés

        try:
            shutil.copy2(src_file_path, dest_file_path)
            self.logger.info(f"Fichier {file_action} : {src_file_path} -> {dest_file_path}")
            self.processed_files_count += 1
            self._report_progress()
        except Exception as e:
            self.logger.error(f"Erreur lors de la copie du fichier : {e}")
            raise  # Relaisser l'exception pour être gérée plus haut

    def _sync_directory(self, src_dir, dest_dir):
        """
        Synchronise un répertoire de la source vers la destination.
        Gère la création de répertoires, la copie de fichiers et la suppression des fichiers obsolètes.

        Args:
            src_dir (Path): Chemin du répertoire source.
            dest_dir (Path): Chemin du répertoire de destination.
        """
        if self._is_excluded_dir(src_dir):
            self.logger.info(f"Répertoire exclu : {src_dir}")
            return

        # Créer le répertoire de destination s'il n'existe pas
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
            self.dirs_added += 1 # Compter le répertoire comme ajouté
            self.logger.info(f"Répertoire créé : {dest_dir}")


        # Parcourir les fichiers et répertoires dans le répertoire source
        for entry in os.scandir(src_dir):
            src_path = Path(entry.path)
            dest_path = dest_dir / entry.name

            if entry.is_file():
                if not self._is_excluded_file(src_path):
                    self._copy_file_and_version(src_path, dest_path)
                else:
                    self.logger.info(f"Fichier exclu : {src_path}")
            elif entry.is_dir():
                self._sync_directory(src_path, dest_path) # Appel récursif
            else:
                self.logger.warning(f"Entrée ignorée (ni fichier ni répertoire) : {src_path}")

    def _cleanup_obsolete(self, dest_dir, source_files, source_dirs):
        """
        Supprime les fichiers et répertoires obsolètes dans le répertoire de destination.
        Un fichier/répertoire est considéré comme obsolète s'il n'existe pas dans la source.

        Args:
            dest_dir (Path): Chemin du répertoire de destination.
            source_files (set): Ensemble des chemins absolus des fichiers source dans la destination.
            source_dirs (set): Ensemble des chemins absolus des répertoires source dans la destination.
        """
        self.logger.info(f"Démarrage de la phase de suppression des obsolètes pour '{self.config_name}'.")
        for entry in os.scandir(dest_dir):
            dest_path = Path(entry.path)
            
            # Ne pas supprimer le répertoire cache
            if dest_path == self.cache_dir:
                continue

            # Construire le chemin source correspondant pour la comparaison
            # Si dest_path est /dest/subdir/file.txt, source_path_expected est /source/subdir/file.txt
            relative_path_from_dest = dest_path.relative_to(self.destination)
            expected_source_path = self.source / relative_path_from_dest

            # Vérifier si l'entrée de destination correspond à un fichier ou répertoire dans la source
            is_in_source_files = expected_source_path in source_files
            is_in_source_dirs = expected_source_path in source_dirs

            if not is_in_source_files and not is_in_source_dirs:
                # Si l'entrée n'est ni un fichier ni un répertoire attendu dans la source, elle est obsolète
                if entry.is_file():
                    try:
                        os.remove(dest_path)
                        self.logger.info(f"Fichier obsolète supprimé : {dest_path}")
                        self.files_deleted += 1
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la suppression du fichier obsolète : {e}")
                elif entry.is_dir():
                    try:
                        shutil.rmtree(dest_path)
                        self.logger.info(f"Répertoire obsolète supprimé : {dest_path}")
                        self.dirs_deleted += 1
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la suppression du répertoire obsolète : {e}")
                else:
                    self.logger.warning(f"Entrée ignorée lors de la suppression (ni fichier ni répertoire): {dest_path}")
            elif entry.is_dir(): # Si c'est un répertoire et qu'il est dans la source, on le parcourt récursivement
                self._cleanup_obsolete(dest_path, source_files, source_dirs)


    def _count_total_files(self, directory):
        """
        Compte le nombre total de fichiers à traiter dans le répertoire source,
        en respectant la blacklist.
        """
        count = 0
        for entry in os.scandir(directory):
            entry_path = Path(entry.path)
            if entry.is_file() and not self._is_excluded_file(entry_path):
                count += 1
            elif entry.is_dir() and not self._is_excluded_dir(entry_path):
                count += self._count_total_files(entry_path)
        return count

    def _report_progress(self):
        """
        Rapporte la progression de la synchronisation si un seuil est atteint.
        """
        if self.total_files_to_process == 0:
            current_progress = 0
        else:
            current_progress = int((self.processed_files_count / self.total_files_to_process) * 100)
        
        # Rapporter la progression seulement si elle a changé de 5% ou plus, ou si c'est 0% ou 100%
        if current_progress % 5 == 0 or current_progress == 0 or current_progress == 100:
            if current_progress != self.last_progress_report:
                self.logger.info(f"Progression: {current_progress}%")
                self.last_progress_report = current_progress


    def run_sync(self):
        """
        Effectue la synchronisation des fichiers et répertoires.
        """
        self.logger.info(f"Démarrage de la synchronisation pour la configuration : '{self.config_name}'")
        sync_start_time = time.time() # Pour calculer la durée totale

        try:
            self._verify_paths()
        except Exception as e:
            self.logger.error(f"Erreur de vérification des chemins : {e}")
            self.logger.info(f"Synchronisation terminée avec des erreurs.")
            return  # Arrêter la synchronisation si les chemins sont invalides

        # Réinitialiser les compteurs pour cette exécution
        self.dirs_added = 0
        self.files_added = 0
        self.files_modified = 0
        self.files_deleted = 0
        self.dirs_deleted = 0
        self.processed_files_count = 0
        self.last_progress_report = -1 # Réinitialiser le dernier rapport de progression

        # Pré-calculer le nombre total de fichiers pour la progression
        self.total_files_to_process = self._count_total_files(self.source)
        self.logger.info(f"Total des fichiers à traiter : {self.total_files_to_process}")

        # Phase de copie/mise à jour
        self._sync_directory(self.source, self.destination)
        self.logger.info(f"Phase de copie/mise à jour terminée pour '{self.config_name}'.")

        # Collecter tous les fichiers et répertoires de la source (pour la suppression des obsolètes)
        source_files_abs = set()
        source_dirs_abs = set()

        def collect_source_paths(directory):
            for entry in os.scandir(directory):
                entry_path = Path(entry.path)
                if entry.is_file() and not self._is_excluded_file(entry_path):
                    source_files_abs.add(entry_path)
                elif entry.is_dir() and not self._is_excluded_dir(entry_path):
                    source_dirs_abs.add(entry_path)
                    collect_source_paths(entry_path)

        collect_source_paths(self.source)

        # Phase de suppression des obsolètes
        self._cleanup_obsolete(self.destination, source_files_abs, source_dirs_abs)
        
        sync_end_time = time.time()
        duration_sec = int(sync_end_time - sync_start_time)

        self.logger.info(f"Synchronisation pour '{self.config_name}' terminée avec succès.")
        
        # --- SYNTHÈSE FINALE POUR LE BACKEND ---
        self.logger.info("\nSynthèse de l'opération :")
        self.logger.info(f"  Durée totale: {duration_sec} secondes")
        self.logger.info(f"  Répertoires ajoutés: {self.dirs_added}")
        self.logger.info(f"  Fichiers ajoutés: {self.files_added}")
        self.logger.info(f"  Répertoires modifiés: 0") # Non suivi directement par ce script, mais peut être 0
        self.logger.info(f"  Fichiers modifiés: {self.files_modified}")
        self.logger.info(f"  Répertoires supprimés: {self.dirs_deleted}")
        self.logger.info(f"  Fichiers supprimés: {self.files_deleted}")
        self.logger.info(f"  Total des fichiers traités: {self.processed_files_count}") # Inclut copiés, modifiés, identiques
        # ------------------------------------

    def get_sync_stats(self):
        """
        Retourne les statistiques de la dernière synchronisation.
        Utilisé par le backend pour récupérer les données.
        """
        return {
            "dirs_added": self.dirs_added,
            "files_added": self.files_added,
            # Note: Le script ne suit pas directement les répertoires modifiés.
            # On peut laisser à 0 ou adapter si la logique de modification de répertoire est ajoutée.
            "dirs_modified": 0, 
            "files_modified": self.files_modified,
            "files_deleted": self.files_deleted,
            "dirs_deleted": self.dirs_deleted,
            "total_processed_files": self.processed_files_count
        }


def main(source, destination, frequency_hours, blacklist_files, blacklist_dirs, config_name, log_file):
    """
    Fonction principale pour lancer la synchronisation.

    Args:
        source (str): Chemin du répertoire source.
        destination (str): Chemin du répertoire de destination.
        frequency_hours (int): Fréquence de synchronisation en heures.
        blacklist_files (str): Chaîne des fichiers exclus, séparés par ';'.
        blacklist_dirs (str): Chaîne des répertoires exclus, séparés par ';'.
        config_name (str): Le nom de la configuration.
        log_file (str): Le chemin du fichier de log.
    """
    # Convertir les chaînes blacklist en listes
    blacklist_files_list = blacklist_files.split(';') if blacklist_files else []
    blacklist_dirs_list = blacklist_dirs.split(';') if blacklist_dirs else []
    log_file_path = Path(log_file)

    engine = SyncEngine(source, destination, frequency_hours, blacklist_files_list, blacklist_dirs_list, config_name, log_file_path)
    try:
        engine.run_sync()
    except Exception as e:
        engine.logger.critical(f"Erreur fatale lors de la synchronisation pour '{config_name}': {e}")
        engine.logger.exception(e) # Ceci ajoute le traceback complet au log
        # IMPORTANT: Ne pas print de message non formaté ici qui pourrait casser le parsing du backend.
        # Le backend lit le log du script, pas sa sortie standard directe pour les erreurs.
        # Le `logger.exception(e)` est suffisant.
    finally:
        logging.shutdown() #important


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Synchronise des fichiers et répertoires.")
    parser.add_argument("--source", required=True, help="Chemin du répertoire source.")
    parser.add_argument("--destination", required=True, help="Chemin du répertoire de destination.")
    parser.add_argument("--frequency", type=int, required=True, help="Fréquence de synchronisation en heures.")
    parser.add_argument("--blacklist-files", default="", help="Fichiers à exclure (séparés par ';').")
    parser.add_argument("--blacklist-dirs", default="", help="Répertoires à exclure (séparés par ';').")
    parser.add_argument("--log-file", required=True, help="Chemin du fichier de log.")
    parser.add_argument("--config-name", required=True, help="Nom de la configuration.")

    args = parser.parse_args()

    main(args.source, args.destination, args.frequency, args.blacklist_files, args.blacklist_dirs, args.config_name, args.log_file)

