"""Textes FRANCAIS des 55 cartes d'Alien vs. Predator (RyCoRan) : ajoutes (idempotent : un bloc existant est REMPLACE) a la fin de
ui-app/src/board/textes-fr-fanmade.ts ET de Fusion/marvel-lcg-src/public/js/traduction/textes-fr-fanmade.js.
Vocabulaire officiel (textes-fr-complets.ts) : deck Rencontre, pile de défausse Rencontre, carte Rencontre face cachée, carte de boost face
cachée, jeton Actif, pion Accélération, Collaboration, Renfort, Garde, Incitation, Patrouille, Coup Rapide, Vilenie, Ténacité, Perçant,
Déferlement, Riposte, Entrave, Victoire. Noms propres et traits [[...]] laissés en anglais (GUIDE §11.1).
Usage : python3 .planning/alien-vs-predator/textes_fr.py"""
import os
import re

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TS = os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")
JS = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "js", "traduction", "textes-fr-fanmade.js")

T = {}

PLACE = "[star] Quand {nom} manigance, placez cette menace sur sa manigance annexe au lieu de la manigance principale, si possible."
REINE = (PLACE.format(nom="Alien Queen") + "\n[star] <b>Réponse forcée</b> : après qu'Alien Queen a attaqué et infligé des dégâts à un "
         "personnage que vous contrôlez, mélangez une carte Xenomorph dans votre deck.\n<b>Une fois vaincue</b> : retournez cette carte.")
WARLORD = (PLACE.format(nom="Predator Warlord") + "\n[star] <b>Interruption forcée</b> : quand Predator Warlord attaque, placez 2 menaces sur "
           "la manigance principale ou il gagne +1 ATQ pour cette attaque.\n<b>Une fois vaincu</b> : retournez cette carte.")


def defaite(n, autre, lui, stade):
    return (f"<b>Une fois révélée</b> : soignez {n}[per_hero] dégâts de {autre} et donnez-{lui} une carte d'état Tenace. Passez au stade "
            f"{stade}. Retirez de la partie chaque manigance annexe permanente et cette carte.")


for cid, mode in (("ap001", "A"), ("ap003", "B")):
    T[cid + "a"] = (f"Alien Queen ({mode})", "Villain", REINE)
    T[cid + "b"] = (f"Alien Queen « Defeated » ({mode})", "Villain", defaite(4 if mode == "A" else 6, "Predator Warlord", "lui", "3A"))
for cid, mode in (("ap002", "A"), ("ap004", "B")):
    T[cid + "a"] = (f"Predator Warlord ({mode})", "Villain", WARLORD)
    T[cid + "b"] = (f"Predator Warlord « Defeated » ({mode})", "Villain", defaite(4 if mode == "A" else 6, "Alien Queen", "lui", "4A"))

T["ap005a"] = ("The Ultimate Hunt (1A)", "MainScheme",
    "<b>Contenu</b> : Alien Queen et Predator Warlord, face A <i>(B en mode expert)</i>. Alien vs. Predator, deck Xenomorph, Apex Standard et "
    "un set modulaire <i>(Clan Yautja)</i>.\n"
    "<b>Mise en place</b> : mettez en jeu Skulls for the Taking et Expanding Hive. Placez le deck Xenomorph à côté d'Alien Queen et placez "
    "le jeton Actif sur elle.")
T["ap005b"] = ("The Ultimate Hunt (1B)", "MainScheme",
    "<i>Deux superprédateurs s'affrontent. Une chasse Predator. Une ruche Alien. La Terre devient leur champ de bataille.</i>\n"
    "[star] <b>Réponse forcée</b> : après la résolution de l'étape 1 de la phase du Méchant, s'il n'y a aucune menace sur la manigance annexe "
    "de chaque méchant, infligez 2 dégâts à chaque méchant.\n"
    "<b>Réponse forcée</b> : après qu'un méchant s'est activé, déplacez le jeton Actif vers le méchant suivant.")
T["ap006a"] = ("Battleground Earth (2A)", "MainScheme",
    "<i>Les tirs de plasma et les xénomorphes qui surgissent font des rues de la ville une zone de guerre. Les héros se démènent pour contenir "
    "les deux menaces avant que la destruction ne devienne incontrôlable.</i>\n"
    "<b>Une fois révélée</b> : chaque joueur cherche dans le deck Rencontre et la pile de défausse Rencontre un sbire [[YAUTJA]] et un sbire "
    "[[XENOMORPH]] et les met en jeu engagés avec lui. Mélangez le deck Rencontre.")
