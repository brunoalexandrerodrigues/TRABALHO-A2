import streamlit as st
import pandas as pd
import requests

def baixaAutoresProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json"
    r = requests.get(url)
    autores_proposicoes = r.json()["dados"]
    return autores_proposicoes

def baixaDeputados(idLegislatura):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}"
    r = requests.get(url)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

def baixaProposicoesDeputado(idDeputado):
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?itens=100&autorId={idDeputado}&ordem=ASC&ordenarPor=id"
    r = requests.get(url)
    proposicoes = []
    if r.status_code == 200:
        try:
            proposicoes = r.json()["dados"]
        except KeyError:
            pass
    return proposicoes

st.title("Lista de Deputados do Rio de Janeiro que são Autores de Proposições")

autores_proposicoes = baixaAutoresProposicoes()

autores_proposicoes_rj = [autor for autor in autores_proposicoes if autor["dados"]["siglaUf"] == "RJ"]

deputados_rj_ids = [autor["idAutor"] for autor in autores_proposicoes_rj]

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)

df_deputados_rj_autores = df[df["id"].isin(deputados_rj_ids)]

selected_deputado = st.selectbox("Selecione um deputado:", df_deputados_rj_autores["nome"])

selected_deputado_info = df_deputados_rj_autores[df_deputados_rj_autores["nome"] == selected_deputado]

if not selected_deputado_info.empty:
    selected_deputado_info = selected_deputado_info.iloc[0]
    st.markdown(
        '<h2 style="background-color: #ff9900; padding: 10px; border-radius: 5px; color: #ffffff;">Detalhes do Deputado</h2>',
        unsafe_allow_html=True,
    )
    st.image(selected_deputado_info["urlFoto"], width=130)
    st.write("Nome: " + selected_deputado_info["nome"])
    st.write("Partido: " + selected_deputado_info["siglaPartido"])
    st.write("UF: " + selected_deputado_info["siglaUf"])
    st.write("ID: " + str(selected_deputado_info["id"]))
    st.write("Email: " + str(selected_deputado_info["email"]))

    st.header("Lista de Proposições do Deputado")
    proposicoes = baixaProposicoesDeputado(selected_deputado_info["id"])
    for proposta in proposicoes:
        st.write("ID: ", proposta["id"])
        st.write("Ementa: ", proposta["ementa"])
        st.markdown("---")
