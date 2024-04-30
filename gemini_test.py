import google.generativeai as genai
import speech_recognition as sr
import textwrap
from IPython.display import Markdown
import sys
import keyboard

#Texto a Voz
import pyttsx3

sys.stdout.reconfigure(encoding='utf-8')
 
# Usamos el modelo generativo de la IA 
modelo = genai.GenerativeModel('gemini-pro')
 
# Configuramos la API KEY 
GOOGLE_API_KEY='INSERTA_TU_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)
 

def convertir_a_voz(respuesta):
  # Crear un objeto de la clase pyttsx3
  engine = pyttsx3.init()
  # Establecer la velocidad de habla
  engine.setProperty('rate', 150)
  # Establecer la voz (opcional)
  # engine.setProperty('voice', 'spanish')  # Cambia a una voz en español si está disponible
  # Convertir texto a voz y reproducirlo
  engine.say(respuesta)
  engine.runAndWait()

def reconocer_voz():
    # Crear un objeto recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Presiona la tecla 'R' para comenzar a grabar y 'P' para detener...")
        grabando = False
        audio = None
        while True:
            if keyboard.is_pressed("r") and not grabando:
                print("Comenzando a grabar...")
                grabando = True
                audio = recognizer.listen(source)
            elif keyboard.is_pressed("p") and grabando:
                print("Deteniendo la grabación...")
                grabando = False
                break
            elif keyboard.is_pressed("m"):
                print("[Programa detenido por el usuario]")
                exit()

    try:
        print("Reconociendo...")
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Dijiste:", texto)

        # Respuesta generada por Gemini
        respuesta = modelo.generate_content(texto).text

        respuesta = genai.GenerativeModel('gemini-pro').generate_content(f"Melody, {texto}").text

        # Limitar la respuesta a 100 palabras
        respuesta = ' '.join(respuesta.split()[:100])
      
        print(respuesta)

        # Llamada al metodo para convertir la respuesta a "voz"
        convertir_a_voz(respuesta)

    except sr.UnknownValueError:
        print("No se pudo entender lo que dijiste")
    except sr.RequestError as e:
        print("Error al solicitar resultados; {0}".format(e))
 
if __name__ == "__main__":
    reconocer_voz()