T["ap006b"] = ("Battleground Earth (2B)", "MainScheme",
    "<b>Réponse forcée</b> : après qu'un méchant a attaqué, donnez-lui une carte de boost face cachée, puis déplacez le jeton Actif vers le "
    "méchant suivant.\n"
    "<b>Réponse forcée</b> : après que de la menace a été placée ici, s'il y a au moins 4[per_hero] menaces ici, distribuez à chaque joueur "
    "une carte Rencontre face cachée. Puis retirez 2[per_hero] menaces de cette manigance.")
T["ap007a"] = ("Predator's Pursuit (3A)", "MainScheme",
    "<i>La menace Alien éliminée, le Predator tourne toute son attention vers de nouvelles proies. Pièges mortels et frappes camouflées "
    "marquent la dernière phase de la chasse, avec les héros pour trophées ultimes !</i>\n"
    "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un attachement [[WEAPON]] soit défaussé. "
    "Révélez cette carte.")
T["ap007b"] = ("Predator's Pursuit (3B)", "MainScheme",
    "Predator Warlord est le méchant actif.\n"
    "<b>Une fois révélée</b> : chaque joueur cherche dans le deck Rencontre et la pile de défausse Rencontre un sbire [[YAUTJA]] et le révèle.\n"
    "<b>Si ce stade est accompli, les joueurs perdent la partie.</b>")
T["ap008a"] = ("Queen's Dominion (4A)", "MainScheme",
    "<i>Le chasseur abattu, des créatures surgissent de l'ombre et infestent la ville en ruine. Les héros luttent désespérément pour contenir "
    "la ruche qui s'étend. Si la Reine n'est pas vite arrêtée, la Terre elle-même pourrait rejoindre sa couvée extraterrestre.</i>\n"
    "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un attachement [[XENOMORPH]] soit défaussé. "
    "Révélez cette carte.")
T["ap008b"] = ("Queen's Dominion (4B)", "MainScheme",
    "Alien Queen est le méchant actif.\n"
    "<b>Une fois révélée</b> : chaque joueur cherche dans le deck Rencontre et la pile de défausse Rencontre un sbire [[XENOMORPH]] et le "
    "révèle.\n"
    "<b>Si ce stade est accompli, les joueurs perdent la partie.</b>")
ICONE = "Tant qu'il n'y a aucune menace ici, cette manigance perd l'icône [acceleration]."
T["ap009"] = ("Expanding Hive", "SideScheme",
    f"<b>Manigance d'Alien Queen.</b>\nPermanent.\n{ICONE}\n"
    "<b>Interruption forcée</b> : quand un sbire ayant 3 points de vie imprimés ou plus est vaincu, donnez-le au méchant actif en tant que "
    "carte de boost face cachée.")
T["ap010"] = ("Skulls for the Taking", "SideScheme",
    f"<b>Manigance de Predator Warlord.</b>\nPermanent.\n{ICONE}\n"
    "<b>Réponse forcée</b> : après qu'un allié a été vaincu par une attaque ennemie, glissez-le sous cette carte.")
T["ap011"] = ("Plasmacaster", "Attachment",
    "Attachez à Predator Warlord. Sinon, cette carte gagne Renfort.\nUtilisations (3 compteurs plasma).\n"
    "[star] <b>Interruption forcée</b> : quand Predator Warlord vous attaque, retirez 1 compteur plasma d'ici et défaussez la carte du dessus "
    "de votre deck → subissez des dégâts indirects égaux au coût imprimé de cette carte.")
ARME = "Attachez à Predator Warlord. Si vous ne pouvez pas, attachez à un sbire [[YAUTJA]]. Sinon, cette carte gagne Renfort."
T["ap012"] = ("Yautja Wrist Blades", "Attachment",
    f"{ARME}\n[star] Les attaques de l'ennemi attaché gagnent Perçant.\n"
    "<b>Action de héros</b> : dépensez des ressources [energy][physical] → défaussez cette carte.")
FIN_DE_TOUR = ("<b>Réponse forcée</b> : après la fin de votre tour, subissez 2 dégâts et placez 2 menaces sur la manigance principale.")
T["ap013"] = ("Thermal Target", "Attachment",
    f"Attachez à votre identité.\n{FIN_DE_TOUR}\n"
    "<b>Action d'alter ego</b> : trouvez un sbire [[YAUTJA]] et révélez-le → défaussez cette carte.\n"
    "[star] <b>Boost</b> : révélez cette carte.")
