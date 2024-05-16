import logging
import time

import pika
import json

host = 'rat.rmq2.cloudamqp.com'
username = 'qojzruiu'
password = 'apgHrzsZgzGr1SBXE9DwJ3WvhuiS0Raz'
max_retries = 5

credentials = pika.PlainCredentials(username, password)
# Conexión al servidor RabbitMQ en localhost
connection_params = pika.ConnectionParameters(host, 5672, 'qojzruiu', credentials)

logging.getLogger("pika").setLevel(logging.WARNING)


def send_task(data_src, data_type, url, origin_url, queue='default'):
    data_src = data_src.replace("//", "/")
    data_src = data_src.replace("\\", "/")

    retries = 0
    while retries < max_retries:
        try:
            # Conectar al servidor RabbitMQ
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()

            # Declarar una cola
            channel.queue_declare(queue=queue)

            # Crear el mensaje con atributos adicionales
            message_body = {
                'data_src': data_src,
                'type': data_type,
                'url': url,
                'origin_url': origin_url
            }

            # Convertir el mensaje a formato JSON
            message_json = json.dumps(message_body)

            # Publicar el mensaje en la cola
            channel.basic_publish(exchange='',
                                  routing_key=queue,
                                  body=message_json)

            print(f" [x] Sent '{message_json}'")

            # Cerrar la conexión
            connection.close()
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error de conexión, reintentando en 5 segundos... ({retries + 1}/{max_retries})")
            retries += 1
            time.sleep(5)
        except Exception as e:
            print(f"Error inesperado: {e}")
            break
