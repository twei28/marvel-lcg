from . import *

# Rodeo Extravaganza — OBLIGATION. 2 icones de boost.
# Give to the Drew Daniels player.
# Your identity cannot be readied by player card effects.
# Alter-Ego Action: Exhaust Drew Daniels -> remove Rodeo Extravaganza from the
#   game.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau dit « TEXAS TWISTER », pas « TEXAS
# TWISTER NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc
# ICI. `database.py:197` cherche le module dans le dossier du SET : range dans
# `_nemesis/`, il ne serait JAMAIS charge et l'obligation entrerait en jeu
# sans rien faire, en silence. Piege bt019 / nt012 / yd013 / dr010 / bk017 —
# SIXIEME fois qu'il se presente, et la deuxieme ou il est vu AVANT d'ecrire.
#
# CARTES DE REFERENCE
#  - `28021` Weight of the World : LE jumeau structurel — une obligation qui
#    RESTE en jeu, bloque un redressement, et s'enleve par une Alter-Ego
#    Action a cout d'inclinaison. Meme squelette, ligne pour ligne.
#  - `21159` Unnatural Storm : la formule exacte « by player card effects »,
#    rendue par `by_effect_face=CardFinder(card_type=PlayerCard)`.
#
# TEXTE CONTRE CODE
#  ⚠ CETTE OBLIGATION NE SE DEFAUSSE PAS TOUTE SEULE. Contrairement a yd013,
#    dr010 et bk017, elle n'offre aucun choix a la revelation : elle entre en
#    jeu et y reste jusqu'a ce qu'on paie. C'est la carte la plus punitive du
#    pack, parce que tout le kit consiste a se redresser (tt002, tt004, tt010,
#    tt019).
#  « YOUR identity » -> `control_by="You"`, et non toutes les identites de la
#    table : en multijoueur, seul le porteur de l'obligation est bloque.
#  « by PLAYER CARD effects » -> le vilain, lui, peut toujours redresser
#    l'identite si un jour il le voulait ; et le redressement automatique de
#    debut de tour n'est pas un effet de carte, il continue de fonctionner.
#  « REMOVE from the game » et non « discard » : elle ne revient jamais.
#  « Exhaust DREW DANIELS » -> `CostFunc.Exhaust("YourAlterEgo")`, montage
#    `28021`, et non `"This"` : c'est l'ALTER-EGO qu'on incline, pas la carte
#    de rencontre.


def GetAbilities() -> Sequence['Ability']:

    def quitter_le_rodeo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveAllFromGame([this], effect)

    return [
        *AbilityFactory.CardCannotReady(
            Identity,
            control_by="You",
            by_effect_face=CardFinder(card_type=PlayerCard),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            quitter_le_rodeo,
        ).SetCostFunc(CostFunc.Exhaust("YourAlterEgo")),
    ]
