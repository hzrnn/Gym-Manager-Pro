from datetime import datetime

class Membre:
    """
    Modèle représentant un abonné de la salle de sport.
    Applique l'encapsulation stricte et la validation métier.
    """
    def __init__(self, nom, date_debut, date_fin, statut="Actif"):
        # L'appel direct aux attributs sans le tiret du bas déclenche automatiquement 
        # les setters ci-dessous, ce qui valide les données dès la création !
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.statut = statut

    # ==========================================
    # 1. ENCAPSULATION ET VALIDATION (GETTERS & SETTERS)
    # ==========================================

    @property
    def nom(self):
        """Getter : Permet de lire le nom protégé."""
        return self._nom

    @nom.setter
    def nom(self, valeur):
        """Setter : Valide et modifie le nom."""
        if not isinstance(valeur, str) or not valeur.strip():
            # Validation métier : interdiction d'avoir un nom vide
            raise ValueError("Erreur : Le nom du membre ne peut pas être vide.")
        
        # On protège la donnée avec un _ et on la force en majuscules pour être propre
        self._nom = valeur.strip().upper()

    @property
    def date_debut(self):
        """Getter : Permet de lire la date de début."""
        return self._date_debut

    @date_debut.setter
    def date_debut(self, valeur):
        """Setter : Vérifie que la date est bien au format JJ-MM-AAAA."""
        try:
            datetime.strptime(valeur, "%d-%m-%Y")
            self._date_debut = valeur
        except ValueError:
            raise ValueError(f"Format de date de début invalide ({valeur}). Utilisez JJ-MM-AAAA.")

    @property
    def date_fin(self):
        """Getter : Permet de lire la date de fin."""
        return self._date_fin

    @date_fin.setter
    def date_fin(self, valeur):
        """Setter : Vérifie que la date est bien au format JJ-MM-AAAA."""
        try:
            datetime.strptime(valeur, "%d-%m-%Y")
            self._date_fin = valeur
        except ValueError:
            raise ValueError(f"Format de date de fin invalide ({valeur}). Utilisez JJ-MM-AAAA.")

    @property
    def statut(self):
        """Getter : Permet de lire le statut du membre."""
        return self._statut

    @statut.setter
    def statut(self, valeur):
        """Setter : Bloque tout statut qui n'est pas dans la liste officielle."""
        valeurs_autorisees = ["Actif", "Expiré", "Suspendu"]
        if valeur not in valeurs_autorisees:
            raise ValueError(f"Statut invalide. Choisissez parmi : {valeurs_autorisees}")
        self._statut = valeur

    # ==========================================
    # 2. SÉRIALISATION (POUR LE STOCKAGE JSON)
    # ==========================================

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour la sauvegarde dans le fichier JSON."""
        return {
            "nom": self.nom, # Appelle le getter pour garantir une donnée propre
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "statut": self.statut
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée un objet Membre à partir d'un dictionnaire lu dans le fichier JSON.
        Utilise des valeurs de secours (fallback) au format JJ-MM-AAAA si la donnée manque.
        """
        return cls(
            nom=data.get("nom", "Inconnu"),
            date_debut=data.get("date_debut", "01-01-2000"),
            date_fin=data.get("date_fin", "01-01-2000"),
            statut=data.get("statut", "Actif")
        )

    # ==========================================
    # 3. MÉTHODES SPÉCIALES (DUNDER)
    # ==========================================

    def __str__(self):
        """Définit l'affichage lisible (print) de l'objet, très utile pour le débogage."""
        return f"[{self.statut}] {self.nom} (Du {self.date_debut} au {self.date_fin})"

    def __eq__(self, autre):
        """Permet de vérifier l'égalité entre deux objets avec l'opérateur ==."""
        if not isinstance(autre, Membre):
            return False
        # Deux membres sont considérés identiques s'ils ont le même nom et la même date de début
        return self.nom == autre.nom and self.date_debut == autre.date_debut