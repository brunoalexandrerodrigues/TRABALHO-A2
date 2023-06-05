import streamlit as st
import requests

def get_proposicoes(dataInicio=None, dataFim=None, id=None, ano=None, dataApresentacaoInicio=None, dataApresentacaoFim=None, idAutor=None, autor=None):
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "dataInicio": dataInicio,
        "dataFim": dataFim,
        "id": id,
        "ano": ano,
        "dataApresentacaoInicio": dataApresentacaoInicio,
        "dataApresentacaoFim": dataApresentacaoFim,
        "idAutor": idAutor,
        "autor": autor
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["dados"]
    else:
        return []

def main():
    st.title("Consulta de Proposições na Câmara dos Deputados")
    st.write("Este aplicativo consulta as proposições na Câmara dos Deputados.")

    dataInicio = st.text_input("Data de Início (formato: AAAA-MM-DD)")
    dataFim = st.text_input("Data de Fim (formato: AAAA-MM-DD)")
    idAutor = st.text_input("ID do Autor")
    autor = st.text_input("Nome do Autor")
    
    if st.button("Buscar Proposições"):
        proposicoes = get_proposicoes(dataInicio=dataInicio, dataFim=dataFim, idAutor=idAutor, autor=autor)
        
        if proposicoes:
            st.write(f"Foram encontradas {len(proposicoes)} proposições:")
            for proposta in proposicoes:
                st.write(f"ID: {proposta['id']}")
                st.write(f"Ementa: {proposta['ementa']}")
                st.write("-----")
        else:
            st.write("Nenhuma proposição encontrada.")

if __name__ == "__main__":
    main()
