"""Le contenu de la bande du bas de l'ecran de connexion : anecdotes de comics et conseils sur le jeu.

  - ANECDOTES : `anecdotes_comics.json`, un objet par fait, avec `fr`, `en` et `source` (la page Wikipedia de laquelle
    le fait a ete releve le 18/11/2026). RIEN n'y est ecrit de memoire : chaque date et chaque numero vient de la page.
    A relire par l'utilisateur avant la mise en ligne.
  - ASTUCES : ci-dessous. Chacune decrit quelque chose qui existe dans le code (la reference est dans le commentaire).

`pour_la_page(langue, rng)` rend ce que la page embarque : la liste melangee (une anecdote, une astuce, une anecdote...),
l'indice de depart (tire au hasard a chaque visite) et les deux etiquettes.
"""
import json
import os
import random

ICI = os.path.dirname(os.path.abspath(__file__))

NOMS = {
    "fr": {"comics": "Le saviez-vous ?", "astuce": "Astuce"},
    "en": {"comics": "Did you know?", "astuce": "Tip"},
}

# Combien d'anecdotes une page embarque (le fichier en contient bien plus).
TAILLE_TIRAGE = 40

ASTUCES = [
    # ui-app/src/board : le volet de reglages du plateau (disposition de l'ecran, affichage, langue).
    {"fr": "Dans les réglages, tu peux changer la disposition de l'écran, l'affichage et la langue du plateau.",
     "en": "In the settings you can change the screen layout, the display and the language of the board."},
    # ui-app/src/board.tsx : sauvegarde automatique au debut de chaque phase + trois emplacements manuels.
    {"fr": "Le jeu se sauvegarde tout seul au début de chaque phase. Tu as aussi trois emplacements à toi avec le bouton Save.",
     "en": "The game saves itself at the start of every phase. You also have three slots of your own with the Save button."},
    # site/orchestrateur.py (_pied_de_page) : les invites rejoignent par leur lien, sans compte.
    {"fr": "Pour jouer à plusieurs, envoie leur lien à tes amis : ils rejoignent ta partie sans avoir besoin d'un compte.",
     "en": "To play with friends, send them their link: they join your game without needing an account."},
    # selection des heros : filtre Fan-made, bordure doree.
    {"fr": "Les héros fan-made ont une bordure dorée dans la sélection, et un filtre rien que pour eux.",
     "en": "Fan-made heroes have a gold border in the hero selection, and a filter just for them."},
    # site/orchestrateur.py : le createur de cartes est ouvert a tout compte connecte.
    {"fr": "Avec un compte, tu peux fabriquer tes propres cartes dans MC Creator.",
     "en": "With an account, you can make your own cards in MC Creator."},
    # public/js/prepare/reprise.js : « Reprendre une partie », « Statistiques », hauts faits.
    {"fr": "L'écran de préparation garde tes statistiques, tes hauts faits et la liste de tes parties à reprendre.",
     "en": "The setup screen keeps your statistics, your feats and the list of games you can resume."},
    # public/sandbox.html + memoire bac-a-sable : clic droit = mettre en main / en jeu.
    {"fr": "Dans le bac à sable, un clic droit sur une carte la met en main ou en jeu : pratique pour tester un effet.",
     "en": "In the sandbox, right-clicking a card puts it in your hand or into play: handy to test an effect."},
    # ui-app/src/board : volets Aide, Tchat, Journal.
    {"fr": "Le journal de la partie, le tchat et l'aide sont dans des volets sur le bord de l'écran, ou dans le menu « … » sur téléphone.",
     "en": "The game log, the chat and the help are in panels on the edge of the screen, or in the “…” menu on a phone."},
    # tools/cas : decks importables dans l'assistant.
    {"fr": "Tu as déjà un deck ailleurs ? Tu peux l'importer dans l'assistant au lieu de le refaire carte par carte.",
     "en": "Already have a deck somewhere else? You can import it in the setup screen instead of rebuilding it card by card."},
]


def _anecdotes() -> list:
    chemin = os.path.join(ICI, "anecdotes_comics.json")
    try:
        with open(chemin, encoding="utf-8") as f:
            return [a for a in json.load(f) if a.get("fr") and a.get("en")]
    except (OSError, ValueError):
        return []


def pour_la_page(langue: str, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    lg = "en" if langue == "en" else "fr"
    comics = [{"type": "comics", "texte": a[lg], "source": a.get("source_fr" if lg == "fr" else "source", "")} for a in _anecdotes()]
    astuces = [{"type": "astuce", "texte": a[lg], "source": ""} for a in ASTUCES]
    # Plusieurs centaines d'anecdotes : la page n'en embarque qu'un tirage (poids de la page, et chaque visite en montre d'autres).
    rng.shuffle(comics)
    rng.shuffle(astuces)
    comics = comics[:TAILLE_TIRAGE]
    # Une astuce pour deux anecdotes : on lit surtout des histoires de heros, avec un conseil de temps en temps.
    items, ia = [], 0
    for k, c in enumerate(comics):
        items.append(c)
        if k % 2 == 1 and ia < len(astuces):
            items.append(astuces[ia]); ia += 1
    items += astuces[ia:]
    if not items:
        items = astuces
    return {"items": items, "depart": rng.randrange(len(items)), "noms": NOMS[lg]}
