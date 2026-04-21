# 💪 Gym Manager Pro

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-MVC-purple.svg)
![Statut](https://img.shields.io/badge/Statut-Achevé-success.svg)

**Gym Manager Pro** est une application logicielle de bureau permettant de gérer les abonnements d'une salle de sport. 

Ce projet a été développé dans le cadre du module **Programmation Python 2** à la Faculté des Sciences d'Agadir (FSA). L'objectif principal de cette application n'est pas seulement fonctionnel, mais architectural : il démontre l'application stricte des principes d'ingénierie logicielle tels que la **Programmation Orientée Objet (POO)**, l'**encapsulation**, la **gestion robuste des exceptions** et la **séparation des préoccupations (MVC)**.

---

## 👥 Équipe de Développement
* **Youness Habzhour** : Architecte Back-End & Tech Lead
* **Mohamed Amine Hdidouch** : Développeur Front-End & Interface Graphique
* **Noureddine Henni** : Responsable Persistance & Stockage des Données

---

## ✨ Fonctionnalités Principales

* **Gestion des Membres (CRUD) :** Ajouter, visualiser, rechercher et supprimer des abonnés de manière sécurisée.
* **Interface Graphique Moderne :** UI fluide et intuitive développée avec `customTkinter`.
* **Intelligence Métier :** Vérification mathématique automatique des dates d'abonnement (format JJ-MM-AAAA) et détection stricte des doublons.
* **Générateur de Rapports (Alertes) :** Analyse automatique de la base de données pour détecter les abonnements expirés ou arrivant à terme, avec génération d'un rapport textuel dans `output/`.
* **Stockage Sécurisé :** Persistance des données au format JSON avec création dynamique et automatique des répertoires de sauvegarde en cas d'absence.
* **Tolérance aux pannes (Fail Fast) :** Interception stricte des erreurs de saisie (`ValueError`) et de fichiers (`FileNotFoundError`) pour empêcher tout plantage de l'application.

---

## 🏗️ Architecture Technique (MVC)

Le projet respecte une architecture modulaire stricte, séparant totalement l'interface utilisateur (Front-End) de la logique métier et des données (Back-End) via le principe d'**Injection de Dépendances**.

```text
📁 Gym-Manager-Pro/
├── 📄 main.py                  # Point d'entrée unique (Initialisation)
├── 📄 requirements.txt         # Liste des dépendances externes
├── 📁 data/                    # Dossier généré automatiquement
│   └── input.json              # Base de données persistante
├── 📁 output/                  # Dossier généré automatiquement
│   └── rapport_alertes.txt     # Exports et rapports générés
└── 📁 src/
    ├── 📄 app.py               # Interface Graphique (Vue) - customTkinter
    └── 📁 core/
        ├── 📄 models.py        # Modélisation POO, Encapsulation, Dunder methods
        ├── 📄 logic.py         # Contrôleur, Logique Métier, Calculs temporels
        └── 📄 storage.py       # Couche d'accès aux données (I/O)