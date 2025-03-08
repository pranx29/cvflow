import logging
from utils.exceptions import WebhookException
import httpx

async def send_webhook(headers: dict, payload: dict, url: str):
    """ Sends a webhook request after processing the CV """
    async with httpx.AsyncClient() as client:
        try:
            # Send request
            response = await client.post(url, json=payload, headers=headers)

            # Check response
            if response.status_code == 200:
                logging.info(f"Webhook sent successfully: {response.status_code}")
            else:
                logging.error(f"Failed to send webhook: {response.status_code}, {response.text}")
                raise WebhookException(f"Failed to send webhook: {response.status_code}, {response.text}")

        except httpx.RequestError as e:
            logging.error(f"Unexpected error in sending webhook: {str(e)}")
            raise WebhookException(f"Error sending webhook: {str(e)}")
