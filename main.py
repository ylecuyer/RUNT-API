import requests
import subprocess
import json

cedula = input("Cedula: ")
placa = input("Placa: ")

s = requests.Session()

output = ""
data = {}

#Tant que le json retourne une erreur
while True:

        #Tant que le captcha n'est pas resolu
        while True:
                #Download captcha
                with open('output.jpg', 'wb') as handle:
                    response = s.get('https://www.runt.com.co/consultaCiudadana/captcha', stream=True)

                    for block in response.iter_content(1024):
                      handle.write(block)

                #Tente la resolution
                p = subprocess.Popen(["tesseract", "output.jpg", "stdout", "-psm 8", "-c", "tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                (output, err) = p.communicate()
                p_status = p.wait()

                output = output.strip()

                if len(output) == 5:
                  break

        captcha = str(output, "utf-8")

        response = s.post('https://www.runt.com.co/consultaCiudadana/publico/automotores/', json={"captcha": captcha, "codigoSoat": None, "noDocumento": cedula, "noPlaca": placa, "procedencia": "NACIONAL", "soat": None, "tipoConsulta": "1", "tipoDocumento": "C", "vin": None})

        data = json.loads(response.text.splitlines()[1])

        if "error" not in data:
          break

print(data["informacionGeneralVehiculo"]["marca"])
print(data["informacionGeneralVehiculo"]["linea"])

