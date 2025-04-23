import requests
from bs4 import BeautifulSoup


def get_watchlist(username):
    base_url = f'https://letterboxd.com/{username}/watchlist/'
    page = 1
    watchlist = []

    while True:
        # Adiciona o número da página à URL
        url = f"{base_url}page/{page}/"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar a página {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos os filmes na página atual
        movies = soup.find_all('div', class_='film-poster')

        if not movies:
            print("Não há mais filmes ou página vazia. Terminando...")
            break

        for movie in movies:
            title = movie.find('img')['alt']
            watchlist.append(title)

        # Tentar avançar para a próxima página
        page += 1

    # Contar o número de filmes na watchlist
    print(f"Total de filmes na sua watchlist: {len(watchlist)}")

    return watchlist
