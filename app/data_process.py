import json
import time
import pika
import logging
import requests

from fuzzywuzzy import fuzz, process
from openpyxl import load_workbook

API_URL = "http://localhost:8000/api"

host = 'rat.rmq2.cloudamqp.com'
username = 'qojzruiu'
password = 'apgHrzsZgzGr1SBXE9DwJ3WvhuiS0Raz'

credentials = pika.PlainCredentials(username, password)
# Conexión al servidor RabbitMQ en localhost
connection_params = pika.ConnectionParameters(host, 5672, 'qojzruiu', credentials)

logging.getLogger("pika").setLevel(logging.WARNING)

certs = []


def find_certificates(text, certs):
    found_certs = []
    for cert in certs:
        matches = process.extract(cert, text.split(), limit=2, scorer=fuzz.token_sort_ratio)
        for match in matches:
            if match[1] > 80:  # 80 es un umbral de similitud, puedes ajustarlo según sea necesario
                found_certs.append((cert, match[0], match[1]))
    return found_certs


def basic_process(data_src, data_type, url):
    # print(f'Processing {data_type} from {url}')

    text = ''

    match data_type:
        case 'txt':
            with open(data_src, 'r', encoding='utf-8') as file:
                text = file.read()
            # print(f'Text data: {data}')

        case 'img':
            print('')
            # image = Image.open(data_src)
            # print(f'Image data: {image.format}, {image.size}, {image.mode}')
            # image.show()  # Mostrar la imagen (opcional)

        case 'doc':
            print('')
            # doc = Document(data_src)
            # doc_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            # print(f'Document data: {doc_text}')

        case _:
            print(f'Unsupported data type: {data_type}')

    found_certs = find_certificates(text, certs)

    if found_certs:
        url = requests.get(f"{API_URL}/urls/{url}")

        if url.status_code != 200:
            logging.error(f"Error al obtener la company")
            return

        for cert, match, score in found_certs:
            print(f'Found certificate: {cert} as {match} with score {score}')

            data_cert = requests.get(f"{API_URL}/certificates?name={cert}")

            if data_cert.status_code != 200:
                data_cert = requests.post(f'{API_URL}/certificates',
                                          json={'name': cert})


    #         TODO, guardar certificados




    # time.sleep(.5)


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

    message = json.loads(body)

    data_src = message.get('data_src')
    data_type = message.get('type')
    url = message.get('url')

    basic_process(data_src, data_type, url)

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

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Error de conexión, reintentando en 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    print('Procesando datos en la cola')

    wb = load_workbook('Glosario_Certificaciones.xlsx')
    sheet = wb.active
    # Leer todas las filas de la columna B y convertirlas en un array de certificados
    for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        cell_value = row[0]
        if cell_value is not None:
            certs.append(cell_value)

    consume_messages('data_process')
