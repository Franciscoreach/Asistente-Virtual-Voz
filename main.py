#API de personajes
from characterai import aiocai
import asyncio
import speech_recognition as sr
import keyboard
#Libreria Texto a Voz
import pyttsx3
#Liberia de Traducción
from googletrans import Translator
import pyaudio
import wave
import os
import time

# Ruta al archivo de registro
log_file_path = "log/conversation_log.txt"

def log_conversacion(message):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] {message}\n")

# Colores para los print en consola
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def reconocer_voz():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(colors.MAGENTA + "Presiona la tecla 'R' para comenzar a grabar y 'P' para detener...")
        grabando = False
        audio = None
        while True:
            if keyboard.is_pressed("r") and not grabando:
                print(colors.GREEN + "Comenzando a grabar...")
                grabando = True
                audio = recognizer.listen(source)
            elif keyboard.is_pressed("p") and grabando:
                print(colors.RED + "Deteniendo la grabación...")
                grabando = False
                break
            elif keyboard.is_pressed("m"):
                print(colors.RED + "[Programa detenido por el usuario]")
                exit()
    try:
        print(colors.YELLOW + "[Reconociendo la voz]")
        texto = recognizer.recognize_google(audio, language="es-ES")
        return texto

    except sr.UnknownValueError:
        print("[Repite la prueba se detecto un error en la 'voz']")

def convertir_a_voz(respuesta_voz, output_file):
    engine = pyttsx3.init()
    # Establecer la velocidad de voz
    engine.setProperty('rate', 140)
    engine.setProperty('voice', 'spanish')  # Voz en español
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, output_file)
    
    # Convertir texto a voz y guardar en archivo WAV
    engine.save_to_file(respuesta_voz, output_path)
    engine.runAndWait()

def reproducir_audio(file):
    CHUNK = 1024

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def traducir(texto):
    translator = Translator()
    traduccion = translator.translate(texto, src='en', dest='es')
    return traduccion.text

def abrir_archivo_con_reproductor(file):
    output_path = os.path.join("output", file)
    
    try:
        os.startfile(output_path)
    except FileNotFoundError:
        print("El archivo de audio no se encuentra en la carpeta de salida.")

async def main():
    output_file = "audio.wav"


    #Configuración del personaje según el token seleccionado "char_token"

    from tokens import character_token,client_token

    char = character_token

    client = aiocai.Client(client_token)

    me = await client.get_me()

    async with await client.connect() as chat:
        new, answer = await chat.new_chat(
            char, me.id
        )

        #Presentación del BOT // sin traducir // sin voz
        #print(f'{answer.name}: {answer.text}')
        
        while True:
            texto_reconocido = reconocer_voz()  

            if texto_reconocido is None:
                continue  # Si el texto es None, forzar al usuario a grabar de nuevo

            log_conversacion(f"Usuario: {texto_reconocido}")
            
            print(colors.GREEN + "Usuario: ", texto_reconocido)

            text = texto_reconocido

            message = await chat.send_message(
                char, new.chat_id, text
            )

            traduccion_consola = traducir(message.text)

            print(colors.BLUE + f'{message.name}: {traduccion_consola}')

            texto_traducido = traducir(message.text)

            log_conversacion(f'{message.name}:{texto_traducido}')

            output_file = "audio_" + str(time.time()) + ".wav"  # Nombre de archivo único basado en el tiempo actual
            convertir_a_voz(texto_traducido, output_file)

            abrir_archivo_con_reproductor(output_file)

asyncio.run(main())