import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaPropostasDeputado(idDeputado):
    url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?itens=100&idAutor=' + str(idDeputado)
    r = requests.get(url)
    propostas = r.json()['dados']
    df = pd.DataFrame(propostas)
    return df

st.title('Lista de Deputados em Exercício')
st.markdown('<h1 style="text-align: center;">Lista de Deputados em Exercício</h1>', unsafe_allow_html=True)

idLegislatura = st.slider('Escolha de qual legislatura você quer a lista de deputados', 50, 57, 57)

df = baixaDeputados(idLegislatura)

st.header('Lista de deputados')
with st.expander('Mostrar deputados'):
    st.dataframe(df[['nome', 'id']])

st.download_button('Baixar lista de deputados', data=df.to_csv(), file_name='deputados.csv', mime='text/csv')

st.header('Gráficos')
st.subheader('Número de deputados por partido')
st.bar_chart(df['siglaPartido'].value_counts())
st.subheader('Número de deputados por estado')
st.bar_chart(df['siglaUf'].value_counts())

st.header('Lista de deputados do Rio de Janeiro')
df_rio_de_janeiro = df[df['siglaUf'] == 'RJ']
selected_deputado = st.selectbox('Selecione um deputado:', df_rio_de_janeiro['nome'])
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

st.header('Lista de Propostas de Pautas de Governo')
id_deputado = selected_deputado_info['id']
df_propostas = baixaPropostasDeputado(id_deputado)
st.dataframe(df_propostas[['id', 'siglaTipo', 'ementa']])

