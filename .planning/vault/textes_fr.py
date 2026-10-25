"""Textes FRANCAIS des 27 cartes de The Vault : ajoutes (idempotent) a la fin de ui-app/src/board/textes-fr-fanmade.ts ET de
Fusion/marvel-lcg-src/public/js/traduction/textes-fr-fanmade.js. Usage : python3 .planning/vault/textes_fr.py"""
import os, re, sys
RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TS = os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")
JS = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "js", "traduction", "textes-fr-fanmade.js")

REP = "<b>Réponse forcée</b> : après que vous avez attaqué {nom} avec une carte que vous contrôlez, choisissez : {a} ou placez 1 menace sur la manigance principale."
VILAINS = {
    "Batroc": ("1", "défaussez les 3 premières cartes du deck de rencontre", "chaque joueur défausse les 5 premières cartes de son deck", "« Sacre Bleu! You are fastaire than ever Avengaire. »"),
    "Mentallo": ("2", "inclinez votre identité", "chaque joueur incline un personnage qu'il contrôle", "« Drôle comme les hallucinations peuvent parfois sembler si réelles. »"),
    "Grey Gargoyle": ("3", "sonnez l'attaquant", "chaque joueur sonne un personnage qu'il contrôle", "« Pardonnez-moi de ne pas vous serrer la main, monsieur... »"),
    "Hydro-Man": ("4", "infligez 1 dégât à chaque personnage que vous contrôlez", "infligez 1 dégât à chaque personnage allié", None),
    "Mad Thinker": ("5", "placez 1 menace sur chaque manigance annexe", "placez 1 menace sur la manigance principale pour chaque ennemi en jeu", "« Je prévois toutes les éventualités ! »"),
    "Nekra": ("6", "donnez à Nekra 1 carte de boost face cachée", "donnez à chaque méchant 1 carte de boost face cachée", "« Nekra n'a besoin de l'aide de personne !! »"),
    "Vapor": ("7", "désorientez l'attaquant", "chaque joueur désoriente un personnage qu'il contrôle", "« ...on ne frappe pas ce dont on ne peut toucher la forme ! »"),
    "Venom": ("8", "soignez-le de 1 dégât", None, "« The Vault ne peut pas nous retenir, minable ! On s'en est déjà évadés deux fois ! »"),
}
CITATION_HYDRO = "« ...il suffit que je « tsunamise » cet idiot de grimpe-murs... »"
T = {}
for i, (nom, (ordre, a, wr, cit)) in enumerate(VILAINS.items()):
    for stade in (1, 2):
        n = 2 * i + stade
        txt = f"<b>Ordre d'activation {ordre}</b>\n"
        if nom == "Venom" and stade == 2:
            txt += "Robuste. Tenacité.\n"
        if stade == 2 and wr:
            txt += f"<b>Une fois révélée</b> : {wr}.\n"
        txt += REP.format(nom=nom, a=a)
        c = CITATION_HYDRO if nom == "Hydro-Man" and stade == 1 else cit
        if c:
            txt += f"\n<i>{c}</i>"
        T[f"vt{n:03d}"] = (nom + (" (II)" if stade == 2 else " (I)"), "Villain", txt)

T["vt017a"] = ("The Vault Breakout (1A)", "MainScheme",
    "<b>Contenu</b> : tous les méchants (I) <i>(les stades (II) à la place en mode expert)</i>. Ensembles de rencontre The Vault et Standard. Un ensemble modulaire de rencontre <i>(Sinister Syndicate)</i>.\n"
    "<b>Mise en place</b> : créez le deck de méchants <i>(voir l'encart)</i>. Mettez en jeu l'environnement The Vault. Puis glissez dessous, face cachée, les 4 premières cartes méchant et le sbire némésis ([unique]) de chaque joueur. Mettez de côté, hors jeu, l'obligation Inspection of the Vault.")
T["vt017b"] = ("The Vault Breakout (1B)", "MainScheme",
    "<b>Une fois révélée</b> : révélez la première carte du deck de méchants.\n"
    "[star] <b>Interruption forcée</b> : quand cette manigance serait accomplie, faites à la place chacune des actions suivantes :\n"
    "1. Retirez d'ici toute la menace sauf 1[per_hero].\n2. Révélez 1 méchant au hasard sous The Vault.\n3. Révélez Inspection of the Vault.")
