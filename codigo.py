!pip install streamlit requests zipfile pandas
import streamlit as st
import pandas as pd
import requests

def baixaDeputados(idLegislatura):
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=' + str(idLegislatura)
    r = requests.get(url)
    deputados = r.json()['dados']
    df = pd.DataFrame(deputados)
    return df

def baixaPropostasGoverno():
    url = 'https://cdn.tse.jus.br/estatistica/sead/odsele/proposta_governo/proposta_governo_2022_RJ.zip'
    response = requests.get(url)
    with open('proposta_governo_2022_RJ.zip', 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile('proposta_governo_2022_RJ.zip', 'r') as zip_ref:
        zip_ref.extractall('proposta_governo_2022_RJ')

def carregaPropostasGoverno():
    csv_file = 'proposta_governo_2022_RJ/proposta_governo_2022_RJ.csv'
    df = pd.read_csv(csv_file)
    return df

def getPropostasDeputado(df_propostas, id_deputado):
    df_deputado = df_propostas[df_propostas['id_cand'] == id_deputado]
    return df_deputado

st.title('Lista de Deputados e Propostas de Governo')

idLegislatura = 57  # Defina aqui o valor da legislatura desejada

df_deputados = baixaDeputados(idLegislatura)

st.header('Lista de Deputados do Rio de Janeiro')
df_rio_de_janeiro = df_deputados[df_deputados['siglaUf'] == 'RJ']  # Filtra apenas os deputados do Rio de Janeiro

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

    st.header('Propostas de Governo do Deputado')

    # Baixa e carrega as propostas de governo
    baixaPropostasGoverno()
    df_propostas_governo = carregaPropostasGoverno()

    # Filtra as propostas de governo pelo ID do deputado selecionado
    df_propostas_deputado = getPropostasDeputado(df_propostas_governo, selected_deputado_info['id'])

    if not df_propostas_deputado.empty:
        st.dataframe(df_propostas_deputado)
    else:
        st.write('Nenhuma proposta de governo encontrada para o deputado selecionado.')
else:
    st.write('Nenhum deputado selecionado.')

