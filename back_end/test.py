from fastapi import FastAPI
import classes
import model
from database import engine

model.Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar")
def criar_valores(nova_mensagem: classes.Mensagem):
    print(nova_mensagem)
    return{"Mensagem": f"Titulo:{nova_mensagem.titulo}Conteudo: {nova_mensagem.conteudo}Publicada:{nova_mensagem.publica}"}
