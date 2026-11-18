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

## Tool use -silmukan toiminta

Sovelluksessa tekoälymallille (`nvidia/nemotron-3.5-super-vl:free`) välitetään viestihistorian lisäksi `web_search`-työkalun kuvaus (`chat_core.py`). Kun käyttäjä lähettää kysymyksen `/chat`-reitille, `ask_chat()`-funktio kutsuu kielimallia OpenRouterin kautta. Jos malli arvioi tarvitsevansa ajantasaista tai ulkoista tietoa, se ei vastaa suoraan tekstinä vaan palauttaa `tool_calls`-pyynnön haluamallaan hakusanalla. Sovellus suorittaa tällöin `search.py`-tiedoston `web_search()`-funktion, joka hakee tiedon Wikipedian APIsta `curl`-komennolla, ja lähettää hakutuloksen takaisin mallille `tool`-roolilla. Lopuksi malli muodostaa varsinaisen vastauksen käyttäjälle hakutulosten pohjalta ja käyttöliittymä näyttää tiedon käytetystä hausta.

## Reflektio

1. **Agentin virheet ja niiden huomaaminen:** Suunnittelu- ja toteutusvaiheessa agentti ehdotti aluksi erilaista ympäristömuuttujan nimeä (`OPEN_ROUTER_UUS`) pohjatiedoston (`weather.py`) perusteella. Huomasin tämän jo suunnitteluvaiheessa ennen koodin kirjoittamista ja ohjasin sen käyttämään yhtenäistä `OPENROUTER_API_KEY`-muuttujaa. Lisäksi testausvaiheessa piti erikseen varmistaa, että OpenRouterin API-avaimen luottoraja ei ole nollassa, sillä muuten pyynnöt kaatuivat autentikointivirheeseen.

2. **Heikoimmin ymmärretty osa koodista:** Heikoimmin ymmärrän `chat_core.py`-tiedoston viestihistorian rakenteen siinä vaiheessa, kun mallille palautetaan työkalun tulos (`role: "tool"` ja `tool_call_id`). Jos jatkaisin projektia, tulostaisin välimuuttujien sisällön terminaaliin tai lukisin OpenAI:n function calling -dokumentaatiota ymmärtääkseni tarkemmin, miten keskustelun tila säilyy useamman peräkkäisen hakukierroksen aikana.

3. **Vaikutus oppimiseen:** Agentin käyttö nopeutti rutiinikoodin (kuten HTML-käyttöliittymän ja Flask-reittien) kirjoittamista huomattavasti ja auttoi hahmottamaan sovelluksen jakamisen loogisiin osiin (`search.py`, `chat_core.py`, `app.py`). Toisaalta valmiin koodin lukeminen ei opeta syntaksia yhtä syvällisesti kuin itse kirjoittaminen, joten arkkitehtuurin ja työnkulun ymmärtäminen korostui yksittäisten koodirivien sijaan.

4. **Mallin päätökset hakea tietoa:** Malli teki järkeviä päätöksiä: yleistietoon tai laskutoimituksiin (kuten yksinkertaisiin matemaattisiin kysymyksiin) se vastasi suoraan ilman työkalukutsua, mutta ajankohtaisissa faktakysymyksissä (kuten Suomen nykyistä presidenttiä kysyttäessä) se osasi kutsua `web_search`-työkalua ja hyödyntää hakutulosta vastauksessaan.
