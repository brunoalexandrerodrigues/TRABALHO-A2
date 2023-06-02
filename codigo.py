import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaProposicoesDeputado(idDeputado):
    url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{idDeputado}/proposicoes'
    r = requests.get(url)
    proposicoes = r.json()['dados']
    df = pd.DataFrame(proposicoes)
    return df

st.title('Lista de Deputados em Exercício')
st.markdown('<h1 style="text-align: center;">Lista de Deputados em Exercício</h1>', unsafe_allow_html=True)

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)

st.header('Lista de deputados do Rio de Janeiro')
df_rio_de_janeiro = df[df['siglaUf'] == 'RJ']  # Filtra apenas os deputados do Rio de Janeiro

col1, col2 = st.columns([2, 6])
with col1:
    selected_deputado = st.selectbox('Selecione um deputado:', df_rio_de_janeiro['nome'])

with col2:
    selected_deputado_info = df_rio_de_janeiro[df_rio_de_janeiro['nome'] == selected_deputado]

if not selected_deputado_info.empty:
    selected_deputado_info = selected_deputado_info.iloc[0]
    st.markdown('<h2 style="background-color: #ff9900; padding: 10px; border-radius: 5px; color: #ffffff;">Detalhes do Deputado</h2>', unsafe_allow_html=True)
    st.image(selected_deputado_info['urlFoto'], width=130)
    st.write('Nome: ' + selected_deputado_info['nome'])
    st.write('Partido: ' + selected_deputado_info['siglaPartido'])
    st.write('UF: ' + selected_deputado_info['siglaUf'])
    st.write('ID: ' + str(selected_deputado_info['id']))
    st.write('Email: ' + str(selected_deputado_info['email']))

    st.header('Lista de Proposições do Deputado')
    id_deputado = selected_deputado_info['id']
    df_proposicoes = baixaProposicoesDeputado(id_deputado)
    st.dataframe(df_proposicoes[['id', 'ementa']])
