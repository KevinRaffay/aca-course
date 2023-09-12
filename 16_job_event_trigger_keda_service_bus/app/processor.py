#!/usr/bin/env python

import os
import asyncio
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from azure.identity.aio import DefaultAzureCredential

SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_QUEUE_NAME = os.getenv("SERVICEBUS_QUEUE_NAME")
MANAGED_IDENTITY_CLIENT_ID = os.getenv("MANAGED_IDENTITY_CLIENT_ID")

print(f"SERVICEBUS_QUEUE_NAME: {SERVICEBUS_QUEUE_NAME}")
print(f"SERVICEBUS_FULLY_QUALIFIED_NAMESPACE: {SERVICEBUS_FULLY_QUALIFIED_NAMESPACE}")
print(f"MANAGED_IDENTITY_CLIENT_ID: {MANAGED_IDENTITY_CLIENT_ID}")

# Get credential object
credential = DefaultAzureCredential(
  exclude_visual_studio_code_credential=True, 
  exclude_interactive_browser_credential=True, 
  exclude_environment_credential=True, 
  exclude_workload_identity_credential=True,
  exclude_developer_cli_credential=True,
  exclude_powershell_credential=True,
  exclude_shared_token_cache_credential=True,
  exclude_managed_identity_credential=False,
  exclude_cli_credential=False,
  managed_identity_client_id=MANAGED_IDENTITY_CLIENT_ID)

async def send_single_message(sender):
    message = ServiceBusMessage("My First Message")
    await sender.send_messages(message)
    print(f"Sent message: {str(message)}")

async def receive_single_message(receiver):
    messages = await receiver.receive_messages(max_message_count=1, max_wait_time=5)
    print(f"Received message: {str(messages[0])}")
    await receiver.complete_message(messages[0])

async def main():
    servicebus_client = ServiceBusClient(
        fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE, 
        credential=credential)

    async with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=SERVICEBUS_QUEUE_NAME)
        async with sender:
            await send_single_message(sender)

        receiver = servicebus_client.get_queue_receiver(queue_name=SERVICEBUS_QUEUE_NAME)
        async with receiver:
            await receive_single_message(receiver)
    
asyncio.run(main())