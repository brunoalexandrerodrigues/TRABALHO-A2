import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}&siglaUf=RJ&itens=100"
    r = requests.get(url)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

def baixaProposicoesAutores():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json"
    r = requests.get(url)
    proposicoes_autores = r.json()
    return proposicoes_autores

def baixaProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json"
    r = requests.get(url)
    proposicoes = r.json()
    return proposicoes

st.title("Lista de Deputados do Rio de Janeiro que são Autores de Proposições")

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df_deputados = baixaDeputados(idLegislatura)
df_proposicoes_autores = baixaProposicoesAutores()
df_proposicoes = baixaProposicoes()

deputados_rj_autores = df_deputados[df_deputados["siglaUf"] == "RJ"]
deputados_rj_autores_ids = deputados_rj_autores["id"].tolist()

autores_proposicoes_rj = df_proposicoes_autores[df_proposicoes_autores["idDeputado"].isin(deputados_rj_autores_ids)]
autores_proposicoes_rj_ids = autores_proposicoes_rj["idDeputado"].tolist()

deputados_rj_autores_proposicoes = deputados_rj_autores[deputados_rj_autores["id"].isin(autores_proposicoes_rj_ids)]

if not deputados_rj_autores_proposicoes.empty:
    st.header("Lista de Deputados do Rio de Janeiro que são Autores de Proposições")
    for index, deputado in deputados_rj_autores_proposicoes.iterrows():
        st.markdown(
            '<h2 style="background-color: #ff9900; padding: 10px; border-radius: 5px; color: #ffffff;">Detalhes do Deputado</h2>',
            unsafe_allow_html=True,
        )
        st.image(deputado["urlFoto"], width=130)
        st.write("Nome: " + deputado["nome"])
        st.write("Partido: " + deputado["siglaPartido"])
        st.write("UF: " + deputado["siglaUf"])
        st.write("ID: " + str(deputado["id"]))
        st.write("Email: " + str(deputado["email"]))

        st.header("Lista de Proposições do Deputado")
        proposicoes_deputado = df_proposicoes[df_proposicoes["idAutor"].isin([deputado["id"]])]
        for index, proposicao in proposicoes_deputado.iterrows():
            st.write("ID: ", proposicao["id"])
            st.write("Ementa: ", proposicao["ementa"])
            st.markdown("---")
