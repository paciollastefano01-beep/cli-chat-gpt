# 💬 CLI Chat GPT

Chat da terminale con OpenAI GPT-3.5-turbo.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

---

## 📋 Descrizione

Applicazione da terminale per chattare con GPT-3.5-turbo di OpenAI. Un progetto educativo per imparare a integrare API di intelligenza artificiale in applicazioni Python.

### ✨ Funzionalità Attuali (Giorno 18)
- ✅ Chat interattiva con GPT-3.5-turbo
- ✅ Storico completo della conversazione
- ✅ Risposte in italiano
- ✅ Gestione errori e retry automatico
- ✅ Interfaccia CLI colorata e intuitiva

### 🔮 In Sviluppo (Giorno 19-21)
- ⏳ Salvataggio conversazioni con comando `/save`
- ⏳ Caricamento conversazioni salvate con `/load`
- ⏳ Reset chat con comando `/new`
- ⏳ Esportazione conversazioni in formato Markdown

---

## 🎬 Demo

<!-- SCREENSHOT 1: Avvio applicazione -->
![Avvio CLI](screenshots/01-avvio.png)
*Schermata di avvio dell'applicazione*

<!-- SCREENSHOT 2: Conversazione esempio -->
![Esempio conversazione](screenshots/02-conversazione.png)
*Esempio di conversazione con GPT-3.5-turbo*


---

## 🚀 Installazione

### Prerequisiti

