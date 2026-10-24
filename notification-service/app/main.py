import json
import threading
import time
import pika

from fastapi import FastAPI

app = FastAPI(title="MaltaShop Notification Service")


@app.get("/")
def home():
    return {"message": "Notification Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


def consume_orders():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )

            channel = connection.channel()
            channel.queue_declare(queue="order_events", durable=True)

            def callback(ch, method, properties, body):
                event = json.loads(body)
                print(
                    f"NOTIFICATION SENT | "
                    f"Order ID: {event['order_id']} | "
                    f"Product: {event['product_name']}",
                    flush=True
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue="order_events",
                on_message_callback=callback
            )

            print("Notification Service waiting for orders...", flush=True)
            channel.start_consuming()

        except Exception as error:
            print(f"RabbitMQ connection error: {error}", flush=True)
            time.sleep(5)


@app.on_event("startup")
def start_consumer():
    thread = threading.Thread(target=consume_orders, daemon=True)
    thread.start()