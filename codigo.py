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

def baixaDeputados(idLegislatura):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}"
    r = requests.get(url)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

st.title("Lista de Deputados do Rio de Janeiro e suas Ementas")

autores_proposicoes = baixaAutoresProposicoes()
proposicoes = baixaProposicoes()
deputados = baixaDeputados(57)

autores_proposicoes_rj = [autor for autor in autores_proposicoes if autor["siglaUFAutor"] == "RJ"]

df_autores_proposicoes_rj = pd.DataFrame(autores_proposicoes_rj)
df_proposicoes = pd.DataFrame(proposicoes)

df_deputados_rj_autores = pd.merge(df_autores_proposicoes_rj, df_deputados, left_on="idProposicao", right_on="id", how="inner")

df_final = pd.merge(df_deputados_rj_autores, df_proposicoes, left_on="idProposicao", right_on="id", how="inner")

for index, row in df_final.iterrows():
    st.markdown(f"## {row['nomeAutor']} ({row['siglaPartidoAutor']})")
    st.image(row['urlFoto'], width=200)
    st.write(f"**Ementa:** {row['ementa']}")
    st.markdown("---")
