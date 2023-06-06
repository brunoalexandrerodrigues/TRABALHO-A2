import streamlit as st
import requests

def get_deputies_data():
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=RJ&ordem=ASC&ordenarPor=nome"
    response = requests.get(url)
    data = response.json()
    deputies = data["dados"]
    return deputies

def get_deputy_proposals(deputy_id):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/proposicoes?ordem=ASC&ordenarPor=id"
    response = requests.get(url)
    data = response.json()
    proposals = []

    if "dados" in data:
        for proposal in data["dados"]:
            proposal_id = proposal["id"]
            ementa_url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposal_id}"
            ementa_response = requests.get(ementa_url)
            ementa_data = ementa_response.json()
            ementa = ementa_data["dados"]["ementa"]
            sigla_tipo = ementa_data["dados"]["siglaTipo"]

            proposals.append((proposal_id, sigla_tipo, ementa))

    return proposals

# Configurações da aplicação Streamlit
st.title("Lista de Deputados do Rio de Janeiro")

deputies = get_deputies_data()

if deputies:
    for deputy in deputies:
        with st.expander(deputy["nome"]):
            st.write("Nome:", deputy["nome"])
            st.write("Partido:", deputy["siglaPartido"])
            st.write("UF:", deputy["siglaUf"])
            st.write("ID:", deputy["id"])
            st.write("Email:", deputy["email"])
            st.write("---")
            st.write("Proposições:")
            proposals = get_deputy_proposals(deputy["id"])
            for proposal_id, sigla_tipo, ementa in proposals:
                st.write("ID da Proposição:", proposal_id)
                st.write("Sigla do Tipo:", sigla_tipo)
                st.write("Ementa:", ementa)
                st.write("---")
else:
    st.write("Nenhum deputado encontrado para o estado do RJ.")
