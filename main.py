import os
import json
from datetime import datetime
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

# Cartella dove salvare/leggere le conversazioni
CONVERSATIONS_DIR = "conversations"

# Messaggio di sistema iniziale (prompt del modello)
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "Sei un assistente utile in chat da terminale. Rispondi in italiano quando possibile.",
}
# Storico della converazione
messages = [SYSTEM_MESSAGE.copy()]


def new_conversation():
    """Resetta lo storico della conversazione mantenendo il system message originale"""
    global messages

    # Resetta la lista dei messaggi a solo il system message (copiato dalla costante)
    messages = [SYSTEM_MESSAGE.copy()]

    print("🆕 Nuova conversazione iniziata!")


def list_conversations():
    """Mostra conversazioni in conversations/"""

    # Controlla se la cartella esiste
    if not os.path.exists(CONVERSATIONS_DIR):
        print(
            "📂 Nessuna conversazione salvata (cartella 'conversations/' non trovata)."
        )
        return

    # Lista dei file .json nella cartella
    files = [name for name in os.listdir(CONVERSATIONS_DIR) if name.endswith(".json")]

    if not files:
        print("📂 Nessuna conversazione salvata.")
        return

    print("📂 Conversazioni salvate:")

    # 3. Per ogni file, leggi i metadati dal JSON
    for filename in sorted(files):
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"- {filename} | errore lettura file: {e}")
            continue

        # Estraggo metadati con valori di default
        saved_at = data.get("saved_at", "data sconosciuta")
        message_count = data.get("message_count")

        # Fallback: se non c'è message_count, lo calcolo da messages
        if message_count is None:
            msgs = data.get("messages")
            if isinstance(msgs, list):
                message_count = len(msgs)
            else:
                message_count = "sconosciuto"

        # 4. Stampa fotmattato
        print(f"- {filename} | messaggi: {message_count} | salvata il: {saved_at}")


def save_conversation(name: str | None = None):
    """
    Salva l'attuale conversazione in un file JSON dentro la cartella conversations/.

    name: nome opzionale della conversazione ( senza estensione).
        Verrà usato come parte del nome file
    """

    # 1) Ci assicuriamo che la cartella esista
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    # 2) Timestamp attuale (ISO per i metadati)
    now = datetime.now().isoformat(timespec="seconds")  # es: "2025-01-19T11:05:32"

    # 3) Timestamp "safe" per il nome file (niente due punti)
    safe_timestamp = now.replace(":", "-")  # "2025-01-19T11-05-32"

    # 4) Costruisco il nome del file
    if name:
        # Pulizia base del nome: tolgo gli spazi ai bordi e sostituisco spazi interni con underscore
        cleaned_name = name.strip().replace(" ", "_")
        if cleaned_name == "":
            cleaned_name = "untitled"
        filename = f"{safe_timestamp}_{cleaned_name}.json"
    else:
        filename = f"{safe_timestamp}.json"

    filepath = os.path.join(CONVERSATIONS_DIR, filename)

    # 5) Prepara i dati da salvare (struttura JSON)
    data = {"messages": messages, "saved_at": now, "message_count": len(messages)}

    # 6) Scrivi il file JSON
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[ERRORE] Impossibile salvare la conversazione.")
        print("dettagli tecnici:", e)
        return

    print(f"💾 Conversazione salvata in: {filepath}")


