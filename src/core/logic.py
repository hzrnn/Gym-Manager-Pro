from datetime import datetime
from pathlib import Path

# Importation de nos propres modules internes
from src.core.models import Membre
from src.core.storage import Storage

class GymLogic:
    """
    La couche 'Contrôleur' de l'application (Architecture MVC). 
    Elle contient toute la logique métier et fait le pont entre les données et l'interface.
    """
    def __init__(self):
        self.storage = Storage()
        self.membres = []
        self._charger_donnees()

    def _charger_donnees(self):
        """Méthode privée : Charge les dictionnaires du JSON et les transforme en objets Membre."""
        donnees_brutes = self.storage.load()
        for data in donnees_brutes:
            # On utilise la méthode de classe (@classmethod) pour une instanciation propre
            nouveau_membre = Membre.from_dict(data)
            self.membres.append(nouveau_membre)

    def sauvegarder(self):
        """Convertit les objets Membre en dictionnaires et déclenche la persistance."""
        # On utilise une compréhension de liste (très performant et élégant en Python)
        donnees_a_sauver = [m.to_dict() for m in self.membres]
        self.storage.save(donnees_a_sauver)

    # ==========================================
    # OPÉRATIONS CRUD (Create, Read, Update, Delete)
    # ==========================================

    def get_tous_les_membres(self):
        """Renvoie la liste complète en mémoire pour l'affichage dans l'interface."""
        return self.membres

    def rechercher_membre(self, nom_recherche):
        """Recherche un membre par son nom exact (insensible à la casse)."""
        nom_cible = nom_recherche.strip().upper()
        for membre in self.membres:
            if membre.nom == nom_cible:
                return membre
        return None

    def ajouter_membre(self, nom, debut, fin, statut="Actif"):
        """
        Logique métier de création : Vérifie les règles (Business Rules) avant d'ajouter.
        """
        # 1. Vérification des doublons
        if self.rechercher_membre(nom):
            raise ValueError(f"Le membre '{nom.upper()}' existe déjà dans la base de données.")

        # 2. Vérification mathématique des dates (Format : JJ-MM-AAAA)
        d_debut = datetime.strptime(debut, "%d-%m-%Y")
        d_fin = datetime.strptime(fin, "%d-%m-%Y")
        
        if d_fin <= d_debut:
            raise ValueError("Erreur de logique : La date de fin doit être après la date de début.")

        # 3. Création sécurisée de l'objet (le setter de models.py fera les ultimes vérifications)
        nouveau = Membre(nom, debut, fin, statut)
        self.membres.append(nouveau)
        self.sauvegarder()

    def supprimer_membre(self, nom):
        """Supprime un membre s'il existe dans le système."""
        membre_a_supprimer = self.rechercher_membre(nom)
        if not membre_a_supprimer:
            raise ValueError(f"Impossible de supprimer : '{nom}' est introuvable.")
        
        # On retire l'objet de la liste et on sauvegarde immédiatement (Persistance)
        self.membres.remove(membre_a_supprimer)
        self.sauvegarder()

    # ==========================================
    # GÉNÉRATION DE RAPPORTS (Exigence du PDF)
    # ==========================================

    def generer_rapport_alertes(self):
        """
        Analyse les dates d'expiration, met à jour les statuts et génère un rapport texte.
        Utilise pathlib pour cibler le dossier output/ de manière robuste.
        """
        # Calcul du chemin absolu vers la racine du projet (3 dossiers plus haut)
        base_dir = Path(__file__).resolve().parent.parent.parent 
        
        # Création robuste du dossier output à la racine
        dossier_output = base_dir / "output"
        dossier_output.mkdir(exist_ok=True)
        chemin_rapport = dossier_output / "rapport_alertes.txt"

        aujourd_hui = datetime.now()
        alertes = []
        actifs = 0

        # Analyse des données et mise à jour automatique des statuts
        for m in self.membres:
            d_fin = datetime.strptime(m.date_fin, "%d-%m-%Y")
            jours_restants = (d_fin - aujourd_hui).days

            if jours_restants < 0:
                alertes.append(f"[EXPIRÉ] {m.nom} a expiré depuis {abs(jours_restants)} jours.")
                m.statut = "Expiré" # Mise à jour automatique de l'objet !
            elif 0 <= jours_restants <= 7:
                alertes.append(f"[ALERTE] {m.nom} expire bientôt (dans {jours_restants} jours).")
            else:
                actifs += 1
                m.statut = "Actif"

        # On sauvegarde les nouveaux statuts calculés
        self.sauvegarder()

        # Écriture du fichier rapport avec encodage strict
        with open(chemin_rapport, "w", encoding="utf-8") as f:
            f.write("=== RAPPORT D'ANALYSE GYM ===\n")
            # Format d'affichage français pour le timestamp de génération
            f.write(f"Généré le : {aujourd_hui.strftime('%d-%m-%Y %H:%M')}\n\n")
            f.write(f"Membres en règle : {actifs}\n")
            f.write(f"Membres en alerte/expirés : {len(alertes)}\n")
            f.write("-" * 30 + "\n")
            
            if alertes:
                for a in alertes:
                    f.write(a + "\n")
            else:
                f.write("Aucune alerte à signaler aujourd'hui.\n")

        # On renvoie le chemin pour l'afficher sur l'interface graphique
        return str(chemin_rapport)