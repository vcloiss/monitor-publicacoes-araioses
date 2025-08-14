import requests
from bs4 import BeautifulSoup
import os

URL = "https://dom.araioses.ma.gov.br/publicacoes"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1405342651561017404/SrI8h6zpsiJx2KkqZ8U2LW0yD8_C0GZixacgxYQMHraiOy_280uhW4LNJAAlzlge2oq_"
ARQUIVO = "ultimo_registro.txt"

def enviar_discord(mensagem):
    data = {"content": mensagem}
    r = requests.post(DISCORD_WEBHOOK, json=data)
    if r.status_code != 204:
        print(f"Erro ao enviar para o Discord: {r.text}")

def verificar_atualizacao():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    primeira_publicacao = soup.find("a", class_="card-link")
    if not primeira_publicacao:
        print("Nenhuma publicação encontrada.")
        return

    titulo = primeira_publicacao.text.strip()
    link = primeira_publicacao["href"]

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            ultimo = f.read().strip()
    else:
        ultimo = ""

    if titulo != ultimo:
        enviar_discord(f"🆕 Nova publicação no DOM de Araioses:\n**{titulo}**\n🔗 {link}")
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(titulo)
        print("Nova publicação detectada e enviada.")
    else:
        print("Nenhuma novidade.")

if __name__ == "__main__":
    verificar_atualizacao()
