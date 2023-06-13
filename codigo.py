#requests para fazer requisições HTTP, streamlit para criar a interface do aplicativo web, e pandas para manipulação de dados tabulares.
import requests
import streamlit as st
import pandas as pd

# scrape_proposals é responsável por fazer a raspagem dos dados das propostas e seus autores a partir de duas URLs fornecidas.
# @st.cache é um decorador fornecido pelo Streamlit que permite o armazenamento em cache dos resultados de uma função
@st.cache
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
                    proposals[nome_autor] = list()

                proposals[nome_autor].append((id_proposal, tipo_autor, sigla_partido_autor, sigla_uf_autor))

    return proposals
#count_proposals recebe o dicionário de propostas como argumento e retorna um novo dicionário com o nome do autor como chave e o número de propostas como valor
def count_proposals(proposals):
    counts = {}

    for author, data in proposals.items():
        counts[author] = len(data)

    return counts

url_proposals = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
url_proposal_authors = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'

proposals = scrape_proposals(url_proposals, url_proposal_authors)

# Filtrando apenas os deputados do RJ.
proposals_rj = {author: data for author, data in proposals.items() if data and any(d[3] == 'RJ' for d in data)}

# Exibindo os dados no Streamlit.
st.title('Proposições dos Deputados do RJ')

# Lista de deputados.
deputies = list(proposals_rj.keys())
selected_deputy = st.selectbox('Selecione o deputado', deputies)

# Dados do deputado selecionado.
st.subheader('Dados do Deputado')
data_deputy = proposals_rj[selected_deputy]
st.write('Nome:', selected_deputy)
st.write('Partido:', data_deputy[0][2])

# Limita o número de proposições para 5.
proposals_limit = 5
top_proposals = data_deputy[:proposals_limit]

# Display para as 5 prpoposições
st.subheader(f'Top {proposals_limit} Proposições')
proposals_set = set()
for proposal in top_proposals:
    if proposal[0] not in proposals_set:
        proposals_set.add(proposal[0])
        url_proposal = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposal[0]}"
        st.markdown(f"[Proposição {proposal[0]}]({url_proposal}) - {proposal[1]}")

# Total número de proposições
total_proposals = count_proposals(proposals_rj)[selected_deputy]
st.write(f"Total Proposições: {total_proposals}")

# Gráfico de número de proposições por deputado
proposal_counts = count_proposals(proposals_rj)
df_proposal_counts = pd.DataFrame.from_dict(proposal_counts, orient='index', columns=['Número de Proposições'])

st.subheader('Número de Proposições por Deputado')
st.bar_chart(df_proposal_counts)
