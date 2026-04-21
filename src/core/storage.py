import json
from pathlib import Path

class Storage:
    """
    Couche d'accès aux données (Data Access Layer).
    Gère la persistance (lecture et écriture) des données de l'application au format JSON.
    Conçue pour être tolérante aux pannes (fichiers ou dossiers manquants, données corrompues).
    """
    def __init__(self):
        # Calcul du chemin absolu robuste vers la racine du projet
        # __file__ correspond à src/core/storage.py
        # resolve().parent.parent.parent permet de remonter de 3 niveaux (vers Gym-Manager-Pro)
        base_dir = Path(__file__).resolve().parent.parent.parent 
        
        self.dossier_data = base_dir / "data"
        self.fichier = self.dossier_data / "input.json"

    def load(self):
        """
        Charge les données depuis le fichier JSON.
        Retourne une liste vide de manière sécurisée si le fichier est introuvable ou illisible.
        """
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except FileNotFoundError:
            # Comportement attendu au premier lancement (le fichier n'a pas encore été créé)
            # Permet à la logique (logic.py) de démarrer avec une base vierge.
            return []
            
        except json.JSONDecodeError:
            # Sécurité : Si un utilisateur modifie le JSON à la main et crée une erreur de syntaxe,
            # on évite le crash de l'application en réinitialisant la lecture.
            return []

    def save(self, data):
        """
        Sauvegarde la liste des dictionnaires dans le fichier JSON.
        Génère automatiquement l'arborescence si elle est manquante.
        """
        # Sécurité : Si le dossier 'data' a été supprimé par l'utilisateur, on le recrée silencieusement.
        self.dossier_data.mkdir(exist_ok=True)
        
        # Le paramètre ensure_ascii=False garantit la préservation des accents (é, à, etc.)
        # Le paramètre indent=4 rend le fichier JSON lisible par un humain.
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)