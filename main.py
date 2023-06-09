import csv
import json
import requests
from bs4 import BeautifulSoup

"""
    1. Obtener el maqueteo HTML
     - Si el archivo HTML no existe de forma local, crearlo
     - Si el archivo HTML existe de forma local, obtener su contenido
    2. Obtener la informacion
     - Nombre
     - Categorias
     - Reparto
    3. Generar archivo CSV
"""

URL = 'https://www.imdb.com/calendar/?region=MX'

def get_imdb_content():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.text
    
    return None

def get_imdb_file_local():
    content = None
    try:
        with open('imdb.html', 'r') as file:
            content = file.read()
    except:
        pass
    
    return content
    
def create_imdb_file_local(content):
    
    try:
        with open('imdb.html', 'w') as file:
            file.write(content)
    except:
        pass
    
    return content
    
def get_local_imdb_content():
    content = get_imdb_file_local()
    if content:
        create_imdb_file_local(content)
    return content


def create_movie(tag):
    main_div = tag.find('div', {'class': 'ipc-metadata-list-summary-item__c'})
    sub_div = main_div.find('div', {'class': 'ipc-metadata-list-summary-item__c'})
    name = main_div.div.a.text
    
    
    ul_categories= main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base'
    })
    
    ul_cast = main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base'
    })
    
    categories = [category.span.text for category in ul_categories.find_all('li')]
    
    
    cast = None
    
    cast = [ cast.span.text for cast in ul_cast.find_all('li') ] if ul_cast else []
    
    return (name, categories, cast)


def create_csv_movies_file(movies):
    with open('movies.csv', 'w') as file:
        writer = csv.writer(file, delimiter="-")
        writer.writerow(['name', 'categories', 'cast'])
        
        for movie in movies:
            writer.writerow([
                movie[0],
                ",".join(movie[1]), # Categories
                ",".join(movie[2]), # Cast
            ])   
            
def create_json_movies_file(movies):
    movies_list = [
        {
            'name': movie[0],
                'categories': movie[1],
                'cast': movie[2],
        }
        for movie in movies
    ]
    with open('movies.json', 'w', encoding='latin-1') as file:
        json.dump(movies_list, file, indent=4)

def main():
    content = get_imdb_content()
    
    soup = BeautifulSoup(content, 'html.parser')
    li_tags = soup.find_all('li', {
        'data-testid': 'coming-soon-entry',
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 bpqYIE'
    })
    
    movies = []
    for tag in li_tags:
        movie = create_movie(tag)
        movies.append(movie)
    
    create_csv_movies_file(movies)
    create_json_movies_file(movies)
    
   
if __name__ == '__main__':
    main()