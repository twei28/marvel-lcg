#!/usr/bin/env python3
"""Ecrit (idempotent) les textes FRANCAIS du scenario 5 « Cassandra Nova » et de ses modules Mind Control / Mutant Extinction Agenda dans
`ui-app/src/board/textes-fr-fanmade.ts`, entre les marqueurs `// DEBUT hellfire_hunt_cassandra_nova` / `// FIN hellfire_hunt_cassandra_nova`.
Lecture-modification-ecriture sous flock (`/tmp/cards_json.lock`) : d'autres agents ecrivent le meme fichier.
Usage : python3 textes_fr.py <racine_du_depot>      puis : cd ui-app && node outils/generer-traduction-public.mjs
Vocabulaire : traits-fr.ts / mots-cles.ts (Solide = Steady, Robuste = Stalwart, Péril, Renfort, Déferlement = Overkill, Perçant, Mise en place...)."""
import fcntl
import json
import os
import sys

RACINE = sys.argv[1]
CHEMIN = os.path.join(RACINE, "ui-app", "src", "board", "textes-fr-fanmade.ts")
DEBUT = "  // DEBUT hellfire_hunt_cassandra_nova"
FIN = "  // FIN hellfire_hunt_cassandra_nova"

CTR = "compteur de Contrôle de Cassandra"
CTRS = "compteurs de Contrôle de Cassandra"
REP_NOVA = ("[star] <b>Réponse forcée</b> : après que Cassandra Nova s'active contre vous, placez 1 " + CTR + " sur votre carte d'identité.")
T = {}

T["hf601"] = REP_NOVA + "\n<i>« Les gens doivent apprendre à haïr. Je vais être leur professeur. »</i>"
T["hf602"] = ("Solide.\n<b>Une fois révélée</b> : placez 1 " + CTR + " sur chaque identité.\n" + REP_NOVA +
              "\n<i>« Peut-on parler de meurtre quand il s'agit de microbes ou de vermine ? »</i>")
T["hf603"] = ("Robuste.\n<b>Une fois révélée</b> : placez 1 " + CTR + " sur chaque identité et placez 1[per_hero] jeton(s) d'accélération sur la manigance principale.\n"
              + REP_NOVA + "\n<i>« D'ici, je peux tendre la main, saisir chaque esprit mutant restant sur Terre et l'éteindre. Mais il ne m'en faut qu'un. »</i>")
T["hf604a"] = ("<b>Contenu</b> : Cassandra Nova (I) et Cassandra Nova (II). <i>(Cassandra Nova (II) et Cassandra Nova (III) à la place en mode expert.)</i> "
               "Ensembles de rencontre Cassandra Nova, Immensity et Standard. Deux ensembles de rencontre modulaires <i>(Mind Control et Mutant Extinction Agenda)</i>.\n"
               "<b>Mise en place</b> : retirez du jeu le sbire Cassandra Nova. Mettez en jeu l'environnement Cassandra Domination. En mode expert, avancez au stade 2A.")


def fin_de_tour(menace, autre, cartes):
    return ("<b>Réponse forcée</b> : après la fin de votre tour, s'il y a un " + CTR + " sur votre identité, vous devez choisir : placer %s ici ou %s.\n"
            "<b>Action de héros</b> : défaussez %d cartes du dessus du deck rencontre → retirez un " + CTR + " de votre identité. "
            "<i>(Limite d'une fois par round et par joueur.)</i>") % (menace, autre, cartes)


T["hf604b"] = fin_de_tour("1 menace", "subir 2 dégâts", 5)
T["hf605a"] = ("<i>Cassandra se prépare à faire la guerre aux mutants et à transformer les ennemis des héros en armée personnelle.</i>\n"
               "<b>Une fois révélée</b> : chaque joueur trouve son propre sbire némésis et le met en jeu engagé avec lui-même.")
T["hf605b"] = fin_de_tour("2 menaces", "vous distribuer 1 carte rencontre face cachée", 6)
T["hf606a"] = ("<i>Nova a poursuivi son but en créant des Sentinelles, leur a permis de détecter les mutants à proximité et les a lancées dans une rage meurtrière.</i>\n"
               "<b>Une fois révélée</b> : distribuez à chaque joueur 1 carte rencontre face cachée pour chaque personnage qu'il contrôle.")
T["hf606b"] = fin_de_tour("3 menaces", "défausser 1 carte de votre main", 7) + "\n<b>Quand cette manigance est complétée, les joueurs perdent la partie.</b>"
T["hf607"] = ("<b>Réponse forcée</b> : après qu'un " + CTR + " est placé sur votre carte d'identité, s'il y a au moins 3 " + CTRS + ", retirez-en 3 de cette carte → "
              "vous choisissez : placez 2 menaces sur chaque manigance, sonnez et désorientez votre identité, ou infligez 3 dégâts indirects à un autre personnage ami.")
T["hf608"] = ("Chaque carte rencontre que vous avez révélée gagne Péril.\n<b>Réponse forcée</b> : après la fin de votre tour, défaussez des cartes que vous contrôlez "
              "dont le coût en ressources total est d'au moins 2. Subissez 1 dégât pour chaque carte défaussée. Ensuite, défaussez cette carte. "
              "Sinon, distribuez-vous 1 carte rencontre face cachée.")
T["hf609"] = T["hf608"]
T["hf610"] = ("<b>Réponse forcée</b> : après la fin de votre tour, Cassandra Nova manigance. Désorientez votre identité, puis défaussez cette carte.\n"
              "<b>Action d'alter ego</b> : inclinez votre identité → défaussez cette carte.")
