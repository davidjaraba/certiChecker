import base64
import logging
import os
from urllib.parse import urlparse, urljoin, urlunparse
import requests
from bs4 import BeautifulSoup

from process_queue import send_task

folder = 'resources'

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("aiosqlite").setLevel(logging.WARNING)


def scrap_url(url: str, queue, current_depth, origin_url: str):
    from app.consumer import add_url_to_queue
    base_url = strip_scheme(url)

    parsed_url = urlparse(url)
    if parsed_url.scheme == '':
        url = 'https://' + url
        parsed_url = urlparse(url)

    logging.log(logging.INFO, 'Escaneando url {}'.format(url))
    all_text = ''
    images = []
    new_urls = []
    documents = []
    request = ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        request = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        return all_text, images

    if request.status_code != 200:
        # print('Error accediendo a la url')
        # print(request.status_code)
        # print(request.reason)
        return all_text, images

    soup = BeautifulSoup(request.text, 'html.parser')

    with open(folder + '/' + base_url + '/source.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    texts = soup.stripped_strings
    all_text = ' '.join(texts)

    # Recorrer todos los enlaces de la página
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            # Crear una URL completa para enlaces relativos
            full_url = urljoin(url, href)
            # Analizar la URL completa
            parsed_href = urlparse(full_url)
            # Comprobar si el enlace es del mismo dominio

            # print(href)
            if (parsed_href.netloc == parsed_url.netloc and parsed_href.path != parsed_url.path
                    and parsed_href.path != parsed_url.path + '/'):
                new_urls.append(full_url)
                depth = current_depth - 1
                # print('ASDASDA')
                if depth > 0:
                    add_url_to_queue(queue, full_url, origin_url, depth)
                    # queue.put({'url': full_url, 'depth': depth})

            # Check for document links   , '.doc', '.docx', '.xls', '.xlsx'
            if any(full_url.endswith(ext) for ext in ['.pdf']):
                documents.append(full_url)
                # download_file(full_url, 'documents')

    for img in soup.find_all('img'):
        if not "base64," in img:
            if img.get('src'):
                images.append(get_full_image_url(url, img.get('src')))
            if img.get('data-src'):
                images.append(get_full_image_url(url, img.get('data-src')))
        else:
            images.append(img)

    # base_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)

    return all_text, images, new_urls, documents


def save_text(base_url, filename, content, origin_url):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    send_task(filename, 'txt', base_url, origin_url, 'data_process')


def download_images(base_url, image_urls, folder, origin_url):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, url in enumerate(image_urls):
        # print(url)
        try:
            if not "base64," in url:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    # Asumimos que las imágenes pueden tener extensiones diversas; por defecto usamos .jpg
                    file_path = os.path.join(folder, f'image_{i + 1}{get_extension(url)}')
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    send_task(file_path, 'img', base_url, origin_url, 'data_process')
            else:
                file_path = os.path.join(folder, f'image_{i + 1}.svg')
                image = base64_to_svg_string(url)
                with open(file_path, 'wb') as f:
                    f.write(image)
                send_task(file_path, 'img', base_url, origin_url,'data_process')

        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")


def download_files(base_url, document_urls, directory, origin_url):
    for i, url in enumerate(document_urls):
        try:
            local_filename = os.path.join(directory, url.split('/')[-1])
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Archivo descargado: {local_filename}")

                send_task(local_filename, 'doc', base_url, origin_url, 'data_process')
            except requests.RequestException as e:
                print(f"Error al descargar el archivo: {e}")
        except requests.exceptions as e:
            print(f"Error al descargar el archivo: {e}")


def get_full_image_url(base_url, src_url):
    # Comprueba si la URL de la imagen es absoluta
    if urlparse(src_url).scheme:
        return src_url  # La URL ya es completa
    else:
        # Combina la URL base con la URL relativa de la imagen
        return urljoin(base_url, src_url)


def get_extension(url):
    # Parsear la URL para obtener el componente de la ruta
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Obtener la extensión del archivo desde la última parte de la ruta
    _, ext = os.path.splitext(path)
    return ext


def strip_scheme(url: str):
    # Analizar la URL
    parsed_url = urlparse(url)

    # Construir la URL sin el esquema
    schemeless_url = urlunparse(('', '', parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))

    # Considerar también el netloc (dominio y puerto) si existe
    if parsed_url.netloc:
        schemeless_url = parsed_url.netloc + schemeless_url

    return schemeless_url


def base64_to_svg_string(base64_string):
    # Extraer solo la parte base64 si contiene el prefijo
    if "base64," in base64_string:
        base64_string = base64_string.split('base64,')[1]

    # Decodificar la cadena base64 a bytes
    svg_data = base64.b64decode(base64_string)

    return svg_data


def scrap_process(url: str, queue, depth, origin_url):
    base_url = strip_scheme(url)

    print("Processing", base_url)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(folder + '/' + base_url):
        os.makedirs(folder + '/' + base_url)

    if not os.path.exists(folder + '/' + base_url + '/images'):
        os.makedirs(folder + '/' + base_url + '/images')

    if not os.path.exists(folder + '/' + base_url + '/documents'):
        os.makedirs(folder + '/' + base_url + '/documents')

    all_text, images, new_urls, documents = scrap_url(base_url, queue, depth, origin_url)

    save_text(base_url, folder + '/' + base_url + '/site_text.txt', all_text, origin_url)

    download_images(base_url, images, folder + '/' + base_url + '/images', origin_url)

    download_files(base_url, documents, folder + '/' + base_url + '/documents', origin_url)

    return new_urls
