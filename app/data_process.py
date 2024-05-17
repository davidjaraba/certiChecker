import io
import json
import os
import sys
import time
import pika
import logging
import requests
import fitz

from PIL import Image, ImageFile, UnidentifiedImageError
import pytesseract

from fuzzywuzzy import fuzz, process
from openpyxl import load_workbook

API_URL = "http://localhost:8000/api"

host = 'rat.rmq2.cloudamqp.com'
username = 'qojzruiu'
password = 'apgHrzsZgzGr1SBXE9DwJ3WvhuiS0Raz'

credentials = pika.PlainCredentials(username, password)
# Conexión al servidor RabbitMQ en localhost
connection_params = pika.ConnectionParameters(host, 5672, 'qojzruiu', credentials)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logging.getLogger("pika").setLevel(logging.WARNING)

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\T031105\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# ImageFile.LOAD_TRUNCATED_IMAGES = True

certs = []


def find_certificates(text):
    found_certs = []
    for cert in certs:
        matches = process.extract(cert, text.split(), limit=2, scorer=fuzz.token_sort_ratio)
        for match in matches:
            if match[1] > 80:  # 80 es un umbral de similitud, puedes ajustarlo según sea necesario
                found_certs.append((cert, match[0], match[1]))
    return found_certs


def extract_text(image_src):
    text = ''

    try:
        image = Image.open(image_src)
        text = pytesseract.image_to_string(image, lang='eng')

        logging.debug('TEXTO ENCONTRADO ')
        logging.debug(text)

        return text.strip()

    except Exception as e:
        logging.debug(f"Ocurrió un error inesperado: {str(e)}")


def extract_text_from_pdf(src):
    try:
        # Abrir el archivo PDF
        pdf_document = fitz.open(src)
    except Exception as e:
        logging.debug(f"Error al abrir el archivo PDF: {str(e)}")
        return

    for page_num in range(pdf_document.page_count):
        try:
            page = pdf_document.load_page(page_num)

            # Extraer y mostrar el texto
            text = page.get_text("text")
            # print(f"Texto en la página {page_num + 1}:\n{text}\n")

            # Extraer y guardar imágenes
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        # Verificar si los bytes extraídos son una imagen válida
                        image = Image.open(io.BytesIO(image_bytes))

                        image_text = pytesseract.image_to_string(image, lang='eng')

                        logging.debug('TEXTO ENCONTRADO EN PDF ')
                        logging.debug(image_text)

                        text += ' ' + image_text

                        # image_path = f"pagina{page_num + 1}_imagen{img_index + 1}.{image_ext}"

                        # if not os.path.exists(dir_to_save):
                        #     os.makedirs(dir_to_save)

                        # image.save(dir_to_save+'/'+image_path)

                        # print(
                        #     f"Imagen extraída en la página {page_num + 1}, imagen {img_index + 1} guardada como {image_path}")
                except UnidentifiedImageError:
                    logging.debug(f"No se pudo identificar la imagen en la página {page_num + 1}, imagen {img_index + 1}")
                except IOError as e:
                    logging.debug(f"Error al guardar la imagen en la página {page_num + 1}, imagen {img_index + 1}: {str(e)}")
                except Exception as e:
                    logging.debug(
                        f"Ocurrió un error inesperado al procesar la imagen en la página {page_num + 1}, imagen {img_index + 1}: {str(e)}")

            return text

        except Exception as e:
            logging.debug(f"Ocurrió un error al procesar la página {page_num + 1}: {str(e)}")


def basic_process(data_src, data_type, url, origin_url):
    # print(f'Processing {data_type} from {url}')

    text = ''

    match data_type:
        case 'txt':
            with open(data_src, 'r', encoding='utf-8') as file:
                text = file.read()

        case 'img':
            text = extract_text(data_src)

        case 'doc':
            _, file_extension = os.path.splitext(data_src)

            if file_extension == '.pdf':
                text = extract_text_from_pdf(data_src)


            # doc = Document(data_src)
            # doc_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            # print(f'Document data: {doc_text}')

        case _:
            logging.debug(f'Unsupported data type: {data_type}')

    if text:
        found_certs = find_certificates(text)

        if found_certs:
            response_url = requests.get(f"{API_URL}/urls/{origin_url}")

            if response_url.status_code != 200:
                logging.error(f"Error al obtener la company")
                return

            for cert, match, score in found_certs:
                logging.debug(f'Found certificate: {cert} as {match} with score {score}')

                response_cert = requests.get(f"{API_URL}/certificates?name={cert}")

                data_cert = response_cert.json()

                if data_cert:
                    data_cert = data_cert[0]
                else:
                    data_cert = requests.post(f'{API_URL}/certificates',
                                              json={'name': cert}).json()

                data_type = data_type.upper()

                response = requests.post(f'{API_URL}/resources',
                                         json={'type': data_type, 'url_id': origin_url, 'path_file': data_src,
                                               'full_url': url, 'certificate_id': data_cert.get('id')})

                logging.debug(response.text)

    # time.sleep(.5)


def callback(ch, method, properties, body):
    logging.info(f" [x] Received {body}")

    message = json.loads(body)

    data_src = message.get('data_src')
    data_type = message.get('type')
    url = message.get('url')
    origin_url = message.get('origin_url')

    start_time = time.time()  # Iniciar el cronómetro

    basic_process(data_src, data_type, url, origin_url)

    end_time = time.time()  # Detener el cronómetro
    elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido
    logging.info(f"Tiempo transcurrido en basic_process: {elapsed_time:.2f} segundos")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages(queue='default'):
    while True:
        try:
            # Conectar al servidor RabbitMQ
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()

            # Declarar una cola llamada 'hello'
            channel.queue_declare(queue=queue)

            # Suscribirse a la cola
            channel.basic_consume(queue=queue,
                                  on_message_callback=callback,
                                  auto_ack=False)

            logging.info(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Error de conexión, reintentando en 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    logging.info('Procesando datos en la cola')

    wb = load_workbook('Glosario_Certificaciones.xlsx')
    sheet = wb.active
    # Leer todas las filas de la columna B y convertirlas en un array de certificados
    for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        cell_value = row[0]
        if cell_value is not None:
            certs.append(cell_value)

    consume_messages('data_process')
