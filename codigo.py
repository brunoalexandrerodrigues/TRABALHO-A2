import streamlit as st
import requests

def get_deputies_data(state):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf={state}&ordem=ASC&ordenarPor=nome"
    response = requests.get(url)
    data = response.json()
    deputies = data["dados"]
    return deputies

def get_deputy_ementas(deputy_id):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/proposicoes?ordem=ASC&ordenarPor=id"
    response = requests.get(url)
    data = response.json()
    ementas = [proposicao["ementa"] for proposicao in data["dados"]]
    return ementas

# Configurações da aplicação Streamlit
st.title("Dados dos Deputados")
state = st.selectbox("Selecione o estado", ["RJ", "SP", "MG"])  # Você pode adicionar mais estados aqui

deputies = get_deputies_data(state)

if deputies:
    selected_deputy = st.selectbox("Selecione o deputado", deputies, format_func=lambda deputy: deputy["nome"])
    deputy_id = selected_deputy["id"]
    ementas = get_deputy_ementas(deputy_id)

    st.subheader("Dados do Deputado")
    st.write("Nome:", selected_deputy["nome"])
    st.write("Partido:", selected_deputy["siglaPartido"])
    st.write("Ementas das Proposições:")
    for ementa in ementas:
        st.write("-", ementa)
else:
    st.write("Não foram encontrados deputados para o estado selecionado.")