T["ap015"] = ("Piercing Pharynx", "Attachment",
    "Attachez à Alien Queen et donnez-lui une carte d'état Tenace. Sinon, cette carte gagne Renfort.\nAlien Queen gagne Riposte 1.\n"
    "<b>Action de héros</b> : si Predator Warlord est en jeu, dépensez des ressources [energy][mental] → défaussez cette carte.\n"
    "[star] <b>Boost</b> : révélez cette carte.")
T["ap016"] = ("Facehugger", "Attachment",
    f"Attachez à votre identité.\n{FIN_DE_TOUR}\n"
    "<b>Action d'alter ego</b> : cherchez dans le deck Rencontre et la pile de défausse Rencontre un sbire [[XENOMORPH]] et révélez-le → "
    "défaussez cette carte.")
T["ap018"] = ("Xenomorph Drone", "Minion",
    "Garde. Incitation 2 (3 à la place si Alien Queen est le méchant actif).\n"
    "<b>Une fois vaincu</b> : retirez 2 menaces d'Expanding Hive. Si vous ne pouvez pas, mélangez Xenomorph Drone dans le deck Rencontre.")
T["ap020"] = ("Xenomorph Warrior", "Minion",
    "Coup Rapide.\n"
    "<b>Une fois vaincu</b> : défaussez la carte du dessus du deck Rencontre et infligez des dégâts à un ennemi [[YAUTJA]] pour chaque icône "
    "<i>([star] et [boost])</i> de la zone de boost de la carte défaussée.")
T["ap021"] = ("Alien Praetorian", "Minion",
    "Vilenie.\n<b>Réponse forcée</b> : après le début de la phase du Méchant, Alien Praetorian s'engage avec le premier joueur.")
T["ap022"] = ("Chestburster", "Attachment",
    "Attachez à un sbire [[XENOMORPH]]. Sinon, attachez au méchant actif.\n"
    "[star] <b>Interruption forcée</b> : quand l'ennemi attaché attaque, cette attaque gagne Perçant. À la fin de cette attaque, sonnez "
    "votre identité et défaussez cette carte.")
T["ap023"] = ("Hive Incursion", "Treachery",
    "<b>Une fois révélée</b> : défaussez votre main. Piochez jusqu'à atteindre votre taille de main.\n"
    "[star] <b>Boost</b> : résolvez la capacité « <b>Une fois révélée</b> » de cette carte.")
T["ap024"] = ("Predator's Prize", "Treachery",
    "<b>Une fois révélée</b> : choisissez : donnez cette carte au méchant actif en tant que carte de boost face cachée, ou trouvez votre "
    "allié spécifique à l'identité et retirez-le de la partie.")
T["ap025"] = ("Brood Breakout", "SideScheme",
    "<b>Réponse forcée</b> : après qu'un sbire [[XENOMORPH]] est entré en jeu, donnez-lui une carte d'état Tenace.\n"
    "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un sbire [[XENOMORPH]] soit défaussé. "
    "Révélez ce sbire.")
T["ap026"] = ("Alien Assault", "Treachery",
    "<b>Une fois révélée</b> : si Predator Warlord est le méchant actif, sonnez votre identité. Si Alien Queen est le méchant actif, "
    "désorientez votre identité.\n"
    "[star] <b>Boost</b> : après la fin de cette activation, ne déplacez pas le jeton Actif vers le méchant suivant.")
T["ap027"] = ("Killing Ground", "Treachery",
    "<b>Une fois révélée</b> : déplacez toute la menace de la manigance annexe de méchant qui a le plus de menace vers la manigance "
    "principale. Si aucune menace n'a été déplacée ainsi, inclinez votre identité. Si vous ne pouvez pas, sonnez ou désorientez votre "
    "identité.")
T["ap028"] = ("Predator's Prey", "Treachery",
    "<b>Une fois révélée</b> : défaussez des cartes du dessus de votre deck jusqu'à ce que vous défaussiez un allié, puis mettez cet allié en "
    "jeu sous votre contrôle. Le méchant actif attaque cet allié. Cette attaque gagne Déferlement.")
