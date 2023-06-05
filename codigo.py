import streamlit as st
import pandas as pd
import requests

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

def baixaTiposProposicao():
    url = "https://dadosabertos.camara.leg.br/api/v2/referencias/tiposProposicao"
    r = requests.get(url)
    tipos_proposicao = []
    if r.status_code == 200:
        try:
            tipos_proposicao = r.json()["dados"]
        except KeyError:
            pass
    return tipos_proposicao

st.title("Lista de Deputados em Exercício")

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)

st.header("Lista de deputados do Rio de Janeiro")
df_rio_de_janeiro = df[df["siglaUf"] == "RJ"]  # Filtra apenas os deputados do Rio de Janeiro

selected_deputado = st.selectbox("Selecione um deputado:", df_rio_de_janeiro["nome"])

selected_deputado_info = df_rio_de_janeiro[df_rio_de_janeiro["nome"] == selected_deputado]

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

st.header("Tipos de Proposição")
tipos_proposicao = baixaTiposProposicao()
for tipo in tipos_proposicao:
    st.write("ID: ", tipo["id"])
    st.write("Descrição: ", tipo["descricao"])
    st.markdown("---")
