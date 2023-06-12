import requests
import streamlit as st
import pandas as pd

def raspe_proposições(url_proposições, url_proposições_autores):
    resposta_proposições = requests.get(url_proposições)
    resposta_proposições_autores = requests.get(url_proposições_autores)

    data_proposições = resposta_proposições.json()
    data_proposições_autores = resposta_proposições_autores.json()

    proposições = {}

    for proposição in data_proposições['dados']:
        id_proposição = proposição['id']

        for autor in data_proposições_autores['dados']:
            if autor['idProposicao'] == id_proposição:
                tipo_autor = autor['tipoAutor']
                nome_autor = autor['nomeAutor']
                sigla_partido_autor = autor['siglaPartidoAutor']
                sigla_uf_autor = autor['siglaUFAutor']

                if nome_autor not in proposições:
                    proposições[nome_autor] = set()

                proposições[nome_autor].add((id_proposição, tipo_autor, sigla_partido_autor, sigla_uf_autor))

    return proposições

def count_proposições(proposições):
    count = {}

    for autor, data in proposições.items():
        count[autor] = len(data)

    return count

url_proposições = 'https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json'
url_proposições_autores = 'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json'

proposições = raspe_proposições(url_proposições, url_proposições_autores)

# Filtrando apenas os deputados do RJ
proposições_rj = {}

for autor, data in proposições.items():
    if data and len(data) > 0 and data[0][3] == 'RJ':
        proposições_rj[autor] = data

# Exibindo os dados no Streamlit
st.title('Proposições dos Deputados do RJ')

# Lista de deputados
deputados = list(proposições_rj.keys())
selecione_deputado = st.selectbox('Selecione o deputado', deputados)

# Dados do deputado selecionado
st.subheader('Dados do Deputado')
data_deputado = proposições_rj[selecione_deputado]
st.write('Nome:', selecione_deputado)
st.write('Partido:', data_deputado[0][2])

# Proposições do deputado selecionado
st.subheader('Proposições')
proposições_set = set()
for proposição in data_deputado:
    if proposição[0] not in proposições_set:
        proposições_set.add(proposição[0])
        url_proposições = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{proposição[0]}"
        st.write(f"[Proposição {proposição[0]}] - {proposição[1]}")

# Gráfico de número de proposições por deputado
proposição_count = count_proposições(proposições_rj)
df_proposição_count = pd.DataFrame.from_dict(proposição_count, orient='index', columns=['Número de Proposições'])

st.subheader('Número de Proposições por Deputado')
st.bar_chart(df_proposição_count)
