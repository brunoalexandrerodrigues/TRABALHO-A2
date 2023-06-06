import streamlit as st
import requests

def scrape_proposicoes_autores():
    url = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'
    response = requests.get(url)
    data = response.json()

    autores = []
    for item in data['dados']:
        descricao_tipo = item.get('descricaoTipo', '')
        ementa = item.get('ementa', '')
        ementa_detalhada = item.get('ementaDetalhada', '')
        keywords = item.get('keywords', [])

        autor = {
            'descricaoTipo': descricao_tipo,
            'ementa': ementa,
            'ementaDetalhada': ementa_detalhada,
            'keywords': keywords
        }
        autores.append(autor)

    return autores

def scrape_proposicoes():
    url = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
    response = requests.get(url)
    data = response.json()

    proposicoes = []
    for item in data['dados']:
        descricao_tipo = item.get('descricaoTipo', '')
        ementa = item.get('ementa', '')
        ementa_detalhada = item.get('ementaDetalhada', '')
        keywords = item.get('keywords', [])

        proposicao = {
            'descricaoTipo': descricao_tipo,
            'ementa': ementa,
            'ementaDetalhada': ementa_detalhada,
            'keywords': keywords
        }
        proposicoes.append(proposicao)

    return proposicoes

# Configurações da aplicação Streamlit
st.title("Raspagem de Dados das Proposições")

# Raspagem dos dados
autores = scrape_proposicoes_autores()
proposicoes = scrape_proposicoes()

# Exibição dos resultados no Streamlit
st.header("Proposições Autores")
for autor in autores:
    st.write(autor)

st.header("Proposições")
for proposicao in proposicoes:
    st.write(proposicao)
