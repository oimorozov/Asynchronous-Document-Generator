from faststream.rabbit.fastapi import RabbitRouter

from src.config import settings

router = RabbitRouter(settings.RABBITMQ_URL)

@router.post("/send_msg")
async def pub_msg(name: str):
    await router.broker.publish(
        message=f"The {name} message",
        queue="files"
    )
    return {
        "data": "Success"
    }