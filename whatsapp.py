import requests

def send_whatsapp(phone, message):
    url = "https://api.msg91.com/api/v5/whatsapp/whatsapp-outbound-message/bulk/"

    headers = {
        "authkey": "YOUR_MSG91_KEY",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "from": "YOUR_NUMBER",
                "to": f"91{phone}",
                "type": "text",
                "text": {"body": message}
            }
        ]
    }

    requests.post(url, json=payload, headers=headers)