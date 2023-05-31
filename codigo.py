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

st.title('Lista de Deputados do Rio de Janeiro')

idLegislatura = 57  # Considerando a legislatura atual
df_deputados = baixaDeputados(idLegislatura)

# Filtra a lista apenas para o estado do Rio de Janeiro
df_rio_de_janeiro = df_deputados[df_deputados['siglaUf'] == 'RJ']

# Filtrar por gênero
genero = st.radio('Filtrar por gênero:', ('Todos', 'Homens', 'Mulheres'))

if genero == 'Homens':
    df_rio_de_janeiro = df_rio_de_janeiro[df_rio_de_janeiro['sexo'] == 'M']
elif genero == 'Mulheres':
    df_rio_de_janeiro = df_rio_de_janeiro[df_rio_de_janeiro['sexo'] == 'F']

# Exibe a lista de deputados do Rio de Janeiro filtrada
st.header('Lista de Deputados do Rio de Janeiro')
st.write(df_rio_de_janeiro)

# Seleciona um deputado para visualizar suas propostas de pautas de governo
selected_deputado = st.selectbox('Selecione um deputado:', df_rio_de_janeiro['nome'])

# Obtém as propostas de pautas de governo do deputado selecionado
deputado_id = df_rio_de_janeiro[df_rio_de_janeiro['nome'] == selected_deputado]['id'].values[0]
df_propostas = baixaPropostasDeputado(deputado_id)

# Exibe a lista de propostas de pautas de governo do deputado selecionado
st.header('Propostas de Pautas de Governo de {}'.format(selected_deputado))
st.write(df_propostas)

