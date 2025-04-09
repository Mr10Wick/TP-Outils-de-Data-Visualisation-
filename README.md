TP : Visualisation des Confrontations Internationales – Football

Ce projet Python permet de visualiser les confrontations fréquentes entre nations de football à partir de données issues de Kaggle.

Dataset utilisé : 

results.csv : Résultats des matchs internationaux (équipe à domicile, à l’extérieur, score, etc.)
goalscorers.csv : Buteurs par match
Source : Kaggle – International Football Results

Librairies utilisées : 

pandas : Manipulation des données
seaborn : Graphiques élégants
matplotlib : Personnalisation des graphiques

📌 Structure du code

Le code est divisé en 5 fonctions principales :


1. Chargement des données
def load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"⚠️ Fichier introuvable : {filepath}")
        return None


2. Prétraitement pour la heatmap des confrontations

def preprocess_heatmap_data(df_results, top_n_teams=15):
    df_results["match_pair"] = df_results.apply(lambda x: tuple(sorted([x["home_team"], x["away_team"]])), axis=1)
    match_counts = df_results["match_pair"].value_counts().reset_index()
    match_counts.columns = ["pair", "count"]
    match_counts[["team1", "team2"]] = pd.DataFrame(match_counts["pair"].tolist(), index=match_counts.index)
    heatmap_data = match_counts.pivot(index="team1", columns="team2", values="count").fillna(0)
    

3. Visualisation de la heatmap

def plot_heatmap(data):
    plt.figure(figsize=(12,10))
    sns.heatmap(data, annot=True, fmt="g", cmap="Blues", linewidths=0.5)
    plt.title("Confrontations entre grandes nations de football")
    plt.tight_layout()
    plt.show()



4. Visualisation des meilleurs buteurs

def plot_top_scorers(df_goals):
    top_scorers = df_goals[df_goals["own_goal"] == False]["scorer"].value_counts().head(10).reset_index()
    top_scorers.columns = ["scorer", "goals"]
    sns.barplot(x="goals", y="scorer", data=top_scorers)
    plt.title("Top 10 des meilleurs buteurs")
    plt.tight_layout()
    plt.show()

   
5. Visualisation des victoires et défaites par pays


def plot_wins_losses(df_results, top_n=15):
    df_results['result'] = df_results.apply(lambda x: 'win' if x['home_score'] > x['away_score'] else ('loss' if x['home_score'] < x['away_score'] else 'draw'), axis=1)
    home_results = df_results.groupby(['home_team', 'result']).size().unstack(fill_value=0)[['win', 'loss']]
    away_results = df_results.groupby(['away_team', 'result']).size().unstack(fill_value=0)[['win', 'loss']]
    team_results = home_results.add(away_results, fill_value=0).sort_values(by='win', ascending=False).head(top_n)
    team_results.plot(kind='barh', stacked=False, figsize=(12,8))
    plt.title('Victoires et Défaites par équipe')
    plt.tight_layout()
    plt.show()


ℹ️ Exécution avec les fichiers CSV

df_results = load_csv("/results.csv")
df_goals = load_csv("/goalscorers.csv")


# Traitement et visualisation
if df_results is not None:
    df_results = df_results[df_results["tournament"].isin(["FIFA World Cup", "UEFA Euro"])]
    heatmap = preprocess_heatmap_data(df_results, top_n_teams=15)
    plot_heatmap(heatmap)

if df_goals is not None:
    plot_top_scorers(df_goals)

if df_results is not None:
    plot_wins_losses(df_results, top_n=15)
Les données sont filtrées pour ne conserver que les matchs des compétitions majeures (FIFA World Cup et UEFA Euro).


Conclusion : 


Ce projet permet de visualiser les confrontations, les meilleurs buteurs et les performances des équipes dans les compétitions internationales à travers des graphiques interactifs.
