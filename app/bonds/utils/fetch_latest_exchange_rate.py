import os
import requests

url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno/"


def exchange_rate(url=url) -> float:
    payload={}
    headers = {
    'Bmx-Token': os.environ["BMX_TOKEN"],
    'Cookie': 'Hex25802680=!7pXbgc2hsEugyPf3AjKmtUwBnOY1od48baUZs+/8cf+WL77tP/pnDiXEBL0h6Rt89aFcdPSNGVABhw==; SRVCOOKIE=!YSnXWhXte9jD62r3AjKmtUwBnOY1oXexuMFVYy3LfLykzJ7pL6ngUv/jwUdckeu8mqr5NI1ozeDI1g==; TS012f422b=01ab44a5a8622214f6d7b924f42eb80a69d82aee3ca2badc64f70ff9995047bce99ec5137059f932a7228aca6a15459b12e22221ecc83c5448f76f3e023f87644dc011fa230069322d2ab5075af5a3bc6e744b6b21'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return float(response.json()['bmx']['series'][0]['datos'][0]['dato'])