T["vt018"] = ("The Vault", "Environment",
    "<b>Réponse forcée</b> : après qu'un sbire unique ([unique]) est vaincu, glissez-le sous The Vault, face cachée.\n"
    "<b>Si aucun méchant n'est sous The Vault, les joueurs perdent la partie.</b>\n"
    "<b>Si tous les méchants sont soit sous The Vault, soit vaincus, les joueurs gagnent la partie.</b>")
T["vt019"] = ("Inspection of the Vault", "Obligation",
    "<b><i>À donner au premier joueur.</i></b>\n<b>Action d'alter ego</b> : inclinez votre identité et dépensez une ressource [mental] → mettez cette carte de côté, hors jeu.\n"
    "<i>« Il y a ici des mesures de sécurité pour lesquelles on m'a donné une pile de livres afin de m'aider à comprendre. »</i> —Warden")
T["vt020"] = ("Craven Escape", "Attachment",
    "Attachez-la au méchant qui a le moins de points de vie restants et qui n'a pas déjà une autre Craven Escape. Si vous ne pouvez pas, cette carte gagne Renfort.\n"
    "<b>Réponse forcée</b> : après la fin de la phase des joueurs, mélangez le méchant attaché dans le deck de méchants.\n"
    "<i>« Comment tu as survécu n'a pas d'importance ! Ce qui compte, c'est que tu aies survécu ! »</i> —Venom")
T["vt022"] = ("Corrupted Guardsman", "Minion",
    "Incitation 1.\n<b>Une fois révélée</b> : si Inspection of the Vault est en jeu, révélez 1 sbire au hasard sous The Vault. Si vous ne pouvez pas, cette carte gagne Renfort.\n"
    "[star] <b>Boost</b> : mélangez dans le deck de rencontre 1 sbire de sous The Vault.")
T["vt026"] = ("Burglary", "SideScheme",
    "<b>Une fois révélée</b> : si Inspection of the Vault est en jeu, placez ici 1[per_hero] menace supplémentaire.\n"
    "<b>Une fois déjouée</b> : révélez la première carte du deck de méchants.")
T["vt028"] = ("Contingency Measures", "SideScheme",
    "<i>« Puisque je ne peux te plier à ma volonté... je crains de devoir te briser ! »</i> —Senso\n"
    "<b>Interruption forcée</b> : quand un méchant serait vaincu, mélangez-le à la place dans le deck de méchants.\n"
    "Tant qu'Inspection of the Vault est en jeu, cette carte gagne une icône d'aléas ([hazard]).")
T["vt029"] = ("Scheming from Within", "SideScheme",
    "<b>Une fois révélée</b> : placez ici 1 menace supplémentaire pour chaque méchant sous The Vault.\n"
    "[star] <b>Boost</b> : si Inspection of the Vault est en jeu, cette carte gagne +1 icône de boost ([boost]) pour chaque méchant sous The Vault.")
T["vt030"] = ("Rampage in Public", "Treachery",
    "<b>Une fois révélée</b> : si le nombre de méchants en jeu est inférieur au nombre de joueurs, cette carte gagne Renfort. Révélez la première carte du deck de méchants. "
    "Si vous ne pouvez pas, le méchant dont l'ordre d'activation est le plus élevé s'active contre vous.")
T["vt034"] = ("Riot in the Vault", "Treachery",
    "Renfort.\n<b>Une fois révélée</b> : si Inspection of the Vault n'est pas en jeu, révélez-la. Sinon, placez 1 menace sur la manigance principale pour chaque méchant sous The Vault.\n"
    "<i>« Aucune prison ne peut retenir un esprit tel que le mien. »</i> —Mad Thinker")


def echapper(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def ajouter(chemin, indent, fin):
    contenu = open(chemin, encoding="utf-8").read()
    if "'vt001'" in contenu:
        print(chemin, ": deja present"); return
    bloc = "".join(f"{indent}// the vault — {nom} ({typ})\n{indent}'{cid}': \"{echapper(txt)}\",\n" for cid, (nom, typ, txt) in sorted(T.items()))
    i = contenu.rindex(fin)
    open(chemin, "w", encoding="utf-8").write(contenu[:i] + bloc + contenu[i:])
    print(chemin, ":", len(T), "textes ajoutes")

ajouter(TS, "  ", "\n}")
ajouter(JS, "    ", "\n};")
