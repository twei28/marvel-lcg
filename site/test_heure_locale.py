"""Le temps du site : le serveur envoie un instant, le navigateur ecrit l'heure.

    python3 site/test_heure_locale.py

⚠ LE CAS QUI COMPTE LE PLUS est `le_fuseau_du_serveur_ne_change_rien`. Tout le
reste en decoule : tant que le serveur formate une heure destinee a un humain,
il se trompe pour tout le monde sauf pour quelqu'un qui vivrait dans son
fuseau. Ce test deplace le serveur a Tokyo et a Los Angeles et exige que rien
ne bouge.

Constat d'origine, 14/09/2026 : l'utilisateur lit 07:26 sur sa montre, le site
affiche 05:26. Le serveur tourne en `Etc/UTC`.
"""

import os
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, obtenu, attendu):
    if obtenu == attendu:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : obtenu {obtenu!r}, attendu {attendu!r}")
        echecs.append(nom)


class Fuseau:
    """Deplace le processus dans un fuseau, le temps d'un bloc."""

    def __init__(self, nom):
        self.nom = nom

    def __enter__(self):
        self.avant = os.environ.get("TZ")
        os.environ["TZ"] = self.nom
        time.tzset()
        return self

    def __exit__(self, *_):
        if self.avant is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = self.avant
        time.tzset()


# 2026-09-14 05:26:00 UTC, l'instant du constat.
INSTANT = 1789363560
CHAINE = "2026-09-14 05:26"


def main():
    print("L'horodatage stocke est de l'UTC, et se relit comme tel")
    verifier("chaine -> instant", o._epoque_de(CHAINE), INSTANT)
    verifier("instant -> chaine", time.strftime("%Y-%m-%d %H:%M", time.gmtime(INSTANT)), CHAINE)
    verifier("chaine illisible -> None", o._epoque_de("hier soir"), None)
    verifier("None -> None", o._epoque_de(None), None)

    print("\nle_fuseau_du_serveur_ne_change_rien")
    lectures = {}
    ecritures = {}
    for fuseau in ("UTC", "Asia/Tokyo", "America/Los_Angeles", "Europe/Brussels"):
        with Fuseau(fuseau):
            lectures[fuseau] = o._epoque_de(CHAINE)
            # `_maintenant` doit ecrire l'heure UTC, quel que soit le fuseau.
            ecritures[fuseau] = o._maintenant()
    verifier("une chaine stockee se lit pareil depuis n'importe ou",
             len(set(lectures.values())), 1)
    verifier("une chaine ecrite est la meme depuis n'importe ou",
             len(set(ecritures.values())), 1)
    with Fuseau("UTC"):
        attendue = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    verifier("et cette chaine est bien de l'UTC", set(ecritures.values()), {attendue})

    print("\nLes durees ne dependent d'aucun fuseau")
    ages = {}
    for fuseau in ("UTC", "Asia/Tokyo", "America/Los_Angeles"):
        with Fuseau(fuseau):
            ages[fuseau] = round(o._age_secondes(CHAINE) / 3600)
    verifier("l'age d'une ligne est le meme partout", len(set(ages.values())), 1)
    verifier("un horodatage illisible vaut l'infini, pas zero",
             o._age_secondes("n'importe quoi"), float("inf"))
    verifier("_secondes_depuis suit la meme regle",
             round(o._secondes_depuis(CHAINE)) == round(o._age_secondes(CHAINE)), True)

    print("\nLe HTML porte un instant, pas une heure")
    rendu = o._horodate(CHAINE)
    verifier("balise time avec data-ts", f'data-ts="{INSTANT}"' in rendu, True)
    verifier("la chaine UTC reste en secours dans la balise", CHAINE in rendu, True)
    verifier("une date illisible ne fabrique pas de fausse balise",
             "<time" in o._horodate("hier soir"), False)
    verifier("et elle reste echappee",
             o._horodate("<script>"), "&lt;script&gt;")

    print("\nLes pages qui montrent des dates embarquent le script")
    for nom in ("PAGE", "PAGE_ADMIN"):
        verifier(f"{nom} sait mettre a l'heure", "time[data-ts]" in getattr(o, nom), True)
    # ⚠ PAGE_SUIVI n'affiche que des durees : elle n'en a pas besoin, et la
    # garde `_avec_heure_locale` refuserait de l'y coller faute de </main>.
    verifier("PAGE_SUIVI n'en a pas besoin (que du relatif)",
             "time[data-ts]" in o.PAGE_SUIVI, False)

    print("\nLa garde : un gabarit sans </main> ne passe pas en silence")
    try:
        o._avec_heure_locale("<p>sans main</p>", "GABARIT_DE_TEST")
        verifier("elle leve", "rien leve", "RuntimeError")
    except RuntimeError as erreur:
        verifier("elle leve et nomme le gabarit", "GABARIT_DE_TEST" in str(erreur), True)

    print()
    if echecs:
        print(f"{len(echecs)} ECHEC(S) : " + ", ".join(echecs))
        return 1
    print("tout est vert")
    return 0


if __name__ == "__main__":
    sys.exit(main())
