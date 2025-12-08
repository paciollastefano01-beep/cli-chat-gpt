import os
from dotenv import load_dotenv
from openai import OpenAI

# Carica .env
load_dotenv()

# Verifica che .env sia stato letto
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("❌ ERRORE: .env non trovato o vuoto!")
    print("Controlla che .env sia nella stessa cartella di test_api.py")
else:
    print(f"✅ .env letto! Chiave inizia con: {api_key[:10]}...")

# Client OpenAI
client = OpenAI(api_key=api_key)

print("\n🔄 Test connessione OpenAI...\n")

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Rispondi solo: Funziona con .env!"}
        ]
    )

    print("✅ RISPOSTA:")
    print(response.choices[0].message.content)
    print("\n🎉 .env CONFIGURATO CORRETTAMENTE!")

except Exception as e:
    print(f"❌ ERRORE: {e}")
