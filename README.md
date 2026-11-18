# Hakuchat (Flask + OpenRouter + web_search)

Flask-pohjainen chat-sovellus, joka käyttää OpenRouteria (malli `nvidia/nemotron-3.5-super-vl:free`) ja `web_search`-työkalua. Malli voi kutsu `web_search`-funktiota, joka hakee tietoa Wikipedian API:sta `curl`-komennolla ja palauttaa tiiviin yhteenvedon lähdelinkeineen.

## Rakenne

- `app.py` — Flask-palvelin, reitit `/` ja `/chat`
- `chat_core.py` — OpenAI-kutsu ja työkalukutsujen käsittely (`ask_chat`)
- `search.py` — `web_search`-funktio (Wikipedia API, curl)
- `templates/index.html` — chat-käyttöliittymä
- `requirements.txt` — riippuvuudet

## Asennus

```bash
pip install -r requirements.txt
```

## Käynnistäminen

Aseta OpenRouterin API-avain ympäristömuuttujaan ja käynnistä palvelin:

```bash
OPENROUTER_API_KEY=<avaimesi> python app.py
```

Avaa selaimessa: `http://127.0.0.1:5000`

## Huomioita

- API-avain luetaan suoraan ympäristöstä (`os.environ["OPENROUTER_API_KEY"]`), ei `.env`-tiedostoa.
- `web_search` käyttää `curl`-komentoa (`subprocess`), ei valmista hakukirjastoa.
- Jos mallin kutsuma työkalu epäonnistuu, virhe näkyy chatissa.
