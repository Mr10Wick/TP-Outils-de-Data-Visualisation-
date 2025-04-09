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

# 3. Fonction de visualisation de la heatmap
def plot_heatmap(data, title="Confrontations entre grandes nations", cmap="Blues", size=(12, 10)):
    plt.figure(figsize=size)
    sns.heatmap(data, annot=True, fmt="g", cmap=cmap, linewidths=0.5)
    plt.title(title)
    plt.xlabel("Pays")
    plt.ylabel("Pays")
    plt.tight_layout()
    plt.show()

# 4. Fonction de visualisation des meilleurs buteurs
def plot_top_scorers(df_goals):
    top_scorers = df_goals[df_goals["own_goal"] == False]["scorer"].value_counts().head(10).reset_index()
    top_scorers.columns = ["scorer", "goals"]
    
    plt.figure(figsize=(10,6))
    sns.barplot(x="goals", y="scorer", data=top_scorers, palette="viridis", legend=False)
    plt.title("Top 10 des meilleurs buteurs", fontsize=14)
    plt.xlabel("Nombre de buts")
    plt.ylabel("Joueur")
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# 5. Fonction de visualisation des victoires et défaites par pays (limité aux top_n équipes)
def plot_wins_losses(df_results, top_n=15):
    # Compter le nombre de victoires et défaites
    df_results['result'] = df_results.apply(lambda x: 'win' if x['home_score'] > x['away_score'] else ('loss' if x['home_score'] < x['away_score'] else 'draw'), axis=1)

    # Nombre de victoires et de défaites par équipe à domicile
    home_results = df_results.groupby(['home_team', 'result']).size().unstack(fill_value=0)
    home_results = home_results[['win', 'loss']]

    # Nombre de victoires et de défaites par équipe à l'extérieur
    away_results = df_results.groupby(['away_team', 'result']).size().unstack(fill_value=0)
    away_results = away_results[['win', 'loss']]

    # Fusionner les résultats à domicile et à l'extérieur
    team_results = home_results.add(away_results, fill_value=0)

    # Limiter à top_n équipes les plus présentes
    team_results = team_results.sort_values(by='win', ascending=False).head(top_n)

    # Tracer les résultats
    team_results.plot(kind='barh', stacked=False, figsize=(12,8))
    plt.title('Victoires et Défaites par équipe', fontsize=14)
    plt.xlabel('Nombre de matchs')
    plt.ylabel('Équipe')
    plt.tight_layout()
    plt.show()

# 6. Exécution de mon fichier CSV
df_results = load_csv("/results.csv")
df_goals = load_csv("/goalscorers.csv")
df_shootouts = load_csv("/shootouts.csv")

# Filtre les équipes pour la heatmap
if df_results is not None:
    df_results = df_results[df_results["tournament"].isin(["FIFA World Cup", "UEFA Euro"])]

# Visualisation de la heatmap des confrontations
heatmap = preprocess_heatmap_data(df_results, top_n_teams=15)
plot_heatmap(heatmap)

# Visualisation des top 10 meilleurs buteurs
if df_goals is not None:
    plot_top_scorers(df_goals)

# Visualisation des victoires et défaites par pays
if df_results is not None:
    plot_wins_losses(df_results)
