import streamlit as st
import requests

def scrape_deputies(url):
    response = requests.get(url)
    data = response.json()
    deputies = []

    for item in data['dados']:
        if item['siglaUf'] == 'RJ':
            deputy = {
                'nome': item['nome'],
                'id': item['id']
            }
            deputies.append(deputy)

    return deputies

def scrape_proposals(url):
    response = requests.get(url)
    data = response.json()
    proposals = []

    for item in data['dados']:
        if item['siglaUf'] == 'RJ':
            proposal = {
                'descricaoTipo': item.get('descricaoTipo', ''),
                'ementa': item.get('ementa', ''),
                'ementaDetalhada': item.get('ementaDetalhada', ''),
                'keywords': item.get('keywords', [])
            }
            proposals.append(proposal)

    return proposals

# Configurações da aplicação Streamlit
st.title("Informações dos Deputados e Proposições")

# Raspagem dos dados
url_deputies = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
url_proposals = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'

deputies = scrape_deputies(url_deputies)
proposals = scrape_proposals(url_proposals)

# Exibição dos deputados
st.header("Deputados do RJ")
selected_deputy = st.selectbox("Selecione um deputado", [deputy['nome'] for deputy in deputies])
deputy_id = next((deputy['id'] for deputy in deputies if deputy['nome'] == selected_deputy), None)

if deputy_id:
    st.subheader("Proposições do Deputado")
    deputy_proposals = [proposal for proposal in proposals if proposal['id'] == deputy_id]

    if deputy_proposals:
        for proposal in deputy_proposals:
            st.write(proposal)
    else:
        st.write("Nenhuma proposição encontrada para o deputado selecionado.")
else:
    st.write("Nenhum deputado selecionado.")