T["ap029"] = ("Predation", "Treachery",
    "<b>Une fois révélée</b> : soignez 3 dégâts du méchant actif et donnez-lui une carte d'état Tenace. Infligez 3 dégâts à un ennemi dont "
    "le trait ne correspond pas à celui du méchant actif.\n"
    "[star] <b>Boost</b> : placez 2 menaces sur chaque manigance.")
T["ap030"] = ("Trophy Taken", "Treachery",
    "<b>Une fois révélée</b> : le méchant actif attaque le personnage ami qui a le moins de points de vie restants. Si cette attaque vainc "
    "un allié, retirez cet allié de la partie.")
T["ap031"] = ("Lethal Ambush", "Treachery",
    "<b>Une fois révélée</b> : défaussez les 7 cartes du dessus du deck Rencontre. Mettez en jeu, engagé avec vous, le premier sbire défaussé "
    "ainsi. Puis le méchant et chaque sbire engagé avec vous vous attaquent.")
T["ap032"] = ("Swarm Breaker", "SideScheme",
    "<i>Des silhouettes sombres déferlent sur le champ de bataille, implacables et innombrables. Un tourbillon de tonnerre et d'acier fend "
    "le ciel. Leur assaut vacille, ne serait-ce qu'un instant...</i>\n"
    "Entrave 1[per_hero]. Victoire 0.\n<b>Une fois déjouée</b> : infligez 2[per_hero] dégâts à chaque ennemi.")
T["ap033"] = ("Alien Onslaught", "SideScheme",
    "Entrave 2[per_hero].\n"
    "<b>Une fois révélée</b> : chaque joueur défausse les 2[per_hero] cartes du dessus de son deck. Placez ici 1 pion Accélération pour chaque "
    "sbire [[XENOMORPH]] défaussé ainsi.\n"
    "<b>Réponse forcée</b> : après que vous avez contré cette manigance, défaussez les 2[per_hero] cartes du dessus de votre deck.")

PIOCHE = ("<b>Interruption forcée</b> : quand vous piocheriez ou défausseriez cette carte de votre deck, piochez 1 carte. "
          "Distribuez-vous cette carte en tant que carte Rencontre face cachée.")
SANS_PIOCHE = ("<b>Interruption forcée</b> : quand vous piocheriez ou défausseriez cette carte de votre deck, distribuez-vous cette carte en "
               "tant que carte Rencontre face cachée.")
VAINCU_SCOUT = "<b>Une fois vaincu</b> : placez Alien Scout dans votre pile de défausse."
T["ap101"] = ("Alien Scout (01-04)", "Minion", f"Renfort.\n{PIOCHE}\n{VAINCU_SCOUT}")
T["ap102"] = ("Alien Scout (05-08)", "Minion", f"Garde.\n{SANS_PIOCHE}\n{VAINCU_SCOUT}")
T["ap103"] = ("Alien Scout (09-12)", "Minion", f"Incitation 1. Renfort.\n{PIOCHE}\n{VAINCU_SCOUT}")
T["ap104"] = ("Alien Scout (13-16)", "Minion", f"Collaboration ([[XENOMORPH]]).\n{PIOCHE}\n{VAINCU_SCOUT}")

T["ap201"] = ("Advance", "Treachery",
    "<b>Une fois révélée</b> : le méchant manigance. Placez cette menace sur la manigance principale.")
T["ap202"] = ("Advance Again", "Treachery",
    "<b>Une fois révélée</b> : le méchant manigance. Ne déplacez pas le jeton Actif.")
T["ap203"] = ("Assault", "Treachery",
    "<b>Une fois révélée (alter ego)</b> : cette carte gagne Renfort.\n"
    "<b>Une fois révélée (héros)</b> : le méchant vous attaque. Ne déplacez pas le jeton Actif.")
T["ap204"] = ("Cruel Intentions", "Treachery",
    "Incitation 1.\n<b>Une fois révélée</b> : distribuez à chaque joueur 1 carte Rencontre face cachée. Donnez au méchant 1 carte de boost "
    "face cachée.\n[star] <b>Boost</b> : distribuez-vous 1 carte Rencontre face cachée.")
T["ap205"] = ("Overwhelming Force", "Treachery",
    "<b>Une fois révélée</b> : défaussez l'amélioration ou le soutien au coût le plus élevé que vous contrôlez. Si aucune carte n'a été "
    "défaussée ainsi, cette carte gagne Renfort.\n"
    "[star] <b>Boost</b> : donnez au méchant 1 carte de boost supplémentaire pour cette activation.")
