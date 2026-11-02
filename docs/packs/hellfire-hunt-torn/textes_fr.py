#!/usr/bin/env python3
"""Textes francais des cartes du pack hellfire_hunt_torn (Torn hf501-hf510, Negasonic hf341-hf348, Immensity hf351-hf358).

Ecrit dans `ui-app/src/board/textes-fr-fanmade.ts` (bloc `// DEBUT hellfire_hunt_torn` ... `// FIN hellfire_hunt_torn`, idempotent, lecture-modification-ecriture
sous flock /tmp/cards_json.lock : seul NOTRE bloc est touche), puis `node ui-app/outils/generer-traduction-public.mjs` regenere la copie publique.
Usage : python3 textes_fr.py <racine du depot Marvel-LCG-campagnes>
Vocabulaire officiel FR (mots-cles.ts / textes-fr-fanmade.ts) : Réponse forcée, Interruption forcée, Une fois révélée, Une fois déjouée, Action d'alter ego,
Garde, Patrouille, Incitation, Renfort, Ténacité, Solide, Entrave, Permanent, Victoire ; traits [[EN ANGLAIS MAJUSCULES]], jetons [star] [mental] [per_hero] tels quels.
"""
import fcntl
import json
import os
import sys

PERSO = "Les joueurs"
T = {}

# ----- Emma Frost
INT_VAINCUE = "<b>Interruption forcée</b> : quand Emma Frost serait vaincue, retirez 5 menaces de chaque manigance en jeu, puis retournez cette carte à la place."
FLIP = "<b>Réponse forcée</b> : après la fin de la phase du méchant, retournez cette carte, puis remettez les points de vie d'Emma Frost à ses points de vie imprimés."
T["hf501a"] = ("[star] <b>Réponse forcée</b> : après qu'Emma Frost s'est activée, défaussez la carte du dessus du deck Rencontre ; si elle a le trait [[PSIONIC]], "
               "placez 1 menace sur chaque manigance.\n" + INT_VAINCUE)
T["hf501b"] = "[star] <b>Interruption forcée</b> : quand Emma Frost voudrait s'activer, défaussez à la place les 2 cartes du dessus du deck Rencontre.\n" + FLIP
T["hf502a"] = ("[star] <b>Réponse forcée</b> : après qu'Emma Frost s'est activée, défaussez les 2 cartes du dessus du deck Rencontre ; pour chaque carte [[PSIONIC]] "
               "défaussée ainsi, placez 1 menace sur chaque manigance.\n" + INT_VAINCUE)
T["hf502b"] = ("[star] <b>Interruption forcée</b> : quand Emma Frost s'active contre un joueur, donnez à la place une carte Rencontre face cachée à ce joueur.\n" + FLIP)
T["hf503a"] = ("<b>Contenu</b> : Emma Frost (A1) <i>(Emma Frost (B1) en mode expert)</i>. Ensembles Rencontre Torn, Perfection et Standard.\n"
               "<b>Mise en place</b> : choisissez 3 ensembles modulaires, chacun contenant un sbire [[ELITE]], [[HELLFIRE]] <i>(recommandés : Immensity, Sebastian Shaw, "
               "Negasonic Teenage Warhead)</i>, et mélangez-les dans le deck Rencontre. Mélangez chaque sbire [[ELITE]], [[HELLFIRE]] pour former le deck Hellfire et posez-le "
               "à côté du deck Rencontre <i>(voir l'encart)</i>. Mettez en jeu la manigance annexe Nova's Psychic Puppetry, face [[CONTROLLED]] visible.")
T["hf503b"] = ("Les joueurs ne peuvent pas gagner à moins d'aider Emma Frost à échapper au contrôle de Cassandra.\n"
               "<b>Interruption forcée</b> : au début de la phase des joueurs, dans l'ordre des joueurs, chaque joueur non engagé avec un sbire [[ELITE]], [[HELLFIRE]] "
               "révèle la carte du dessus du deck Hellfire.\n<b>Si cette manigance est complétée, les joueurs perdent la partie.</b>")
REP = ("<b>Réponse forcée</b> : après qu'un sbire [[ELITE]], [[HELLFIRE]] est vaincu, retirez 5 menaces d'une autre manigance annexe. Sinon, retirez 5 menaces d'ici.")
T["hf504a"] = ("Permanent. Entrave 5[per_hero].\n<b>Interruption forcée</b> : quand la dernière menace est retirée de cette manigance, défaussez chaque sbire [[HELLFIRE]] en jeu "
               "et donnez une carte Rencontre face cachée à chaque joueur. Ensuite, retournez cette carte. <i>(Les joueurs peuvent aider Emma Frost à s'échapper de ce côté.)</i>\n" + REP)
T["hf504b"] = ("Permanent. Entrave 12[per_hero].\nChaque sbire [[HELLFIRE]] gagne le trait [[ILLUSION]].\n<b>Interruption forcée</b> : quand la dernière menace est retirée de cette "
               "manigance, Emma Frost échappe au contrôle de Cassandra Nova : les joueurs gagnent la partie.\n" + REP)
T["hf505"] = ("Votre héros a −1 ATQ et −1 DEF.\n<b>Action d'alter ego</b> : inclinez votre identité et révélez 1 carte du deck Hellfire → soignez 1 dégât de chaque personnage allié "
              "en jeu. Défaussez cette carte.")
