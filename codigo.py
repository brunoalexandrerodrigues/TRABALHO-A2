import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}"
    r = requests.get(url)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

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

st.title("Lista de Deputados Autores de Proposições do Rio de Janeiro")

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)
autores_proposicoes = baixaAutoresProposicoes()
proposicoes = baixaProposicoes()

# Filtra apenas os deputados do Rio de Janeiro que são autores de proposições
df_autores_rj = df[(df["siglaUf"] == "RJ") & (df["id"].isin(autores_proposicoes))]

selected_deputado = st.selectbox("Selecione um deputado:", df_autores_rj["nome"])

selected_deputado_info = df_autores_rj[df_autores_rj["nome"] == selected_deputado]

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
    deputado_proposicoes = autores_proposicoes.get(str(selected_deputado_info["id"]), [])
    for proposta_id in deputado_proposicoes:
        proposta = proposicoes.get(proposta_id)
        if proposta:
            st.write("ID: ", proposta_id)
            st.write("Ementa: ", proposta.get("ementa"))
            st.markdown("---")
