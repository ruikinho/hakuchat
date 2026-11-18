# PROMPTS.md

Tässä tiedostossa on koottuna kehityksen vaiheet ja käytetyt promptit. Työ eteni askel kerrallaan, jotta kukin osa voitiin testata erikseen ennen seuraavan lisäämistä.

## Vaihe 1: search.py

**Prompt:** Luo `search.py`, jossa on funktio `web_search(query: str) -> str`, joka hakee tietoa Wikipedian APIsta curl-komennolla ja palauttaa tiiviin tekstiyhteenvedon sekä lähdelinkit. Älä luo vielä muita tiedostoja. Testaa lopuksi että `search.py` toimii yhdellä esimerkkihaulla.

**Miksi:** Eriennetty verkkohakulogiikka omaksi moduulikseen, jotta se voidaan testata erikseen ilman OpenAI-kutsua tai Flaskia.

## Vaihe 2: chat_core.py

**Prompt:** Luo `chat_core.py`, jossa käytetään openai-kirjastoa, OpenRouteria ja mallia `nvidia/nemotron-3.5-super-vl:free` (lue API-avain ympäristömuuttujasta `OPENROUTER_API_KEY`). Liitä mukaan `web_search`-työkalu `search.py:stä` tool use -muodossa. Toteuta funktio `ask_chat(messages)`, joka lähettää viestihistorian mallille, suorittaa mahdolliset tool_call-kutsut (web_search) ja palauttaa lopullisen vastauksen sekä tiedon siitä, mitä hakua käytettiin. Älä tee vielä Flaskia tai HTML:ää.

**Miksi:** Keskitetty OpenAI-vuorovaikutus ja tool-kutsujen käsittely yhteen moduuliin, testattavissa ilman verkkopalvelinta.

## Vaihe 3: app.py + index.html + requirements.txt + .gitignore

**Prompt:** Luo `app.py` (Flask-palvelin) ja `index.html` (tai `templates/index.html`). Palvelimen tulee tarjota etusivu (`/`) sekä `/chat`-reitti, joka ottaa vastaan käyttäjän viestin (ja mahdollisen keskusteluhistorian), kutsuu `chat_core.py:n` `ask_chat`-funktiota ja palauttaa JSON-muodossa vastauksen sekä tiedon käytetyistä hauista. Tee `index.html:stä` selkeä, moderni chat-käyttöliittymä, jossa näkyy myös tieto jos tekoäly teki verkkohaun (esim. "Haettiin: ..."). Luo myös `requirements.txt` (`flask`, `openai`) ja `.gitignore` (`.env`, `__pycache__`, `*.pyc`).

**Miksi:** Sovelluksen pinta ja API-kytkennät lisättiin vasta kun backend-logikka oli valmis ja testattu.

## Miksi askel kerrallaan?

Jokainen vaihe eristää oman huolenaiheensa:

1. `search.py` — data/haku
2. `chat_core.py` — mallin ja työkalujen vuorovaikutus
3. `app.py` + `index.html` — käyttöliittymä ja API-pinta

Tämä helpottaa vianetsintää: jos jotain ei toimi, vian lähde on tiedossa ilman että koko sovellusta tarvitsee käynnistää kerralla.
