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
    url = f'https://dadosabertos.camara.leg.br/api/v2/proposicoes?itens=100&autorId={idDeputado}&ordem=ASC&ordenarPor=id'
    r = requests.get(url)
    proposicoes = r.json()['dados']
    df = pd.DataFrame(proposicoes)
    return df

def baixaPautasGoverno():
    url = 'https://cdn.tse.jus.br/estatistica/sead/odsele/proposta_governo/proposta_governo_2022_RJ.zip'
    r = requests.get(url)
    with open('proposta_governo_2022_RJ.zip', 'wb') as f:
        f.write(r.content)
    st.success('Arquivo baixado com sucesso.')

# Título e seleção da legislatura
st.title('Lista de Deputados em Exercício')
idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df = baixaDeputados(idLegislatura)

# Filtrar deputados do Rio de Janeiro
df_rio_de_janeiro = df[df['siglaUf'] == 'RJ']

# Seleção do deputado
selected_deputado = st.selectbox('Selecione um deputado:', df_rio_de_janeiro['nome'])

# Informações do deputado selecionado
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

    # Botão para baixar as pautas de governo
    if st.button('Baixar Pautas de Governo'):
        baixaPautasGoverno()

    # Lista de proposições do deputado
    st.header('Lista de Proposições do Deputado')
    id_deputado = selected_deputado_info['id']
    df_proposicoes = baixaProposicoesDeputado(id_deputado)
    st.dataframe(df_proposicoes[['id', 'ementa']])