def load_conversation():
    """Permette di caricare una conversazione salvata da conversations/."""

    # 1) Controlla se la cartella esiste
    if not os.path.exists(CONVERSATIONS_DIR):
        print(
            "📂 Nessuna conversazione salvata (cartella 'conversations/' non trovata)."
        )
        return

    # 2) Lista dei file .json nella cartella
    files = [name for name in os.listdir(CONVERSATIONS_DIR) if name.endswith(".json")]

    if not files:
        print("📂 Nessuna conversazione salvata.")
        return

    files = sorted(files)

    print("📂 Conversazioni disponibili:")

    # 3) Mostra elenco numerato con metadati base
    for idx, filename in enumerate(files, start=1):
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

        saved_at = "data sconosciuta"
        message_count = "sconosciuto"

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            saved_at = data.get("saved_at", saved_at)
            mc = data.get("message_count")
            if mc is not None:
                message_count = mc
            else:
                msgs = data.get("messages")
                if isinstance(msgs, list):
                    message_count = len(msgs)
        except Exception as e:
            print(f"{idx}. {filename} | ERRORE lettura metadati: {e}")
            continue

        # STAMPA DENTRO IL FOR: una riga per ogni file
        print(f"{idx}. {filename} | messaggi: {message_count} | salvata il: {saved_at}")

    # 4) Chiedi all'utente quale conversazione caricare
    while True:
        choice = input(
            "Seleziona il numero della conversazione da caricare "
            "(oppure premi Invio per annullare): "
        ).strip()

        if choice == "":
            print("❌ Caricamento annullato.")
            return

        if not choice.isdigit():
            print(
                "Per favore inserisci un numero valido oppure premi Invio per annullare."
            )
            continue

        index = int(choice)
        if not (1 <= index <= len(files)):
            print(
                f"Inserisci un numero fra 1 e {len(files)}, oppure premi Invio per annullare."
            )
            continue

        # Se arrivo qui, l'input è valido → esco dal while
        break

    selected_filename = files[index - 1]
    selected_path = os.path.join(CONVERSATIONS_DIR, selected_filename)

    # 5) Carica i messages dal file selezionato
    try:
        with open(selected_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded_messages = data.get("messages")

        if not isinstance(loaded_messages, list):
            print("❌ Formato file non valido: 'messages' mancante o non è una lista.")
            return

        global messages
        messages = loaded_messages

        print(
            f"✅ Conversazione '{selected_filename}' caricata. Messaggi: {len(messages)}"
        )

    except Exception as e:
        print("\n[ERRORE] Impossibile caricare la conversazione selezionata.")
        print("Dettagli tecnici:", e)
        return


def parse_command(user_input: str) -> bool:
    """
    Riconosce ed esegue comandi.
    Ritorna True se era un comando (già gestito),
    False se non è un comando e va mandato a GPT.
    """

    # Non è un comando se non inizia con "/"
    if not user_input.startswith("/"):
        return False

    # Normalizza e separa comando e argomenti
    parts = user_input.strip().split()
    command = parts[0].lower()  # es: "/new"
    # args = parts[1:]  # per futuri comandi con argomenti

    if command == "/new":
        new_conversation()
        return True

    elif command == "/exit" or command == "/quit":
        print("👋 Arrivederci!")
        return "EXIT"

    elif command == "/list":
        list_conversations()
        return True

    elif command == "/save":
        # Prendo tutto quello che viene dopo il comando come nome opzionale
        if len(parts) > 1:
            # " ".join(parts[1:]) permette nomi con spazi: /save idea cliente

            name = " ".join(parts[1:])
        else:
            name = None

        save_conversation(name)
        return True

    elif command == "/load":
        load_conversation()
        return True

    # Comando sconosciuto
    print(f"❓ Comando sconosciuto: {command}")
    print("💡 Comandi disponibili:")
    print("   /new   - Nuova conversazione")
    print("   /list  - Mostra conversazioni salvate")
    print("   /save [nome] - Salva conversazione")
    print("   /load  - Carica conversazione")
    print("   exit   - Esci dal programma")
    return True


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
        # 1) Leggo input utente
        user_input = input("Tu: ")


        # Se l'utente non scrive niente saltiamo il giro

        if user_input == "":
            print("(Scrivi qualcosa)")
            continue

        # 2) Prima: controlla se è un comando (tipo /new)
        result = parse_command(user_input)
        if result == "EXIT":
            break
        if result:
            continue


        # 3) Chiama la funzione chat e ottieni la risposta di GPT
        print("\nGPT sta scrivendo...")
        assistant_reply = chat(user_input)

        # 4) Stampa la risposta
        print("\nGPT:", assistant_reply, "\n")


if __name__ == "__main__":
    main()
