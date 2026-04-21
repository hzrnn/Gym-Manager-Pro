import sys
from pathlib import Path
# Permet au dossier tests/ de voir le dossier src/
sys.path.append(str(Path(__file__).parent.parent))

import unittest
import os
from datetime import datetime

from src.core.logic import GymLogic

class TestGymIntegrale(unittest.TestCase):
    """
    Script de Test Intégral (End-to-End partiel).
    Vérifie la Logique, les Modèles, la Persistance JSON et les Fichiers de Rapport.
    """

    def setUp(self):
        """
        LE BOUCLIER : S'exécute avant CHAQUE test.
        On fait une sauvegarde invisible de ton vrai fichier JSON pour ne pas le perdre.
        """
        self.logic = GymLogic()
        self.vraies_donnees = self.logic.storage.load() # Backup des vraies données
        self.logic.membres = [] # On vide la mémoire juste pour le test

    def tearDown(self):
        """
        LE NETTOYEUR : S'exécute après CHAQUE test.
        On écrase les fausses données de test et on remet ton vrai fichier JSON intact.
        """
        self.logic.storage.save(self.vraies_donnees)

    # ==========================================
    # 1. TESTS UNITAIRES (Le Cerveau et les Modèles)
    # ==========================================

    def test_01_ajouter_membre_succes(self):
        self.logic.ajouter_membre("Testeur Un", "01-05-2026", "01-06-2026")
        self.assertEqual(len(self.logic.membres), 1)
        self.assertEqual(self.logic.membres[0].nom.upper(), "TESTEUR UN")

    def test_02_erreur_date_invalide(self):
        with self.assertRaises(ValueError):
            self.logic.ajouter_membre("Testeur Erreur", "01-06-2026", "01-05-2026")

    def test_03_recherche_membre(self):
        self.logic.ajouter_membre("Ali", "01-01-2026", "31-12-2026")
        resultat = self.logic.rechercher_membre("ali")
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.nom.upper(), "ALI")

    def test_04_doublon_refuse(self):
        self.logic.ajouter_membre("Doublon", "01-01-2026", "31-12-2026")
        with self.assertRaises(ValueError):
            self.logic.ajouter_membre("Doublon", "10-02-2026", "10-05-2026")

    # ==========================================
    # 2. TESTS D'INTÉGRATION (Fichiers et Disque Dur)
    # ==========================================

    def test_05_persistance_json(self):
        """Vérifie que les données sont physiquement écrites et lues dans data/input.json"""
        # 1. On ajoute un membre fantôme et on sauvegarde sur le disque dur
        self.logic.ajouter_membre("FANTOME", "01-01-2026", "31-12-2026")
        
        # 2. On SIMULE un redémarrage de l'application (on crée un nouveau Cerveau)
        nouveau_cerveau = GymLogic()
        
        # 3. Le nouveau cerveau doit charger le fichier JSON tout seul. On vérifie s'il trouve FANTOME.
        resultat = nouveau_cerveau.rechercher_membre("FANTOME")
        self.assertIsNotNone(resultat, "CRITIQUE: Le fichier JSON ne sauvegarde pas les données !")
        self.assertEqual(resultat.nom.upper(), "FANTOME")

    def test_06_creation_fichier_rapport(self):
        """Vérifie que le système est capable de créer un fichier physique dans output/"""
        # On ajoute un membre avec une date dépassée exprès
        self.logic.ajouter_membre("EXPIRE", "01-01-2023", "01-02-2023")
        
        # On déclenche la génération du rapport
        chemin = self.logic.generer_rapport_alertes()
        fichier_rapport = Path(chemin)
        
        # 1. On vérifie (check) que le fichier existe physiquement sur ton Mac
        self.assertTrue(fichier_rapport.exists(), "Le fichier rapport_alertes.txt n'a pas été créé !")
        
        # 2. On ouvre le fichier pour vérifier s'il a bien écrit dedans
        with open(fichier_rapport, "r", encoding="utf-8") as f:
            contenu = f.read()
            self.assertIn("EXPIRE", contenu, "Le rapport ne contient pas les données attendues.")

if __name__ == '__main__':
    print("Démarrage de la vérification INTÉGRALE du système...")
    unittest.main()