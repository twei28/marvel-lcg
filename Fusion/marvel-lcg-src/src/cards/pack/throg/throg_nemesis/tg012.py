from . import *

# Adorable Distraction — COMPLOT ANNEXE nemesis (N 1/5). 3 icones de boost.
#   Menace de depart 1[per_hero]. Icone de CRISE.
# Hinder 1[per_hero].
# Alligator Loki cannot be attacked.
# (Throg's nemesis side scheme.)
#
# MOTS-CLES (fiches lues avant d'ecrire)
#  - `Hinder` (mots-cles/hinder.md) : BASE AUTOMATIQUE, `desc.Hinder = "1*"`
#    — l'etoile est la notation « par heros » du moteur. AUCUN SCRIPT.
#  - `Crisis` (mots-cles/crisis.md) : BASE AUTOMATIQUE, `desc.Crisis = "1"`.
#    C'est elle qui rend tg006 Thunderous Charge si utile face a ce set.
#
# CARTE DE REFERENCE
#  - `th012` * Puppet Master (pack the_thing) : « Puppet Master cannot be
#    attacked while Hulk is in play » -> `UnitCannotBeAttacked(<qui>,
#    conditions=[...])`. Ici la condition est portee par l'EXISTENCE de ce
#    complot, pas par une condition supplementaire : tant qu'il est en jeu,
#    l'interdiction vaut.
#  - `49038` (pack magneto) : meme fabrique visant une carte NOMMEE plutot que
#    « This ».
#
# TEXTE CONTRE CODE
#  ⚠ « ALLIGATOR LOKI cannot be attacked » -> ce n'est PAS « this scheme » ni
#    « this card » : la carte protege UNE AUTRE carte, le sbire tg013. Le
#    litteral `"This"` de `th012` serait donc faux ici, il faut un
#    `CardFinder(name=...)`. Et le sbire n'a pas besoin d'etre en jeu : sans
#    lui, l'interdiction ne s'applique a personne, ce qui est exact.
#  ⚠ Et le NOM ne suffirait pas a distinguer ce sbire du HEROS `al001a`, qui
#    s'appelle pareil — sauf que `UnitCannotBeAttacked` ne s'interroge que sur
#    la carte qu'on essaie d'attaquer : un heros ami n'est jamais attaquable
#    par son propre joueur, la collision est sans effet. Verifie, pas suppose.
#  « cannot be attacked » ne dit rien du CONTRE ni des degats directs : seule
#    l'attaque est bloquee. Le joueur peut toujours vaincre le sbire par une
#    carte qui inflige des degats sans attaquer.
#  ⚠ La phrase entre parentheses « (Throg's nemesis side scheme.) » est un
#    rappel de reference, pas une capacite. Rien a coder.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitCannotBeAttacked(
            CardFinder(name=NOM_SBIRE, card_type=Minion),
        ),
    ]
