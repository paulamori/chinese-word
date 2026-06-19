from fastapi import FastAPI
import sqlite3
from datetime import datetime
import os

app= FastAPI()


def buscar_palavra_do_dia():
    db_path = os.path.join(os.path.dirname(__file__), '../public', 'dicionario.db')
    conexao = sqlite3.connect(db_path)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM palavras WHERE frequencia > 500 ORDER BY frequencia DESC")
    selecao = cursor.fetchall()
    
    if not selecao:
        return None
    
    diaAno = datetime.now().timetuple().tm_yday
    indice=diaAno % len(selecao)
    
    resultado= selecao[indice]
    
    conexao.close()
    
    return resultado

@app.get("/palavra-dia")
def get_palavra():
    palavra = buscar_palavra_do_dia()
    if not palavra:
        return{"erro": "Nenhuma palavra encontrada"}
    return{
        "tradicional": palavra['tradicional'],
        "simplificado": palavra['simplificado'],
        "pinyin": palavra['pinyin'],
        "definicao": palavra['definicao'],
        "frequencia": palavra ['frequencia']
    }