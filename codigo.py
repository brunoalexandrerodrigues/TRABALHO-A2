import streamlit as st
import pandas as pd
import requests

def baixaAutoresProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json"
    r = requests.get(url)
    autores_proposicoes = r.json()
    return autores_proposicoes

def baixaProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json"
    r = requests.get(url)
    proposicoes = r.json()
    return proposicoes

def baixaDeputados():
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
    params = {
        "siglaUf": "RJ",
        "itens": 100
    }
    r = requests.get(url, params=params)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

st.title("Lista de Deputados do Rio de Janeiro e suas Ementas")

autores_proposicoes = baixaAutoresProposicoes()
proposicoes = baixaProposicoes()
deputados = baixaDeputados()

deputados_rj_autores = []
for proposta in proposicoes:
    if proposta.get("siglaUFAutor") == "RJ":
        id_proposicao = proposta.get("id")
        autores_proposicao = [autor for autor in autores_proposicoes if autor.get("idProposicao") == id_proposicao]
        for autor in autores_proposicao:
            id_autor = autor.get("idAutor")
            deputado_rj = deputados[deputados["id"] == id_autor]
            if not deputado_rj.empty:
                deputados_rj_autores.append(deputado_rj.iloc[0])

df_deputados_rj_autores = pd.DataFrame(deputados_rj_autores)
df_proposicoes = pd.DataFrame(proposicoes)

df_final = pd.merge(df_deputados_rj_autores, df_proposicoes, left_on="id", right_on="id", how="inner")

for index, row in df_final.iterrows():
    st.markdown(f"## {row['nome']} ({row['siglaPartido']})")
    st.image(row['urlFoto'], width=200)
    st.write(f"**Ementa:** {row['ementa']}")
    st.markdown("---")
