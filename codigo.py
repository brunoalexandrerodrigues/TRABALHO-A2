import streamlit as st
import requests

def scrape_deputies(url_deputies):
    response_deputies = requests.get(url_deputies)
    data_deputies = response_deputies.json()

    deputies = {}

    for item in data_deputies['dados']:
        if item['siglaUf'] == 'RJ':
            deputy_id = item['id']
            deputies[deputy_id] = {
                'nome': item['nome'],
                'siglaPartido': item['siglaPartido'],
                'siglaUF': item['siglaUf']
            }

    return deputies

def scrape_proposals(url_proposals, url_proposal_authors):
    response_proposals = requests.get(url_proposals)
    data_proposals = response_proposals.json()

    response_proposal_authors = requests.get(url_proposal_authors)
    data_proposal_authors = response_proposal_authors.json()

    proposals = {}

    for item in data_proposals['dados']:
        proposal_id = item['id']
        proposals[proposal_id] = {
            'descricaoTipo': item.get('descricaoTipo', ''),
            'ementa': item.get('ementa', ''),
            'ementaDetalhada': item.get('ementaDetalhada', '')
        }

    for item in data_proposal_authors['dados']:
        proposal_id = item['idProposicao']
        deputy_id = item['id']
        if deputy_id in deputies:
            if 'autores' not in proposals[proposal_id]:
                proposals[proposal_id]['autores'] = []
            author = {
                'tipoAutor': item.get('tipoAutor', ''),
                'nomeAutor': item.get('nomeAutor', ''),
                'siglaPartidoAutor': item.get('siglaPartidoAutor', ''),
                'siglaUFAutor': item.get('siglaUFAutor', '')
            }
            proposals[proposal_id]['autores'].append(author)

    return proposals

# Configurações da aplicação Streamlit
st.title("Informações das Proposições e Autores")

# URLs para a raspagem dos dados
url_deputies = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
url_proposals = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
url_proposal_authors = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'

# Realiza a raspagem dos dados
deputies = scrape_deputies(url_deputies)
proposals = scrape_proposals(url_proposals, url_proposal_authors)

# Filtra apenas as proposições dos deputados do RJ
filtered_proposals = {
    proposal_id: proposal
    for proposal_id, proposal in proposals.items()
    if any(author['siglaUFAutor'] == 'RJ' for author in proposal.get('autores', []))
}

# Exibe os dados no Streamlit
st.header("Deputados do RJ")
for deputy_id, deputy in deputies.items():
    st.subheader(deputy['nome'])
    st.write("Partido:", deputy['siglaPartido'])
    st.write("UF:", deputy['siglaUF'])
    st.markdown("---")

st.header("Proposições dos Deputados do RJ")
for proposal_id, proposal in filtered_proposals.items():
    st.subheader(f"Proposição ID: {proposal_id}")
    st.write("Tipo de Proposição:", proposal['descricaoTipo'])
    st.write("Ementa:", proposal['ementa'])
    st.write("Ementa Detalhada:", proposal['ementaDetalhada'])
    st.subheader("Autores:")
    for author in proposal.get('autores', []):
        st.write("Tipo de Autor:", author['tipoAutor'])
        st.write("Nome do Autor:", author['nomeAutor'])
        st.write("Partido do Autor:", author['siglaPartidoAutor'])
        st.write("UF do Autor:", author['siglaUFAutor'])
        st.markdown("---")
