from django.shortcuts import render
from django.conf import settings
import requests
# Create your views here.

def landing_page(request):
    # category es el name del select en el template y popular es uno de los valores por defecto
    category = request.GET.get("category", "popular")
    
    search_query = request.GET.get("search", "")
    
    
    API_KEY = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3/movie/"
    error_message = ""
    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}" 
    else:
        # url es la url de la API con el endpoint de películas populares y el API_KEY. Construye La url con el valor de category
        url = f"{base_url}{category}?api_key={API_KEY}"
    try:
        # con el requests se hace la petición a la API y se obtiene la respuesta
        response = requests.get(url)
        # El results es una lista de diccionarios que contiene la información de las películas, y en caso de que no haya resultados, se asigna una lista vacía
        # raise_for_status() se asegura de que la petición se haya hecho correctamente, si no, lanza una excepción
        response.raise_for_status()
        data = response.json().get("results",[])
    except Exception as e:
        # si hay un error al obtener la información de la API, se asigna una lista vacía a data y se guarda el mensaje de error
        data = []
        error_message = f"Error al obtener información de la API"
        
    # se renderiza el template de la landing page y se envía la información de las películas, la categoría y el mensaje de error
    if request.headers.get("HX-request"):
        return render(request, 'movies/partials/_movie_list.html', {
            'movies':data,
            'category':category,
            'search_query':search_query,
            'error_message':error_message 
        })
    
    return render(request, 'movies/landing.html', {
            'movies':data,
            'category':category,
            'search_query':search_query,
            'error_message':error_message 
        })