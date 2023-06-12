import requests
import streamlit as st
import pandas as pd

def raspe_proposiçoes(url_proposiçoes, url_proposiçoes_autores):
    resposta_proposiçoes = requests.get(url_proposiçoes)
    resposta_proposiçoes_autores = requests.get(url_proposiçoes_autores)

    data_proposiçoes = resposta_proposiçoes.json()
    data_propossiçoes_autores = resposta_proposiçoes_autores.json()

    proposiçoes = {}

    for proposiçoes in data_proposiçoes['dados']:
        id_proposiçoes = proposiçoes['id']

        for autor in data_proposiçoes_autores['dados']:
            if autor['idProposicao'] == id_proposiçoes:
                tipo_autor = autor['tipoAutor']
                nome_autor = autor['nomeAutor']
                sigla_partido_autor = autor['siglaPartidoAutor']
                sigla_uf_autor = autor['siglaUFAutor']

                if nome_autor not in proposiçoes:
                    proposiçoes[nome_autor] = set()

                proposiçoes[nome_autor].add((id_proposiçoes, tipo_autor, sigla_partido_autor, sigla_uf_autor))

    return proposiçoes

def count_proposals(proposiçoes):
    numero = {}

    for autor, data in proposiçoes.items():
        numero[autor] = len(data)

    return numero

url_proposiçoes = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
url_proposiçoes_autores = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'

proposiçoes = raspe_proposiçoes(url_proposiçoes, url_proposiçoes_autores)

# Filtrando apenas os deputados do RJ
proposiçoes_rj = {autor: data for autor, data in proposiçoes.items() if data[0][3] == 'RJ'}

# Exibindo os dados no Streamlit
st.title('Proposições dos Deputados do RJ')

# Lista de deputados
deputados = list(proposiçoes_rj.keys())
selecione_deputado = st.selectbox('Selecione o deputado', deputados)

# Dados do deputado selecionado
st.subheader('Dados do Deputado')
data_deputado = proposiçoes_rj[selecione_deputado]
st.write('Nome:', selecione_deputado)
st.write('Partido:', data_deputado[0][2])

# Proposições do deputado selecionado
st.subheader('Proposições')
proposiçoes_set = set()
for proposiçao in data_deputado:
    if proposiçao[0] not in proposiçoes_set:
        proposiçoes_set.add(proposiçao[0])
        url_proposiçoes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposiçao[0]}"
        st.write(f"[Proposição {proposiçao[0]}] - {proposiçao[1]}")

# Gráfico de número de proposições por deputado
proposiçao_numero = numero_proposiçoes(proposiçoes_rj)
df_proposiçao_numero = pd.DataFrame.from_dict(proposiçao_numero, orient='index', columns=['Número de Proposições'])

st.subheader('Número de Proposições por Deputado')
st.bar_chart(df_proposiçao_numero)
