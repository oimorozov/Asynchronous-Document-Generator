from faststream.rabbit import RabbitBroker

from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)

@broker.subscriber(queue="files")
async def sub_msg(data: str):
    print(f"INFO: received message. Content: {data}")
