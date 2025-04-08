import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Fonction pour charger les données et gestion des erreurs
def load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"⚠️ Fichier introuvable : {filepath}")
        return None

# 2. Fonction de prétraitement pour la heatmap des confrontations
def preprocess_heatmap_data(df_results, top_n_teams=15):
    df_results["match_pair"] = df_results.apply(lambda x: tuple(sorted([x["home_team"], x["away_team"]])), axis=1)
    match_counts = df_results["match_pair"].value_counts().reset_index()
    match_counts.columns = ["pair", "count"]
    match_counts[["team1", "team2"]] = pd.DataFrame(match_counts["pair"].tolist(), index=match_counts.index)
    heatmap_data = match_counts.pivot(index="team1", columns="team2", values="count").fillna(0)

    # Combiner team1 et team2 pour récupérer les équipes les plus fréquentes
    all_teams = pd.concat([match_counts["team1"], match_counts["team2"]])
    top_teams = all_teams.value_counts().head(top_n_teams).index.tolist()

    # Filtrer la heatmap uniquement sur les top équipes
    heatmap_data = heatmap_data.loc[
        heatmap_data.index.intersection(top_teams),
        heatmap_data.columns.intersection(top_teams)
    ]
    return heatmap_data

# 3. Fonction de visualisation
def plot_heatmap(data):
    plt.figure(figsize=(12,10))
    sns.heatmap(data, annot=True, fmt="g", cmap="Blues", linewidths=0.5)
    plt.title("Confrontations entre grandes nations de football")
    plt.xlabel("Pays")
    plt.ylabel("Pays")
    plt.tight_layout()
    plt.show()

# 4. Execution de mon fichiers CSV
df_results = load_csv("/results.csv")
heatmap = preprocess_heatmap_data(df_results, top_n_teams=15)
plot_heatmap(heatmap)
