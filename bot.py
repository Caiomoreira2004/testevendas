import discord
import requests
import re

TOKEN = "MTUwMzUzNzI3NDQyNjQ5MDkwMA.GQiP3d.cvZgpPeGBrTFWS7-K1Mr_nXfYpmKLcdLW9swYw"

PUSHCUT_API_KEY = "iJW7T1wzJjXB3hIwDjG7Z"

CANAL_VENDAS = 1497420405894283479
CANAL_PERGUNTAS = 1497420606574952559

PUSHCUT_VENDAS = "https://api.pushcut.io/iJW7T1wzJjXB3hIwDjG7Z/notifications/Venda%20%F0%9F%92%B0"

PUSHCUT_PERGUNTAS = ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online: {client.user}")

@client.event
async def on_message(message):

    if message.author.bot:
        return

    # CANAL DE VENDAS
    if message.channel.id == CANAL_VENDAS:

        texto = message.content or ""

        if not texto and message.embeds:
            for embed in message.embeds:

                texto += (embed.title or "") + "\n"
                texto += (embed.description or "") + "\n"

                for field in embed.fields:
                    texto += f"{field.name}\n{field.value}\n"

        match = re.search(r"R\$\s*[\d.,]+", texto)

        if match:

            valor = match.group(0)

            requests.post(
                PUSHCUT_VENDAS,
                json={
                    "title": "Venda Aprovada💰",
                    "text": valor
                },
                headers={
                    "API-Key": PUSHCUT_API_KEY
                }
            )

            print(f"Venda enviada pro Pushcut: {valor}")

    # CANAL DE PERGUNTAS
    elif message.channel.id == CANAL_PERGUNTAS:

        nome = "Cliente desconhecido"

        texto = message.content or ""

        if message.embeds:

            for embed in message.embeds:

                for field in embed.fields:

                    if "cliente" in field.name.lower():
                        nome = field.value.strip()
                        break

                if nome == "Cliente desconhecido" and embed.description:

                    match_nome = re.search(
                        r"Cliente\s*\n(.+)",
                        embed.description
                    )

                    if match_nome:
                        nome = match_nome.group(1).strip()

        if nome == "Cliente desconhecido" and texto:

            match_nome = re.search(
                r"Cliente\s*\n(.+)",
                texto
            )

            if match_nome:
                nome = match_nome.group(1).strip()

        if PUSHCUT_PERGUNTAS:

            requests.post(
                PUSHCUT_PERGUNTAS,
                json={
                    "title": "Pergunta Recebida!",
                    "text": f"{nome} te enviou uma pergunta"
                },
                headers={
                    "API-Key": PUSHCUT_API_KEY
                }
            )

            print(f"Pergunta de {nome} enviada pro Pushcut")

        else:
            print("URL do Pushcut de perguntas não configurada.")

client.run(TOKEN)
