import streamlit as st
import requests

def get_deputies_data():
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=RJ&ordem=ASC&ordenarPor=nome"
    response = requests.get(url)
    data = response.json()
    deputies = data["dados"]
    return deputies

def get_deputies_list(deputies):
    deputies_list = [deputy["nome"] for deputy in deputies]
    return deputies_list

def get_deputies_by_party(deputies):
    party_counts = {}
    for deputy in deputies:
        party = deputy["siglaPartido"]
        if party in party_counts:
            party_counts[party] += 1
        else:
            party_counts[party] = 1
    return party_counts

# Configurações da aplicação Streamlit
st.title("Lista de Deputados do Rio de Janeiro")

deputies = get_deputies_data()

show_deputies_list = st.button("Mostrar lista de deputados")

if show_deputies_list:
    deputies_list = get_deputies_list(deputies)
    st.write("Lista de Deputados do RJ:")
    for deputy_name in deputies_list:
        st.write(deputy_name)

party_counts = get_deputies_by_party(deputies)
st.subheader("Número de deputados por partido")
st.bar_chart(party_counts)
