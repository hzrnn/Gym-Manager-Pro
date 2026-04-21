import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
import customtkinter as ctk

# On importe le Cerveau ET l'Interface
from src.core.logic import GymLogic
from src.app import App  # Assure-toi que c'est bien le nom de ton fichier et de ta classe

class TestInterfaceGraphique(unittest.TestCase):
    """
    Script de test Front-End.
    Vérifie que l'interface CustomTkinter se construit correctement.
    """

    def setUp(self):
        """
        Avant chaque test, on prépare un Cerveau et on lance l'Interface.
        """
        self.logic = GymLogic()
        self.logic.membres = [] # On utilise une base vide pour ne pas toucher aux vraies données
        
        # On crée l'interface
        self.app = App(self.logic)
        
        # ASTUCE DE PRO : Au lieu de faire app.mainloop() (qui bloquerait le test à l'infini),
        # on force juste l'interface à se dessiner une fois à l'écran.
        self.app.update()

    def tearDown(self):
        """
        Après chaque test, on force la destruction de la fenêtre pour nettoyer la mémoire.
        """
        self.app.destroy()

    def test_01_lancement_fenetre(self):
        """Vérifie que la fenêtre principale s'ouvre sans erreur et porte le bon nom."""
        # On vérifie que l'application est bien une instance de CustomTkinter
        self.assertIsInstance(self.app, ctk.CTk)
        
        # Vérifie que le titre de la fenêtre n'est pas vide
        self.assertTrue(self.app.title() != "", "La fenêtre n'a pas de titre !")

    def test_02_champs_de_saisie_presents(self):
        """
        Vérifie que les champs de saisie des dates (JJ-MM-AAAA) ont bien été créés
        dans le code de ton collègue (Membre 2).
        """
        # Si la fonction init_page_ajouter a bien tourné, l'attribut ent_debut devrait exister
        # hasattr vérifie si l'interface possède bien une variable appelée 'ent_debut'
        
        # Note : Si ton collègue a changé le nom de la variable, il faudra ajuster ce nom ici.
        self.assertTrue(hasattr(self.app, 'ent_debut'), "Le champ de Date de début est manquant !")
        self.assertTrue(hasattr(self.app, 'ent_fin'), "Le champ de Date de fin est manquant !")

if __name__ == '__main__':
    print("Démarrage du test de l'Interface Graphique (Front-End)...")
    unittest.main()