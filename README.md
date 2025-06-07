
# 🧑‍💻 FaceScan – Description du projet et de l’arborescence

Bienvenue sur le dépôt **FaceScan** ! Ce projet explore la détection et l’analyse faciale à travers plusieurs versions, chacune apportant de nouvelles fonctionnalités et une expérience utilisateur enrichie. Voici une description détaillée de l’arborescence et des différences entre chaque version.

---

## 🌳 Arborescence du projet


FaceScan/
├── README.md
├── FaceScan_V1/
│   └── cam.py
├── FaceScan_V2/
│   └── cam.py
└── FaceScan_V3/
    ├── age_deploy.prototxt
    ├── age_net.caffemodel
    ├── camera.py
    ├── data.py
    ├── face_id.png
    ├── gallerie.png
    ├── gender_deploy.prototxt
    ├── gender_net.caffemodel
    ├── logo.ico
    ├── logo.png
    ├── READ.txt
    ├── splash.gif
    ├── top.py
    ├── __pycache__/
    └── background/
        ├── C1.mp4
        ├── C2.mp4
        ├── S1.mp4
        └── S2.mp4


## 🏷️ Détail des versions

### 🥇 FaceScan_V1

- **Fichier principal :** `cam.py`
- **Fonctionnalités :**
  - 📷 Détection de visages et d’yeux en temps réel via la webcam.
  - Utilisation des Haar Cascades d’OpenCV pour la reconnaissance.
  - Interface simple (console ou fenêtre Tkinter basique).
- **Objectif :**
  - Servir de prototype pour valider la détection faciale.
- **Limites :**
  - Pas d’interface graphique avancée.
  - Pas de gestion de base de données ni d’analyse supplémentaire.



### 🥈 FaceScan_V2

- **Fichier principal :** `cam.py`
- **Fonctionnalités :**
  - 🖼️ Interface graphique améliorée avec Tkinter ou CustomTkinter.
  - Affichage en temps réel des visages et yeux détectés sur la webcam.
  - Meilleure gestion des flux vidéo et de l’affichage.
- **Améliorations par rapport à V1 :**
  - Interface utilisateur plus ergonomique et agréable.
  - Expérience utilisateur enrichie grâce à l’affichage graphique.
- **Limites :**
  - Toujours pas d’analyse d’âge/genre ni de base de données.

---

### 🥉 FaceScan_V3

- **Fichiers principaux :** `top.py`, `camera.py`, `data.py`
- **Fonctionnalités avancées :**
  - 🎨 Interface graphique professionnelle avec CustomTkinter, logos, splash screen animé (`splash.gif`), et icônes personnalisées.
  - 🧑‍🦱 Détection de l’âge et du genre grâce à des modèles pré-entraînés (`age_net.caffemodel`, `gender_net.caffemodel`).
  - 🗃️ Connexion à une base de données SQL pour stocker et retrouver les empreintes faciales.
  - 📸 Téléchargement, traitement et gestion d’images (plusieurs formats supportés).
  - 🎥 Vidéos de fond animées pour une interface dynamique (`background/`).
  - 📂 Gestion avancée des erreurs et des exceptions.
  - 📊 Fichiers de données et images pour la galerie et l’identification.
- **Améliorations par rapport à V2 :**
  - Ajout de la reconnaissance d’âge et de genre.
  - Intégration d’une base de données pour la gestion des profils.
  - Interface utilisateur complète et professionnelle.
  - Support multi-format, gestion des médias et expérience utilisateur immersive.
- **Bonus :**
  - Documentation supplémentaire dans `READ.txt`.
  - Fichiers de configuration et modèles pour l’IA.

---

## 📌 Synthèse des différences

| Version      | Interface | Détection visage/yeux | Détection âge/genre | Base de données | Gestion médias | Vidéos de fond | Professionnalisation |
|--------------|-----------|----------------------|---------------------|-----------------|---------------|----------------|---------------------|
| **V1**       | Basique   | ✅                   | ❌                  | ❌              | ❌            | ❌             | ❌                  |
| **V2**       | Améliorée | ✅                   | ❌                  | ❌              | ❌            | ❌             | 🟡                  |
| **V3**       | Pro       | ✅                   | ✅                  | ✅              | ✅            | ✅             | ✅                  |

---

## 🚀 Pour aller plus loin

- Consultez chaque dossier de version pour le code source et les instructions spécifiques.
- Lisez le fichier `READ.txt` dans FaceScan_V3 pour des détails techniques supplémentaires.
- Les modèles IA (âge/genre) sont fournis pour une détection avancée.

---

> 🤝 **Contribuez** ou testez chaque version pour voir l’évolution du projet FaceScan !

```

