from pathlib import Path
import os
import shutil
import json
import requests

import discord

##############
PATH = Path("/home/aurnytoraink/Projets/Code/Bot/Donvert/")

if os.path.exists(PATH / 'files'):
    shutil.rmtree(PATH / "files")
os.makedirs(PATH / "files")

TOKEN = json.loads(open("config.json",'rb').read())["token"]

ext_ref = ["doc","docx","odt","odf","odg","ods","ott","xls","xlsx","ppt","pptx"]

##############
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.attachments != []:
        attachment = message.attachments[0]
        extension = attachment.filename.split(".")[-1]
        output = ".".join(attachment.filename.split(".")[:len(attachment.filename.split("."))-1])+".pdf"
        if extension in ext_ref:
            data = requests.get(attachment.url).content
            with open(PATH/("files/"+attachment.filename),'xb') as f:
                f.write(data)

            print(PATH/("files/"+attachment.filename))
            # os.system(f"libreoffice --headless --convert-to pdf \"{PATH/('files/'+attachment.filename)}\" --outdir \"{PATH/('files/'+output)}\"")
            os.system(f"flatpak run org.libreoffice.LibreOffice --headless --convert-to pdf \"{PATH/('files/'+attachment.filename)}\" --outdir \"{PATH/('files/')}\"")
            await message.channel.send(file=discord.File(PATH/('files/'+output)))

            os.remove(PATH/("files/"+output))
            os.remove(PATH/("files/"+attachment.filename))


client.run(TOKEN)