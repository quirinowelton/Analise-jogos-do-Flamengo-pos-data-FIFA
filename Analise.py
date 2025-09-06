#%%
import pandas as pd

base3 = "campeonato-brasileiro-full.csv"
base7 = "results.csv"

brasileiro = pd.read_csv(base3)
resultados = pd.read_csv(base7)
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
# Merge_asof
resultado = pd.merge_asof(
    jogos_brasil,
    jogos_flamengo,
    on="date",
    direction="forward",
    suffixes=("_brasil", "_flamengo")
)

#%%
resultado['data_formatada_flamengo'] = pd.to_datetime(resultado['data_formatada_flamengo'])
resultado.dropna(subset='vencedor_flamengo', inplace=True)
resultado.drop_duplicates(subset=['data_formatada_flamengo'],keep='last',inplace=True)
resultado.reset_index(drop=True, inplace=True)
resultado['data_formatada_flamengo'] = resultado['data_formatada_flamengo'].dt.strftime('%d/%m%Y')
#%%
resultado['resultado'] = resultado.apply(lambda x: "Vitoria" if x['vencedor_flamengo'] == 'Flamengo' else "Empate" if x['vencedor_flamengo'] == 'Empate' else 'Derrota', axis=1)

'''Poderia usar 
resultado['resultado'] = resultado['vencedor_flamengo'].map({
    'Flamengo': 'Vitoria',
    'Empate': 'Empate'
}).fillna('Derrota')'''

# resultado dos jogos do flamengo apos seleção desde 2003
resultado['resultado'].value_counts(normalize=True)

#%%
# Resultado por ano

resultado['Ano'] = resultado['date'].dt.year
resultado.groupby(['Ano','resultado'])['resultado'].size()

#%%
import matplotlib.pyplot as plt

contagem = resultado.groupby("Ano")["resultado"].value_counts().unstack().fillna(0)

# Plotar gráfico de barras empilhadas
contagem.plot(kind="bar", stacked=True, figsize=(12,6))
plt.title("Resultados por ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade de jogos")
plt.legend(title="Resultado")
plt.show()

#%%
#Gerando grafico de porcentagem de derrota vs Vitoria
# Contagem
contagem = resultado.groupby(["Ano", "resultado"]).size().unstack(fill_value=0)

# Calcular porcentagens relativas
percentuais = contagem.div(contagem.sum(axis=1), axis=0) * 100

# Se quiser, agrupar Vitoria e Outros
percentuais["%Vitoria"] = percentuais.get("Vitoria", 0)
percentuais["%Outros"] = percentuais.get("Empate", 0) + percentuais.get("Derrota", 0)

# Selecionar só as colunas finais
percentuais = percentuais[["%Vitoria", "%Outros"]]

# Plotar gráfico de barras
percentuais.plot(kind="bar", stacked=True, figsize=(12,6))

plt.title("Porcentagem de vitórias e outros resultados por ano")
plt.xlabel("Ano")
plt.ylabel("Porcentagem (%)")
plt.legend(title="Resultado")
plt.show()
#%%