T["hf611"] = T["hf612"] = T["hf610"]
T["hf613"] = ("<b>Une fois révélée</b> : défaussez X cartes du deck rencontre, où X est égal au double du numéro de stade du méchant. Chaque fois qu'une carte "
              "Cassandra Nova est défaussée ainsi, placez 1 " + CTR + " sur votre identité.")
T["hf614"] = T["hf615"] = T["hf613"]
T["hf616"] = ("<b>Une fois révélée</b> : Cassandra Nova s'active contre vous. Vous êtes sonné.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, "
              "cette attaque gagne Déferlement et Perçant. Sinon, placez sur la manigance principale un nombre de menaces égal au nombre de " + CTRS +
              " sur votre identité.")
T["hf617"] = T["hf616"]
T["hf618"] = ("<b>Une fois révélée</b> : défaussez votre main. Piochez jusqu'à votre taille de main. Pour chaque carte défaussée ainsi, soignez 1 dégât de "
              "Cassandra Nova ; si vous ne pouvez pas, placez un " + CTR + " sur votre identité.")
T["hf619"] = T["hf618"]
T["hf620"] = ("Le texte de chaque soutien est considéré comme vide.\n<b>Une fois révélée</b> : pour chaque " + CTR + " en jeu, placez 1 menace ici.\n<hr />\n"
              "[star] <b>Boost</b> : placez 2 " + CTRS + " sur votre carte d'identité.")
T["hf621"] = ("Tant qu'il y a au moins 1 " + CTR + " sur votre identité, vous ne pouvez pas attaquer Cassandra Nova ni contrer la manigance principale.\n"
              "<b>Une fois révélée</b> : pour chaque " + CTR + " en jeu, placez 1 menace ici.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.")

# --- module Mind Control
USE = "dépensez des ressources [mental][mental] → défaussez cette carte"
T["hf371"] = ("Mise en place. Attachez-la au méchant.\nLe personnage attaché ne peut pas être désorienté.\nLe personnage attaché ne peut pas subir de dégâts d'un joueur "
              "tant que ce joueur est désorienté.\n<b>Action</b> : " + USE + ".\n<hr />\n[star] <b>Boost</b> : révélez cette carte.")
T["hf372"] = ("Attachez-la à la manigance principale.\n<b>Interruption forcée</b> : quand un joueur devrait retirer de la menace de la manigance principale, empêchez 2 de ces "
              "menaces d'être retirées. Ensuite, désorientez ce joueur. <i>(Limite d'une fois par phase.)</i>\n<b>Action de héros</b> : " + USE + ".")
T["hf373"] = ("Attachez-la à votre identité.\n<b>Interruption forcée</b> : quand vous devriez contrer, défaussez plutôt cette carte. Ensuite, vous êtes désorienté.\n"
              "<b>Action</b> : " + USE + ".")
T["hf374"] = ("<b>Une fois révélée</b> : vous êtes désorienté. Infligez 1 dégât à chaque personnage désorienté en jeu.\n<hr />\n[star] <b>Boost</b> : vous êtes désorienté.")
T["hf375"] = T["hf374"]
T["hf376"] = ("Péril.\n<b>Une fois révélée</b> : vous êtes désorienté. Vous pouvez défausser autant de cartes que vous voulez de votre main. Ensuite, infligez X dégâts à "
              "chaque identité en jeu, où X est égal à la moitié du nombre de cartes de votre main.")

# --- module Mutant Extinction Agenda
CHERCHE = "cherche un sbire [[Sentinel]] dans le deck et la défausse rencontre. Mettez-le en jeu engagé avec vous."
T["hf381"] = ("Victoire 1.\nChaque sbire [[Sentinel]] gagne +1 ATQ et +1 MNG. Cette carte ne peut pas être vaincue tant qu'un sbire [[Sentinel]] est en jeu.\n"
              "<b>Une fois révélée</b> : chaque joueur, dans l'ordre des joueurs, " + CHERCHE + "\n<hr />\n[star] <b>Boost</b> : mettez cette carte en jeu.")
T["hf382"] = ("<b>Une fois vaincu</b> : le joueur qui l'a vaincu choisit : subir 2 dégâts, ou placer cette carte sous le deck rencontre au lieu de la défausse.")
T["hf383"] = T["hf384"] = T["hf385"] = T["hf382"]
T["hf386"] = ("<b>Une fois révélée</b> : pour chaque sbire [[Sentinel]] en jeu, infligez 1 dégât indirect à chaque joueur. S'il n'y a aucun sbire [[Sentinel]] en jeu, "
              "cherchez un sbire [[Sentinel]] dans le deck et la défausse rencontre et mettez-le en jeu engagé avec vous.")
T["hf387"] = T["hf386"]
T["hf388"] = "Victoire 1.\n<b>Une fois révélée</b> : chaque joueur, dans l'ordre des joueurs, " + CHERCHE


def main() -> None:
    bloc = [DEBUT] + ["  %s: %s," % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in sorted(T.items())] + [FIN]
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        with open(CHEMIN, encoding="utf-8") as f:
            s = f.read()
        if DEBUT in s:
            a = s.index(DEBUT)
            b = s.index(FIN) + len(FIN)
            s = s[:a] + "\n".join(bloc) + s[b:]
        else:
            i = s.rindex("\n}")
            s = s[:i] + "\n" + "\n".join(bloc) + s[i:]
        with open(CHEMIN, "w", encoding="utf-8") as f:
            f.write(s)
    print(len(T), "textes")


main()
