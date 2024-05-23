import io
import json
import os
import sys
import time
import pika
import logging
import requests
import fitz
import cv2

from PIL import Image, ImageFile, UnidentifiedImageError, ImageEnhance
from PIL.Image import Resampling

from text_extract import extract
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

certs_to_find = []

whitelist_chars = " &'(),-.0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ­ÁÂÍÏÑÓáâíïñó"

def find_certificates(text, certs_to_process, nlp):
    # found_certs = []
    # for cert in certs:
    #     matches = process.extract(cert, text.split(), limit=2, scorer=fuzz.token_sort_ratio)
    #     for match in matches:
    #         if match[1] > 80:  # 80 es un umbral de similitud, puedes ajustarlo según sea necesario
    #             found_certs.append((cert, match[0], match[1]))

    return extract(text, certs_to_process, nlp)
    # res_certs = []
    # for cert in certs:
    #     res_certs.append(cert)
    #     print(cert)
    #
    # return res_certs


def get_circular_text_from_img(img_src):
    found_text = ''

    # Read image
    img = cv2.imread(img_src)

    cv2.imwrite('img2.jpg', img)

    # Convert to grayscale, and binarize, especially for removing JPG artifacts
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)[1]

    # Crop center part of image to simplify following contour detection
    h, w = gray.shape
    l = (w - h) // 2
    gray = gray[:, l:l + h]

    # Find (nested) contours (cf. cv2.RETR_TREE) w.r.t. the OpenCV version
    cnts = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Filter and sort contours on area
    cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > 10000]
    cnts = sorted(cnts, key=cv2.contourArea)

    # Remove inner text by painting over using found contours
    # Contour index 1 = outer edge of inner circle
    gray = cv2.drawContours(gray, cnts, 1, 0, cv2.FILLED)

    # If specifically needed, also remove text in the original image
    # Contour index 0 = inner edge of inner circle (to keep inner circle itself)
    img[:, l:l + h] = cv2.drawContours(img[:, l:l + h], cnts, 0, (255, 255, 255),
                                       cv2.FILLED)

    # Rotate image before remapping to polar coordinate space to maintain
    # circular text en bloc after remapping
    gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

    center = (int(h // 2.45), int(h // 2))

    cv2.circle(gray, center, 5, (0, 0, 0), -1)

    cv2.imwrite('img1.jpg', gray)

    max_radius = int(h * 0.5)

    # Actual remapping to polar coordinate space
    gray = cv2.warpPolar(gray, (-1, -1), center, max_radius,
                         cv2.INTER_CUBIC + cv2.WARP_POLAR_LINEAR)
    cv2.imwrite('img2.jpg', gray)
    # Rotate result for OCR
    gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imwrite('img3.jpg', gray)

    # Actual OCR, limiting to capital letters only
    config = f'--psm 6 -c  tessedit_char_whitelist="{whitelist_chars}"'
    text = pytesseract.image_to_string(gray, config=config)

    found_text += text.replace('\n', '').replace('\f', '')

    return found_text


def extract_text(image_src):
    text = ''

    try:
        image = Image.open(image_src)

        try:
            text += get_circular_text_from_img(image_src)
        except Exception as e:
            print(e)

        # Uso de Tesseract con configuraciones mejoradas
        custom_config = f'--oem 3 --psm 6 -c tessedit_char_whitelist="{whitelist_chars}"'
        text += pytesseract.image_to_string(image, lang='eng', config=custom_config)

        print(text)

        return text.strip()

    except Exception as e:
        print(str(e))
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
                    logging.debug(
                        f"No se pudo identificar la imagen en la página {page_num + 1}, imagen {img_index + 1}")
                except IOError as e:
                    logging.debug(
                        f"Error al guardar la imagen en la página {page_num + 1}, imagen {img_index + 1}: {str(e)}")
                except Exception as e:
                    logging.debug(
                        f"Ocurrió un error inesperado al procesar la imagen en la página {page_num + 1}, imagen {img_index + 1}: {str(e)}")

            return text

        except Exception as e:
            logging.debug(f"Ocurrió un error al procesar la página {page_num + 1}: {str(e)}")


def basic_process(data_src, data_type, url, origin_url, certs):
    # print(f'Processing {data_type} from {url}')

    text = ''

    nlp = False

    match data_type:
        case 'txt':
            nlp = True
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

    found_and_filtered_certs = []

    if text:
        found_certs = find_certificates(text, certs, nlp)

        if found_certs:
            response_url = requests.get(f"{API_URL}/urls/{origin_url}")

            if response_url.status_code != 200:
                logging.error(f"Error al obtener la company")
                return

            for cert in found_certs:
                logging.debug(f'Found certificate: {cert} ')

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

                found_and_filtered_certs.append(cert)

                logging.debug(response.text)

        return found_and_filtered_certs

    # time.sleep(.5)


def callback(ch, method, properties, body):
    logging.info(f" [x] Received {body}")

    message = json.loads(body)

    data_src = message.get('data_src')
    data_type = message.get('type')
    url = message.get('url')
    origin_url = message.get('origin_url')

    start_time = time.time()

    basic_process(data_src, data_type, url, origin_url, certs_to_find)

    end_time = time.time()
    elapsed_time = end_time - start_time
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


def unique_characters(strings):
    unique_chars = set()  # Utilizamos un conjunto para evitar caracteres repetidos
    for string in strings:
        for char in string:
            unique_chars.add(char)
            if char.islower():
                unique_chars.add(char.upper())
            elif char.isupper():
                unique_chars.add(char.lower())

    unique_chars.add(' ')

    sorted_chars = sorted(unique_chars)

    return ''.join(sorted_chars)

if __name__ == "__main__":
    logging.info('Procesando datos en la cola')


    wb = load_workbook('Glosario_Certificaciones.xlsx')
    sheet = wb.active
    # Leer todas las filas de la columna B y convertirlas en un array de certificados
    for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        cell_value = row[0]
        if cell_value is not None:
            certs_to_find.append(cell_value)

    # " FECIGZÓacráHyNlT A:­Â(d)o&.8ï'bYK2WzvgXÁâ3ih,SJuÏMO-ejk6L7t9mRqóÍ4fDñÑBín5pPwsUVQ10x"
    whitelist_chars = unique_characters(certs_to_find)

    consume_messages('data_process')
