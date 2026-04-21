import sys
from src.core.logic import GymLogic
from src.app import App

def main():
    """
    Point d'entrée principal de l'application Gym Manager Pro.
    Initialise le contrôleur logique puis lance l'interface graphique.
    """
    print("Démarrage de l'application Gym Manager Pro...")
    
    try:
        # 1. Initialisation du "Cerveau" (Chargement des données JSON via Storage)
        controleur = GymLogic()
        
        # 2. Initialisation de l'Interface Graphique (Front-End)
        # On passe le contrôleur en paramètre pour que les boutons sachent à qui parler.
        interface = App(controleur)
        
        # 3. Lancement de la boucle visuelle
        interface.mainloop()
        
    except Exception as e:
        # Filet de sécurité ultime : Si une erreur fatale imprévue survient tout au début,
        # le programme s'arrête proprement avec un message clair dans la console.
        print(f"\n[ERREUR CRITIQUE] Impossible de lancer l'application : {e}")
        sys.exit(1)

# Cette condition vérifie que le script est exécuté directement, 
# et non importé comme un module par un autre fichier.
if __name__ == "__main__":
    main()