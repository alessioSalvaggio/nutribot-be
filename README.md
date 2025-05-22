# Nutribot REST API

Nutribot è un server API RESTful sviluppato con FastAPI e Uvicorn, progettato per la gestione di dati nutrizionali, pazienti, diete e molto altro. Il progetto è pensato per essere scalabile, modulare e facilmente estendibile.

## Struttura del Progetto

```
nutribot
├── app
│   ├── main.py                   # Entry point dell'applicazione FastAPI
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── manage_patients.py      # Endpoint gestione pazienti
│   │       ├── manage_measurements.py  # Endpoint gestione misurazioni
│   │       ├── manage_payments.py      # Endpoint pagamenti
│   │       ├── manage_diets.py         # Endpoint gestione diete
│   │       └── ...                     # Altri endpoint
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py              # Configurazioni applicative
│   │   ├── mongo_core.py          # Wrapper per accesso a MongoDB
│   │   └── data_accessibility.py  # Controllo accesso ai dati
│   ├── models
│   │   └── __init__.py
│   ├── schemas
│   │   └── __init__.py
│   ├── services
│   │   └── __init__.py
│   └── utils
│       ├── diet_utils.py          # Utility per generazione diete
│       └── ...                    # Altre utility
├── requirements.txt               # Dipendenze Python
├── Dockerfile                     # Configurazione Docker
├── .env                           # Variabili d'ambiente
└── README.md                      # Documentazione progetto
```

## Setup

1. **Clona il repository:**
   ```bash
   git clone https://github.com/yourusername/nutribot.git
   cd nutribot
   ```

2. **Crea un ambiente virtuale:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura le variabili d'ambiente:**
   - Crea un file `.env` e imposta le variabili richieste (es. connessione MongoDB, chiavi API, ecc).

5. **Avvia l'applicazione:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Utilizzo

- L'API sarà disponibile su `http://127.0.0.1:8000` (o sulla porta configurata).
- La documentazione interattiva è accessibile su `http://127.0.0.1:8000/docs`.

## Funzionalità principali

- Gestione pazienti e dati anagrafici
- Gestione misurazioni e progressi
- Generazione automatica di diete personalizzate tramite AI
- Esportazione di diete in PDF
- Gestione pagamenti e accessi
- Middleware di autenticazione e CORS

## Contribuire

Contributi e segnalazioni sono benvenuti! Apri una issue o una pull request per proporre miglioramenti o nuove funzionalità.

## Licenza

Questo progetto è distribuito sotto licenza MIT. Consulta il file LICENSE per dettagli.