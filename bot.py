import os
  import re
  import requests
  import discord

  TOKEN = os.getenv("TOKEN")
  PUSHCUT_API_KEY = os.getenv("iJW7T1wzJjXB3hIwDjG7Z")
  PUSHCUT_VENDAS = os.getenv("https://api.pushcut.io/iJW7T1wzJjXB3hIwDjG7Z/notifications/Venda%20%F0%9F%92%B0")
  PUSHCUT_PERGUNTAS = os.getenv("PUSHCUT_PERGUNTAS", "")

  CANAL_VENDAS = 1497420405894283479
  CANAL_PERGUNTAS = 1497420606574952559

  if not TOKEN:
      raise ValueError("A variável TOKEN não foi configurada no Railway.")

  if not PUSHCUT_API_KEY:
      raise ValueError("A variável PUSHCUT_API_KEY não foi configurada no Railway.")

  if not PUSHCUT_VENDAS:
      raise ValueError("A variável PUSHCUT_VENDAS não foi configurada no Railway.")

  intents = discord.Intents.default()
  intents.message_content = True

  client = discord.Client(intents=intents)


  @client.event
  async def on_ready():
      print(f"Bot online: {client.user}")


  def extrair_texto_mensagem(message):
      texto = message.content or ""

      if message.embeds:
          for embed in message.embeds:
              texto += "\n" + (embed.title or "")
              texto += "\n" + (embed.description or "")

              for field in embed.fields:
                  texto += f"\n{field.name}\n{field.value}"

      return texto.strip()


  @client.event
  async def on_message(message):
      if client.user and message.author.id == client.user.id:
          return

      if message.channel.id == CANAL_VENDAS:
          texto = extrair_texto_mensagem(message)
          valores = re.findall(r"R\$\s*[\d.,]+", texto)

          if valores:
              for valor in valores:
                  valor = valor.strip()

                  response = requests.post(
                      PUSHCUT_VENDAS,
                      json={
                          "title": "Venda Aprovada 💰",
                          "text": valor
                      },
                      headers={
                          "API-Key": PUSHCUT_API_KEY
                      },
                      timeout=15
                  )

                  print(f"Venda enviada pro Pushcut: {valor} | status={response.status_code}")
          else:
              print("Nenhum valor encontrado na mensagem de venda.")

      elif message.channel.id == CANAL_PERGUNTAS:
          texto = extrair_texto_mensagem(message)
          nome = "Cliente desconhecido"

          match_nome = re.search(r"Cliente\s*\n(.+)", texto, re.IGNORECASE)
          if match_nome:
              nome = match_nome.group(1).strip()

          if PUSHCUT_PERGUNTAS:
              response = requests.post(
                  PUSHCUT_PERGUNTAS,
                  json={
                      "title": "Pergunta Recebida!",
                      "text": f"{nome} te enviou uma pergunta"
                  },
                  headers={
                      "API-Key": PUSHCUT_API_KEY
                  },
                  timeout=15
              )

              print(f"Pergunta de {nome} enviada pro Pushcut | status={response.status_code}")
          else:
              print("URL do Pushcut de perguntas não configurada.")


  client.run(TOKEN.strip())
