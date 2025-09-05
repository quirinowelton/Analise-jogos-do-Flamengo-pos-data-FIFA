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
brasileiro
#%%
nomes.head()
#%%
artilheiros.head() 
#%%
resultados.head()
#%%
decisoes.head()
#%%
#dados do Brasil tratados
resultados_brazil_home = resultados[resultados['home_team'] == "Brazil"]#jogos do Brasil como time da casa
resultados_brazil_away = resultados[resultados['away_team'] == "Brazil"] #Jogos do Brasil como time visitante
jogos_brazil = pd.concat([resultados_brazil_home, resultados_brazil_away]) #Concatenando os jogos do Brasil como time da casa e fora de casa
jogos_brasil = jogos_brazil.copy() #Fazendo uma copia do DF para não alterar o df junto original
jogos_brasil = jogos_brasil.sort_values(by='date', ascending=True) #Ordenando os jogos do Brasil pela data
jogos_brasil = jogos_brasil.reset_index(drop=True) #Resetando
jogos_brasil['date'] = pd.to_datetime(jogos_brasil['date']) #Formatando a coluna existente de data para datetime
jogos_brasil['data_formatada'] = jogos_brasil['date'].dt.strftime('%d/%m/%Y') #Criando uma coluna nova de data formatada %d/%m/%Y
jogos_brasil['vencedor'] = jogos_brasil.apply(lambda x: "Empate" if x['home_score'] == x['away_score'] else ("Brasil" if (x['home_team'] == "Brazil" and x['home_score'] > x['away_score']) or (x['away_team'] == "Brazil" and x['away_score'] > x['home_score']) else "Adversário"), axis=1) #criando uma coluna com resultado 
jogos_brasil.s
#%%
#Pegando dados do Flamengo
brasileiro_filtrado = brasileiro[['data', 'mandante', 'visitante', 'vencedor', 'mandante_Placar', 'visitante_Placar']]
flamengo_mandante = brasileiro_filtrado[brasileiro_filtrado['mandante'] == 'Flamengo']
flamengo_visitante = brasileiro_filtrado[brasileiro_filtrado['visitante'] == 'Flamengo']
juntando_flamengo = pd.concat([flamengo_mandante, flamengo_visitante])
jogos_flamengo = juntando_flamengo.copy()
jogos_flamengo['data'] = pd.to_datetime(jogos_flamengo['data'])
jogos_flamengo['data_formatada'] = jogos_flamengo['data'].dt.strftime('%d/%m/%Y')
jogos_flamengo.sort_values(by='data', ascending=True, inplace= True)
jogos_flamengo.reset_index(drop=True, inplace=True)
jogos_flamengo['vencedor'] = jogos_flamengo['vencedor'].str.replace('Botafogo-RJ', 'Botafogo').str.replace('Athletico-PR', 'Athletico Paranaense').str.replace('Atletico-MG', 'Atletico Mineiro').str.replace('-','Empate')
jogos_flamengo.rename(columns={'data':'date'},inplace=True)
jogos_flamengo['vencedor'].value_counts()
#%%
#Padronizando as colunas 
'''nomes_coluna_brasil = {'date': 'data',
                       'home_team': 'mandante',
                       'away_team': 'visitante',
                       'home_score': 'mandante_Placar',
                       'away_score': 'visitante_Placar'
                       }
jogos_brasil_novo = jogos_brasil.rename(columns=nomes_coluna_brasil)
brasil_formatado = jogos_brasil_novo[['data',
                                    'mandante',
                                    'visitante',
                                    'vencedor',
                                    'mandante_Placar',
                                    'visitante_Placar',
                                    'data_formatada']]

   # Para cada data do Brasil, pegar o primeiro Flamengo após '''
#%%
# Merge_asof
resultado = pd.merge_asof(
    jogos_brasil,
    jogos_flamengo,
    on="date",
    direction="forward",
    suffixes=("_brasil", "_flamengo")
)

#%%
#DEU ERRADO MEU RESULTADO, ACHO QUE PRECISO FILTRAR PARA AMBOS TEREM O MESMO PERIODO DE DATAS