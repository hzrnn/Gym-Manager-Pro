# --- Ajouter le chemin racine avant tout ---
# (Astuce de développement pour lancer ce fichier tout seul)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # remonte 3 niveaux

# --- Imports ---
import customtkinter as ctk
from tkinter import messagebox

# --- Import GymLogic ---
try:
    from logic import GymLogic
except ImportError:
    from src.core.logic import GymLogic


# --- APPLICATION ---
class App(ctk.CTk):
    def __init__(self, logique):
        super().__init__()
        self.logic = logique
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Gym Manager Pro")
        self.geometry("900x550")
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        ctk.CTkLabel(self.sidebar, text="💪 GYM MANAGER", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation Buttons
        buttons = [
            ("➕ Ajouter", "ajouter"),
            ("📋 Voir Liste", "voir"),
            ("🔍 Rechercher", "rechercher"),
            ("❌ Supprimer", "supprimer")
        ]
        
        for i, (text, page) in enumerate(buttons, start=1):
            ctk.CTkButton(self.sidebar, text=text, 
                          command=lambda p=page: self.changer_page(p)).grid(row=i, column=0, padx=20, pady=10)
        
        ctk.CTkButton(self.sidebar, text="⚠️ Générer Alertes", fg_color="#C21807", 
                      hover_color="#8B0000", command=self.action_rapport).grid(row=7, column=0, padx=20, pady=20)

        # --- PAGES CONTAINERS ---
        self.page_ajouter = ctk.CTkFrame(self, fg_color="transparent")
        self.page_voir = ctk.CTkFrame(self, fg_color="transparent")
        self.page_rechercher = ctk.CTkFrame(self, fg_color="transparent")
        self.page_supprimer = ctk.CTkFrame(self, fg_color="transparent")
        
        self.init_page_ajouter()
        self.init_page_voir()
        self.init_page_rechercher()
        self.init_page_supprimer()
        
        self.changer_page("ajouter")

    # --- CHANGEMENT DE PAGE ---
    def changer_page(self, nom_page):
        for page in [self.page_ajouter, self.page_voir, self.page_rechercher, self.page_supprimer]:
            page.grid_forget()
        
        if nom_page == "ajouter":
            self.page_ajouter.grid(row=0, column=1, sticky="nsew")
            self.ent_nom.focus()
        elif nom_page == "voir":
            self.page_voir.grid(row=0, column=1, sticky="nsew")
            self.action_voir()
        elif nom_page == "rechercher":
            self.page_rechercher.grid(row=0, column=1, sticky="nsew")
            self.ent_rech.focus()
        elif nom_page == "supprimer":
            self.page_supprimer.grid(row=0, column=1, sticky="nsew")
            self.ent_sup_nom.focus()

    # --- INIT PAGES ---
    def init_page_ajouter(self):
        ctk.CTkLabel(self.page_ajouter, text="NOUVEL ABONNEMENT", font=("Arial", 22, "bold")).pack(pady=(40, 20))
        
        self.ent_nom = ctk.CTkEntry(self.page_ajouter, placeholder_text="Nom complet du membre", width=400, height=40)
        self.ent_nom.pack(pady=10)
        
        # --- CORRECTION 1 : Changement du texte indicatif (placeholder) ---
        # Le format doit correspondre à %Y-%m-%d exigé par ta fonction datetime.strptime dans logic.py
        self.ent_debut = ctk.CTkEntry(self.page_ajouter, placeholder_text="Date début (AAAA-MM-JJ)", width=400, height=40)
        self.ent_debut.pack(pady=10)
        
        self.ent_fin = ctk.CTkEntry(self.page_ajouter, placeholder_text="Date fin (AAAA-MM-JJ)", width=400, height=40)
        self.ent_fin.pack(pady=10)
        
        ctk.CTkButton(self.page_ajouter, text="💾 Enregistrer le Membre", font=("Arial", 14, "bold"),
                      height=45, command=self.action_ajouter).pack(pady=40)

    def init_page_voir(self):
        ctk.CTkLabel(self.page_voir, text="LISTE DES MEMBRES", font=("Arial", 22, "bold")).pack(pady=(30, 10))
        ctk.CTkLabel(self.page_voir, text="NOM | DÉBUT | FIN | STATUT", font=("Courier New", 12)).pack()
        
        self.txt_liste = ctk.CTkTextbox(self.page_voir, width=600, height=350, font=("Courier New", 13))
        self.txt_liste.pack(pady=10, padx=20)

    def init_page_rechercher(self):
        ctk.CTkLabel(self.page_rechercher, text="RECHERCHE", font=("Arial", 22, "bold")).pack(pady=(30, 20))
        
        search_frame = ctk.CTkFrame(self.page_rechercher, fg_color="transparent")
        search_frame.pack(pady=10)
        
        self.ent_rech = ctk.CTkEntry(search_frame, placeholder_text="Nom du membre...", width=300)
        self.ent_rech.pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="🔍", width=50, command=self.action_rechercher).pack(side="left")
        
        self.txt_rech = ctk.CTkTextbox(self.page_rechercher, width=600, height=200, font=("Courier New", 13))
        self.txt_rech.pack(pady=20)

    def init_page_supprimer(self):
        ctk.CTkLabel(self.page_supprimer, text="ZONE DE SUPPRESSION", font=("Arial", 22, "bold"), text_color="#FF4444").pack(pady=(40, 20))
        
        self.ent_sup_nom = ctk.CTkEntry(self.page_supprimer, placeholder_text="Nom EXACT pour confirmation", width=400, height=40)
        self.ent_sup_nom.pack(pady=20)
        
        ctk.CTkButton(self.page_supprimer, text="Supprimer définitivement", fg_color="#8B0000", 
                      hover_color="#550000", command=self.action_supprimer).pack(pady=10)

    # --- ACTIONS ---
    def action_ajouter(self):
        try:
            self.logic.ajouter_membre(self.ent_nom.get(), self.ent_debut.get(), self.ent_fin.get())
            messagebox.showinfo("Succès", f"Membre {self.ent_nom.get()} ajouté avec succès !")
            for ent in [self.ent_nom, self.ent_debut, self.ent_fin]:
                ent.delete(0, 'end')
            self.changer_page("voir")
        except ValueError as e:
            messagebox.showerror("Erreur de saisie", str(e))

    def action_voir(self):
        self.txt_liste.configure(state="normal")
        self.txt_liste.delete("1.0", "end")
        membres = self.logic.get_tous_les_membres()
        if not membres:
            self.txt_liste.insert("end", "\n\n      --- Aucun membre dans la base de données ---")
        else:
            for m in membres:
                line = f"{m.nom:<20} | {m.date_debut} | {m.date_fin} | {m.statut}\n"
                self.txt_liste.insert("end", line)
        self.txt_liste.configure(state="disabled")

    def action_rechercher(self):
        self.txt_rech.configure(state="normal")
        self.txt_rech.delete("1.0", "end")
        try:
            # --- CORRECTION 2 : Traitement d'un objet unique au lieu d'une liste ---
            # La fonction logic.rechercher_membre renvoie un objet unique, pas une liste.
            # On retire donc la boucle 'for m in resultats:' qui causait un crash.
            membre_trouve = self.logic.rechercher_membre(self.ent_rech.get())
            
            if not membre_trouve:
                self.txt_rech.insert("end", "Aucun membre trouvé.")
            else:
                # Affichage direct des attributs de l'objet trouvé
                self.txt_rech.insert("end", f"TROUVÉ: {membre_trouve.nom} ({membre_trouve.statut})\n")
                self.txt_rech.insert("end", f"Expire le: {membre_trouve.date_fin}\n")
                self.txt_rech.insert("end", "-"*30 + "\n")
                
        except ValueError as e:
            messagebox.showwarning("Info", str(e))
            
        self.txt_rech.configure(state="disabled")

    def action_supprimer(self):
        nom = self.ent_sup_nom.get().strip()
        if not nom:
            return
        if messagebox.askyesno("Confirmation", f"Êtes-vous certain de vouloir supprimer {nom} ?"):
            try:
                self.logic.supprimer_membre(nom)
                messagebox.showinfo("Confirmé", "Membre retiré de la base.")
                self.ent_sup_nom.delete(0, 'end')
                self.action_voir()
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

    def action_rapport(self):
        chemin = self.logic.generer_rapport_alertes()
        messagebox.showinfo("Rapport Généré", f"Le fichier d'alerte a été créé :\n{chemin}")


# --- LANCEMENT ---
if __name__ == "__main__":
    logic_instance = GymLogic()
    app = App(logic_instance)
    app.mainloop()