import requests
import logging
from utils.exceptions import WebhookException


def send_webhook(headers: dict, payload: dict, url: str):
    """ Sends a webhook request after processing the CV """
    try:
        # Send request
        response = requests.post(url, json=payload, headers=headers)

        # Check response
        if response.status_code == 200:
            logging.info(f"Webhook sent successfully: {response.status_code}")
        else:
            logging.error(f"Failed to send webhook: {response.status_code}, {response.text}")
            raise WebhookException(f"Failed to send webhook: {response.status_code}, {response.text}")

    except requests.RequestException as e:
        logging.error(f"Unexpected error in sending webhook: {str(e)}")
        raise WebhookException(f"Error sending webhook: {str(e)}")

