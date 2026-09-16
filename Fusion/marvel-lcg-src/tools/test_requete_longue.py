"""Le lancement d'une partie passe par l'URL : elle doit pouvoir etre longue.

⚠ POURQUOI CE FICHIER EXISTE (16/09/2026). Un joueur s'est retrouve bloque net :
sa table repondait, mais lancer une partie ne faisait RIEN. Dans le journal de
son moteur :

    aiohttp.http_exceptions.LineTooLong: 400, message:
      Got more than 8190 bytes when reading: b'/new?data=%7B%22campaign_json...'

`GET /new?data=<descripteur>` fait tenir dans l'URL le scenario ENTIER et le
deck de CHAQUE joueur. aiohttp plafonne la ligne de requete a 8190 octets par
defaut, et rend un 400 que rien ne montre au joueur.

Ce n'etait pas un cas extreme : mesure sur le depot le meme jour, le deck de
depart le plus gros pese **7861 octets une fois encode**, a lui seul. Une
partie ORDINAIRE a un joueur franchissait donc la limite.

Ce test monte un aiohttp configure comme le moteur et prouve les deux sens :
sans le reglage la requete est refusee, avec lui elle passe.

Usage : python3 tools/test_requete_longue.py
"""
import asyncio
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "src", "engine", "network", "web_server.py")

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def limite_du_moteur() -> int:
    """La valeur ECRITE DANS LE MOTEUR, pas une copie qui divergerait."""
    texte = open(SOURCE, encoding="utf-8").read()
    trouve = re.search(r"^MAX_LIGNE_REQUETE\s*=\s*(\d+)\s*\*\s*(\d+)", texte, re.M)
    if trouve:
        return int(trouve.group(1)) * int(trouve.group(2))
    brut = re.search(r"^MAX_LIGNE_REQUETE\s*=\s*(\d+)", texte, re.M)
    return int(brut.group(1)) if brut else 0


def le_runner_est_configure() -> bool:
    """Le reglage doit etre PASSE au runner : une constante seule ne sert a rien."""
    texte = open(SOURCE, encoding="utf-8").read()
    return ("max_line_size=MAX_LIGNE_REQUETE" in texte
            and "max_field_size=MAX_LIGNE_REQUETE" in texte)


async def essai(limite, taille) -> str:
    from aiohttp import web
    import aiohttp

    app = web.Application()

    async def repondre(requete):
        return web.Response(text="ok:" + str(len(requete.query.get("data", ""))))

    app.router.add_get("/new", repondre)
    reglages = {"max_line_size": limite, "max_field_size": limite} if limite else {}
    runner = web.AppRunner(app, **reglages)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 2399)
    await site.start()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:2399/new?data=" + "x" * taille) as reponse:
                return "%d" % reponse.status
    except Exception as souci:
        return type(souci).__name__
    finally:
        await runner.cleanup()


async def tout() -> None:
    limite = limite_du_moteur()
    print("Le moteur accepte une URL longue")
    verifier("la constante existe et est genereuse",
             limite >= 64 * 1024, "lue : %d" % limite)
    verifier("elle est PASSEE au runner, pas seulement declaree",
             le_runner_est_configure())

    # 34 000 octets : une table a quatre joueurs avec les plus gros decks.
    defaut = await essai(None, 34000)
    verifier("sans le reglage, une vraie partie est REFUSEE (c'est le defaut)",
             defaut == "400", "obtenu : " + defaut)
    await asyncio.sleep(0.2)

    avec = await essai(limite, 34000)
    verifier("avec le reglage du moteur, elle passe", avec == "200", "obtenu : " + avec)
    await asyncio.sleep(0.2)

    # Le pire cas mesure sur le depot, avec de la marge.
    large = await essai(limite, 100000)
    verifier("et 100 000 octets passent encore", large == "200", "obtenu : " + large)


asyncio.run(tout())
print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
