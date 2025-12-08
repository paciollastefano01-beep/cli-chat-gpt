import os
from dotenv import load_dotenv
from openai import OpenAI

# 1) Carica le variabili d'ambiente dal file .env
load_dotenv()

# 2) Leggi la chiave API dalla variabile di ambiente
api_key = os.getenv("OPENAI_API_KEY")

# 3) Controllo base: se la chiave non esiste, fermiamo il programma con un errore chiaro
if not api_key:
    raise ValueError(
        "Errore: variabile OPENAI_API_KEY non trovata. Controlla il file .env"
    )

# 4) Crea il client OpenAI usando la chiave
client = OpenAI(api_key=api_key)
# Nome del modello da usare per la chat
MODEL_NAME = "gpt-3.5-turbo"

# Storico della converazione
messages = [
    {
        "role": "system",
        "content": "Sei un assistente utile in una chat da terminale. Rispondi in italiano quando possibile.",
    }
]


def chat(user_message: str) -> str:
    """
    Gestisce un turno di chat:
    - aggiunge il messaggio dell'utente allo storico
    - chiama l'API OpenAI con tutto lo storico
    - aggiunge la risposta di gpt allo storico
    - restituisce il testo della risposta
    """

    # 1) Aggiungi il messaggio dell'utente allo storico
    messages.append({"role": "user", "content": user_message})

    try:

        # 2) Chiamata all'API con tutto lo storico
        response = client.chat.completions.create(model=MODEL_NAME, messages=messages)

    except Exception as e:
        # Gesione errore: non facciamp crashare il programma
        print("\n[ERRORE] Problema durante la chiamata all'API OpenAI")
        print("Dettagli tecnici:", e)

        # Rimiovo l'ultimo messaggio utente dallo storico perchè non è mai stato letto dal modello
        messages.pop()

        # Risposta di coresia all'utente
        return "Scusa, si è verificato un errore tecnico con l'AI. Riprova tra poco"

    # Se tutto ok, estraggo testo della risposta di GPT
    assistant_message = response.choices[0].message.content

    # 4) Aggiungi la risposta di GPT allo storico
    messages.append({"role": "assistant", "content": assistant_message})

    # 5) Restituisci il testo della risposta
    return assistant_message


def main():
    print("💬 CLI Chat GPT")
    print("Scrivi un messaggio e premi Invio.\n")

    while True:
        # 1) Leggo inpurt utente
        user_input = input("Tu: ")

        # Se l'utente non scrive niente saltiamo il giro

        if user_input == "":
            print("(Scrivi qualcosa o 'exit' per uscire.)")
            continue

        # 2)Controlla se l'utente vuole uscire
        if user_input.lower() == "exit":
            print("👋 Arrivederci!")
            break

        # 3) Chiama la funzione chat e ottieni la risposta di GPT
        print("\nGPT sta scrivendo...")
        assistant_reply = chat(user_input)

        # 4) Stampa la risposta
        print("\nGPT:", assistant_reply, "\n")


if __name__ == "__main__":
    main()
