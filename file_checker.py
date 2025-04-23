import os
import json

def get_local_movies(folder_path):
    movies = os.listdir(folder_path)
    return [movie.lower() for movie in movies]  # Considera todos os nomes em minúsculas para comparação

def compare_movies(watchlist, local_movies):
    missing_movies = [movie for movie in watchlist if movie.lower() not in local_movies]
    return missing_movies
