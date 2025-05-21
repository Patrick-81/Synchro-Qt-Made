# Fichier: Synchro_qt_made/api_client.py
#
# Historique des versions:
#
# Version 1.1 (2025-05-20):
#   - Ajout du bloc d'historique des versions.
#
# Version 1.0 (2025-05-15):
#   - Implémentation initiale de la classe ApiClient pour interagir avec le backend Flask.
#   - Méthodes pour les requêtes GET, POST, PUT, DELETE.
#   - Gestion des erreurs de connexion et des réponses HTTP.
#   - Fonctions spécifiques pour les tâches de synchronisation et la gestion des configurations.
#
# Description Générale du Fichier:
# Ce fichier contient la classe ApiClient, responsable de la communication avec le backend de l'application.
# Il fournit des méthodes pour envoyer des requêtes HTTP aux différentes routes de l'API.
#
############################################################################################################


import requests
import json

class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:7555"):
        self.base_url = base_url

    def _make_request(self, method, endpoint, data=None, params=None):
        """
        Effectue une requête HTTP générique au backend.
        Retourne (data, status_code) en cas de succès, ou ({"error": message}, None) en cas d'échec de connexion.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        try:
            if method == 'GET':
                response = requests.get(url, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(data))
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, data=json.dumps(data))
            else:
                return {"error": "Méthode HTTP non supportée"}, None

            response.raise_for_status()  # Lève une exception pour les codes d'état 4xx/5xx

            # Essayer de décoder le JSON, mais permettre une réponse vide ou non JSON
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return {"message": response.text}, response.status_code # Retourne le texte si pas du JSON
            
        except requests.exceptions.ConnectionError:
            return {"error": "Impossible de se connecter au backend. Assurez-vous que le serveur est lancé."}, None
        except requests.exceptions.Timeout:
            return {"error": "La requête a expiré."}, None
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return error_data, e.response.status_code
            except json.JSONDecodeError:
                return {"error": f"Erreur HTTP: {e.response.text}", "status_code": e.response.status_code}, e.response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": f"Une erreur inattendue est survenue: {e}"}, None

    def get_configs(self):
        return self._make_request('GET', '/api/configs')

    def get_config(self, config_name):
        return self._make_request('GET', f'/api/configs/{config_name}')

    def create_or_update_config(self, config_name, config_data):
        return self._make_request('PUT', f'/api/configs/{config_name}', data=config_data)

    def delete_config(self, config_name):
        return self._make_request('DELETE', f'/api/configs/{config_name}')

    def start_sync_task(self, config_name):
        return self._make_request('POST', f'/api/sync_tasks/start/{config_name}')

    def stop_sync_task(self, config_name):
        return self._make_request('POST', f'/api/sync_tasks/stop/{config_name}')

    def get_sync_tasks(self):
        return self._make_request('GET', '/api/sync_tasks')

    def get_sync_status(self, config_name):
        return self._make_request('GET', f'/api/sync_tasks/{config_name}/status')

    def get_sync_log(self, config_name):
        return self._make_request('GET', f'/api/sync_tasks/{config_name}/log')

    def get_synthesis(self):
        return self._make_request('GET', '/api/synthesis')

    def clear_log(self):
        """Méthode pour demander au backend de vider ses logs (si implémenté)."""
        return self._make_request('POST', '/api/logs/clear')
