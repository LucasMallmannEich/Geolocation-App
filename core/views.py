from django.shortcuts import render
from django.views.generic import View
from core.utils import yelp_search, get_client_data


class IndexView(View):

    def get(self, request, *args, **kwargs):
        items = []
        city = None

        # Até alguma cidade ser gerada.
        while not city:
            r = get_client_data()
            if r:
                city = r['city']
        location = city

        # Usuário informando palavra chave e cidade.
        q = request.GET.get('key', None)
        loc = request.GET.get('loc', None)

        # Context que envia a cidade, mas não realiza a busca.
        context = {
            'city': location,
            'busca': False
        }

        # Caso o usuário informou a cidade, "loc" existirá, logo, atualizamos a variável "location".
        if loc:
            location = loc
        # Caso o usuário informou uma palavra chave, realizamos a busca.
        if q:
            items = yelp_search(keyword=q, location=location)  # Busca no Yelp.
            # Context enviado.
            context = {
                'items': items,
                'city': location,
                'busca': True
            }

        return render(request, 'index.html', context)