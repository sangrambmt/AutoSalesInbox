from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient

from config.settings import settings


async def send_message(queue_name: str, body: str) -> None:
    async with ServiceBusClient.from_connection_string(settings.service_bus_connection_string) as client:
        async with client.get_queue_sender(queue_name) as sender:
            await sender.send_messages(ServiceBusMessage(body))


async def receive_messages(queue_name: str, max_messages: int = 10) -> list[dict]:
    messages = []
    async with ServiceBusClient.from_connection_string(settings.service_bus_connection_string) as client:
        async with client.get_queue_receiver(queue_name, max_wait_time=5) as receiver:
            async for msg in receiver:
                messages.append({"id": str(msg.message_id), "body": str(msg)})
                await receiver.complete_message(msg)
                if len(messages) >= max_messages:
                    break
    return messages