T["hf506"] = ("<b>Action d'alter ego</b> : inclinez votre identité → soignez 5 dégâts du méchant et retirez 5 menaces d'une manigance annexe. Défaussez cette obligation.")
T["hf507"] = ("<i>L'influence psychique de Nova enveloppe ses marionnettes, les protégeant des coups tandis qu'elle tisse sa toile tordue.</i>\nVictoire 1.\n"
              "Chaque sbire gagne Garde et Patrouille.\n<hr />\n[star] <b>Boost</b> : donnez une carte d'état Tenace à chaque sbire.")
T["hf508"] = ("<i>La toile de tromperie et d'illusion de Frost piège les héros dans un labyrinthe de sa propre conception.</i>\nVictoire 1.\n"
              "On ne peut pas retirer de menace des autres manigances annexes.\n<b>Une fois déjouée</b> : donnez une carte Rencontre face cachée à chaque joueur.")
T["hf509"] = ("Emma Frost a +10 points de vie.\nChaque carte [[ILLUSION]] gagne Incitation 1.\n<b>Une fois révélée</b> : donnez 1 carte Rencontre face cachée à chaque joueur "
              "sans sbire engagé.")
T["hf510"] = ("On ne peut retirer de menace d'ici qu'en contrant.\n<b>Réponse forcée</b> : après qu'un sbire [[HELLFIRE]] a été vaincu par un joueur, s'il s'agit de White Queen, "
              "Emma Frost attaque ce joueur. Sinon, Emma Frost complote.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.")
# ----- Negasonic Teenage Warhead
T["hf341"] = ("Solide. Ténacité.\n[star] Quand Negasonic Teenage Warhead vous attaque, vous devez incliner un soutien ou une amélioration que vous contrôlez, si possible.\n"
              "<hr />\n[star] <b>Boost</b> : inclinez un soutien ou une amélioration que vous contrôlez.")
for i in ("hf342", "hf343"):
    T[i] = ("Attachez-la à votre identité.\nLe personnage attaché ne peut pas être redressé.\n<b>Action d'alter ego</b> : dépensez [mental][mental] → défaussez cette carte.\n"
            "<hr />\n[star] <b>Boost</b> : changez de forme <i>(retournez votre carte d'identité)</i>.")
for i in ("hf344", "hf345"):
    T[i] = ("<b>Une fois révélée</b> : révélez la carte Attachement du dessus de la défausse Rencontre. Sinon, cette carte gagne Renfort.\n<hr />\n"
            "[star] <b>Boost</b> : inclinez votre héros.")
for i in ("hf346", "hf347", "hf348"):
    T[i] = ("<b>Une fois révélée</b> : défaussez une carte que vous contrôlez, puis cherchez dans votre deck et votre défausse une carte du même type dont le coût en ressources "
            "est inférieur à celui de la carte défaussée, et mettez-la en jeu. Sinon, cette carte gagne Renfort.")
# ----- Immensity
T["hf351"] = ("Solide.\n<b>Une fois révélée</b> : trouvez l'attachement Cassandra's Telepathic Cloak et mettez-le en jeu.\n<hr />\n"
              "[star] <b>Boost</b> : mettez Cassandra Nova en jeu, engagée avec vous.")
T["hf352"] = ("<b>Une fois révélée</b> : défaussez les 3 cartes du dessus du deck Rencontre. Révélez chaque obligation défaussée ainsi. Si aucune obligation n'a été révélée ainsi, "
              "cherchez dans le deck Rencontre, la défausse, la zone mise de côté et la zone des cartes retirées du jeu un exemplaire de votre obligation, puis révélez-le et "
              "retirez cette carte de la partie.")
T["hf353"] = "Renfort.\n<b>Une fois révélée</b> : vous êtes sonné et désorienté.\n<hr />\n[star] <b>Boost</b> : vous êtes sonné et désorienté."
T["hf354"] = ("Attachez-la à Cassandra Nova. Si elle n'est pas en jeu, trouvez Cassandra Nova, révélez-la, puis attachez cette carte à elle.\n"
              "Cassandra Nova ne peut subir aucun dégât.\n<b>Réponse forcée</b> : après que Cassandra Nova vous a attaqué, défaussez cette carte.")
for i in ("hf355", "hf356"):
    T[i] = ("Attachez-la au sbire qui a le plus de points de vie. Sinon, cette carte gagne Renfort.\n[star] <b>Interruption forcée</b> : quand le personnage attaché vous attaque, "
            "donnez-lui 1 carte de boost supplémentaire pour cette activation.\n<hr />\n[star] <b>Boost</b> : donnez-vous 1 carte Rencontre face cachée.")
for i in ("hf357", "hf358"):
    T[i] = "<b>Action d'alter ego</b> : inclinez votre identité → défaussez cette carte."

DEBUT, FIN = "  // DEBUT hellfire_hunt_torn\n", "  // FIN hellfire_hunt_torn\n"


def main():
    racine = sys.argv[1]
    chemin = os.path.join(racine, "ui-app", "src", "board", "textes-fr-fanmade.ts")
    bloc = DEBUT + "".join("  %s: %s,\n" % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in sorted(T.items())) + FIN
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        s = open(chemin, encoding="utf-8").read()
        if DEBUT in s:
            i, j = s.index(DEBUT), s.index(FIN) + len(FIN)
            s = s[:i] + s[j:]
        fin = s.rstrip().rfind("\n}")
        assert fin > 0, "fin de l'objet introuvable"
        s = s[:fin + 1] + bloc + s[fin + 1:]
        open(chemin, "w", encoding="utf-8").write(s)
    print(len(T), "textes ecrits")


main()
