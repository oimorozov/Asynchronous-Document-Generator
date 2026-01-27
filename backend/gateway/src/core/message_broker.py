from faststream.rabbit import RabbitBroker

from src.core.config import settings

broker = RabbitBroker(settings.RABBITMQ_URL)
