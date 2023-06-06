import streamlit as st
import requests

def scrape_data(url):
    response = requests.get(url)
    data = response.json()

    results = []
    for item in data['dados']:
        descricao_tipo = item.get('descricaoTipo', '')
        ementa = item.get('ementa', '')
        ementa_detalhada = item.get('ementaDetalhada', '')
        keywords = item.get('keywords', [])

        result = {
            'descricaoTipo': descricao_tipo,
            'ementa': ementa,
            'ementaDetalhada': ementa_detalhada,
            'keywords': keywords
        }
        results.append(result)

    return results

# Configurações da aplicação Streamlit
st.title("Raspagem de Dados das Proposições")

# Raspagem dos dados
url_autores = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'
url_proposicoes = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'

autores = scrape_data(url_autores)
proposicoes = scrape_data(url_proposicoes)

# Exibição dos resultados no Streamlit
st.header("Proposições Autores")
for autor in autores:
    st.write(autor)

st.header("Proposições")
for proposicao in proposicoes:
    st.write(proposicao)