Prima di iniziare, assicurati di avere:
- **Python 3.8 o superiore** installato ([Download Python](https://www.python.org/downloads/))
- **Account OpenAI** con API key ([Registrati qui](https://platform.openai.com/signup))
- **Crediti OpenAI** (minimo $5 consigliati per testing)

### Setup Rapido

**1. Clona il repository:**
```bash
git clone https://github.com/paciollastefano01-beep/cli-chat-gpt.git
cd cli-chat-gpt
```

**2. Crea ambiente virtuale (consigliato):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

**4. Configura l'API key:**

Crea un file chiamato `.env` nella root del progetto:
```plaintext
OPENAI_API_KEY=sk-proj-LA_TUA_CHIAVE_API_QUI
```

⚠️ **IMPORTANTE:** Ottieni la tua chiave API su [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## 💻 Utilizzo

### Avvio Applicazione

```bash
python main.py
```

### Comandi Disponibili

| Comando | Descrizione |
|---------|-------------|
| Scrivi un messaggio | Invia il messaggio a GPT |
| `exit` o `quit` | Termina l'applicazione |
| `/save` | (In sviluppo) Salva conversazione |
| `/load` | (In sviluppo) Carica conversazione |
| `/new` | (In sviluppo) Nuova conversazione |

### Esempio di Conversazione

```
💬 CLI Chat GPT
Scrivi un messaggio e premi Invio. Digita 'exit' per uscire.

Tu: Ciao, come stai?

GPT: Ciao! Sto bene, grazie per aver chiesto. Come posso aiutarti oggi?

Tu: Raccontami una barzelletta sui programmatori

GPT: Certo! Eccone una:
Perché i programmatori confondono Halloween e Natale?
Perché Oct 31 = Dec 25! 🎃🎄
(31 in ottale = 25 in decimale)

Tu: Spiega il machine learning in modo semplice

GPT: Il machine learning è come insegnare a un bambino a riconoscere
gli animali. Invece di dargli regole tipo "se ha 4 zampe e miagola è
un gatto", gli mostri tante foto di gatti finché impara da solo a
riconoscerli. Il computer fa lo stesso con i dati!

Tu: exit
👋 Arrivederci! Conversazione terminata.
```

---

## 🛠️ Tecnologie

- **Python 3.11** - Linguaggio di programmazione
- **OpenAI API** - GPT-3.5-turbo per intelligenza artificiale
- **python-dotenv** - Gestione sicura delle variabili d'ambiente

---

## 📁 Struttura Progetto

```
cli-chat-gpt/
├── screenshots/          # Screenshot per documentazione
│   ├── 01-avvio.png
│   ├── 02-conversazione.png
│   └── 03-errori.png
├── .env                  # API key (NON committare!)
├── .gitignore           # File da ignorare su Git
├── main.py              # Codice principale applicazione
├── requirements.txt     # Dipendenze Python
└── README.md           # Questa documentazione
```

---

## 💰 Costi API

### Modello GPT-3.5-turbo

| Tipo | Costo |
|------|-------|
| **Input** | $0.50 per 1M token |
| **Output** | $1.50 per 1M token |

### Stime Pratiche

- **Una conversazione tipica (10 messaggi):** ~$0.002 (0.2 centesimi)
- **100 conversazioni:** ~$0.20
- **Credito $5:** ~2.500 conversazioni

💡 **Tip:** Monitora i costi su [platform.openai.com/usage](https://platform.openai.com/usage)

---

## 🔒 Sicurezza

### ⚠️ Regole Fondamentali

1. **MAI committare il file `.env` su GitHub!**
2. **MAI condividere la tua API key** pubblicamente
3. **Rigenera la chiave** se esposta accidentalmente

### File Protetti da `.gitignore`

```
.env
__pycache__/
*.pyc
*.pyo
venv/
.vscode/
.idea/
```

### Se Hai Esposto la Chiave

1. Vai su [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Elimina la chiave compromessa
3. Crea una nuova chiave
4. Aggiorna il file `.env`

---

## 📝 Roadmap

### ✅ Fase 1 - Base (Completata)
- [x] Connessione API OpenAI
- [x] Chat interattiva funzionante
- [x] Gestione errori base
- [x] README documentazione

### 🔄 Fase 2 - Persistenza (In corso)
- [ ] Comando `/save` per salvare chat
- [ ] Comando `/load` per caricare chat salvate
- [ ] Comando `/new` per reset conversazione
- [ ] Formato JSON per storage

### 🔮 Fase 3 - Miglioramenti (Futuri)
- [ ] Refactoring con OOP (classi)
- [ ] Indicatore "GPT sta scrivendo..."
- [ ] Colorazione sintassi codice
- [ ] Statistiche conversazione (token, costi)
- [ ] Export in Markdown/PDF
- [ ] Supporto GPT-4

---

## 🐛 Troubleshooting

### Problema: "API key non valida"

**Soluzione:**
```bash
# Verifica che .env contenga la chiave corretta
# Assicurati che non ci siano spazi extra
OPENAI_API_KEY=sk-proj-TUA_CHIAVE  # ❌ Spazio dopo!
OPENAI_API_KEY=sk-proj-TUA_CHIAVE   # ✅ Corretto
```

### Problema: "ModuleNotFoundError: No module named 'openai'"

**Soluzione:**
```bash
# Reinstalla dipendenze
pip install -r requirements.txt

# Oppure installa manualmente
pip install openai python-dotenv
```

### Problema: "Rate limit exceeded"

**Soluzione:**
- Hai superato il limite di richieste/minuto
- Aspetta 60 secondi
- Riprova la richiesta

### Problema: "Insufficient credits"

**Soluzione:**
- Crediti OpenAI esauriti
- Aggiungi credito su [platform.openai.com/billing](https://platform.openai.com/billing)

---

## 🤝 Contribuire

Contributi benvenuti! Se vuoi migliorare il progetto:

1. **Fork** del repository
2. Crea un **branch** per la feature (`git checkout -b feature/nuova-funzione`)
3. **Commit** delle modifiche (`git commit -m 'Aggiunta nuova funzione'`)
4. **Push** al branch (`git push origin feature/nuova-funzione`)
5. Apri una **Pull Request**

---

## 👤 Autore

**Stefano Paciolla**

- 📧 Email: [paciollastefano01@gmail.com](mailto:paciollastefano01@gmail.com)
- 🔗 LinkedIn: [linkedin.com/in/stefano-paciolla-561519209](https://www.linkedin.com/in/stefano-paciolla-561519209/)
- 🐙 GitHub: [@paciollastefano01-beep](https://github.com/paciollastefano01-beep)

💼 **AI Automation Specialist** in formazione
🎯 Progetto #1 del percorso da 180 giorni in AI e Automazione

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza **MIT License**.

Puoi:
- ✅ Usare commercialmente
- ✅ Modificare
- ✅ Distribuire
- ✅ Uso privato

Vedi il file [LICENSE](LICENSE) per i dettagli completi.

---

## 🙏 Crediti

- [OpenAI](https://openai.com/) per l'API GPT-3.5-turbo
- [Python Software Foundation](https://www.python.org/) per Python
- Community open-source per le librerie utilizzate

---

## ⭐ Supporto

Se questo progetto ti è stato utile:

- ⭐ Lascia una **stella** al repository
- 🐛 Segnala **bug** o **problemi**
- 💡 Proponi **nuove feature**
- 📢 **Condividi** con altri sviluppatori

---

## 📚 Risorse Utili

- [Documentazione OpenAI API](https://platform.openai.com/docs)
- [Guida Python Dotenv](https://pypi.org/project/python-dotenv/)
- [Best Practices API Keys](https://platform.openai.com/docs/guides/production-best-practices)

---

**Buon coding! 🚀**
