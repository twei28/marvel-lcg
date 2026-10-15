"""Genere defs/secret_invasion_fr.txt (UNE entree par card_id : sk189a ... sk227b) a partir de secret_invasion_cards.py.

Vocabulaire : Guide de reference FR (« Une fois révélé(e) », « Réponse forcée », « Interruption forcée », « Action de héros »,
Garde, Riposte, Ténacité, Coup rapide, Déferlement, Perçant, Distance, Vilenie, Incitation, Renfort, carte d'état Tenace,
« dégâts consécutifs ») ; modele : defs/paibok_fr.txt. Les traits [[TRAIT]] et les noms propres restent en anglais.
Les textes d'ambiance (flavor) ne sont pas repris en francais (comme sk111).
Usage : python3 .planning/skrull-menace/defs/generer_fr_secret_invasion.py
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from secret_invasion_cards import CARDS, IMP  # noqa: E402

WDYT = "\\\"Who Do You Trust?\\\""
FR = {}

# ---------------------------------------------------------------------------------------------------------------------
SW = ("Spider-Woman ne peut pas subir de dégâts.\\n[star] <b>Réponse forcée</b> : après que Spider-Woman vous a attaqué, placez 1 jeton de "
      f"soupçon sur {WDYT}.\\n<i>You are a Skrull!</i> — <b>Action de héros</b> : inclinez un héros et dépensez 1[per_hero] ressources de "
      "n'importe quel type → retournez Spider-Woman. <i>(Les joueurs peuvent payer les coûts de cette capacité en groupe.)</i>")
QV_BASE = ("<b>Réponse forcée</b> : après la fin de la phase du Méchant, si un joueur est sous forme d'alter ego, retournez Queen Veranke.")
QV_VAINCUE = f"<b>Une fois vaincue</b> : retirez tous les jetons de soupçon de {WDYT}."
QV_III = " Sinon, défaussez la première carte du deck Rencontre ; si c'est une traîtrise, retournez Queen Veranke."
for cid in ("sk189a", "sk190a", "sk191a"):
    FR[cid] = SW
for cid in ("sk189b", "sk190b"):
    FR[cid] = QV_BASE + "\\n" + QV_VAINCUE
FR["sk191b"] = QV_BASE + QV_III

FR["sk192a"] = ("<b>Contenu</b> : Spider-Woman (I) et Spider-Woman (II) <i>(Spider-Woman (II) et Spider-Woman (III) en mode expert)</i>. Les sets de "
                "rencontre Secret Invasion et Standard. Un set de rencontre modulaire <i>(Army of Skrulls)</i>.\\n<b>Mise en place</b> : créez le deck "
                f"[[IMPOSTOR]] et placez-le à côté du deck Rencontre <i>(voir l'encart)</i>. Mettez en jeu l'environnement {WDYT}.")
FR["sk192b"] = ("[star] Placez 1 menace supplémentaire ici pour chaque ennemi [[SKRULL]] en jeu et chaque allié [[IMPOSTOR]] en jeu.\\n"
                f"<b>Réponse forcée</b> : après la fin de votre tour, s'il y a moins de 2[per_hero] jetons de soupçon sur {WDYT}, mettez en jeu "
                "sous votre contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]].")
FR["sk193a"] = (f"<b>Une fois révélée</b> : si Mistrust and Paranoia est en jeu, retirez 2[per_hero] jetons de soupçon de {WDYT}. Sinon, cherchez "
                "Mistrust and Paranoia et révélez-le.")
FR["sk193b"] = ("X est égal à deux fois le nombre d'ennemis [[SKRULL]] en jeu.\\n"
                f"<b>Réponse forcée</b> : après la fin de votre tour, s'il y a moins de 2[per_hero] jetons de soupçon sur {WDYT}, mettez en jeu, "
                "engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].\\n"
                "<b>Si ce stade est achevé, les joueurs perdent la partie.</b>")
FR["sk194"] = ("<b>Interruption forcée</b> : quand n'importe quelle quantité de menaces est placée sur la manigance principale, retirez d'ici une "
               "quantité égale de jetons de soupçon.\\n<b>Interruption forcée</b> : quand n'importe quelle quantité de menaces est retirée de la "
               "manigance principale, placez ici une quantité égale de jetons de soupçon.")
FR["sk195"] = ("Considérez l'allié attaché comme un sbire [[SKRULL]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne "
               "subit pas de dégâts consécutifs.\\n<b>Une fois révélée</b> : attachez cette carte à l'allié non-[[SKRULL]] ayant le plus de points de "
               "vie restants qui n'a pas d'exemplaire d'Impostor attaché. L'allié attaché s'engage avec son contrôleur. Sinon, le méchant manigance.")
ENH_ATT = ("Attachez cette carte au sbire [[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'autre Super-Skrull Enhancement attaché. "
           "Si vous ne pouvez pas, choisissez un allié [[CAMOUFLAGED]], retournez-le et attachez-lui cette carte. Sinon, cette carte gagne Renfort.")
ENH_BOOST = "<hr />\\n[star] <b>Boost</b> : révélez cette carte, après la fin de cette activation."
FR["sk196"] = ENH_ATT + "\\nLe sbire attaché gagne 2 points de vie.\\n" + ENH_BOOST.replace("<hr />\\n", "<hr />\\n", 1)
FR["sk197"] = ENH_ATT + "\\n" + ENH_BOOST
FR["sk198"] = ENH_ATT + "\\nLe sbire attaché gagne Riposte 1.\\n" + ENH_BOOST
FR["sk199"] = ("Incitation 2.\\n<b>Une fois révélée</b> : placez ici X menaces supplémentaires, X étant égal à la MNG totale de tous les personnages "
               "[[IMPOSTOR]] en jeu.")
FR["sk200"] = "Entrave 1[per_hero].\\nChaque sbire [[SKRULL]] gagne Garde et Patrouille."
FR["sk201"] = ("Les joueurs ne peuvent pas attaquer les sbires engagés avec d'autres joueurs, ni défendre contre eux. Les joueurs ne peuvent pas payer "
               "en groupe les coûts d'une carte ou d'une capacité.\\n<b>Une fois révélée</b> : placez ici 1 menace supplémentaire pour chaque "
               "personnage allié en jeu.")
FR["sk202"] = ("<b>Une fois révélée</b> : chaque joueur met en jeu sous son contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck "
               "[[IMPOSTOR]].\\n<hr />\\n[star] <b>Boost</b> : mettez en jeu sous votre contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck "
               "[[IMPOSTOR]].")
FR["sk203"] = (f"<b>Une fois révélée</b> (Queen Veranke) : retournez Queen Veranke. Retirez 3 jetons de soupçon de {WDYT}.\\n"
               "<b>Une fois révélée</b> (Spider-Woman) : Spider-Woman manigance.\\n<hr />\\n[star] <b>Boost</b> : retournez Queen Veranke, après la fin "
               "de cette activation.")
FR["sk204"] = ("<b>Une fois révélée</b> : donnez une carte d'état Tenace au méchant et à chaque sbire [[SKRULL]] engagé avec vous. Si le méchant a "
               "déjà une carte d'état Tenace, cette carte gagne Renfort.\\n<hr />\\n[star] <b>Boost</b> : donnez une carte d'état Tenace au méchant.")
FR["sk205"] = ("<b>Une fois révélée</b> : mettez en jeu sous le contrôle de n'importe quel joueur un allié [[CAMOUFLAGED]] pris au hasard dans le "
               "deck [[IMPOSTOR]]. Si vous ne pouvez pas, cette carte gagne Renfort.\\n<hr />\\n[star] <b>Boost</b> : retirez 3 jetons de soupçon de "
               f"{WDYT}.")
FR["sk206"] = ("<b>Une fois révélée</b> : chaque joueur met en jeu, engagé avec lui, un sbire [[REVEALED]] pris au hasard dans le deck "
               "[[IMPOSTOR]].\\n<hr />\\n[star] <b>Boost</b> : mettez en jeu, engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck "
               "[[IMPOSTOR]].")
FR["sk207"] = ("<b>Une fois révélée</b> : retournez l'allié [[CAMOUFLAGED]] ayant le plus de points de vie restants. Si vous ne pouvez pas, mettez "
               "en jeu, engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].\\n<hr />\\n[star] <b>Boost</b> : retournez 1 "
               "allié [[CAMOUFLAGED]] que vous contrôlez, après la fin de cette activation.")

# ---------------------------------------------------------------------------------------------------------------------
# Paquet IMPOSTOR
# ---------------------------------------------------------------------------------------------------------------------
LUI = {"him": "le", "her": "la"}
PRON = {"him": "il", "her": "elle"}
for (n, num, nom, court, sbire, lui, pv, sch, atk, pastilles, desc_sbire, avant, apres, flavor) in IMP:
    a, b = f"sk{num}a", f"sk{num}b"
    FR[a] = f"<b>Interruption forcée</b> : quand {court} est censé{'e' if lui == 'her' else ''} quitter le jeu, retournez-{LUI[lui]} à la place."
    nom_rev = "Hagar" if num == 223 else sbire
    pre = {
        27: "Garde. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le méchant.)</i>\\n",
        30: "Ténacité. <i>(Ce personnage entre en jeu avec une carte d'état Tenace.)</i>\\n",
        31: "Tant que le joueur engagé est engagé avec un autre sbire [[SKRULL]], Trl'k ne peut pas subir de dégâts.\\n",
        33: "Diminuez de 1 la quantité de dégâts que Sn'Tlo subit à chaque attaque.\\n",
        34: "Patrouille. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas déjouer la manigance principale.)</i>\\n",
        35: "Riposte 1.\\n",
        36: "En tant que coût supplémentaire pour attaquer De'Lila, vous devez dépenser 1 ressource de n'importe quel type.\\n",
        38: "[star] Tant que le méchant a le trait [[REVEALED]], Ssrov gagne +1 MNG et +1 ATQ.\\n",
        40: "[star] Les attaques de H'kurrek gagnent Déferlement, Perçant et Distance.\\n",
        43: "[star] Les attaques de Hagar infligent des dégâts indirects.\\n",
        44: "Vilenie. <i>(Quand ce sbire s'active, donnez-lui une carte de boost.)</i>\\n",
        45: "Coup rapide.\\n",
        46: "Incitation 3. <i>(Quand cette carte est révélée, placez 3 menaces sur la manigance principale.)</i>\\n",
    }.get(n, "")
    revele = f"<b>Une fois révélé</b> : soignez tous les dégâts de {nom_rev} et mettez-{LUI[lui]} en jeu, engagé{'e' if lui == 'her' else ''} avec vous."
    post = {
        28: "\\n<b>Une fois vaincu</b> : retirez tous les jetons de soupçon de " + WDYT + ".",
        29: "\\n[star] <b>Interruption forcée</b> : quand M'lanz vous attaque, résolvez également son attaque contre chaque autre héros.",
        32: "\\n<b>Une fois vaincue</b> : donnez une carte Rencontre face cachée au joueur qui a vaincu Fry'lu.",
        37: "\\n<b>Une fois vaincu</b> : le méchant attaque le joueur qui a vaincu Grrix <i>(même si ce joueur est sous forme d'alter ego)</i>.",
        39: "\\n<b>Une fois vaincu</b> : le joueur qui a vaincu Hs'fld met en jeu sous son contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le "
            "deck [[IMPOSTOR]].",
        41: "\\n[star] <b>Réponse forcée</b> : après que Korya vous a attaqué, défaussez la première carte du deck de chaque joueur.",
        42: "\\n<b>Une fois vaincu</b> : retournez Queen Veranke.",
    }.get(n, "")
    FR[b] = pre + revele + post
    if n in (29, 41):   # « Une fois vaincue » / féminin : relu par la lettre
        pass

# ---------------------------------------------------------------------------------------------------------------------
sortie = []
for carte in CARDS:
    cid = carte["card_id"]
    sortie.append(f"  // skrull_menace — {carte['name'].lstrip('* ')} ({carte['type']}, {carte['set_name']})")
    sortie.append(f"  '{cid}': \"{FR[cid]}\",")
chemin = os.path.join(ICI, "secret_invasion_fr.txt")
with open(chemin, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(sortie) + "\n")
print(len(CARDS), "entrees ->", chemin)
