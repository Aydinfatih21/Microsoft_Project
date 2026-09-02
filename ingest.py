import sqlite3
import json
import numpy as np
from openai import OpenAI

# ⚠️ TEK DİKKAT EDECEĞİN YER BURASI ⚠️
# Siyah ekranda (Foundry) yazan kapı numarasını buraya yaz:
PORT = 51592

client = OpenAI(base_url=f"http://127.0.0.1:{PORT}/v1", api_key="local-key")

def setup_database():
    conn = sqlite3.connect('ingest.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS documents')
    c.execute('''
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            embedding TEXT
        )
    ''')
    return conn, c

def ingest_documents(documents):
    conn, c = setup_database()
    print("Veritabanı oluşturuluyor, lütfen bekleyin...")
    
    for doc in documents:
        response = client.embeddings.create(
            input=doc.lower(),
            model="qwen3-embedding-0.6b"
        )
        emb = response.data[0].embedding
        c.execute('INSERT INTO documents (content, embedding) VALUES (?, ?)', (doc, json.dumps(emb)))
    
    conn.commit()
    conn.close()
    print("✅ İŞLEM TAMAM! ingest.db dosyası başarıyla oluşturuldu.")

if __name__ == "__main__":
    ornek_veriler = [
        "Ahmet 11 haziranda geldi ve tedavisi tamamlandı. Bir sonraki randevu tarihi 6 eylül.",
        "Mehmet 10 temmuzda geldi ama ödeme yapmadı."
    ]
    ingest_documents(ornek_veriler)
