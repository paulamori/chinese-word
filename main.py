from fastapi import FastAPI
import sqlite3
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite pedidos de qualquer origem
    allow_methods=["*"],
    allow_headers=["*"],
)

def buscar_palavra_do_dia():
    conexao = sqlite3.connect('dicionario.db')
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT (*) FROM palavras")
    total = cursor.fetchone()[0]
    
    diaAno = datetime.now().timetuple().tm_yday
    indice=diaAno % total
    
    cursor.execute("SELECT * FROM palavras LIMIT 1 OFFSET ?", (indice,))
    resultado= cursor.fetchone()
    
    conexao.close()
    
    return resultado

@app.get("/api/palavra-dia")
def get_palavra():
    palavra = buscar_palavra_do_dia()
    if not palavra:
        return{"erro": "Nenhuma palavra encontrada"}
    return{
        "tradicional": palavra['tradicional'],
        "simplificado": palavra['simplificado'],
        "pinyin": palavra['pinyin'],
        "definicao": palavra['definicao']
    }