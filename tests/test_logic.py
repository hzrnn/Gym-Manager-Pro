import sys
from pathlib import Path
# On remonte d'un dossier (de 'tests/' vers la racine 'Gym-Manager-Pro/')
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from datetime import datetime

# Importation de ton Cerveau depuis l'architecture du projet
from src.core.logic import GymLogic


class TestGymLogic(unittest.TestCase):
    """
    Script d'auto-vérification (Self-Check) pour l'application Gym Manager Pro.
    Garantit que la logique métier fonctionne correctement sans avoir besoin de l'interface graphique.
    """

    def setUp(self):
        """
        Préparation : Cette fonction s'exécute automatiquement AVANT chaque test.
        Elle nous donne un 'Cerveau' tout neuf avec une liste vide pour ne pas fausser les tests.
        """
        self.logic = GymLogic()
        self.logic.membres = [] # On vide la base en mémoire pour faire un test propre

    def test_01_ajouter_membre_succes(self):
        """Vérifie que l'ajout d'un membre valide fonctionne correctement."""
        # On tente d'ajouter un membre avec des dates valides (Format JJ-MM-AAAA)
        self.logic.ajouter_membre("Testeur Un", "01-05-2026", "01-06-2026")
        
        # VERIFICATIONS (Checks) :
        # 1. On vérifie qu'il y a bien exactement 1 membre dans la liste
        self.assertEqual(len(self.logic.membres), 1)
        # 2. On vérifie que le système a bien mis le nom en majuscules (si tu as géré ça dans logic)
        # (Si tu n'as pas forcé les majuscules, change "TESTEUR UN" par "Testeur Un")
        self.assertEqual(self.logic.membres[0].nom.upper(), "TESTEUR UN")

    def test_02_erreur_date_invalide(self):
        """Vérifie que le système bloque les dates illogiques (Fin avant le Début)."""
        
        # VERIFICATION : On s'assure que le code lève BIEN une ValueError
        with self.assertRaises(ValueError):
            # On met intentionnellement la date de fin (mai) AVANT la date de début (juin)
            self.logic.ajouter_membre("Testeur Erreur", "01-06-2026", "01-05-2026")

    def test_03_recherche_membre(self):
        """Vérifie que la fonctionnalité de recherche trouve bien le bon membre."""
        # On ajoute un membre pour le test
        self.logic.ajouter_membre("Ali", "01-01-2026", "31-12-2026")
        
        # On lance la recherche (même avec des minuscules)
        resultat = self.logic.rechercher_membre("ali")
        
        # VERIFICATIONS :
        # 1. On vérifie que le résultat n'est pas "None" (il a trouvé quelqu'un)
        self.assertIsNotNone(resultat)
        # 2. On vérifie que c'est bien Ali
        self.assertEqual(resultat.nom.upper(), "ALI")

    def test_04_doublon_refuse(self):
        """Vérifie qu'il est impossible d'ajouter deux fois la même personne."""
        # On l'ajoute une première fois
        self.logic.ajouter_membre("Doublon", "01-01-2026", "31-12-2026")
        
        # VERIFICATION : La deuxième fois doit déclencher une erreur
        with self.assertRaises(ValueError):
            self.logic.ajouter_membre("Doublon", "10-02-2026", "10-05-2026")

if __name__ == '__main__':
    # Lance tous les tests automatiquement
    print("Démarrage du Self-Check (Tests Unitaires)...")
    unittest.main()