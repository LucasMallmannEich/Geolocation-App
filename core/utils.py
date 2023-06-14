import requests
from random import randint
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geoip2 import geoip2

# Endereço da plataforma Yelp que utilizamos para realizar buscas de acordo com nossos paramêtros.
YELP_SEARCH_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'


# Iremos utilizar palavras chaves em determinadas cidades.
# Por exemplo, keyword=pizzaria, location=SaoPaulo (para pesquisar pizzarias em São Paulo).
def yelp_search(keyword=None, location=None):
    headers = {"Authorization": "Bearer " + settings.YELP_API_KEY}  # Autorização necessária para realiza busca no Yelp.

    if keyword and location:
        params = {"term": keyword, "location": location}  # Busca caso seja passado parâmetros.
    else:
        params = {"term": "Pizzaria", "location": "Porto Alegre"}  # Busca padrão caso não for passado parâmetros.

    r = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)

    return r.json()  # Envia a resposta do request em formato json.


def get_client_data():
    g = GeoIP2()  # A partir desse objeto que podemos encontrar valores de endereços.
    ip = get_random_ip()  # Gera um número IP aleatório.
    try:
        return g.city(ip)  # Retorna a localidade (cidade, país, etc) através do endereço de IP.
    except geoip2.errors.AddressNotFoundError:
        return None  # Caso ele não encontre a localidade através do IP.


def get_random_ip():
    # Gera uma lista com 4 números aleatórios de 0 até 255.
    # Essa lista torna-se uma string, onde cada número está separado por ponto.
    return '.'.join([str(randint(0, 255)) for x in range(4)])
