import telebot
import requests
import random
from faker import Faker
fake = Faker()
import json
import subprocess
import re
import os

bot = telebot.TeleBot("") #Replace with your token
fake = Faker()

@bot.message_handler(commands=['spotify_download'])
def get_data(message):
    # Try to get Spotify URL
    try:
        spotify_url = message.text.split(" ", 1)[1]  # Obtener el URL
    except IndexError:
        bot.reply_to(message, "Por favor ingresa un URL ejem: https://open.spotify.com/intl-es/track/... ")
        return

    # Extract ID from Spotify URL
    match = re.search(r'track/([^?]+)', spotify_url)
    if not match:
        bot.reply_to(message, "URL de Spotify no válido.")
        return

    track_id = match.group(1)
    download_url = f"https://api.spotifydown.com/download/{track_id}"

    # Run the JavaScript script with the new URL
    result = subprocess.run(['node', 'musica.js', download_url], capture_output=True, text=True)

    #Check for errors in script execution
    if result.returncode != 0:
        print(result.stderr)
        bot.reply_to(message, "Error al ejecutar el script: " + result.stderr)
        return

    # Read the extracted data
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        # Prepare the message to send
        message_text = (
            f"ID: {data['id']}\n"
            f"Título: {data['title']}\n"
            f"Álbum: {data['album']}\n"
            f"Portada: {data['cover']}\n"
            f"Fecha de lanzamiento: {data['releaseDate']}\n"
        )
        bot.reply_to(message, message_text)

        url = data['link']
        user_agent = fake.user_agent()  # Generate a random user agent
        headers = {
            "User-Agent": user_agent
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            nombre_song = data['title'].replace('/', '-')  # Replaces invalid characters
            with open(f"{nombre_song}.mp3", 'wb') as f:
                f.write(response.content)

            # Send the audio to the user
            with open(f"{nombre_song}.mp3", 'rb') as audio:
                bot.send_audio(chat_id=message.chat.id, audio=audio)
        else:
            bot.reply_to(message, "Error al descargar el archivo: " + str(response.status_code))

    except Exception as e:
        bot.reply_to(message, "Error al leer los datos: " + str(e))
#If you want you can delete the songs that are downloaded.
#Recommended to leave on hosts.
#Viva RZ.
bot.polling()
