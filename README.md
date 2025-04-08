# TP-Outils-de-Data-Visualisation-

# 📊 Visualisation Avancée des Confrontations Internationales – Football

Ce projet Python utilise des données issues de **Kaggle** pour représenter de manière visuelle et interactive les confrontations les plus fréquentes entre nations de football.

---

## 📁 Dataset utilisé

- **results.csv** : contient les résultats détaillés des matchs internationaux (équipe à domicile, à l’extérieur, date, score, etc.)
- Source : [Kaggle – International Football Results](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)

---

## 🛠 Librairies utilisées

- `pandas` : manipulation des données
- `seaborn` : création de graphiques statistiques élégants
- `matplotlib` : personnalisation des figures

---

## 📌 Fonction principale : `plot_heatmap_matches()`

Cette fonction permet d'afficher une **heatmap des confrontations les plus fréquentes** entre nations.

### ➕ Fonctionnalités :
- Compte le nombre de confrontations entre chaque paire de pays (match aller/retour groupé)
- Trie les pays les plus présents
- Affiche une heatmap lisible et annotée
- Paramètre `top_n_teams` pour limiter le nombre de pays visualisés

### 💻 Exemple d'utilisation :

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Chargement du fichier CSV
df_results = pd.read_csv('/content/results.csv')

# Fonction d’affichage de la heatmap
def plot_heatmap_matches(df_results, top_n_teams=15):
    df_results["match_pair"] = df_results.apply(lambda x: tuple(sorted([x["home_team"], x["away_team"]])), axis=1)
    match_counts = df_results["match_pair"].value_counts().reset_index()
    match_counts.columns = ["pair", "count"]
    match_counts[["team1", "team2"]] = pd.DataFrame(match_counts["pair"].tolist(), index=match_counts.index)

    heatmap_data = match_counts.pivot(index="team1", columns="team2", values="count").fillna(0)
    top_teams = match_counts["team1"].value_counts().head(top_n_teams).index.tolist()
    heatmap_data = heatmap_data.loc[top_teams, top_teams]

    plt.figure(figsize=(12,10))
    sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="Blues", linewidths=0.5)
    plt.title("Confrontations entre grandes nations de football")
    plt.xlabel("Pays")
    plt.ylabel("Pays")
    plt.tight_layout()
    plt.show()

# Appel
plot_heatmap_matches(df_results)
