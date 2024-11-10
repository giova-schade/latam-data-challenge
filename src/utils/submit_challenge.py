import requests  # type: ignore


def submit_challenge_submission():
    """
    Envía un POST request con mis datos para enviar la solución del desafío.
    """
    url = "https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/data-engineer"
    payload = {
        "name": "Giovanni Schade",
        "mail": "giovanni.schade@gmail.com",
        "github_url": "https://github.com/giova-schade/latam-data-challenge.git",
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Desafío enviado con éxito.")
    else:
        print(f"Error al enviar el desafío: {response.status_code}")
        print(response.text)
