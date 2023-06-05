import pandas as pd
import requests

# Obtendo os dados dos deputados do RJ
url_deputados_rj = "https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=RJ"
response_deputados_rj = requests.get(url_deputados_rj)
data_deputados_rj = response_deputados_rj.json()
deputados_rj = pd.DataFrame(data_deputados_rj["dados"])

# Obtendo os dados das proposições do RJ
url_proposicoes_rj = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaUfAutor=RJ"
response_proposicoes_rj = requests.get(url_proposicoes_rj)
data_proposicoes_rj = response_proposicoes_rj.json()
proposicoes_rj = pd.DataFrame(data_proposicoes_rj["dados"])

# Filtrando as colunas desejadas do DataFrame de proposições
df_autores_proposicoes_rj = proposicoes_rj[["id", "ementa"]]

# Realizando a junção dos DataFrames
df_deputados_rj_autores = pd.merge(df_autores_proposicoes_rj, deputados_rj, left_on="idDeputadoAutor", right_on="idDeputado", how="inner")

# Exibindo o resultado
df_deputados_rj_autores
