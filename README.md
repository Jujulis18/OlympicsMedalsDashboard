# 🏅 Olympic Dashboard – Paris 2024

Bienvenue dans le projet de visualisation et d’analyse des médaillés des Jeux Olympiques d’été de Paris 2024.

Ce dashboard interactif, construit avec Python, Streamlit et Plotly, permet d’explorer les performances des athlètes médaillés selon plusieurs dimensions : pays, disciplines, âge, genre, etc.

---

## 📚 Documentation du projet

Pour mieux comprendre chaque composant du projet, voici les documents disponibles :

### 1. Dataset

- **Description complète des données utilisées**  
  Consultez [`data/data_card.md`](data/data_card.md) pour les détails sur la structure du dataset (médaillés, variables, prétraitement, limites).

### 2. Scripts

- **Structure modulaire du dashboard**  
  Les scripts sont organisés par fonctionnalités dans le dossier `scripts/`. Le dossier `components/` regroupe les blocs d’interface réutilisables (graphiques, tableaux, filtres).

### 3. Visualisations

- **Exemples de visualisations intégrées au dashboard**  
  On retrouve : histogrammes d’âge, pyramides des âges par sexe, cartes des médailles par pays, tops des disciplines, etc.


---

## 🚀 Comment démarrer

1. Clonez le dépôt 
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancez le dashboard :

```bash
streamlit run app.py
```

---

## 🛠️ Fonctionnalités principales

* 🎌 **Filtrage par pays, genre, discipline, médaille**
* 📊 **Visualisation dynamique avec Plotly**
* 👶 **Analyse des âges des médaillés**
* 🥇 **Distribution des médailles par pays ou sport**

---

## 🔗 Ressource externe

* [Dataset Kaggle – Paris 2024 Olympic Games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games)

