from faststream.rabbit import RabbitBroker

from src.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)

async def publish_msg(filename: str):
    """
    Публикует сообщение в RabbitMQ
    """
    await broker.publish(
        message=f"{filename}",
        queue="input_files"
    )
    return {
        "data": "Success"
    }
