import requests
import streamlit as st

def scrape_proposals(url_proposals, url_proposal_authors):
    response_proposals = requests.get(url_proposals)
    response_proposal_authors = requests.get(url_proposal_authors)

    data_proposals = response_proposals.json()
    data_proposal_authors = response_proposal_authors.json()

    proposals = {}

    for proposal in data_proposals['dados']:
        id_proposal = proposal['id']

        for author in data_proposal_authors['dados']:
            if author['idProposicao'] == id_proposal:
                tipo_autor = author['tipoAutor']
                nome_autor = author['nomeAutor']
                sigla_partido_autor = author['siglaPartidoAutor']
                sigla_uf_autor = author['siglaUFAutor']

                if nome_autor not in proposals:
                    proposals[nome_autor] = []

                proposals[nome_autor].append({
                    'idProposicao': id_proposal,
                    'tipoAutor': tipo_autor,
                    'siglaPartidoAutor': sigla_partido_autor,
                    'siglaUFAutor': sigla_uf_autor
                })

    return proposals

url_proposals = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
url_proposal_authors = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'

proposals = scrape_proposals(url_proposals, url_proposal_authors)

# Filtrando apenas os deputados do RJ
proposals_rj = {author: data for author, data in proposals.items() if data[0]['siglaUFAutor'] == 'RJ'}

# Exibindo os dados no Streamlit
st.title('Proposições dos Deputados do RJ')

for author, data in proposals_rj.items():
    st.write('---')
    st.subheader('Autor')
    st.write('Nome:', author)
    st.write('Partido:', data[0]['siglaPartidoAutor'])

    st.subheader('Proposições')
    for proposal in data:
        url_proposal = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposal['idProposicao']}"
        st.write(f"[Proposição {proposal['idProposicao']}]({url_proposal})")