# Reskins mot pour mot du core : texte officiel de 01192 / 01190 (textes-fr-complets.ts).
T["ap206"] = ("Masterplan", "Treachery",
    "<b>Une fois révélée</b> : placez 4 menaces sur chaque manigance annexe. S'il n'y a pas de manigance annexe en jeu, défaussez des cartes "
    "du dessus du deck Rencontre jusqu'à ce qu'une manigance annexe soit défaussée. Révélez cette manigance annexe.")
T["ap207"] = ("Shadow of the Past", "Treachery",
    "<b>Une fois révélée</b> : révélez votre sbire Némésis mis de côté et mettez-le en jeu engagé avec vous. Révélez votre manigance annexe "
    "Némésis mise de côté et mettez-la en jeu. Mélangez dans le deck Rencontre les cartes restantes de votre set de rencontre Némésis mis de "
    "côté. Si votre sbire Némésis n'entre pas en jeu à cause de cet effet, cette carte gagne Renfort.")

T["ap301"] = ("Yautja Young Blood", "Minion",
    "Patrouille. Incitation 2 (3 à la place si Predator Warlord est le méchant actif).\n"
    "<b>Une fois vaincu</b> : placez 2 menaces sur The Ultimate Hunt ; si vous ne pouvez pas, mélangez Yautja Young Blood dans le deck "
    "Rencontre.")
T["ap302"] = ("Blooded Predator", "Minion",
    "<b>Une fois révélée</b> : sonnez votre identité. Si vous êtes déjà sonné, subissez 3 dégâts.\n"
    "<b>Une fois vaincu</b> : donnez une carte d'état Tenace à Predator Warlord. Si vous ne pouvez pas, donnez cette carte au méchant actif "
    "en tant que carte de boost face cachée.")
T["ap303"] = ("Predator Elite", "Minion",
    "<b>Une fois révélée</b> : défaussez une amélioration ou un soutien que vous contrôlez.\n"
    "<b>Une fois vaincu</b> : défaussez la carte du dessus de votre deck et infligez à un ennemi [[XENOMORPH]] des dégâts égaux au coût "
    "imprimé de cette carte.")
T["ap304"] = ("Apex Predator", "Minion",
    "Ténacité.\n[star] Les attaques d'Apex Predator gagnent Perçant.\n"
    "<b>Réponse forcée</b> : après qu'un personnage a attaqué Apex Predator, défaussez la carte du dessus du deck Rencontre. Si c'est une "
    "traîtrise, sonnez l'attaquant.")
T["ap305"] = ("The Hunt Begins", "SideScheme",
    "Les alliés ne peuvent pas défendre contre les attaques ennemies.\n"
    "<b>Réponse forcée</b> : après qu'un ennemi [[YAUTJA]] a attaqué, donnez-lui une carte d'état Tenace.\n"
    "<b>Une fois déjouée</b> : sonnez ou désorientez un ennemi.")
T["ap306"] = ("Cloaking Device", "Attachment",
    f"{ARME}\nRéduisez de 2 les dégâts que l'ennemi attaché subit de chaque attaque.\n"
    "<b>Action de héros</b> : après qu'un héros a fait une attaque de base contre cet ennemi, dépensez des ressources [energy][physical] → "
    "défaussez cette carte.")


def echapper(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


DEBUT = "// alien vs. predator — debut du bloc (genere par .planning/alien-vs-predator/textes_fr.py)\n"
FIN = "// alien vs. predator — fin du bloc\n"


def ajouter(chemin, indent, fin):
    contenu = open(chemin, encoding="utf-8").read()
    motif = re.compile(re.escape(indent + DEBUT) + ".*?" + re.escape(indent + FIN), re.S)
    contenu = motif.sub("", contenu)
    bloc = indent + DEBUT + "".join(
        f"{indent}// alien vs. predator — {nom} ({typ})\n{indent}'{cid}': \"{echapper(txt)}\",\n" for cid, (nom, typ, txt) in sorted(T.items())
    ) + indent + FIN
    i = contenu.rindex(fin)
    open(chemin, "w", encoding="utf-8").write(contenu[:i] + "\n" + bloc.rstrip("\n") + contenu[i:])
    print(chemin, ":", len(T), "textes")


if __name__ == "__main__":
    ajouter(TS, "  ", "\n}")
    ajouter(JS, "    ", "\n};")
