import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI


class ChatManager:
    """
    Gestisce tutta la logica della CLI Chat GPT:
    - configurazione OpenAI
    - stato della conversazione
    - comandi (/new, /save, /load, /list, /exit)
    - loop principale della chat
    """

    def __init__(self):
        """
        Inizializza:
        - variabili di configurazione (modello, cartella conversazioni, ecc..)
        -client OpenAI
        - messaggio di sistema
        - storico iniziale della conversazione
        """

        # 1) Carica le variabili d'ambiente del file .env
        load_dotenv()

        # 2) leggi la chiave API della variabile d'ambiente
        api_key = os.getenv("OPENAI_API_KEY")

        # Controllo base: se la chiave non esiste fermiamo con un errore chiaro:
        if not api_key:
            raise ValueError(
                "Errore: variabile OPENAI_API_KEY non trovata. Controlla il file .env"
            )

        # 4) Crea il client OpenAI usando la chiave
        self.client: OpenAI = OpenAI(api_key=api_key)

        # 5) configurazione applicazione
        self.model_name: str = "gpt-4o-mini"
        self.conversations_dir: str = "conversations"

        # 6) Messaggio di sistema iniziale (prompt del modello)
        self.system_message: dict = {
            "role": "system",
            "content": (
                "Sei un assistente utile in chat da terminale. "
                "Rispondi in italiano quando possibile."
            ),
        }

        # 7) Storico della conversazione: parte dal solo system message
        self.messages: list[dict] = [self.system_message.copy()]

    def new_conversation(self):
        """
        Reset della conversazione:
        - svuota lo storico
        - reimposta solo il messaggio di sistema
        """
        # Nessun global_ lavoriamo su attributi di istanza
        self.messages = [self.system_message.copy()]

        print("🆕 Nuova conversazione iniziata!")

    def save_conversation(self, name: str | None = None):
        """
        Salva la conversazione corrente in un file JSON.

        name: opzionale della conversazione (senza estensione).
            Verrà usato come parte del nome del file
        Struttura JSON:
        {
            "messages": [...],
            "saved_at": "...",
            "message_count": 15
        }
        """
        # 1) Ci assicuriamo che la cartella esista
        os.makedirs(self.conversations_dir, exist_ok=True)

        # 2) Timestamp attuale (ISO per i metadati)
        now = datetime.now().isoformat(timespec="seconds")  # es: "2025-01-19T11:05:32"

        # 3) Timestamp "safe" per il nome file (niente due punti)
        safe_timestamp = now.replace(":", "-")  # "2025-01-19T11-05-32"
        # 4) Costruisco il nome del file
        if name:
            # Pulizia del nome: tolgo spazi ai bordi e sostituisco spazi interni con underscore
            cleaned_name = name.strip().replace(" ", "_")
            if cleaned_name == "":
                cleaned_name = "untitled"
            filename = f"{safe_timestamp}_{cleaned_name}.json"
        else:
            filename = f"{safe_timestamp}.json"

        filepath = os.path.join(self.conversations_dir, filename)

        # 5) Preparo i dati da salvare (struttuta JSON)
        data = {
            "messages": self.messages,
            "saved_at": now,
            "message_count": len(self.messages),
        }

        # 6) Scrivi il file JSON
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("[ERRORE] Impossibile salvare la conversazione.")
            print("Dettagli tecnici:", e)
            return

        print(f"💾 Conversazione salvata in {filepath}")

    def list_conversations(self):
        """
        Mostra le conversazione slavate nella cartella configurata:
        - controlla se la cartella esiste
        - legge i file .json
        - stampa metadati (nome file, numero messaggi, data salvataggio)
        """
        # 1) Controlla se la cartella esiste
        if not os.path.exists(self.conversations_dir):
            print(
                f"📂 Nessuna conversazione salvata "
                f"(cartella '{self.conversations_dir}/' non trovata)."
            )
            return

        # 2) Lista dei file .json nella cartella
        files = [
            name
            for name in os.listdir(self.conversations_dir)
            if name.endswith(".json")
        ]

        if not files:
            print("📂 Nessuna conversazione salvata.")
            return

        print("📂 Conversazioni salvate: ")

        # 3) Per ognin file, leggi i metadati dal JSON
        for filename in sorted(files):
            filepath = os.path.join(self.conversations_dir, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"- {filename} | errore lettura file: {e}")
                continue

            # Estraggo i metadati con valori di default
            saved_at = data.get("saved_at", "data sconosciuta")
            message_count = data.get("message_count")

            # Fallback se non c'è message_count, lo calcolo da messages
            if message_count is None:
                msgs = data.get("messages")
                if isinstance(msgs, list):
                    message_count = len(msgs)
                else:
                    message_count = "sconosciuto"

            # 4) Stampa formattato
            print(f"- {filename} | messaggi: {message_count} | salvata il: {saved_at}")

    def load_conversation(self):
        """
        Carica una conversazione salvata:
        - mostra elenco numerato dei file disponibili
        - chiede all'utente quale numero selezionare
        - carica i messages del file scelto
        - sostituisce lo storico corrente (self.messages)
        """

        # 1) Controlla se la cartella esiste
        if not os.path.exists(self.conversations_dir):
            print(
                f"📂 Nessuna conversazione salvata "
                f"(cartella '{self.conversations_dir}/' non trovata)."
            )
            return

        # 2) Lista die file .json in carella
        files = [
            name
            for name in os.listdir(self.conversations_dir)
            if name.endswith(".json")
        ]

        if not files:
            print("📂 Nessuna conversazione salvata.")
            return

        files = sorted(files)

        print("📂 Conversazioni disponibili:")

        # 3) Mostra elenco numerato con metadati base
        for idx, filename in enumerate(files, 1):
            filepath = os.path.join(self.conversations_dir, filename)

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

            print(
                f"{idx}. {filename} | messaggi: {message_count} | salvata il: {saved_at}"
            )

        # 4) Chiedo all'utente quale conversazione vuole caricare
        while True:
            choice = input(
                "Seleziona il numero della conversazione da caricare"
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
                    f"inserisci un numero fra 1 e {len(files)}"
                    f"oppure premi Invio per annullare"
                )
                continue

            # Se arrivo qui input è valido --> esco dal while
            break

        selected_filename = files[index - 1]
        selected_path = os.path.join(self.conversations_dir, selected_filename)

        # 5) Carica i messages dal file selezionato
        try:
            with open(selected_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            loaded_messages = data.get("messages")

            if not isinstance(loaded_messages, list):
                print(
                    "❌ Formato file non valido: 'messages' mancante o non è una lista."
                )
                return

            # NESSUN global: sostituiamo lo storico sull'istanza
            self.messages = loaded_messages

            print(
                f"✅ Conversazione '{selected_filename}' caricata. "
                f"Messaggi: {len(self.messages)}"
            )

        except Exception as e:
            print("\n[ERRORE] Impossibile caricare la conversazione selezionata.")
            print("Dettagli tecnici", e)

    # === Metodi di inerazione con l'utente / comandi ===

    def chat(self, user_message: str) -> str:
        """
        Gestisce un turno di chat con GPT:
        - aggiunge il messaggio dell'utente allo storico
        - chiama l'API OpenAI con tutto lo storico
        - gestisce eventuali errori
        - aggiunge la risposta di GPT allo storico
        - restituisce il testo della risposta
        """
        # 1) Aggiungo il messaggio dell'utente allo storico
        self.messages.append({"role": "user", "content": user_message})

        try:
            # 2) Chiamata API con tutto lo storico
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
            )

        except Exception as e:
            # Gestione errore non crasha il programma
            print("\n[ERRORE] Problema durante la chiamata all'API OpenAI")
            print("Dettagli tecnici:", e)

            # Rimuovo ultimo messaggio utende dallo storico
            # perchè non è mai stato letto dal modello
            self.messages.pop()

            # risposta di cortesia all'utente
            return "Scusa, si è verificato un errore tecnico con l'AI. Riprova tra poco"

        # 3) Se tutto ok, estraggo testo della risposta di GPT
        assistant_message = response.choices[0].message.content

        # 4) Aggiungo la risposta di GPT allo storico
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def print_help(self):
        """Stampa la lista dei comandi disponibili."""
        print("💡 Comandi disponibili:")
        print("   /new             - Nuova conversazione")
        print("   /list            - Mostra conversazioni salvate")
        print("   /save [nome]     - Salva conversazione")
        print("   /load            - Carica conversazione")
        print("   /help            - Mostra questo aiuto")
        print("   /exit o /quit    - Esci dal programma")

    def parse_command(self, user_input: str):
        """
        Riconosce ed esegue i comandi digitati dall'utente.

        Ritorna:
        - False se NON è un comando (deve essere inviato a GPT)
        - True se è un comando gestito (non mandare a GPT)
        - "EXIT" se bisogna terminare il programma
        """
        if not user_input.startswith("/"):
            return False
        # Normalizza e separa comando e argomenti
        parts = user_input.strip().split()
        command = parts[0].lower()  # es: "/new"
        # args = parts[1:] # per futiri comandi con argomenti

        if command == "/new":
            self.new_conversation()
            return True

        elif command in ("/exit", "/quit"):
            print("👋 Arrivederci!")
            return "EXIT"

        elif command == "/list":
            self.list_conversations()
            return True

        elif command == "/save":
            # Prendo tutto quello che viene dopo il comando come nome opzionale
            if len(parts) > 1:
                # " ".join(parts[1:]) permette nomi con spazi: /save idea cliente
                name = " ".join(parts[1:])
            else:
                name = None

            self.save_conversation(name)
            return True

        elif command == "/load":
            self.load_conversation()
            return True

        elif command in ("/help", "/h"):
            self.print_help()
            return True

        print(f"❓ Comando sconosciuto: {command}")
        self.print_help()
        return True

    def run(self):
        """
        Loop principale della CLI:
        - stampa messaggio di benvenuto
        - legge input utente in un while True
        - gestisce input vuoti
        passi i comandi a parse_command()
        - per il testo normale chiama chat() e stampa il risultato
        """
        print("💬 CLI Chat GPT")
        print("Scrivi un messaggio e premi Invio.")
        print("Usa i comandi /new, /list, /save, /load, /exit\n")

        while True:
            # 1) Leggo input utente
            user_input = input("Tu: ")

            # 2)Se l'utente non scrive niente saltiamo il giro
            if user_input.strip() == "":
                print("(Scrivi qualcosa)")
                continue

            # 3) Prima: controllo se è un comando (tipo /new, /save, /load, /exit)
            result = self.parse_command(user_input)
            if result == "EXIT":
                break
            if result:
                # Era un comando gestito non mandiamo nulla a GPT
                continue

            # 4) Non è un comando: inviamo il messaggio a GPT)
            print("\nGPT sta scrivendo...")
            assistant_reply = self.chat(user_input)

            # 5) Stampa la risposta
            print("\nGPT:", assistant_reply, "\n")
