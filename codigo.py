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

# Exemplo de uso:
proposicoes = get_proposicoes(dataInicio="2023-05-01", dataFim="2023-05-31")
for proposta in proposicoes:
    print("ID: ", proposta["id"])
    print("Ementa: ", proposta["ementa"])
    print("-----")
