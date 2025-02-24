from fastapi import FastAPI
from fastapi.params import Body
import classes

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Corinthians"}

@app.post("/criar")
def criar_valores(nova_mensagem: classes.Mensagem):
    print(nova_mensagem)
    return {"Mensagem": f"Título: {nova_mensagem.titulo} Conteúdo: {nova_mensagem.conteudo} Publicada:{nova_mensagem.publicada}"}
