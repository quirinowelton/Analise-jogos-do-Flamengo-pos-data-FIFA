#%%
import pandas as pd

base1 = "campeonato-brasileiro-cartoes.csv"
base2 = "campeonato-brasileiro-estatisticas-full.csv"
base3 = "campeonato-brasileiro-full.csv"
base4 = "campeonato-brasileiro-gols.csv"
base5 = "former_names.csv"
base6 = "goalscorers.csv"
base7 = "results.csv"
base8 = "shootouts.csv"

cartoes = pd.read_csv(base1)
estatisticas = pd.read_csv(base2)
brasileiro = pd.read_csv(base3)
gols = pd.read_csv(base4)
nomes = pd.read_csv(base5)
artilheiros = pd.read_csv(base6)
resultados = pd.read_csv(base7)
decisoes = pd.read_csv(base8)
#%%
cartoes.head()
#%%
gols.head()
#%%
estatisticas.head()
#%%
brasileiro.head()
#%%
nomes.head()
#%%
artilheiros.head() 
#%%
resultados.head()
#%%
decisoes.head()
#%%
resultados_brazil_home = resultados[resultados['home_team'] == "Brazil"]#jogos do Brasil como time da casa
resultados_brazil_away = resultados[resultados['away_team'] == "Brazil"] #Jogos do Brasil como time visitante
jogos_brazil = pd.concat([resultados_brazil_home, resultados_brazil_away]) #Concatenando os jogos do Brasil como time da casa e fora de casa
jogos_brasil = jogos_brazil.copy()
jogos_brasil = jogos_brasil.sort_values(by='date', ascending=True) #Ordenando os jogos do Brasil pela data
jogos_brasil = jogos_brasil.reset_index(drop=True) #Resetando
jogos_brasil['date'] = pd.to_datetime(jogos_brasil['date']) #Formatando a coluna existente de data para datetime
jogos_brasil['data_formatada'] = jogos_brasil['date'].dt.strftime('%d/%m/%Y') #Criando uma coluna nova de data formatada %d/%m/%Y
jogos_brasil['ganhador'] = jogos_brasil.apply(lambda x: "Empate" if x['home_score'] == x['away_score'] else ("Brasil" if (x['home_team'] == "Brazil" and x['home_score'] > x['away_score']) or (x['away_team'] == "Brazil" and x['away_score'] > x['home_score']) else "Adversário"), axis=1) #criando uma coluna com resultado 