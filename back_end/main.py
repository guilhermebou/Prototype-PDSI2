from fastapi import FastAPI, status, Depends, HTTPException
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scrape-menu", status_code=status.HTTP_201_CREATED, response_model=List[classes.Menu])
def scrape_and_save_menu(db: Session = Depends(get_db)):
    url = "https://ufu.br"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch URL: {str(e)}"
        )

    soup = BeautifulSoup(response.content, 'html.parser')
    nav_ensino = soup.find('nav', id='block-ufu-rodape-2')
    coluna_ensino = nav_ensino.find('ul', class_='nav navbar-nav')

    titulos = []
    for linha in coluna_ensino:
        titulo = linha.text.strip().replace('\n', '')
        if titulo:
            titulos.append(titulo)

    links = coluna_ensino.find_all('a')
    urls = [url + link.get('href', '') for link in links]

    menus_to_add = [
        model.Model_Menu(titulo=titulo, url=url)
        for titulo, url in zip(titulos, urls)
    ]

    try:
        db.add_all(menus_to_add)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

    for menu in menus_to_add:
        db.refresh(menu)

    return menus_to_add

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session=Depends(get_db)):
    mensagem_criada=model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return{"Mensagem": mensagem_criada}

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int=0, limit: int=100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens
