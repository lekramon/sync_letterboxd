import json
import re
from scraper import get_watchlist
from file_checker import get_local_movies
from fuzzywuzzy import fuzz

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def clean_movie_name(name):
    """Limpa o nome do filme, removendo detalhes extras como ano, qualidade, etc."""
    # Remover tudo que está entre parênteses e colchetes (ano, qualidade, tags)
    name = re.sub(r'[\(\[].*?[\)\]]', '', name)
    # Remover palavras irrelevantes, como qualidade, áudio, etc.
    name = re.sub(r'(bluray|1080p|dual áudio|hd|cam|web|rip)', '', name, flags=re.IGNORECASE)
    # Remover espaços extras e transformar para minúsculas
    name = name.strip().lower()
    return name

def fuzzy_match(title, local_files, threshold=70):
    """Compara o título do filme com os nomes dos arquivos locais e retorna o mais próximo acima de um limiar de confiança"""
    cleaned_title = clean_movie_name(title)  # Limpeza do nome do filme da watchlist
    for local_movie in local_files:
        cleaned_local_movie = clean_movie_name(local_movie)  # Limpeza do nome do arquivo local
        ratio = fuzz.ratio(cleaned_title, cleaned_local_movie)
        print(f"Comparando: '{cleaned_title}' com '{cleaned_local_movie}' - Similaridade: {ratio}%")
        if ratio >= threshold:
            print(f"Correspondência encontrada: {title} -> {local_movie}")
            return local_movie
    return None  # Se não houver correspondência suficiente

def main():
    config = load_config()
    username = config['username']  # Coloque seu nome de usuário do Letterboxd
    movies_folder = config['movies_folder']

    # Obter filmes da watchlist
    print("Obtendo filmes da sua watchlist...")
    watchlist = get_watchlist(username)
    if not watchlist:
        print("Erro ao obter a watchlist.")
        return

    # Obter filmes locais
    print(f"Obtendo filmes da pasta: {movies_folder}...")
    local_movies = get_local_movies(movies_folder)

    # Comparar filmes com fuzzy matching
    print("Comparando filmes...")
    missing_movies = []
    existing_movies = []

    for movie in watchlist:
        matched_movie = fuzzy_match(movie, local_movies)
        if matched_movie:
            existing_movies.append(movie)
        else:
            missing_movies.append(movie)

    # Exibir resultados
    print(f"\nTotal de filmes na sua watchlist: {len(watchlist)}")
    print(f"Filmes que já estão na sua pasta local: {len(existing_movies)}")
    print(f"Filmes que faltam na sua pasta local: {len(missing_movies)}")

    if missing_movies:
        print("\nFilmes que faltam na sua pasta local:")
        for movie in missing_movies:
            print(f"- {movie}")
    else:
        print("\nTodos os filmes da sua watchlist estão na pasta.")

    if existing_movies:
        print("\nFilmes que já estão na sua pasta local:")
        for movie in existing_movies:
            print(f"- {movie}")

if __name__ == "__main__":
    main()
