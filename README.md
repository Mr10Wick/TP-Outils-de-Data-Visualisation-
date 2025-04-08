📊 Visualisation Avancée des Confrontations Internationales – Football

Ce projet Python utilise des données issues de Kaggle pour représenter de manière visuelle et interactive les confrontations les plus fréquentes entre nations de football.

📁 Dataset utilisé

• results.csv : contient les résultats détaillés des matchs internationaux (équipe à domicile, à l’extérieur, date, score, etc.)
• goalscorers.csv : buteurs par match

Source : Kaggle – International Football Results

🛠 Librairies utilisées

• pandas : manipulation des données
• seaborn : création de graphiques statistiques élégants
• matplotlib : personnalisation des figures

📌 Structure du code

Le code est découpé en 5 fonctions modulaires + une partie d'exécution pour plus de lisibilité et de réutilisabilité :

1. Fonction pour charger les données et gestion des erreurs
def load_csv(filepath): 
    try: 
        return pd.read_csv(filepath) 
    except FileNotFoundError: 
        print(f"⚠️ Fichier introuvable : {filepath}") 
        return None
Cette fonction permet de charger les fichiers CSV et gère l'erreur en cas de fichier manquant.

2. Fonction de prétraitement pour la heatmap des confrontations
def preprocess_heatmap_data(df_results, top_n_teams=15):
    df_results["match_pair"] = df_results.apply(lambda x: tuple(sorted([x["home_team"], x["away_team"]])), axis=1)
    match_counts = df_results["match_pair"].value_counts().reset_index()
    match_counts.columns = ["pair", "count"]
    match_counts[["team1", "team2"]] = pd.DataFrame(match_counts["pair"].tolist(), index=match_counts.index)
    heatmap_data = match_counts.pivot(index="team1", columns="team2", values="count").fillna(0)

    all_teams = pd.concat([match_counts["team1"], match_counts["team2"]])
    top_teams = all_teams.value_counts().head(top_n_teams).index.tolist()

    heatmap_data = heatmap_data.loc[
        heatmap_data.index.intersection(top_teams),
        heatmap_data.columns.intersection(top_teams)
    ]
    return heatmap_data
Cette fonction prépare les données pour la création d'une heatmap des confrontations entre équipes.

3. Fonction de visualisation de la heatmap
def plot_heatmap(data):
    plt.figure(figsize=(12,10)) 
    sns.heatmap(data, annot=True, fmt="g", cmap="Blues", linewidths=0.5) 
    plt.title("Confrontations entre grandes nations de football") 
    plt.xlabel("Pays") 
    plt.ylabel("Pays") 
    plt.tight_layout() 
    plt.show()
Cette fonction génère la heatmap des confrontations entre les équipes les plus présentes.

4. Fonction de visualisation des meilleurs buteurs
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
Cette fonction génère un barplot des 10 meilleurs buteurs (hors buts contre leur camp).

5. Fonction de visualisation des victoires et défaites par pays
def plot_wins_losses(df_results, top_n=15):
    df_results['result'] = df_results.apply(lambda x: 'win' if x['home_score'] > x['away_score'] else ('loss' if x['home_score'] < x['away_score'] else 'draw'), axis=1)
    home_results = df_results.groupby(['home_team', 'result']).size().unstack(fill_value=0)
    home_results = home_results[['win', 'loss']]
    away_results = df_results.groupby(['away_team', 'result']).size().unstack(fill_value=0)
    away_results = away_results[['win', 'loss']]
    team_results = home_results.add(away_results, fill_value=0)
    team_results = team_results.sort_values(by='win', ascending=False).head(top_n)
    team_results.plot(kind='barh', stacked=False, figsize=(12,8))
    plt.title('Victoires et Défaites par équipe', fontsize=14)
    plt.xlabel('Nombre de matchs')
    plt.ylabel('Équipe')
    plt.tight_layout()
    plt.show()
Cette fonction génère un barplot horizontal pour afficher le nombre de victoires et de défaites par pays (limité aux 15 premières équipes selon le nombre de victoires).

ℹ️ Exécution avec le fichier CSV

Voici comment utiliser le code avec les fichiers CSV :

df_results = load_csv("/results.csv")
df_goals = load_csv("/goalscorers.csv")
df_shootouts = load_csv("/shootouts.csv")

if df_results is not None:
    df_results = df_results[df_results["tournament"].isin(["FIFA World Cup", "UEFA Euro"])]
    heatmap = preprocess_heatmap_data(df_results, top_n_teams=15)
    plot_heatmap(heatmap)

if df_goals is not None:
    plot_top_scorers(df_goals)

if df_results is not None:
    plot_wins_losses(df_results, top_n=15)
Le DataFrame est filtré uniquement sur les matchs joués dans les compétitions majeures : FIFA World Cup et UEFA Euro.
