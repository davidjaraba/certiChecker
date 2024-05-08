import os
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

folder = 'resources'


def scrap_url(url: str):
    print('Escaneando url {}'.format(url))
    request = requests.get('https://'+url)

    if request.status_code != 200:
        print('Error accediendo a la url')
        return

    soup = BeautifulSoup(request.text, 'html.parser')

    with open(folder+'/'+url+'/source.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    texts = soup.stripped_strings
    all_text = ' '.join(texts)

    # images = [img['src'] for img in soup.find_all('img') if img.get('src')]

    images = [get_full_image_url('https://'+url, img['src']) for img in soup.find_all('img') if img.get('src')]

    return all_text, images


def save_text(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def download_images(current_url, image_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, url in enumerate(image_urls):
        print(url)
        try:
            # url_to_download = url

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Asumimos que las imágenes pueden tener extensiones diversas; por defecto usamos .jpg
                file_path = os.path.join(folder, f'image_{i + 1}.jpg')
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")

def get_full_image_url(base_url, src_url):
    # Comprueba si la URL de la imagen es absoluta
    if urlparse(src_url).scheme:
        return src_url  # La URL ya es completa
    else:
        # Combina la URL base con la URL relativa de la imagen
        return urljoin(base_url, src_url)


def scrap_process(url: str):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(folder + '/' + url):
        os.makedirs(folder + '/' + url)

    if not os.path.exists(folder + '/' + url + '/images'):
        os.makedirs(folder + '/' + url + '/images')

    all_text, images = scrap_url(url)

    print(all_text)

    save_text(folder + '/' + url + '/site_text.txt', all_text)

    download_images(url, images, folder + '/' + url + '/images')

    return True
