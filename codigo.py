import streamlit as st
import pandas as pd
import requests

def baixaAutoresProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-2023.json"
    r = requests.get(url)
    autores_proposicoes = r.json()
    return autores_proposicoes

def baixaProposicoes():
    url = "https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2023.json"
    r = requests.get(url)
    proposicoes = r.json()
    return proposicoes

def baixaDeputados(idLegislatura):
    url = f"https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura={idLegislatura}"
    r = requests.get(url)
    deputados = r.json()["dados"]
    df = pd.DataFrame(deputados)
    return df

st.title("Lista de Deputados do Rio de Janeiro e suas Ementas")

autores_proposicoes = baixaAutoresProposicoes()
proposicoes = baixaProposicoes()
deputados = baixaDeputados(57)

autores_proposicoes_rj = []
for autor in autores_proposicoes:
    if isinstance(autor, dict) and autor.get("siglaUFAutor") == "RJ":
        id_proposicao = autor.get("idProposicao")
        proposicao = next((p for p in proposicoes if p.get("id") == id_proposicao), None)
        if proposicao is not None:
            autor["ementa"] = proposicao.get("ementa")
            autor["uriProposicao"] = proposicao.get("uri")
            autores_proposicoes_rj.append(autor)

df_autores_proposicoes_rj = pd.DataFrame(autores_proposicoes_rj)

deputados_rj = deputados[deputados['siglaUf'] == 'RJ']

df_deputados_rj_autores = pd.merge(df_autores_proposicoes_rj, deputados_rj, left_on="idDeputadoAutor", right_on="id", how="inner")

for index, row in df_deputados_rj_autores.iterrows():
    st.markdown(f"## {row['nomeAutor']} ({row['siglaPartidoAutor']})")
    st.image(row['urlFoto'], width=200)
    st.write(f"**Ementa:** {row['ementa']}")
    st.write(f"**ID da Proposição:** {row['idProposicao']}")
    st.write(f"**URI da Proposição:** {row['uriProposicao']}")
    st.write("---")
