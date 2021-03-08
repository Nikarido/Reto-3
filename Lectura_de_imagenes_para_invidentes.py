# -*- coding: utf-8 -*-
"""
Ricardo Cruz Y.
Lectura de una imagen a voz con cognitive services para personas invidentes
"""
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from array import array
import os
from PIL import Image
import sys
import time

#Suscripcion de Computer vision
subscription_key = ""
endpoint = ""

#Suscripcion de Speech
speech_config = SpeechConfig(subscription="", region="" )

#Autenticacion del cliente
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#Consumir el servicio para analizar la imagen

#Imagen 1
#remote_image_url = "https://image.slidesharecdn.com/greenfinance-150427100253-conversion-gate01/95/green-finance-8-638.jpg?cb=1430129290"

#Imagen 2
#remote_image_url = "https://image.slidesharecdn.com/subculturerepresentation-170607074544/95/subculture-representation-30-638.jpg?cb=1496821576"

#Imagen 3
remote_image_url = "https://image1.slideserve.com/2042659/fault-tolerance-l.jpg"


##### Codigo para obtener el texto de la imagen ######

print("===== Leyendo la imagen =====")
# Obtener la imagen con texto
remote_image_handw_text_url = remote_image_url

# Llamar a la API
recognize_handw_results = computervision_client.read(remote_image_handw_text_url,  raw=True)


# Resultados de lectura
operation_location_remote = recognize_handw_results.headers["Operation-Location"]
# Obtenemos el texto de la imagen
operation_id = operation_location_remote.split("/")[-1]

while True:
    get_handw_text_results = computervision_client.get_read_result(operation_id)
    if get_handw_text_results.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

#Crear el archivo de texto donde se guardara el texto obtenido de la imagen
archivo = open("archivo.txt","w")

# Imprimimos el texto linea por linea
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            archivo.write(line.text)
            #print(line.bounding_box)
print()

archivo.close()



###### Código para convertir el texto obtenido y archivado en la imagen en audio ######

#Creacion del audio del texto obtenido
audio_config = AudioOutputConfig(use_default_speaker=True)

# #Escritura del archivo de audio
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
archivo_string = open("archivo.txt", "r",encoding="utf-8-sig").read()
synthesizer.speak_text_async(archivo_string).get()



