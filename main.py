import requests
from subprocess import call

s = requests.Session()


with open('output.jpg', 'wb') as handle:
    response = s.get('https://www.runt.com.co/consultaCiudadana/captcha', stream=True)

    for block in response.iter_content(1024):
        handle.write(block)

call(["open", "output.jpg"])


captcha = raw_input("Captcha: ")


response = s.post('https://www.runt.com.co/consultaCiudadana/publico/automotores/', json={"captcha": captcha, "codigoSoat": None, "noDocumento": "31203652", "noPlaca": "GXQ74A", "procedencia": "NACIONAL", "soat": None, "tipoConsulta": "1", "tipoDocumento": "C", "vin": None})

print(response.text)


