
import json
from uuid import uuid4

import pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MaltaShop Order Service")


@app.get("/")
def home():
    return {"message": "MaltaShop Order Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


class OrderRequest(BaseModel):
    product_name: str
    quantity: int


@app.post("/orders")
def create_order(order: OrderRequest):
    order_id = str(uuid4())

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )

    channel = connection.channel()
    channel.queue_declare(queue="order_events", durable=True)

    event = {
        "event_type": "order.created",
        "order_id": order_id,
        "product_name": order.product_name,
        "quantity": order.quantity
    }

    channel.basic_publish(
        exchange="",
        routing_key="order_events",
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

    return {
        "order_id": order_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": "created"
    }

